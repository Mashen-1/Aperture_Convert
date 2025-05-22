<p align="center">
  <img src="![Screenshot (43)](https://github.com/user-attachments/assets/cf86916d-f18b-47f3-9220-083ec174597f)" width="400" alt="Aperture Convert Preview">
</p>

<h1 align="center">Aperture Convert</h1>

<p align="center">
  A drag-and-drop batch image converter with live previews, multiple image format support, and clean UI.
</p>

---

**Aperture Convert** is a clean and intuitive image conversion tool that lets you batch-convert images into multiple formats using a modern drag-and-drop GUI. Built with Python and Tkinter, it supports multiple formats and features real-time conversion control with the ability to stop conversions mid-process.

---

## Features

- Convert images from: **JPEG, PNG, TIFF, WEBP, HEIF/HEIC, CR2, ICO**  to : **JPEG, PNG, TIFF, HEIF, BMP, ICO**
  
- Batch processing via drag-and-drop or file dialog

- Automatically saves to a dedicated "Converted Images" folder within the same folder as the original image

- Stop conversion mid-process with a single click

- Remove individual images from the que or clear the full que with a single click

- Live preview with image name and progress tracker

- Simple, themed UI with smooth user experience

- Built with Python 3, Pillow, pillow-heif, and tkinterdnd2

---

## Installation

```bash
git clone https://github.com/Mashen-1/Aperture_Convert.git
cd Aperture_Convert
pip install Pillow pillow-heif tkinterdnd2
````

---

## Usage

```bash
python gui.py
```

* Drag files in or use **Locate Image(s)**
* Choose a format in the dropdown and click **Convert**
* Click **Stop** anytime
* Remove individual files from the que by clicking **Remove**
* Remove all files from que by clicking **Clear**
* All files save to a `/Converted Images/` folder next to the originals

---

## Project Structure

```
Aperture_Convert/
├── gui.py                 # GUI interface
├── file_converstion.py    # Conversion backend
├── img_assets/            # UI icons and logos
├── README.md              # This file
```

---

## Packaging to executable (Optional)

* For Windows users you can directly download the .zip [Here](https://www.mediafire.com/file/s5m3a18rr8w1cg9/Aperture_Convert.zip/file)

```bash
pip install auto-py-to-exe
python -m auto_py_to_exe
```

In the `auto-py-to-exe` GUI:

* Onefile: checked
* Window based: checked
* Additional files:

```
file_converstion.py
```
* Hidden imports:

```
PIL
pillow_heif
tkinterdnd2
```
* Include your `img_assets` folder in the same directory as the `.exe`

---

## Dependencies

- [Python 3.8+](https://www.python.org/)
- [Pillow](https://pypi.org/project/Pillow/)
- [pillow-heif](https://pypi.org/project/pillow-heif/)
- [tkinterdnd2](https://github.com/pmgagne/tkinterdnd2)
- [PyInstaller](https://www.pyinstaller.org/) (optional)
- [auto-py-to-exe](https://github.com/brentvollebregt/auto-py-to-exe) (optional)

---

## License

This project is licensed under the [GNU GPL v2.0](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html).

You are free to use, modify, and distribute it under the terms of this license.

---

## Credits

- Made by [Mashen](https://github.com/Mashen-1)
- Logo design & GUI by [Mashen](https://github.com/Mashen-1)

---
