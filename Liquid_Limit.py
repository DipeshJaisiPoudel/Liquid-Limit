import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np

# Function to plot the particle size distribution curve
def plot_curve(blows, water_content, student_info):
    plt.figure(figsize=(10, 6))

    # Perform linear regression on the log of the blows to find the best fit line
    log_blows = np.log10(blows)
    slope, intercept = np.polyfit(log_blows, water_content, 1)
    best_fit_line = np.poly1d([slope, intercept])

    x_interp = np.linspace(min(blows), max(blows), 1000)
    y_interp = best_fit_line(np.log10(x_interp))

    # Plot the best fit straight line
    plt.plot(x_interp, y_interp, color='b', label='Best Fit Line')

    # Plot data points
    plt.scatter(blows, water_content, color='r', label='Data Points')

    # Plot vertical line at 25 blows
    y_at_25_blows = best_fit_line(np.log10(25))
    plt.axvline(x=25, color='g', linestyle='--', label=f'Liquid Limit: {y_at_25_blows:.2f}')
    plt.scatter(25, y_at_25_blows, color='g', marker='x')

    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xlabel("Number of Blows")
    plt.ylabel("Water Content")
    plt.title(f"Lab 4: Consistency Limits Test for Fine Grained Soil - Liquid Limit\nStudent: {student_info['name']}, Roll No: {student_info['roll']}, Exam Symbol: {student_info['exam_symbol']}")
    plt.xscale('log')  # Set x-axis to logarithmic scale
    plt.xticks([1, 10, 100])  # Set x-axis ticks at intervals of multiples of 10
    plt.legend()
    plt.show()

# Function to get data points from the user
def get_data_points(num_points, student_info):
    data_window = tk.Tk()
    data_window.title("Enter Data Points")
    data_window.geometry("800x600")

    font_large = ("Times New Roman", 30, "bold")
    font_medium = ("Times New Roman", 20, "bold")
    font_small = ("Times New Roman", 14, "bold")

    title_label = tk.Label(data_window, text="Lab 4: Consistency Limits Test for Fine Grained Soil - Liquid Limit", font=font_large, bg="lightblue", pady=10)
    title_label.pack(pady=10)

    form_frame = tk.Frame(data_window)
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Number of Blows", font=font_medium).grid(row=0, column=0, padx=5, pady=5)
    tk.Label(form_frame, text="Water Content", font=font_medium).grid(row=0, column=1, padx=5, pady=5)

    blows = []
    water_content = []

    entries = []
    for i in range(num_points):
        entry_row = []
        for j in range(2):
            entry = tk.Entry(form_frame, font=font_medium)
            entry.grid(row=i + 1, column=j, padx=5, pady=5)
            entry_row.append(entry)
        entries.append(entry_row)

    def on_ok():
        try:
            for entry_row in entries:
                blow = float(entry_row[0].get())
                water = float(entry_row[1].get())
                if not (0 <= water <= 100):
                    raise ValueError("Water content must be between 0 and 100.")
                blows.append(blow)
                water_content.append(water)
            if len(set(blows)) != len(blows):
                raise ValueError("Number of blows must be unique.")
            data_window.destroy()
            plot_curve(blows, water_content, student_info)
        except ValueError as ve:
            messagebox.showerror("Invalid input", f"Please enter valid numerical values.\nError: {ve}")

    ok_button = tk.Button(data_window, text="OK", command=on_ok, font=font_medium)
    ok_button.pack(pady=10)

    credit_frame = tk.Frame(data_window, bd=2, relief="groove", padx=10, pady=10)
    credit_frame.pack(side="bottom", pady=10)
    credit_label = tk.Label(credit_frame, text="Developed by: Er. Dipesh Jaisi Poudel\nMSc. in Structural Engineering\nLecturer, School of Engineering, Pokhara University", font=font_small, fg="darkblue")
    credit_label.pack()

    data_window.mainloop()

# Custom dialog to get initial student info and number of data points
def get_initial_info():
    initial_info_window = tk.Tk()
    initial_info_window.title("Student Information")
    initial_info_window.geometry("800x600")

    font_large = ("Times New Roman", 30, "bold")
    font_medium = ("Times New Roman", 20, "bold")
    font_small = ("Times New Roman", 14, "bold")

    title_label = tk.Label(initial_info_window, text="Lab 4: Consistency Limits Test for Fine Grained Soil - Liquid Limit", font=font_large, bg="lightblue", pady=10)
    title_label.pack(pady=10)

    form_frame = tk.Frame(initial_info_window)
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Student Name:", font=font_medium).grid(row=0, column=0, padx=5, pady=5, sticky='e')
    tk.Label(form_frame, text="Roll Number:", font=font_medium).grid(row=1, column=0, padx=5, pady=5, sticky='e')
    tk.Label(form_frame, text="Exam Symbol Number:", font=font_medium).grid(row=2, column=0, padx=5, pady=5, sticky='e')
    tk.Label(form_frame, text="Number of Data Points:", font=font_medium).grid(row=3, column=0, padx=5, pady=5, sticky='e')

    name_entry = tk.Entry(form_frame, font=font_medium)
    roll_entry = tk.Entry(form_frame, font=font_medium)
    exam_symbol_entry = tk.Entry(form_frame, font=font_medium)
    num_points_entry = tk.Entry(form_frame, font=font_medium)

    name_entry.grid(row=0, column=1, padx=5, pady=5)
    roll_entry.grid(row=1, column=1, padx=5, pady=5)
    exam_symbol_entry.grid(row=2, column=1, padx=5, pady=5)
    num_points_entry.grid(row=3, column=1, padx=5, pady=5)

    def on_ok():
        try:
            student_info = {
                'name': name_entry.get(),
                'roll': roll_entry.get(),
                'exam_symbol': exam_symbol_entry.get()
            }
            num_points = int(num_points_entry.get())
            if not student_info['name'] or not student_info['roll'] or not student_info['exam_symbol']:
                raise ValueError("All fields are required.")
            initial_info_window.destroy()
            get_data_points(num_points, student_info)
        except ValueError as ve:
            messagebox.showerror("Invalid input", f"Please fill in all the fields with valid information.\nError: {ve}")

    ok_button = tk.Button(initial_info_window, text="OK", command=on_ok, font=font_medium)
    ok_button.pack(pady=10)

    credit_frame = tk.Frame(initial_info_window, bd=2, relief="groove", padx=10, pady=10)
    credit_frame.pack(side="bottom", pady=10)
    credit_label = tk.Label(credit_frame, text="Developed by: Er. Dipesh Jaisi Poudel\nMSc. in Structural Engineering\nLecturer, School of Engineering, Pokhara University", font=font_small, fg="darkblue")
    credit_label.pack()

    initial_info_window.mainloop()


# Start the program
get_initial_info()
