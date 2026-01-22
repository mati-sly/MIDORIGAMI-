import customtkinter as ctk
from PIL import Image, ImageTk 
from CTkMessagebox import CTkMessagebox 
import screeninfo
import subprocess
import os
import json 

# --- CONFIGURACIÓN DE ESTILO ---
ctk.set_appearance_mode("Dark") 
ctk.set_default_color_theme("green") 

# Archivos de configuración
CONFIG_FILE = os.path.expanduser("~/.midorigami_config.json")
FAVORITES_FILE = os.path.expanduser("~/.midorigami_favs.json")

class WallpaperPicker(ctk.CTkToplevel):
    """
    Explorador visual personalizado. Funciona para archivos o carpetas.
    """
    def __init__(self, parent, start_dir, on_select_callback, folder_mode=False):
        super().__init__(parent)
        self.on_select = on_select_callback
        self.folder_mode = folder_mode  # <-- NUEVO PARAMETRO
        
        # Validar directorio de inicio
        self.current_dir = start_dir if os.path.isdir(start_dir) else os.path.expanduser("~")
        
        title_text = "Seleccionar Carpeta / フォルダ選択" if folder_mode else "Selector Visual / ビジュアルセレクター"
        self.title(title_text)
        self.geometry("1100x700")
        
        self.favorites = self.load_favorites()

        # --- LAYOUT PRINCIPAL ---
        self.grid_columnconfigure(1, weight=1) 
        self.grid_columnconfigure(2, weight=2) 
        self.grid_rowconfigure(1, weight=1)

        # 0. SIDEBAR FAVORITOS
        self.fav_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.fav_frame.grid(row=0, column=0, rowspan=3, sticky="nsew")
        self.fav_frame.grid_rowconfigure(2, weight=1) 

        self.fav_label = ctk.CTkLabel(self.fav_frame, text="Favoritos / ⭐", font=("Roboto", 14, "bold"))
        self.fav_label.grid(row=0, column=0, pady=15, padx=10)

        self.add_fav_btn = ctk.CTkButton(
            self.fav_frame, text="+ Guardar Carpeta Actual", 
            command=self.add_current_to_favs, 
            fg_color="#2ecc71", hover_color="#27ae60",
            font=("Roboto", 11)
        )
        self.add_fav_btn.grid(row=1, column=0, pady=(0, 10), padx=10)

        self.fav_scroll = ctk.CTkScrollableFrame(self.fav_frame, label_text="Rutas Guardadas")
        self.fav_scroll.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)

        # 1. BARRA SUPERIOR
        self.top_bar = ctk.CTkFrame(self, height=40, fg_color="transparent")
        self.top_bar.grid(row=0, column=1, columnspan=2, sticky="ew", padx=10, pady=5)
        
        self.up_btn = ctk.CTkButton(self.top_bar, text="⬆ Subir", width=80, command=self.go_up)
        self.up_btn.pack(side="left", padx=5)

        self.path_label = ctk.CTkLabel(self.top_bar, text=self.current_dir, font=("Consolas", 12), text_color="gray80")
        self.path_label.pack(side="left", padx=10, fill="x", expand=True)

        # 2. LISTA DE ARCHIVOS
        self.file_scroll = ctk.CTkScrollableFrame(self, label_text="Contenido")
        self.file_scroll.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        # 3. PREVISUALIZACIÓN
        self.preview_frame = ctk.CTkFrame(self)
        self.preview_frame.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)
        
        preview_text = "Navega a la carpeta deseada\ny confirma abajo." if folder_mode else "Selecciona una imagen"
        self.preview_label = ctk.CTkLabel(self.preview_frame, text=preview_text)
        self.preview_label.pack(expand=True, fill="both", padx=10, pady=10)

        # 4. BOTONERA
        self.bottom_bar = ctk.CTkFrame(self, height=50, fg_color="transparent")
        self.bottom_bar.grid(row=2, column=1, columnspan=2, sticky="ew", padx=10, pady=10)

        self.cancel_btn = ctk.CTkButton(self.bottom_bar, text="Cancelar", fg_color="transparent", border_width=1, command=self.destroy)
        self.cancel_btn.pack(side="right", padx=10)

        # Configuración del botón de acción según modo
        btn_text = "✔ Seleccionar esta Carpeta" if folder_mode else "Confirmar Selección"
        btn_state = "normal" if folder_mode else "disabled" # En modo carpeta, siempre activo (seleccionas donde estás)
        
        self.select_btn = ctk.CTkButton(
            self.bottom_bar, text=btn_text, 
            state=btn_state, 
            command=self.confirm_selection,
            fg_color="#3498db" if folder_mode else "#2ecc71" # Azul para carpetas, Verde para archivos
        )
        self.select_btn.pack(side="right", padx=10)

        self.selected_file = None
        self.load_favorites_ui()
        self.load_directory()
        self.after(100, self.safe_grab_set)

    def safe_grab_set(self):
        try:
            self.lift()
            self.grab_set()
        except: pass

    # --- Lógica Favoritos ---
    def load_favorites(self):
        if os.path.exists(FAVORITES_FILE):
            try:
                with open(FAVORITES_FILE, 'r') as f: return json.load(f)
            except: pass
        return [os.path.expanduser("~"), os.path.expanduser("~/Imágenes")]

    def save_favorites(self):
        try:
            with open(FAVORITES_FILE, 'w') as f: json.dump(self.favorites, f)
        except: pass

    def load_favorites_ui(self):
        for widget in self.fav_scroll.winfo_children(): widget.destroy()
        for path in self.favorites:
            folder_name = os.path.basename(path) if path != "/" else "Raíz"
            if path == os.path.expanduser("~"): folder_name = "Home 🏠"

            frame = ctk.CTkFrame(self.fav_scroll, fg_color="transparent")
            frame.pack(fill="x", pady=2)
            
            ctk.CTkButton(
                frame, text=f"📂 {folder_name}", fg_color="transparent", anchor="w",
                command=lambda p=path: self.change_dir(p), width=120
            ).pack(side="left", fill="x", expand=True)

            ctk.CTkButton(
                frame, text="✕", width=25, fg_color="#e74c3c", 
                command=lambda p=path: self.remove_fav(p)
            ).pack(side="right")

    def add_current_to_favs(self):
        if self.current_dir not in self.favorites:
            self.favorites.append(self.current_dir)
            self.save_favorites()
            self.load_favorites_ui()

    def remove_fav(self, path):
        if path in self.favorites:
            self.favorites.remove(path)
            self.save_favorites()
            self.load_favorites_ui()

    def change_dir(self, new_path):
        if os.path.isdir(new_path):
            self.current_dir = new_path
            self.load_directory()

    def load_directory(self):
        for widget in self.file_scroll.winfo_children(): widget.destroy()
        self.path_label.configure(text=f"{self.current_dir}")
        try: items = sorted(os.listdir(self.current_dir))
        except: 
            self.go_up()
            return

        folders = [i for i in items if os.path.isdir(os.path.join(self.current_dir, i)) and not i.startswith('.')]
        images = [i for i in items if i.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))]

        for f in folders:
            ctk.CTkButton(self.file_scroll, text=f"📁 {f}", fg_color="transparent", anchor="w", command=lambda p=f: self.enter_folder(p)).pack(fill="x", pady=2)
        
        # En modo carpeta, mostramos imágenes pero al hacer click solo previsualizan, no "seleccionan"
        for img in images:
            ctk.CTkButton(self.file_scroll, text=f"🖼️ {img}", fg_color=("gray85", "gray25"), anchor="w", command=lambda p=img: self.preview_image(p)).pack(fill="x", pady=2)

    def go_up(self):
        p = os.path.dirname(self.current_dir)
        if p != self.current_dir: self.change_dir(p)

    def enter_folder(self, folder_name):
        self.change_dir(os.path.join(self.current_dir, folder_name))

    def preview_image(self, file_name):
        full_path = os.path.join(self.current_dir, file_name)
        
        # Si NO estamos en modo carpeta, esto activa el botón de seleccionar
        if not self.folder_mode:
            self.selected_file = full_path
            self.select_btn.configure(state="normal")
            
        try:
            img = Image.open(full_path)
            max_w, max_h = self.preview_frame.winfo_width()-20, self.preview_frame.winfo_height()-20
            if max_w < 10: max_w = 400
            if max_h < 10: max_h = 400
            img.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)
            self.preview_label.configure(image=ctk.CTkImage(img, img, size=img.size), text="")
        except: pass

    def confirm_selection(self):
        if self.folder_mode:
            # En modo carpeta, devolvemos el directorio actual
            self.on_select(self.current_dir)
            self.destroy()
        elif self.selected_file:
            # En modo archivo, devolvemos el archivo seleccionado
            self.on_select(self.selected_file)
            self.destroy()


class MonitorFrame(ctk.CTkFrame):
    def __init__(self, master, monitor_name, width, height, index, app_instance, initial_image=None, **kwargs):
        super().__init__(master, **kwargs)
        self.monitor_name = monitor_name
        self.resolution = f"{width}x{height}"
        self.index = index
        self.app = app_instance 
        self.selected_image_path = initial_image 

        self.grid_columnconfigure(0, weight=1)

        self.label = ctk.CTkLabel(self, text=f"Monitor {index + 1}: {monitor_name}\n({self.resolution})", font=("Roboto", 12, "bold"))
        self.label.grid(row=0, column=0, pady=5, padx=5)

        self.preview_btn = ctk.CTkButton(
            self, text="Explorar y Seleccionar" if not initial_image else "", 
            fg_color="transparent", border_width=2, height=150,
            command=self.open_custom_picker
        )
        self.preview_btn.grid(row=1, column=0, pady=10, padx=10, sticky="ew")

        if self.selected_image_path: self.update_preview(self.selected_image_path)

    def open_custom_picker(self):
        start_dir = os.path.expanduser("~")
        if self.selected_image_path:
            start_dir = os.path.dirname(self.selected_image_path)
        elif self.app.global_default_dir:
            start_dir = self.app.global_default_dir
            
        # Llamada normal (Modo archivo = False por defecto)
        WallpaperPicker(self.winfo_toplevel(), start_dir, self.on_image_selected)

    def on_image_selected(self, file_path):
        if file_path:
            self.selected_image_path = file_path
            self.update_preview(file_path)

    def update_preview(self, path):
        try:
            img = Image.open(path)
            ratio = img.width / img.height
            ctk_img = ctk.CTkImage(img, img, size=(int(140*ratio), 140))
            self.preview_btn.configure(image=ctk_img, text="") 
        except: self.preview_btn.configure(text="Error imagen")

class MidoriGamiApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MidoriGami (緑紙) 🌿")
        self.geometry("1100x750")
        
        self.global_default_dir = None 
        
        # Icono
        self.sidebar_icon = None
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(script_dir, "icono.png")
            pil_img = Image.open(icon_path)
            self.wm_iconphoto(False, ImageTk.PhotoImage(pil_img.resize((128,128), Image.Resampling.LANCZOS)))
            self.sidebar_icon = ctk.CTkImage(pil_img, pil_img, size=(100, 100))
        except: pass

        self.config_data = self.load_config()
        self.favorites = self.load_favorites() 

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=260, corner_radius=0) 
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(1, weight=1) 

        # HEADER
        self.header_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(40, 10))
        
        self.logo_label = ctk.CTkLabel(
            self.header_frame, text=" MidoriGami 🌿\n 緑紙", 
            image=self.sidebar_icon, compound="top", font=("Roboto", 24, "bold")
        )
        self.logo_label.pack()
        ctk.CTkLabel(self.header_frame, text="Wallpaper Manager", font=("Roboto", 12), text_color="gray").pack()

        # BODY (LISTA DE RUTAS)
        self.paths_frame = ctk.CTkScrollableFrame(self.sidebar, label_text="Accesos Directos / ショートカット")
        self.paths_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
        # Botón para añadir ruta manual (USANDO NUESTRO PICKER)
        self.add_path_btn = ctk.CTkButton(
            self.sidebar, text="+ Nueva Ruta", 
            command=self.add_manual_path, # <--- Aquí llamamos a la nueva función
            fg_color="transparent", border_width=1, font=("Roboto", 11)
        )
        self.add_path_btn.grid(row=2, column=0, padx=20, pady=(0, 10))


        # FOOTER
        self.footer_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.footer_frame.grid(row=3, column=0, sticky="ew", pady=20)

        self.apply_btn = ctk.CTkButton(
            self.footer_frame, text="APLICAR / 適用", 
            command=self.apply_wallpapers, 
            fg_color="#2ecc71", hover_color="#27ae60",
            font=("Roboto", 16, "bold"), height=50
        )
        self.apply_btn.pack(padx=20, pady=10, fill="x")

        self.theme_switch = ctk.CTkSwitch(self.footer_frame, text="Modo Oscuro", command=self.toggle_theme)
        self.theme_switch.select() 
        self.theme_switch.pack(pady=10)

        ctk.CTkLabel(self.footer_frame, text="Dev by Matías © 2026", font=("Roboto", 10), text_color="gray").pack()

        # MAIN AREA
        self.main_area = ctk.CTkScrollableFrame(self, label_text="Monitores / モニター")
        self.main_area.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.monitor_frames = []
        self.load_sidebar_paths() 
        self.load_monitors()

    # --- LÓGICA DE RUTAS EN SIDEBAR ---
    def load_favorites(self):
        if os.path.exists(FAVORITES_FILE):
            try:
                with open(FAVORITES_FILE, 'r') as f: return json.load(f)
            except: pass
        return [os.path.expanduser("~"), os.path.expanduser("~/Imágenes")]

    def save_favorites(self):
        try:
            with open(FAVORITES_FILE, 'w') as f: json.dump(self.favorites, f)
        except: pass

    def load_sidebar_paths(self):
        for widget in self.paths_frame.winfo_children(): widget.destroy()
        
        for path in self.favorites:
            name = os.path.basename(path) if path != "/" else "Raíz"
            if path == os.path.expanduser("~"): name = "Home"
            
            btn = ctk.CTkButton(
                self.paths_frame, 
                text=f"📂 {name}", 
                fg_color="transparent", 
                border_width=1,
                anchor="w",
                command=lambda p=path: self.set_global_path(p)
            )
            btn.pack(fill="x", pady=2)

    def set_global_path(self, path):
        self.global_default_dir = path
        CTkMessagebox(master=self, title="Ruta Fijada", message=f"Ahora el selector se abrirá en:\n{path}", icon="info")

    def add_manual_path(self):
        # AQUI REEMPLAZAMOS filedialog.askdirectory() POR NUESTRO PICKER
        WallpaperPicker(self, os.path.expanduser("~"), self.on_folder_selected, folder_mode=True)

    def on_folder_selected(self, path):
        # Callback cuando el usuario selecciona una carpeta en el picker
        if path and path not in self.favorites:
            self.favorites.append(path)
            self.save_favorites()
            self.load_sidebar_paths()

    # --- RESTO DE LA LÓGICA ---
    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f: return json.load(f)
            except: pass
        return {}

    def save_config(self):
        data = {}
        for frame in self.monitor_frames:
            if frame.selected_image_path:
                data[frame.monitor_name] = frame.selected_image_path
        try:
            with open(CONFIG_FILE, 'w') as f: json.dump(data, f, indent=4)
        except: pass

    def load_monitors(self):
        try: monitors = screeninfo.get_monitors()
        except: monitors = []
        for i, m in enumerate(monitors):
            saved = self.config_data.get(m.name)
            frame = MonitorFrame(self.main_area, m.name, m.width, m.height, i, self, initial_image=saved)
            frame.pack(pady=10, padx=10, fill="x")
            self.monitor_frames.append(frame)

    def toggle_theme(self):
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("Dark")
            self.theme_switch.configure(text="Modo Oscuro")
        else:
            ctk.set_appearance_mode("Light")
            self.theme_switch.configure(text="Modo Claro")

    def apply_wallpapers(self):
        command = ["feh", "--bg-fill"]
        images_args = []
        missing = []
        
        for frame in self.monitor_frames:
            if frame.selected_image_path:
                images_args.append(frame.selected_image_path)
            else:
                missing.append(frame.monitor_name)

        if missing:
            CTkMessagebox(master=self, title="Faltan Imágenes", message=f"Falta configurar:\n{', '.join(missing)}", icon="cancel")
            return

        try:
            subprocess.run(command + images_args)
            with open(os.path.expanduser("~/.fehbg"), "w") as f: f.write(" ".join(command + images_args))
            self.save_config()
            CTkMessagebox(master=self, title="Éxito", message="Wallpapers aplicados.", icon="check")
        except Exception as e:
            CTkMessagebox(master=self, title="Error", message=str(e), icon="cancel")

if __name__ == "__main__":
    app = MidoriGamiApp()
    app.mainloop()