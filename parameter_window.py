import tkinter as tk
import main_with_interface

from tkinter import *

buttonClicked = False
root = tk.Tk()
width_variable = tk.StringVar(root)
width = tk.Entry(root, textvariable=width_variable)
width.insert(0, "925")

number_of_lines_variable = tk.StringVar(root)
number_of_lines = tk.Entry(root, textvariable=number_of_lines_variable)
number_of_lines.insert(0, "5")

space_between_lines_variable = tk.StringVar(root)
space_between_lines = tk.Entry(root, textvariable=space_between_lines_variable)
space_between_lines.insert(0, "150")

angle_of_lines_variable = tk.StringVar(root)
angle_of_lines = tk.Entry(root, textvariable=angle_of_lines_variable)
angle_of_lines.insert(0, "110")

crop_x1_variable = tk.StringVar(root)
crop_x1 = tk.Entry(root, textvariable=crop_x1_variable)
crop_x1.insert(0, "0")

crop_x2_variable = tk.StringVar(root)
crop_x2 = tk.Entry(root, textvariable=crop_x2_variable)
crop_x2.insert(0, "1920")

crop_y1_variable = tk.StringVar(root)
crop_y1 = tk.Entry(root, textvariable=crop_y1_variable)
crop_y1.insert(0, "0")

crop_y2_variable = tk.StringVar(root)
crop_y2 = tk.Entry(root, textvariable=crop_y2_variable)
crop_y2.insert(0, "1080")

check_car_var = tk.IntVar()
chk_car = tk.Checkbutton(root, text='Cars', variable=check_car_var)

check_person_var = tk.IntVar()
chk_person = tk.Checkbutton(root, text='People', variable=check_person_var)

check_bollard_var = tk.IntVar()
chk_bollard = tk.Checkbutton(root, text='Bollard', variable=check_bollard_var)

# check_wall_var = tk.IntVar()
# chk_wall = tk.Checkbutton(root, text='Wall', variable=check_wall_var)


def parameter_window():
    root.title("Choose parameters")
    root.geometry('500x500')
    root.config(bg='gray')

    title = Label(root, text="Car Front Camera")
    title.config(font=("Courier", 14))

    width_label = Label(root, text="Width of lines")
    width_label.config(font=("Courier", 14))

    number_of_lines_label = Label(root, text="Number of lines")
    number_of_lines_label.config(font=("Courier", 14))

    space_between_lines_label = Label(root, text="Space between lines")
    space_between_lines_label.config(font=("Courier", 14))

    angle_of_lines_label = Label(root, text="Angle of lines")
    angle_of_lines_label.config(font=("Courier", 14))

    crop_x_label = Label(root, text="Crop in x")
    crop_x_label.config(font=("Courier", 14))

    crop_y_label = Label(root, text="Crop in y")
    crop_y_label.config(font=("Courier", 14))

    detecting_label = Label(root, text="Objects to detect")
    detecting_label.config(font=("Courier", 14))

    confirm = Button(text="Confirm",
                     command=lambda: main_with_interface.main(check_car_var.get(), check_person_var.get(), check_bollard_var.get(),
                                                              int(crop_x1_variable.get()),
                                                              int(crop_x2_variable.get()),
                                                              int(crop_y1_variable.get()),
                                                              int(crop_y2_variable.get()),
                                                              int(width_variable.get()),
                                                              int(number_of_lines_variable.get()),
                                                              int(space_between_lines_variable.get()),
                                                              int(angle_of_lines_variable.get())))

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
    chk_car.pack()
    chk_person.pack()
    chk_bollard.pack()
    # chk_wall.pack()
    confirm.pack()

    root.mainloop()
