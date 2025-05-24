import os
from PIL import Image as Img
from pillow_heif import register_heif_opener
from tkinter.filedialog import askopenfilenames

image_locations = []


def get_locations():
    return image_locations


def remove_image(index, img_loc_count_var):
    image_locations.pop(index)
    img_loc_count_var.set(len(image_locations))


def handle_drop(img_loc_count_var, img_convert_count_var, files):

    supported_types = [
        '.jpg',
        '.jpeg',
        '.png',
        '.tif',
        '.tiff',
        '.webp',
        '.heic',
        '.heif',
        '.cr2',
        '.ico']

    for file in files:
        file_name, ext = os.path.splitext(file)
        if ext.lower() in supported_types and file not in image_locations:
            image_locations.append(file)

    img_loc_count_var.set(len(image_locations))
    img_convert_count_var.set(0)


def find_file(img_loc_count_var, img_convert_count_var):

    file_paths = askopenfilenames(
        initialdir='/',
        title="Select File",
        filetypes=[("Image files",
                    "*.jpg *.jpeg *.png *.tif *.tiff *.webp *.heic *.heif *.cr2 *.ico")])

    if file_paths:
        for file_path in file_paths:
            if file_path not in image_locations:
                image_locations.append(file_path)

    img_loc_count_var.set(len(image_locations))
    img_convert_count_var.set(0)


def clear_loc_list(img_loc_count_var):
    global image_locations

    image_locations = []
    img_loc_count_var.set(0)


def create_new_folder():

    working_dir = os.path.dirname(image_locations[0])
    new_folder_path = os.path.join(working_dir, 'Converted Images')

    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)

    return new_folder_path


def unique_name(name):
    file, ext = os.path.splitext(name)
    output_folder = create_new_folder()

    current_name = name
    path = os.path.join(output_folder, current_name)

    file_counter = 1

    while os.path.exists(path):
        current_name = f"{file}({file_counter}){ext}"
        path = os.path.join(output_folder, current_name)
        file_counter += 1

    return current_name


def convert_image(file_type, img_convert_count_var, stop_event, window):
    global image_locations
    register_heif_opener()

    img_convert_count_var.set(0)

    for image_location in range(len(image_locations)):
        if stop_event.is_set():
            break

        else:
            try:
                img_loc = image_locations[image_location]
                image = Img.open(img_loc)
                image_name = os.path.basename(img_loc).replace(".", "").replace(f"{image.format.lower()}", "")

                new_name = f"{image_name}.{file_type.lower()}"
                new_unique = unique_name(new_name)

                output_folder = create_new_folder()
                full_path = os.path.join(output_folder, new_unique)

                current_count = img_convert_count_var.get()

                if image.format != file_type:

                    if file_type == 'PNG':
                        image.convert("RGBA").save(
                            full_path,
                            format=file_type)

                    else:
                        image.convert("RGB").save(
                            full_path,
                            format=file_type,
                            quality=95)

                    img_convert_count_var.set(current_count + 1)
                    window.after(0, img_convert_count_var.set, current_count + 1)

                else:
                    current_count = img_convert_count_var.get()
                    img_convert_count_var.set(current_count)
                    window.after(0, img_convert_count_var.set, current_count)

                    raise Exception("Can't convert to same file type.")

            except Exception as e:
                current_count = img_convert_count_var.get()
                img_convert_count_var.set(current_count)
                window.after(0, img_convert_count_var.set, current_count)

                print(e)

    if not stop_event.is_set() and img_convert_count_var.get() == len(image_locations):
        image_locations = []
