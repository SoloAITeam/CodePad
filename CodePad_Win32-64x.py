import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import shutil

class CodeEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("Code Editor")
        self.master.attributes('-fullscreen', True)  # Set fullscreen mode
        
        # Text area
        self.text_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, font=("Courier New", 12))
        self.text_area.pack(expand=True, fill='both')
        
        # Menu bar
        menu_bar = tk.Menu(master)
        
        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As", command=self.save_as_file, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Move to Recycle Bin", command=self.move_to_recycle_bin)
        file_menu.add_command(label="Print", command=self.print_file)
        file_menu.add_command(label="Print Now", command=self.print_now)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_app, accelerator="Ctrl+Q")
        menu_bar.add_cascade(label="File", menu=file_menu)
        
        # Edit menu
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        
        # Language menu
        language_menu = tk.Menu(menu_bar, tearoff=0)
        language_menu.add_command(label="English", command=lambda: self.set_language("English"))
        language_menu.add_command(label="Spanish", command=lambda: self.set_language("Spanish"))
        language_menu.add_command(label="French", command=lambda: self.set_language("French"))
        menu_bar.add_cascade(label="Language", menu=language_menu)
        
        self.master.config(menu=menu_bar)
        
        # Bind shortcuts
        self.master.bind("<Control-n>", lambda event: self.new_file())
        self.master.bind("<Control-o>", lambda event: self.open_file())
        self.master.bind("<Control-s>", lambda event: self.save_file())
        self.master.bind("<Control-S>", lambda event: self.save_as_file())
        self.master.bind("<Control-q>", lambda event: self.exit_app())
        self.master.bind("<Control-z>", lambda event: self.undo())
        self.master.bind("<Control-y>", lambda event: self.redo())

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
                self.current_file = file_path
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file:\n{e}")

    def save_file(self):
        if hasattr(self, 'current_file'):
            try:
                with open(self.current_file, "w") as file:
                    content = self.text_area.get(1.0, tk.END)
                    file.write(content)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{e}")
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "w") as file:
                    content = self.text_area.get(1.0, tk.END)
                    file.write(content)
                    self.current_file = file_path
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{e}")

    def move_to_recycle_bin(self):
        if hasattr(self, 'current_file'):
            try:
                recycle_bin_path = os.path.expanduser('~\\AppData\\Local\\Recycle Bin')
                if not os.path.exists(recycle_bin_path):
                    os.makedirs(recycle_bin_path)
                shutil.move(self.current_file, recycle_bin_path)
                self.new_file()
                messagebox.showinfo("Success", "File moved to Recycle Bin")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to move file to Recycle Bin:\n{e}")

    def print_file(self):
        if hasattr(self, 'current_file'):
            self.print_document(self.current_file)

    def print_now(self):
        if hasattr(self, 'current_file'):
            self.print_document(self.current_file)

    def print_document(self, file_path):
        try:
            os.startfile(file_path, "print")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to print file:\n{e}")

    def set_language(self, language):
        messagebox.showinfo("Language", f"Language set to {language}")

    def exit_app(self):
        self.master.quit()

    def undo(self):
        try:
            self.text_area.edit_undo()
        except Exception as e:
            messagebox.showerror("Error", f"Nothing to undo:\n{e}")

    def redo(self):
        try:
            self.text_area.edit_redo()
        except Exception as e:
            messagebox.showerror("Error", f"Nothing to redo:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeEditor(root)
    root.mainloop()
