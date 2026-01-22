
<div align="center">
  <img src="icono.png" alt="MidoriGami Logo" width="140" height="140">

  <h1>MidoriGami (緑紙)</h1>

  <p>
    <strong>
      “The art of folding your desktop /  
      El arte de plegar tu escritorio.”
    </strong>
  </p>

  <p>
    <a href="https://www.python.org/">
      <img src="https://img.shields.io/badge/Python-3.10+-green?style=for-the-badge&logo=python&logoColor=white" alt="Python">
    </a>
    <a href="https://linuxmint.com/">
      <img src="https://img.shields.io/badge/Linux_Mint-Compatible-87CF3E?style=for-the-badge&logo=linuxmint&logoColor=white" alt="Linux Mint">
    </a>
    <a href="https://opensource.org/licenses/MIT">
      <img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="License">
    </a>
  </p>

  <p>
    <a href="#-english">🇺🇸 English</a> •
    <a href="#-español">🇪🇸 Español</a>
  </p>
</div>

---

## 🇺🇸 English

### 🌿 Description

**MidoriGami** is an advanced and aesthetic wallpaper manager for Linux, specifically designed for **multi-monitor** setups.

Unlike other managers, MidoriGami includes its own **Visual File Explorer (Mini-Nemo)**, allowing you to browse folders, preview images, and manage favorite paths without relying on outdated system dialogs.

---

### 📸 Screenshots

<div align="center">
  <img src="captura1.png" alt="MidoriGami Main Screen" width="800">
  <p><em>Main interface and multi-monitor management</em></p>
</div>

<br>

<div align="center">
  <img src="captura2.png" alt="Mini-Nemo Visual Selector" width="800">
  <p><em>Visual explorer (Mini-Nemo) with wallpaper preview</em></p>
</div>

---

### ✨ Features

- 🖥️ **True Multi-Monitor Support**  
  Set a different wallpaper for each detected screen.

- 📂 **Integrated Mini-Nemo**  
  Custom visual file explorer (*WallpaperPicker*) with instant large previews.

- ⭐ **Favorites Sidebar**  
  Save frequent paths like `~/Wallpapers/Anime` or `~/Downloads`.

- 💾 **Persistence**  
  Remembers your configuration and `feh` state after reboot.

- 🎨 **Modern UI**  
  Dark interface with green accents, inspired by Linux Mint and built with **CustomTkinter**.

---

### 🚀 Requirements

MidoriGami uses:
- `feh` as the wallpaper backend  
- `python3-tk` for the GUI  

#### Debian / Ubuntu / Linux Mint
```bash
sudo apt update
sudo apt install feh python3-tk
````

#### Arch Linux

```bash
sudo pacman -S feh tk
```

---

### 🛠️ Installation

```bash
git clone https://github.com/TU_USUARIO/midorigami.git
cd midorigami

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
python midorigami.py
```

---

## 🇪🇸 Español

### 🌿 Descripción

**MidoriGami** es un gestor de fondos de pantalla avanzado y estético para Linux, diseñado específicamente para entornos **multi-monitor**.

A diferencia de otros gestores, incluye su propio **Explorador Visual de Archivos (Mini-Nemo)**, permitiendo navegar carpetas, previsualizar imágenes y gestionar rutas favoritas sin depender de diálogos de sistema anticuados.

---

### 📸 Capturas

<div align="center">
  <img src="captura1.png" alt="Pantalla principal de MidoriGami" width="800">
  <p><em>Pantalla principal y gestión multi-monitor</em></p>
</div>

<br>

<div align="center">
  <img src="captura2.png" alt="Selector visual Mini-Nemo" width="800">
  <p><em>Explorador visual (Mini-Nemo) con previsualización de fondos</em></p>
</div>

---

### ✨ Características

* 🖥️ **Soporte Multi-Monitor Real**
  Configura un fondo distinto para cada pantalla detectada.

* 📂 **Mini-Nemo Integrado**
  Explorador visual personalizado (*WallpaperPicker*) con previsualizaciones grandes al instante.

* ⭐ **Sidebar de Favoritos**
  Guarda rutas frecuentes como `~/Wallpapers/Anime` o `~/Descargas`.

* 💾 **Persistencia**
  Recuerda la configuración al reiniciar (estado de `feh` + GUI).

* 🎨 **UI Moderna**
  Interfaz oscura con acentos verdes, inspirada en Linux Mint y construida con **CustomTkinter**.

---

### 🚀 Requisitos Previos

MidoriGami utiliza:

* `feh` como backend para establecer el fondo de pantalla
* `python3-tk` para la interfaz gráfica

#### Debian / Ubuntu / Linux Mint

```bash
sudo apt update
sudo apt install feh python3-tk
```

#### Arch Linux

```bash
sudo pacman -S feh tk
```

---

### 🛠️ Instalación

```bash
git clone https://github.com/TU_USUARIO/midorigami.git
cd midorigami

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
python midorigami.py
```

---

### 🎮 Cómo usar

1. **Seleccionar fondo**
   Haz clic en *“Explorar y Seleccionar”* en el monitor deseado.

2. **Navegar**
   Usa el explorador visual para encontrar tu imagen.

3. **Guardar rutas**
   Usa **+ Guardar Carpeta Actual** o **+ Nueva Ruta** en la barra lateral.

4. **Aplicar**
   Presiona **APLICAR / 適用** para establecer los cambios.

---

### 🤝 Contribuciones

Las sugerencias y Pull Requests son bienvenidas.
Si tienes ideas para mejorar **Mini-Nemo** o añadir soporte para otros backends (como `nitrogen`), siéntete libre de contribuir.

---

<p align="center">
  Dev by <strong>Matías</strong> © 2026
</p>


