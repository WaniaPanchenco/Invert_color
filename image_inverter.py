import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps
import tkinter.messagebox
import os

class ImageInverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Инвертор цветов изображений")
        self.root.geometry("600x450")
        self.root.configure(bg="#f0f0f0")

        self.image_path = None
        self.original_image = None
        self.inverted_image = None

    

        button_color = "black"  
        text_color = "white" 
        self.load_button = tk.Button(root, text="Загрузить изображение", command=self.load_image, bg=button_color, fg=text_color, padx=10, pady=5, font=("Arial", 10))
        self.load_button.pack(pady=(20, 10))

        self.invert_button = tk.Button(root, text="Инвертировать", command=self.invert_image, state=tk.DISABLED, bg=button_color, fg=text_color, padx=10, pady=5, font=("Arial", 10))
        self.invert_button.pack(pady=(0, 10))

        self.save_button = tk.Button(root, text="Сохранить изображение", command=self.save_image, state=tk.DISABLED, bg=button_color, fg=text_color, padx=10, pady=5, font=("Arial", 10))
        self.save_button.pack(pady=(0, 20))

        self.image_label = tk.Label(root, bg="#f0f0f0")
        self.image_label.pack()

    def load_image(self):
        self.image_path = filedialog.askopenfilename(
            initialdir=".",
            title="Выберите изображение",
            filetypes=(("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif;*.tiff"), ("all files", "*.*"))
        )

        if self.image_path:
            try:
                self.original_image = Image.open(self.image_path)
                self.inverted_image = None
                self.display_image(self.original_image)
                self.invert_button["state"] = tk.NORMAL
                self.save_button["state"] = tk.DISABLED  # Disable save until inverted
            except Exception as e:
                tkinter.messagebox.showerror("Ошибка", f"Не удалось загрузить изображение: {e}")

    def invert_image(self):
        if self.original_image is not None:
            try:
                # Преобразование в RGB, если изображение в формате RGBA (Ненавижу)
                if self.original_image.mode == "RGBA":
                    self.original_image = self.original_image.convert("RGB")

                self.inverted_image = ImageOps.invert(self.original_image)
                self.display_image(self.inverted_image)
                self.save_button["state"] = tk.NORMAL  
            except Exception as e:
                tkinter.messagebox.showerror("Ошибка", f"Не удалось инвертировать изображение: {e}")

    def save_image(self):
        if self.inverted_image is not None:
            try:
                file_extension = os.path.splitext(self.image_path)[1]
                suggested_name = "inverted" + file_extension
                save_path = filedialog.asksaveasfilename(
                    initialdir=".",
                    title="Сохранить изображение как",
                    defaultextension=file_extension,
                    initialfile=suggested_name,
                    filetypes=[("Image file", "*" + file_extension), ("all files", "*.*")]
                )
                if save_path:
                    self.inverted_image.save(save_path)
                    tkinter.messagebox.showinfo("Сохранено", "Изображение успешно сохранено.")
            except Exception as e:
                tkinter.messagebox.showerror("Ошибка", f"Не удалось сохранить изображение: {e}")
        else:
            tkinter.messagebox.showerror("Ошибка", "Нет инвертированного изображения для сохранения.")

    def display_image(self, image):

        maximum_size = (500, 300)

        image.thumbnail(maximum_size)
        imgtk = ImageTk.PhotoImage(image=image)
        self.image_label.imgtk = imgtk
        self.image_label.config(image=imgtk)

if __name__ == "__main__":
    root = tk.Tk()
    gui = ImageInverterGUI(root)
    root.mainloop()