import tkinter as tk
import threading
from threading import Thread
from tkinter import ttk
from file_converstion import *
from PIL import Image, ImageTk, ImageOps
from pillow_heif import register_heif_opener
from tkinterdnd2 import TkinterDnD, DND_FILES


# -- Global Variables --

current_image_displayed = 0
convert_running = False
stop_event = threading.Event()
conversion_thread = None


# -- Window Setup --

window = TkinterDnD.Tk()
window.geometry('1000x800')
window.resizable(width=False, height=False)
window.title('Aperture Convert')

icon = tk.PhotoImage(file="img_assets/aperture studios logo gray back.png")
window.iconphoto(False, icon)

window.config(background="#222222")


# -- GUI Functions --

def convert_wrapper():
    global selected_file_type, img_convert_count_var, current_image_displayed, convert_running, conversion_thread
    global stop_event

    try:
        convert_image(selected_file_type.get(), img_convert_count_var, stop_event, window)

    except Exception as e:
        print(f"Error in threaded_conversion: {e}")

    finally:
        convert_running = False
        conversion_thread = None
        convert_button.config(text='Convert', command=threaded_convert)
        locations = get_locations()

        if locations:
            display_image()
            current_image_displayed = 0
        else:
            display_current_image.config(image='')

        show_file_name(locations)


def threaded_convert():
    global conversion_thread, convert_running, stop_event

    stop_event.clear()

    if not convert_running:

        convert_running = True
        convert_button.config(text='Stop', command=stop_conversion)
        conversion_thread = Thread(target=convert_wrapper)
        conversion_thread.start()

    else:
        stop_conversion()


def stop_conversion():
    global convert_running, conversion_thread
    convert_running = False
    stop_event.set()
    convert_button.config(text='Convert', command=threaded_convert)


def find_file_wrapper():
    global img_loc_count_var, img_convert_count_var, current_image_displayed, convert_running

    if not convert_running:
        find_file(img_loc_count_var, img_convert_count_var)

        locations = get_locations()

        if locations:
            current_image_displayed = 0
            display_image()
        else:
            display_current_image.config(image='')

        show_file_name(locations)


def clear_loc_list_wrapper():
    global img_loc_count_var, current_image_displayed, convert_running

    if not convert_running:
        clear_loc_list(img_loc_count_var)

        locations = get_locations()

        display_current_image.config(image='')
        current_image_displayed = 0

        show_file_name(locations)


def drop_wrapper(files):
    global img_loc_count_var, img_convert_count_var, current_image_displayed, convert_running

    if not convert_running:
        handle_drop(img_loc_count_var, img_convert_count_var, files)

        locations = get_locations()

        if locations:
            current_image_displayed = 0
            display_image()
        else:
            display_current_image.config(image='')

        show_file_name(locations)


def remove_wrapper():
    global current_image_displayed, img_loc_count_var, convert_running

    if not convert_running:
        locations = get_locations()

        if locations:
            remove_image(current_image_displayed, img_loc_count_var)

        if 0 < current_image_displayed <= len(locations):
            current_image_displayed -= 1

        if locations:
            if len(locations) != 0:
                display_image()
            else:
                display_current_image.config(image='')
        else:
            display_current_image.config(image='')

        show_file_name(locations)


def display_image(*args):
    global current_image_displayed
    register_heif_opener()

    locations = get_locations()

    if locations:
        orig_img = Image.open(locations[current_image_displayed])
        resize_img = ImageOps.pad(orig_img, (680, 544), color='#222222')
        display = ImageTk.PhotoImage(resize_img)

        display_current_image.config(image=display)
        display_current_image.image = display

    else:
        display_current_image.config(image='')
        display_current_image.image = None


def update_label(*args):
    global conversion_thread

    current_img_loc_count = img_loc_count_var.get()
    current_conv_count = img_convert_count_var.get()

    if current_img_loc_count == 0:
        progress_label.config(text='0 out of 0 converted')

    elif 0 < current_img_loc_count == current_conv_count:
        progress_label.config(text=f"{current_conv_count} out of {current_img_loc_count} converted Done!")

    else:
        progress_label.config(text=f"{current_conv_count} out of {current_img_loc_count} converted")


def show_file_name(locations, *args):
    global current_image_displayed

    if locations:
        image_name = os.path.basename(locations[current_image_displayed])
        display_image_name.config(text=image_name)

    else:
        display_image_name.config(text="Drop Images in The Box or Press 'Locate Image(s)'")


def right_arrow_press():
    global current_image_displayed

    locations = get_locations()

    if locations:
        if current_image_displayed != (len(locations) - 1):
            current_image_displayed += 1
            display_image()
        else:
            current_image_displayed = 0
            display_image()
    else:
        display_current_image.config(image='')

    show_file_name(locations)


def left_arrow_press():
    global current_image_displayed

    locations = get_locations()

    if locations:
        if current_image_displayed != 0:
            current_image_displayed -= 1
            display_image()
        else:
            current_image_displayed = (len(locations) - 1)
            display_image()
    else:
        display_current_image.config(image='')

    show_file_name(locations)


# -- Creating Classes for Buttons and DragAndDrop --

class Button(tk.Button):
    def __init__(self, master, text_label, x_pos, y_pos, command_func, **kwargs):
        super().__init__(master, text=text_label, command=command_func, **kwargs)

        self.bind('<Button-1>', self.on_click_down)
        self.bind('<ButtonRelease-1>', self.on_click_up)
        self.image = tk.PhotoImage(file="img_assets/button.png")
        self.image_clicked = tk.PhotoImage(file="img_assets/button clicked.png")

        self.config(
            bg='#222222',
            fg='#222222',
            activebackground='#222222',
            activeforeground='#222222',
            borderwidth=0,
            font=("Calibri", 16, 'bold'),
            image=self.image,
            compound='center',
            cursor="hand2")

        self.place(x=x_pos, y=y_pos, anchor=tk.CENTER)

    def on_click_down(self, event):
        self.config(image=self.image_clicked)

    def on_click_up(self, event):
        self.config(image=self.image)


class ButtonSmall(tk.Button):
    def __init__(self, master, text_label, x_pos, y_pos, command_func, **kwargs):
        super().__init__(master, text=text_label, command=command_func, **kwargs)

        self.bind('<Button-1>', self.on_click_down)
        self.bind('<ButtonRelease-1>', self.on_click_up)
        self.image = tk.PhotoImage(file="img_assets/Button small.png")
        self.image_clicked = tk.PhotoImage(file="img_assets/Button small clicked.png")

        self.config(
            bg="#222222",
            fg="#222222",
            activebackground="#222222",
            activeforeground="#222222",
            borderwidth=0,
            font=("Calibri", 12, 'bold'),
            image=self.image,
            compound='center',
            cursor="hand2")

        self.place(x=x_pos, y=y_pos, anchor=tk.CENTER)

    def on_click_down(self, event):
        self.config(image=self.image_clicked)

    def on_click_up(self, event):
        self.config(image=self.image)


class Arrow(tk.Button):
    def __init__(self, master, image, image_clicked, x_pos, y_pos, command_func, **kwargs):
        super().__init__(master, command=command_func, **kwargs)

        self.bind('<Button-1>', self.on_click_down)
        self.bind('<ButtonRelease-1>', self.on_click_up)
        self.image = image
        self.image_clicked = image_clicked

        self.config(
            bg='#222222',
            activebackground='#222222',
            borderwidth=0,
            image=self.image,
            compound='center',
            cursor='hand2')

        self.place(x=x_pos, y=y_pos, anchor=tk.CENTER)

    def on_click_down(self, event):
        self.config(image=self.image_clicked)

    def on_click_up(self, event):
        self.config(image=self.image)


class DragAndDrop(tk.Label):
    def __init__(self, master, background_color, x_pos, y_pos, image, **kwargs):
        super().__init__(master, **kwargs)

        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.on_drop)

        self.master_window = master
        self.image = tk.PhotoImage(file=image)

        self.config(
                bg=background_color,
                image=self.image,
                borderwidth=0,
                compound='bottom')

        self.place(x=x_pos, y=y_pos, anchor=tk.CENTER)

    def on_drop(self, event):

        if event.data:
            files = self.tk.splitlist(event.data)
            drop_wrapper(files)


# -- Setting up Drag and Drop --

d_n_d = DragAndDrop(
    master=window,
    background_color="#222222",
    image="img_assets/Display Box.png",
    x_pos=500,
    y_pos=286)

logo_field = DragAndDrop(
    master=window,
    background_color="#222222",
    image="img_assets/aperture logo.png",
    x_pos=500,
    y_pos=285)


# -- Setting Up image Display Label --

display_current_image = DragAndDrop(
    master=window,
    background_color='#A35400',
    x_pos=500,
    y_pos=286,
    image='')


# -- Setting Up Image Conversion Progress --

img_loc_count_var = tk.IntVar()
img_loc_count_var.set(0)

img_convert_count_var = tk.IntVar()
img_convert_count_var.set(0)

progress_label = tk.Label(
    master=window,
    text='0 out of 0 converted',
    font=("Calibri", 18, 'bold'),
    bg="#222222",
    fg="#A35400")
progress_label.place(x=500, y=688, anchor=tk.CENTER)

img_loc_count_var.trace_add("write", update_label)
img_convert_count_var.trace_add("write", update_label)


# --Setting Up File Name Display --

display_image_name = tk.Label(
    window,
    text="Drop Images in The Box or Press 'Locate Image(s)'",
    font=("Calibri", 18, 'bold'),
    bg='#222222',
    fg='#A35400')
display_image_name.place(x=500, y=591, anchor=tk.CENTER)


# -- Setting Up Buttons --

left_arrow = Arrow(
    master=window,
    image=tk.PhotoImage(file="img_assets/left arrow.png"),
    image_clicked=tk.PhotoImage(file="img_assets/left arrow clicked.png"),
    x_pos=112,
    y_pos=285,
    command_func=left_arrow_press)

right_arrow = Arrow(
    master=window,
    image=tk.PhotoImage(file="img_assets/right arrow.png"),
    image_clicked=tk.PhotoImage(file="img_assets/right arrow clicked.png"),
    x_pos=887,
    y_pos=285,
    command_func=right_arrow_press)

file_locate_button = Button(
    master=window,
    text_label="Locate Image(s)",
    x_pos=248,
    y_pos=685,
    command_func=find_file_wrapper)

convert_button = Button(
    master=window,
    text_label="Convert",
    x_pos=752,
    y_pos=685,
    command_func=threaded_convert)

clear_button = ButtonSmall(
    master=window,
    text_label="Clear",
    x_pos=500,
    y_pos=729,
    command_func=clear_loc_list_wrapper)

remove_button = ButtonSmall(
    master=window,
    text_label="Remove",
    x_pos=500,
    y_pos=630,
    command_func=remove_wrapper)

# -- Setting Up File Type Dropdown --

file_types = ['JPEG', 'PNG', 'TIFF', 'HEIF', 'BMP', 'ICO']

selected_file_type = tk.StringVar()
selected_file_type.set(file_types[0])

file_type_dropdown = ttk.OptionMenu(
    window,
    selected_file_type,
    file_types[0],
    *file_types,)
file_type_dropdown.place(x=815, y=740, anchor=tk.CENTER)

select_label = tk.Label(window,
                        text='Convert To:',
                        font=('Calibri', 18, 'bold'),
                        bg='#222222',
                        fg='#A35400')
select_label.place(x=720, y=740, anchor=tk.CENTER)

if __name__ == "__main__":
    window.mainloop()
