import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as messagebox
from PIL import Image, ImageTk
import docx
import PyPDF2
import argparse

def levenstein(str_1, str_2):
    n, m = len(str_1), len(str_2)
    if n > m:
        str_1, str_2 = str_2, str_1
        n, m = m, n

    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if str_1[j - 1] != str_2[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]

class AntiPlagiarismApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Перевірка схожості текстових файлів")
        image_frame = tk.Frame(root)
        image_frame.pack()

        background_image = Image.open("nubip.png")
        background_image.thumbnail((background_image.width // 2, background_image.height // 2))
        background_photo = ImageTk.PhotoImage(background_image)
        background_label = tk.Label(image_frame, image=background_photo)
        background_label.image = background_photo
        background_label.pack()

        frame = tk.Frame(root)
        frame.pack(padx=400, pady=100)

        self.file_type_var = tk.StringVar()
        self.file_type_var.set("docx")

        self.file_type_menu = tk.OptionMenu(frame, self.file_type_var, "docx", "pdf", "txt")
        self.file_type_menu.pack()

        self.compare_button = tk.Button(frame, text="Перевірити схожість", command=self.compare_files)
        self.compare_button.pack()

def compare_files(self):
        file_type = self.file_type_var.get()
        first_path = filedialog.askopenfilename(filetypes=self.get_filetypes(file_type))
        second_path = filedialog.askopenfilename(filetypes=self.get_filetypes(file_type))

        if not first_path or not second_path:
            self.show_error("Оберіть два файли для порівняння.")
            return

        first_text = self.read_file(file_type, first_path)
        second_text = self.read_file(file_type, second_path)

        similarity_score = 1 - levenstein(first_text, second_text) / len(second_text)
        if (similarity_score <= 0):
            tk.messagebox.showinfo("Результат порівняння", f"Схожість текстів: {0*100:.1f}%")
        else:
            tk.messagebox.showinfo("Результат порівняння", f"Схожість текстів: {similarity_score*100:.1f}%")