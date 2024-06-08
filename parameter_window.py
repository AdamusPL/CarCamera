import tkinter as tk
from tkinter import ttk, Frame, Label, Button, Entry, Checkbutton, IntVar
import cv2

import main_with_interface


def detect_cameras(max_cameras=2):
    available_cameras = []
    for i in range(max_cameras):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available_cameras.append(i)
            cap.release()
    return available_cameras


root = tk.Tk()
options_frame = Frame(root)
canvas = tk.Canvas(root, width=960, height=540, bg='white')

width_variable = tk.StringVar(root)
width = Entry(options_frame, textvariable=width_variable)
width.insert(0, "925")

cameras = detect_cameras()
camera_var = tk.StringVar()
camera_var.set(cameras[0] if cameras else "No cameras found")

number_of_lines_variable = tk.StringVar(root)
number_of_lines = Entry(options_frame, textvariable=number_of_lines_variable)
number_of_lines.insert(0, "5")

space_between_lines_variable = tk.StringVar(root)
space_between_lines = Entry(options_frame, textvariable=space_between_lines_variable)
space_between_lines.insert(0, "80")

angle_of_lines_variable = tk.StringVar(root)
angle_of_lines = Entry(options_frame, textvariable=angle_of_lines_variable)
angle_of_lines.insert(0, "40")

crop_x1_variable = tk.StringVar(root)
crop_x1 = Entry(options_frame, textvariable=crop_x1_variable)
crop_x1.insert(0, "0")

crop_x2_variable = tk.StringVar(root)
crop_x2 = Entry(options_frame, textvariable=crop_x2_variable)
crop_x2.insert(0, "960")

crop_y1_variable = tk.StringVar(root)
crop_y1 = Entry(options_frame, textvariable=crop_y1_variable)
crop_y1.insert(0, "0")

crop_y2_variable = tk.StringVar(root)
crop_y2 = Entry(options_frame, textvariable=crop_y2_variable)
crop_y2.insert(0, "540")

check_frame = Frame(options_frame)

check_car_var = IntVar(value=1)
chk_car = Checkbutton(check_frame, text='Cars', variable=check_car_var, onvalue=1, offvalue=0)
chk_car.grid(row=0, column=0)

check_person_var = IntVar(value=1)
chk_person = Checkbutton(check_frame, text='People', variable=check_person_var, onvalue=1, offvalue=0)
chk_person.grid(row=0, column=1)

check_bollard_var = IntVar(value=1)
chk_bollard = Checkbutton(check_frame, text='Bollard', variable=check_bollard_var, onvalue=1, offvalue=0)
chk_bollard.grid(row=0, column=2)

check_wall_var = IntVar(value=1)
chk_wall = Checkbutton(check_frame, text='Wall', variable=check_wall_var, onvalue=1, offvalue=0)
chk_wall.grid(row=0, column=3)

confidence_var = tk.StringVar(root)
confidence = Entry(options_frame, textvariable=confidence_var)
confidence.insert(0, "0.3")


def on_mode_change(event):
    if mode_var.get() == "Camera":
        camera_menu.config(state="normal")
    else:
        camera_menu.config(state="disabled")


mode_var = tk.StringVar(value="Camera")
mode_menu = ttk.Combobox(options_frame, textvariable=mode_var, values=["Camera", "File"])
mode_menu.bind("<<ComboboxSelected>>", on_mode_change)

camera_menu = ttk.Combobox(options_frame, textvariable=camera_var, values=cameras)


def draw_line(x1, y1, x2, y2, nr_of_line, thickness):
    if nr_of_line == 0 or nr_of_line == 1:
        color = "red"
    elif nr_of_line == 2 or nr_of_line == 3:
        color = "orange"
    else:
        color = "green"
    canvas.create_line(x1, y1, x2, y2, fill=color, width=thickness)


def update_lines():
    crop_x1 = int(crop_x1_variable.get())
    crop_x2 = int(crop_x2_variable.get())
    crop_y1 = int(crop_y1_variable.get())
    crop_y2 = int(crop_y2_variable.get())
    space_between_lines = int(space_between_lines_variable.get()) // 2
    nr_of_lines = int(number_of_lines_variable.get())
    angle_of_lines = int(angle_of_lines_variable.get()) // 2
    offset = int(width_variable.get()) // 2
    canvas.delete("all")

    start_draw_lines_y = crop_y2
    end_draw_lines_y = max(crop_y1, crop_y2 - nr_of_lines * space_between_lines)
    height_of_line = crop_y2
    middle = (crop_x2 + crop_x1) // 2
    middle_line_left_x = middle - offset // 2
    middle_line_right_x = middle + offset // 2
    nr_of_line = 0
    thickness = 9

    for y in range(start_draw_lines_y, end_draw_lines_y, -space_between_lines):
        left_x1 = middle_line_left_x
        right_x1 = middle_line_right_x
        left_x2 = middle_line_left_x + angle_of_lines
        right_x2 = middle_line_right_x - angle_of_lines

        draw_line(left_x1, y, left_x2, y - space_between_lines, nr_of_line, thickness)
        draw_line(right_x1, y, right_x2, y - space_between_lines, nr_of_line, thickness)

        draw_line(left_x2, y - space_between_lines, left_x2 + 50, y - space_between_lines, nr_of_line, thickness)
        draw_line(right_x2 - 50, y - space_between_lines, right_x2, y - space_between_lines, nr_of_line, thickness)

        middle_line_left_x = left_x2
        middle_line_right_x = right_x2

        nr_of_line += 1


def parameter_window():
    root.title("Choose parameters")
    root.geometry("1350x550")
    root.config(bg='white')

    title = Label(options_frame, text="Car Front Camera")
    title.config(font=("Courier", 14))

    width_label = Label(options_frame, text="Width of lines")
    width_label.config(font=("Courier", 14))

    number_of_lines_label = Label(options_frame, text="Number of lines")
    number_of_lines_label.config(font=("Courier", 14))

    space_between_lines_label = Label(options_frame, text="Space between lines")
    space_between_lines_label.config(font=("Courier", 14))

    angle_of_lines_label = Label(options_frame, text="Angle of lines")
    angle_of_lines_label.config(font=("Courier", 14))

    crop_x_label = Label(options_frame, text="Crop in x")
    crop_x_label.config(font=("Courier", 14))

    crop_y_label = Label(options_frame, text="Crop in y")
    crop_y_label.config(font=("Courier", 14))

    detecting_label = Label(options_frame, text="Objects to detect")
    detecting_label.config(font=("Courier", 14))

    confidence_label = Label(options_frame, text="Detection confidence")
    confidence_label.config(font=("Courier", 14))

    filepath_label = Label(options_frame, text="Choose source to run detection on")
    filepath_label.config(font=("Courier", 14))

    buttons = Frame(options_frame)
    confirm = Button(buttons, text="Confirm",
                     command=lambda: (root.destroy(), main_with_interface.main(check_car_var.get(), check_person_var.get(),
                                                              check_bollard_var.get(),
                                                              check_wall_var.get(),
                                                              int(crop_x1_variable.get()),
                                                              int(crop_x2_variable.get()),
                                                              int(crop_y1_variable.get()),
                                                              int(crop_y2_variable.get()),
                                                              int(width_variable.get()),
                                                              int(number_of_lines_variable.get()),
                                                              int(space_between_lines_variable.get()),
                                                              int(angle_of_lines_variable.get()),
                                                              float(confidence_var.get()),
                                                              camera_var.get(),
                                                              mode_var.get())))
    confirm.pack(side=tk.LEFT)
    check = Button(buttons, text="Check lines", command=update_lines)
    check.pack(side=tk.RIGHT)

    title.pack()
    crop_x_label.pack()
    crop_x1.pack()
    crop_x2.pack()
    crop_y_label.pack()
    crop_y1.pack()
    crop_y2.pack()
    width_label.pack()
    width.pack()
    number_of_lines_label.pack()
    number_of_lines.pack()
    space_between_lines_label.pack()
    space_between_lines.pack()
    angle_of_lines_label.pack()
    angle_of_lines.pack()
    detecting_label.pack()
    check_frame.pack()
    confidence_label.pack()
    confidence.pack()
    filepath_label.pack()
    mode_menu.pack()
    camera_menu.pack()
    buttons.pack()
    options_frame.pack(side=tk.LEFT)
    canvas.pack(side=tk.RIGHT)

    on_mode_change(None)
    root.mainloop()

if __name__ == '__main__':
    parameter_window()
