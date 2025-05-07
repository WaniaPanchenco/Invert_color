import tkinter as tk  # Для создания графического интерфейса
from tkinter import filedialog  # Для открытия диалогов выбора/сохранения файлов
from PIL import Image, ImageTk, ImageOps  # Для работы с изображениями
import tkinter.messagebox  # Для отображения всплывающих сообщений
import os  # Для работы с файловой системой

class ImageInverterGUI:  # Класс для графического интерфейса
    def __init__(self, root):
        self.root = root
        self.root.title("Инвертор цветов")
        self.root.geometry("1920x1080")
        self.root.configure(bg="#f0f0f0")

        self.image_path = None  # Путь к файлу изображения
        self.original_image = None  # Оригинальное изображение (PIL)
        self.inverted_image = None  # Инвертированное изображение (PIL)
        self.original_image_format = None # Формат оригинального изображения (JPEG, PNG и т.д.)

        button_color = "black"
        text_color = "white"
        self.load_button = tk.Button(root, text="Загрузить", command=self.load_image, bg=button_color, fg=text_color, padx=10, pady=5, font=("Arial", 10))
        self.load_button.pack(pady=(20, 10))

        self.invert_button = tk.Button(root, text="Инвертировать", command=self.invert_image, state=tk.DISABLED, bg=button_color, fg=text_color, padx=10, pady=5, font=("Arial", 10))
        self.invert_button.pack(pady=(0, 10))

        self.save_button = tk.Button(root, text="Сохранить", command=self.save_image, state=tk.DISABLED, bg=button_color, fg=text_color, padx=10, pady=5, font=("Arial", 10))
        self.save_button.pack(pady=(0, 20))

        self.image_label = tk.Label(root, bg="#f0f0f0")  # Метка для отображения изображения
        self.image_label.pack()


    def load_image(self):  # Загрузка изображения из файла
        self.image_path = filedialog.askopenfilename(initialdir=".", title="Выберите изображение", filetypes=(("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif;*.tiff"), ("all files", "*.*")))

        if self.image_path:
            try:
                self.original_image = Image.open(self.image_path)
                self.original_image_format = self.original_image.format # Сохраняем формат файла
                self.inverted_image = None
                self.display_image(self.original_image)
                self.invert_button["state"] = tk.NORMAL # Включаем кнопку "Инвертировать"
                self.save_button["state"] = tk.DISABLED  # Выключаем кнопку "Сохранить"
            except Exception as e:
                tkinter.messagebox.showerror("Ошибка", f"Не удалось загрузить: {e}")  # Отображаем ошибку


    def invert_image(self):  # Инвертирование цветов изображения
        if self.original_image is not None:
            try:
                if self.original_image.mode == "RGBA":  # Преобразование RGBA в RGB
                    self.original_image = self.original_image.convert("RGB")

                self.inverted_image = ImageOps.invert(self.original_image)
                self.display_image(self.inverted_image)
                self.save_button["state"] = tk.NORMAL  # Включаем кнопку "Сохранить"
            except Exception as e:
                tkinter.messagebox.showerror("Ошибка", f"Не удалось инвертировать: {e}")


    def save_image(self):  # Сохранение инвертированного изображения
        if self.inverted_image is not None:
            try:
                save_path = filedialog.asksaveasfilename(
                    initialdir=".",
                    title="Сохранить как",
                    defaultextension="." + self.original_image_format.lower() if self.original_image_format else "",  # Расширение из исходного формата
                    initialfile="inverted",
                    filetypes=[(f"Image file ({self.original_image_format})", "*." + self.original_image_format.lower())] if self.original_image_format else [("all files", "*.*")]
                )
                if save_path:
                    self.inverted_image.save(save_path, format=self.original_image_format)  # Сохраняем в исходном формате!
                    tkinter.messagebox.showinfo("Сохранено", "Изображение сохранено.")
            except Exception as e:
                tkinter.messagebox.showerror("Ошибка", f"Не удалось сохранить: {e}")
        else:
            tkinter.messagebox.showerror("Ошибка", "Нет изображения для сохранения.")


    def display_image(self, image):  # Отображение изображения (с изменением размера)
        maximum_size = (9000, 5000)
        image.thumbnail(maximum_size)
        imgtk = ImageTk.PhotoImage(image=image)
        self.image_label.imgtk = imgtk  # Предотвращаем сборку мусора
        self.image_label.config(image=imgtk)


if __name__ == "__main__":  # Запуск GUI
    root = tk.Tk()
    gui = ImageInverterGUI(root)
    root.mainloop()
