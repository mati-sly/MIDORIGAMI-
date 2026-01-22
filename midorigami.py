import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk 
from CTkMessagebox import CTkMessagebox 
import screeninfo
import subprocess
import os
import json 
import locale

# --- CONFIGURACIÓN DE ESTILO ---
ctk.set_appearance_mode("Dark") 
ctk.set_default_color_theme("green") 

# Archivos de configuración
CONFIG_FILE = os.path.expanduser("~/.midorigami_config.json")
FAVORITES_FILE = os.path.expanduser("~/.midorigami_favs.json")

# --- DICCIONARIO DE IDIOMAS ---
TRANSLATIONS = {
    "es": {
        "window_title": "MidoriGami (緑紙) 🌿",
        "fav_title": "Favoritos / ⭐",
        "add_current_folder": "+ Guardar Carpeta Actual",
        "saved_paths_title": "Rutas Guardadas",
        "up": "⬆ Subir",
        "content": "Contenido",
        "preview_default": "Selecciona una imagen\npara previsualizar",
        "preview_folder": "Navega a la carpeta deseada\ny confirma abajo.",
        "cancel": "Cancelar",
        "confirm_file": "Confirmar Selección",
        "confirm_folder": "✔ Seleccionar esta Carpeta",
        "monitor": "Monitor",
        "explore_btn": "Explorar y Seleccionar",
        "app_subtitle": "Wallpaper Manager",
        "shortcuts_title": "Accesos Directos / ショートカット",
        "add_path": "+ Nueva Ruta",
        "apply": "APLICAR / 適用",
        "dev_credits": "Dev by Matías © 2026",
        "dark_mode": "Modo Oscuro",
        "light_mode": "Modo Claro",
        "msg_path_title": "Ruta Fijada",
        "msg_path_body": "Ahora el selector se abrirá en:\n{}",
        "msg_missing_title": "Faltan Imágenes",
        "msg_missing_body": "Falta configurar:\n{}",
        "msg_success_title": "Éxito",
        "msg_success_body": "Wallpapers aplicados.",
        "msg_error_title": "Error",
        "monitors_section": "Monitores / モニター"
    },
    "en": {
        "window_title": "MidoriGami (Green Paper) 🌿",
        "fav_title": "Favorites / ⭐",
        "add_current_folder": "+ Save Current Folder",
        "saved_paths_title": "Saved Paths",
        "up": "⬆ Up",
        "content": "Content",
        "preview_default": "Select an image\nto preview",
        "preview_folder": "Browse to desired folder\nand confirm below.",
        "cancel": "Cancel",
        "confirm_file": "Confirm Selection",
        "confirm_folder": "✔ Select this Folder",
        "monitor": "Display",
        "explore_btn": "Browse & Select",
        "app_subtitle": "Wallpaper Manager",
        "shortcuts_title": "Shortcuts",
        "add_path": "+ New Path",
        "apply": "APPLY SETTINGS",
        "dev_credits": "Dev by Matías © 2026",
        "dark_mode": "Dark Mode",
        "light_mode": "Light Mode",
        "msg_path_title": "Path Set",
        "msg_path_body": "Picker will now open at:\n{}",
        "msg_missing_title": "Images Missing",
        "msg_missing_body": "Please configure:\n{}",
        "msg_success_title": "Success",
        "msg_success_body": "Wallpapers applied successfully.",
        "msg_error_title": "Error",
        "monitors_section": "Displays"
    },
    "ja": {
        "window_title": "緑紙 (MidoriGami) 🌿",
        "fav_title": "お気に入り / ⭐",
        "add_current_folder": "+ 現在のフォルダを保存",
        "saved_paths_title": "保存されたパス",
        "up": "⬆ 上へ",
        "content": "コンテンツ",
        "preview_default": "画像を選択して\nプレビュー",
        "preview_folder": "フォルダに移動して\n下で確定してください。",
        "cancel": "キャンセル",
        "confirm_file": "選択を確定",
        "confirm_folder": "✔ このフォルダを選択",
        "monitor": "モニター",
        "explore_btn": "参照して選択",
        "app_subtitle": "壁紙マネージャー",
        "shortcuts_title": "ショートカット",
        "add_path": "+ 新しいパス",
        "apply": "適用する",
        "dev_credits": "開発者: Matías © 2026",
        "dark_mode": "ダークモード",
        "light_mode": "ライトモード",
        "msg_path_title": "パス設定完了",
        "msg_path_body": "セレクターの初期位置:\n{}",
        "msg_missing_title": "画像不足",
        "msg_missing_body": "設定が必要です:\n{}",
        "msg_success_title": "成功",
        "msg_success_body": "壁紙が適用されました。",
        "msg_error_title": "エラー",
        "monitors_section": "モニター"
    }
}

# Variable global para el idioma actual
CURRENT_LANG = "es"

def tr(key):
    """Función helper para traducir"""
    return TRANSLATIONS.get(CURRENT_LANG, TRANSLATIONS["es"]).get(key, key)

class WallpaperPicker(ctk.CTkToplevel):
    def __init__(self, parent, start_dir, on_select_callback, folder_mode=False):
        super().__init__(parent)
        self.on_select = on_select_callback
        self.folder_mode = folder_mode
        self.current_dir = start_dir if os.path.isdir(start_dir) else os.path.expanduser("~")
        
        # Título dinámico
        title_key = "confirm_folder" if folder_mode else "window_title"
        self.title(tr("window_title")) # Usamos el título genérico o podrías hacer uno específico
        self.geometry("1100x700")
        
        self.favorites = self.load_favorites()

        # Layout
        self.grid_columnconfigure(1, weight=1) 
        self.grid_columnconfigure(2, weight=2) 
        self.grid_rowconfigure(1, weight=1)

        # 0. Sidebar
        self.fav_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.fav_frame.grid(row=0, column=0, rowspan=3, sticky="nsew")
        self.fav_frame.grid_rowconfigure(2, weight=1) 

        self.fav_label = ctk.CTkLabel(self.fav_frame, text=tr("fav_title"), font=("Roboto", 14, "bold"))
        self.fav_label.grid(row=0, column=0, pady=15, padx=10)

        self.add_fav_btn = ctk.CTkButton(
            self.fav_frame, text=tr("add_current_folder"), 
            command=self.add_current_to_favs, 
            fg_color="#2ecc71", hover_color="#27ae60", font=("Roboto", 11)
        )
        self.add_fav_btn.grid(row=1, column=0, pady=(0, 10), padx=10)

        self.fav_scroll = ctk.CTkScrollableFrame(self.fav_frame, label_text=tr("saved_paths_title"))
        self.fav_scroll.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)

        # 1. Top Bar
        self.top_bar = ctk.CTkFrame(self, height=40, fg_color="transparent")
        self.top_bar.grid(row=0, column=1, columnspan=2, sticky="ew", padx=10, pady=5)
        
        self.up_btn = ctk.CTkButton(self.top_bar, text=tr("up"), width=80, command=self.go_up)
        self.up_btn.pack(side="left", padx=5)

        self.path_label = ctk.CTkLabel(self.top_bar, text=self.current_dir, font=("Consolas", 12), text_color="gray80")
        self.path_label.pack(side="left", padx=10, fill="x", expand=True)

        # 2. Files
        self.file_scroll = ctk.CTkScrollableFrame(self, label_text=tr("content"))
        self.file_scroll.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        # 3. Preview
        self.preview_frame = ctk.CTkFrame(self)
        self.preview_frame.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)
        
        prev_txt = tr("preview_folder") if folder_mode else tr("preview_default")
        self.preview_label = ctk.CTkLabel(self.preview_frame, text=prev_txt)
        self.preview_label.pack(expand=True, fill="both", padx=10, pady=10)

        # 4. Bottom
        self.bottom_bar = ctk.CTkFrame(self, height=50, fg_color="transparent")
        self.bottom_bar.grid(row=2, column=1, columnspan=2, sticky="ew", padx=10, pady=10)

        self.cancel_btn = ctk.CTkButton(self.bottom_bar, text=tr("cancel"), fg_color="transparent", border_width=1, command=self.destroy)
        self.cancel_btn.pack(side="right", padx=10)

        btn_text = tr("confirm_folder") if folder_mode else tr("confirm_file")
        btn_state = "normal" if folder_mode else "disabled"
        
        self.select_btn = ctk.CTkButton(
            self.bottom_bar, text=btn_text, 
            state=btn_state, 
            command=self.confirm_selection,
            fg_color="#3498db" if folder_mode else "#2ecc71"
        )
        self.select_btn.pack(side="right", padx=10)

        self.selected_file = None
        self.load_favorites_ui()
        self.load_directory()
        self.after(100, self.safe_grab_set)

    def safe_grab_set(self):
        try: self.lift(); self.grab_set()
        except: pass

    # --- Logic ---
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
            name = "Home 🏠" if path == os.path.expanduser("~") else os.path.basename(path) or path
            frame = ctk.CTkFrame(self.fav_scroll, fg_color="transparent")
            frame.pack(fill="x", pady=2)
            ctk.CTkButton(frame, text=f"📂 {name}", fg_color="transparent", anchor="w", command=lambda p=path: self.change_dir(p), width=120).pack(side="left", fill="x", expand=True)
            ctk.CTkButton(frame, text="✕", width=25, fg_color="#e74c3c", command=lambda p=path: self.remove_fav(p)).pack(side="right")

    def add_current_to_favs(self):
        if self.current_dir not in self.favorites:
            self.favorites.append(self.current_dir); self.save_favorites(); self.load_favorites_ui()

    def remove_fav(self, path):
        if path in self.favorites:
            self.favorites.remove(path); self.save_favorites(); self.load_favorites_ui()

    def change_dir(self, new_path):
        if os.path.isdir(new_path): self.current_dir = new_path; self.load_directory()

    def load_directory(self):
        for widget in self.file_scroll.winfo_children(): widget.destroy()
        self.path_label.configure(text=f"{self.current_dir}")
        try: items = sorted(os.listdir(self.current_dir))
        except: self.go_up(); return

        folders = [i for i in items if os.path.isdir(os.path.join(self.current_dir, i)) and not i.startswith('.')]
        images = [i for i in items if i.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))]

        for f in folders:
            ctk.CTkButton(self.file_scroll, text=f"📁 {f}", fg_color="transparent", anchor="w", command=lambda p=f: self.enter_folder(p)).pack(fill="x", pady=2)
        for img in images:
            ctk.CTkButton(self.file_scroll, text=f"🖼️ {img}", fg_color=("gray85", "gray25"), anchor="w", command=lambda p=img: self.preview_image(p)).pack(fill="x", pady=2)

    def go_up(self):
        p = os.path.dirname(self.current_dir)
        if p != self.current_dir: self.change_dir(p)

    def enter_folder(self, folder_name):
        self.change_dir(os.path.join(self.current_dir, folder_name))

    def preview_image(self, file_name):
        full_path = os.path.join(self.current_dir, file_name)
        if not self.folder_mode:
            self.selected_file = full_path
            self.select_btn.configure(state="normal")
        try:
            img = Image.open(full_path)
            max_w, max_h = self.preview_frame.winfo_width()-20, self.preview_frame.winfo_height()-20
            if max_w < 10: max_w, max_h = 400, 400
            img.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)
            self.preview_label.configure(image=ctk.CTkImage(img, img, size=img.size), text="")
        except: pass

    def confirm_selection(self):
        if self.folder_mode: self.on_select(self.current_dir); self.destroy()
        elif self.selected_file: self.on_select(self.selected_file); self.destroy()


class MonitorFrame(ctk.CTkFrame):
    def __init__(self, master, monitor_name, width, height, index, app_instance, initial_image=None, **kwargs):
        super().__init__(master, **kwargs)
        self.monitor_name = monitor_name
        self.resolution = f"{width}x{height}"
        self.index = index
        self.app = app_instance 
        self.selected_image_path = initial_image 

        self.grid_columnconfigure(0, weight=1)

        self.label = ctk.CTkLabel(self, text="", font=("Roboto", 12, "bold")) # Texto se setea dinámicamente
        self.label.grid(row=0, column=0, pady=5, padx=5)

        self.preview_btn = ctk.CTkButton(
            self, text="", fg_color="transparent", border_width=2, height=150,
            command=self.open_custom_picker
        )
        self.preview_btn.grid(row=1, column=0, pady=10, padx=10, sticky="ew")

        self.update_texts() # Setear textos iniciales
        if self.selected_image_path: self.update_preview(self.selected_image_path)

    def update_texts(self):
        self.label.configure(text=f"{tr('monitor')} {self.index + 1}: {self.monitor_name}\n({self.resolution})")
        if not self.selected_image_path:
            self.preview_btn.configure(text=tr("explore_btn"))

    def open_custom_picker(self):
        start_dir = os.path.expanduser("~")
        if self.selected_image_path: start_dir = os.path.dirname(self.selected_image_path)
        elif self.app.global_default_dir: start_dir = self.app.global_default_dir
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
        except: self.preview_btn.configure(text="Error")

class MidoriGamiApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # 1. Detectar idioma inicial
        global CURRENT_LANG
        self.config_data = self.load_config()
        
        # Prioridad: 1. Config guardada, 2. Sistema operativo, 3. Inglés
        saved_lang = self.config_data.get("language")
        if saved_lang in TRANSLATIONS:
            CURRENT_LANG = saved_lang
        else:
            sys_lang = locale.getdefaultlocale()[0]
            if sys_lang and sys_lang.startswith('ja'): CURRENT_LANG = 'ja'
            elif sys_lang and sys_lang.startswith('es'): CURRENT_LANG = 'es'
            else: CURRENT_LANG = 'en'

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

        self.favorites = self.load_favorites() 

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=260, corner_radius=0) 
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(1, weight=1) 

        # Header
        self.header_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(30, 10))
        self.logo_label = ctk.CTkLabel(self.header_frame, text=" MidoriGami 🌿\n 緑紙", image=self.sidebar_icon, compound="top", font=("Roboto", 24, "bold"))
        self.logo_label.pack()
        self.subtitle_label = ctk.CTkLabel(self.header_frame, text="", font=("Roboto", 12), text_color="gray")
        self.subtitle_label.pack()

        # Rutas
        self.paths_frame = ctk.CTkScrollableFrame(self.sidebar, label_text="")
        self.paths_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
        self.add_path_btn = ctk.CTkButton(self.sidebar, text="", command=self.add_manual_path, fg_color="transparent", border_width=1, font=("Roboto", 11))
        self.add_path_btn.grid(row=2, column=0, padx=20, pady=(0, 10))

        # Footer
        self.footer_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.footer_frame.grid(row=3, column=0, sticky="ew", pady=20)

        self.apply_btn = ctk.CTkButton(self.footer_frame, text="", command=self.apply_wallpapers, fg_color="#2ecc71", hover_color="#27ae60", font=("Roboto", 16, "bold"), height=50)
        self.apply_btn.pack(padx=20, pady=5, fill="x")

        # SELECTOR DE IDIOMA
        self.lang_var = ctk.StringVar(value=self.get_lang_display_name(CURRENT_LANG))
        self.lang_menu = ctk.CTkOptionMenu(
            self.footer_frame, 
            values=["Español", "English", "日本語"],
            command=self.change_language,
            variable=self.lang_var,
            width=150
        )
        self.lang_menu.pack(pady=5)

        self.theme_switch = ctk.CTkSwitch(self.footer_frame, text="", command=self.toggle_theme)
        self.theme_switch.select() 
        self.theme_switch.pack(pady=10)

        self.credits_label = ctk.CTkLabel(self.footer_frame, text="", font=("Roboto", 10), text_color="gray")
        self.credits_label.pack()

        # Main Area
        self.main_area = ctk.CTkScrollableFrame(self, label_text="")
        self.main_area.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.monitor_frames = []
        
        # Inicializar textos y cargar
        self.update_ui_language() 
        self.load_sidebar_paths() 
        self.load_monitors()

    # --- GESTIÓN DE IDIOMA ---
    def get_lang_display_name(self, code):
        if code == 'es': return "Español"
        if code == 'ja': return "日本語"
        return "English"

    def change_language(self, choice):
        global CURRENT_LANG
        if choice == "Español": CURRENT_LANG = "es"
        elif choice == "日本語": CURRENT_LANG = "ja"
        else: CURRENT_LANG = "en"
        
        self.update_ui_language()
        
        # Guardar preferencia
        self.config_data["language"] = CURRENT_LANG
        self.save_config_data()

    def update_ui_language(self):
        """Actualiza todos los textos de la interfaz al vuelo"""
        self.title(tr("window_title"))
        self.subtitle_label.configure(text=tr("app_subtitle"))
        self.paths_frame.configure(label_text=tr("shortcuts_title"))
        self.add_path_btn.configure(text=tr("add_path"))
        self.apply_btn.configure(text=tr("apply"))
        self.theme_switch.configure(text=tr("dark_mode") if self.theme_switch.get() else tr("light_mode"))
        self.credits_label.configure(text=tr("dev_credits"))
        self.main_area.configure(label_text=tr("monitors_section"))
        
        # Actualizar monitores
        for frame in self.monitor_frames:
            frame.update_texts()

    # --- RESTO DE FUNCIONES ---
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
            name = "Home" if path == os.path.expanduser("~") else os.path.basename(path)
            ctk.CTkButton(
                self.paths_frame, text=f"📂 {name}", fg_color="transparent", border_width=1, anchor="w",
                command=lambda p=path: self.set_global_path(p)
            ).pack(fill="x", pady=2)

    def set_global_path(self, path):
        self.global_default_dir = path
        CTkMessagebox(master=self, title=tr("msg_path_title"), message=tr("msg_path_body").format(path), icon="info")

    def add_manual_path(self):
        WallpaperPicker(self, os.path.expanduser("~"), self.on_folder_selected, folder_mode=True)

    def on_folder_selected(self, path):
        if path and path not in self.favorites:
            self.favorites.append(path); self.save_favorites(); self.load_sidebar_paths()

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f: return json.load(f)
            except: pass
        return {}

    def save_config_data(self):
        try:
            with open(CONFIG_FILE, 'w') as f: json.dump(self.config_data, f, indent=4)
        except: pass

    def save_config_wallpapers(self):
        # Guardamos wallpapers en la misma estructura o separada, aquí actualizamos el dict principal
        monitor_data = {}
        for frame in self.monitor_frames:
            if frame.selected_image_path:
                monitor_data[frame.monitor_name] = frame.selected_image_path
        
        self.config_data["wallpapers"] = monitor_data
        self.save_config_data()

    def load_monitors(self):
        try: monitors = screeninfo.get_monitors()
        except: monitors = []
        
        wallpapers = self.config_data.get("wallpapers", {})
        
        for i, m in enumerate(monitors):
            saved = wallpapers.get(m.name)
            frame = MonitorFrame(self.main_area, m.name, m.width, m.height, i, self, initial_image=saved)
            frame.pack(pady=10, padx=10, fill="x")
            self.monitor_frames.append(frame)

    def toggle_theme(self):
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("Dark"); self.theme_switch.configure(text=tr("dark_mode"))
        else:
            ctk.set_appearance_mode("Light"); self.theme_switch.configure(text=tr("light_mode"))

    def apply_wallpapers(self):
        command = ["feh", "--bg-fill"]
        images_args = []
        missing = []
        for frame in self.monitor_frames:
            if frame.selected_image_path: images_args.append(frame.selected_image_path)
            else: missing.append(frame.monitor_name)

        if missing:
            CTkMessagebox(master=self, title=tr("msg_missing_title"), message=tr("msg_missing_body").format(', '.join(missing)), icon="cancel")
            return

        try:
            subprocess.run(command + images_args)
            with open(os.path.expanduser("~/.fehbg"), "w") as f: f.write(" ".join(command + images_args))
            self.save_config_wallpapers()
            CTkMessagebox(master=self, title=tr("msg_success_title"), message=tr("msg_success_body"), icon="check")
        except Exception as e:
            CTkMessagebox(master=self, title=tr("msg_error_title"), message=str(e), icon="cancel")

if __name__ == "__main__":
    app = MidoriGamiApp()
    app.mainloop()