import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from fpdf import FPDF

class FileConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Type Converter")
        self.root.geometry("500x500")
        self.root.resizable(False, False)

        self.selected_file = None

        # Try loading icon
        try:
            icon_img = Image.open("file_icon.png")
            icon_img = icon_img.resize((80, 80), Image.ANTIALIAS)
            self.tk_icon = ImageTk.PhotoImage(icon_img)
            self.icon_label = tk.Label(root, image=self.tk_icon)
            self.icon_label.pack(pady=10)
        except:
            self.icon_label = tk.Label(root, text="📂", font=("Arial", 50))
            self.icon_label.pack(pady=10)

        # UI Elements
        self.label = tk.Label(root, text="Select a File to Convert", font=("Arial", 14))
        self.label.pack(pady=10)

        self.select_button = tk.Button(root, text="Choose File", command=self.choose_file, font=("Arial", 12), bg="#0078D7", fg="white")
        self.select_button.pack(pady=5)

        # Dropdown for target format
        self.format_label = tk.Label(root, text="Select Target Format:", font=("Arial", 12))
        self.format_label.pack(pady=5)

        self.format_var = tk.StringVar()
        self.format_dropdown = ttk.Combobox(root, textvariable=self.format_var, state="readonly", font=("Arial", 12))
        self.format_dropdown['values'] = ("jpg", "jpeg", "png", "pdf")
        self.format_dropdown.current(0)
        self.format_dropdown.pack(pady=5)

        self.convert_button = tk.Button(root, text="Convert", command=self.convert_file, font=("Arial", 12), bg="#28A745", fg="white", state=tk.DISABLED)
        self.convert_button.pack(pady=10)

        # Preview area
        self.preview_label = tk.Label(root, text="", font=("Arial", 10))
        self.preview_label.pack(pady=5)
        self.preview_canvas = tk.Label(root)
        self.preview_canvas.pack(pady=5)

        self.quit_button = tk.Button(root, text="Exit", command=root.quit, font=("Arial", 12), bg="#DC3545", fg="white")
        self.quit_button.pack(pady=10)

    def choose_file(self):
        self.selected_file = filedialog.askopenfilename(title="Select a File", filetypes=[
            ("Images and PDF", "*.jpg;*.jpeg;*.png;*.bmp;*.gif;*.pdf"),
            ("All Files", "*.*")
        ])
        if self.selected_file:
            self.label.config(text=f"Selected: {os.path.basename(self.selected_file)}")
            self.convert_button.config(state=tk.NORMAL)
            self.show_preview()

    def show_preview(self):
        file_ext = os.path.splitext(self.selected_file)[1].lower()
        try:
            if file_ext in [".jpg", ".jpeg", ".png", ".bmp", ".gif"]:
                img = Image.open(self.selected_file)
                img.thumbnail((200, 200))
                self.tk_preview = ImageTk.PhotoImage(img)
                self.preview_canvas.config(image=self.tk_preview)
                self.preview_label.config(text="Image Preview")
            elif file_ext == ".pdf":
                from pdf2image import convert_from_path
                pages = convert_from_path(self.selected_file, first_page=1, last_page=1)
                pages[0].thumbnail((200, 200))
                self.tk_preview = ImageTk.PhotoImage(pages[0])
                self.preview_canvas.config(image=self.tk_preview)
                self.preview_label.config(text="PDF Preview (Page 1)")
            else:
                self.preview_canvas.config(image='')
                self.preview_label.config(text="Preview not available.")
        except Exception as e:
            print(f"Preview error: {e}")
            self.preview_canvas.config(image='')
            self.preview_label.config(text="Preview not available.")

    def convert_file(self):
        if not self.selected_file:
            messagebox.showerror("Error", "No file selected!")
            return

        target_format = self.format_var.get()
        file_ext = os.path.splitext(self.selected_file)[1].lower()

        output_dir = os.path.join(os.path.dirname(self.selected_file), "Converted_Files")
        os.makedirs(output_dir, exist_ok=True)

        output_name = os.path.splitext(os.path.basename(self.selected_file))[0] + f"_converted.{target_format}"
        output_path = os.path.join(output_dir, output_name)

        try:
            if file_ext in [".jpg", ".jpeg", ".png", ".bmp", ".gif"]:
                self.convert_image(output_path, target_format)
            elif file_ext == ".pdf":
                self.convert_pdf(output_path, target_format)
            else:
                messagebox.showinfo("Unsupported", f"Conversion for {file_ext} is not supported yet.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def convert_image(self, output_path, target_format):
        with Image.open(self.selected_file) as img:
            if target_format == "pdf":
                img.convert("RGB").save(output_path, "PDF")
            else:
                img.save(output_path, target_format.upper())
        messagebox.showinfo("Success", f"File converted successfully: {output_path}")

    def convert_pdf(self, output_path, target_format):
        from pdf2image import convert_from_path
        pages = convert_from_path(self.selected_file)

        if target_format == "pdf":
            messagebox.showinfo("Info", "Source and target formats are both PDF!")
            return

        for idx, page in enumerate(pages):
            single_output = output_path.replace(f".{target_format}", f"_page{idx+1}.{target_format}")
            page.save(single_output, target_format.upper())

        messagebox.showinfo("Success", f"PDF converted to {target_format.upper()} images!")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileConverterApp(root)
    root.mainloop()