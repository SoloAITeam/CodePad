import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import platform

class CodeEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("Cross-Platform Code Editor")
        self.master.geometry("800x600")

        # Make the window fullscreen
        self.master.attributes("-fullscreen", True)

        # Set background gradient (from white to gray)
        self.canvas = tk.Canvas(self.master)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self.draw_gradient)

        self.text_area = scrolledtext.ScrolledText(self.canvas, wrap=tk.WORD)
        self.text_area.place(relwidth=1, relheight=1)

        self.menu_bar = tk.Menu(master)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_as_file)
        self.file_menu.add_separator()
        
        if platform.system() == 'Linux':
            self.file_menu.add_command(label="Print", command=self.print_file)

        self.file_menu.add_command(label="Exit", command=self.exit_app)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Undo", command=self.undo)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        self.font_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.font_menu.add_command(label="Arial", command=lambda: self.set_font("Arial"))
        self.font_menu.add_command(label="Helvetica", command=lambda: self.set_font("Helvetica"))
        self.font_menu.add_command(label="Times New Roman", command=lambda: self.set_font("Times New Roman"))
        self.menu_bar.add_cascade(label="Fonts", menu=self.font_menu)
        
        self.language_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.language_menu.add_command(label="English", command=lambda: self.set_language("English"))
        self.language_menu.add_command(label="Spanish", command=lambda: self.set_language("Spanish"))
        self.language_menu.add_command(label="French", command=lambda: self.set_language("French"))
        self.menu_bar.add_cascade(label="Language", menu=self.language_menu)

        self.master.config(menu=self.menu_bar)

        # Set default font
        self.set_font("Arial")

    def draw_gradient(self, event=None):
        self.canvas.delete("gradient")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        limit = height
        (r1, g1, b1) = (255, 255, 255)
        (r2, g2, b2) = (192, 192, 192)
        r_ratio = float(r2 - r1) / limit
        g_ratio = float(g2 - g1) / limit
        b_ratio = float(b2 - b1) / limit

        for i in range(limit):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = f"#{nr:02x}{ng:02x}{nb:02x}"
            self.canvas.create_line(0, i, width, i, tags=("gradient"), fill=color)
        self.canvas.lower("gradient")

    def new_file(self):
        self.text_area.delete(1.0, tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file:\n{e}")

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "w") as file:
                    content = self.text_area.get(1.0, tk.END)
                    file.write(content)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{e}")

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "w") as file:
                    content = self.text_area.get(1.0, tk.END)
                    file.write(content)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{e}")

    def set_font(self, font_name):
        self.text_area.configure(font=(font_name, 12))

    def set_language(self, language):
        messagebox.showinfo("Language", f"Language set to {language}")

    def print_file(self):
        file_content = self.text_area.get(1.0, tk.END)
        temp_file = '/tmp/tempfile_to_print.txt'
        try:
            with open(temp_file, 'w') as file:
                file.write(file_content)
            os.system(f'lpr {temp_file}')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to print file:\n{e}")

    def undo(self):
        try:
            self.text_area.edit_undo()
        except:
            pass

    def exit_app(self):
        self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeEditor(root)
    root.mainloop()
