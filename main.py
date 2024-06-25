import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import re
import translate
import threading

def translate_lua_code(lua_code, source_language, target_language):
    translator = translate.Translator(to_lang=target_language)
    pattern = r"'(.*?)'"  # match single-quoted strings
    matches = re.findall(pattern, lua_code)
    for match in matches:
        translation = translator.translate(match)
        lua_code = lua_code.replace(f"'{match}'", f"'{translation}'")
    return lua_code

def translate_and_save():
    file_path = filedialog.askopenfilename(title="Lua Datei auswählen", filetypes=[("Lua files", "*.lua")])
    if file_path:
        progress_bar.config(mode="indeterminate")
        progress_bar.start()
        progress_label.config(text="Übersetzung startet...")
        messagebox.showinfo("Übersetzung startet", "Die Übersetzung wird gestartet. Bitte warten Sie...")
        
        def translate_thread():
            with open(file_path, "r", encoding="utf-8") as file:
                lua_code = file.read()
            source_language = source_language_var.get()
            target_language = target_language_var.get()
            translated_code = translate_lua_code(lua_code, source_language, target_language)
            translated_file_path = file_path + ".übersetzt"
            with open(translated_file_path, "w", encoding="utf-8") as file:
                file.write(translated_code)
            progress_bar.stop()
            progress_bar.config(mode="determinate")
            progress_bar.config(value=100)
            progress_label.config(text="Übersetzung abgeschlossen!")
            messagebox.showinfo("Übersetzung abgeschlossen", f"Übersetzte Datei gespeichert als {translated_file_path}")
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.INSERT, translated_code)
        
        threading.Thread(target=translate_thread).start()

def open_file():
    file_path = filedialog.askopenfilename(title="Lua Datei auswählen", filetypes=[("Lua files", "*.lua")])
    if file_path:
        text_area.delete(1.0, tk.END)
        with open(file_path, "r", encoding="utf-8") as file:
            lua_code = file.read()
        text_area.insert(tk.INSERT, lua_code)

def save_file():
    file_path = filedialog.asksaveasfilename(title="Lua Datei speichern", filetypes=[("Lua files", "*.lua")])
    if file_path:
        lua_code = text_area.get(1.0, tk.END)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(lua_code)
        messagebox.showinfo("Datei gespeichert", f"Datei gespeichert als {file_path}")

def about():
    messagebox.showinfo("Über", "Ersteller: Tobi\nErstellt am: 25.06.2024\nVersion: 1.0")

root = tk.Tk()
root.title("Lua Code Translator")
root.configure(background='#333333')  # dark gray background

menu = tk.Menu(root, background='#333333', foreground='#f7f7f7')
root.config(menu=menu)

file_menu = tk.Menu(menu, background='#333333', foreground='#f7f7f7')
menu.add_cascade(label="Datei", menu=file_menu, background='#333333', foreground='#f7f7f7')
file_menu.add_command(label="Öffnen", command=open_file, background='#333333', foreground='#f7f7f7')
file_menu.add_command(label="Speichern", command=save_file, background='#333333', foreground='#f7f7f7')
file_menu.add_command(label="Übersetzen und Speichern", command=translate_and_save, background='#333333', foreground='#f7f7f7')
file_menu.add_separator(background='#333333')
file_menu.add_command(label="Info", command=about, background='#333333', foreground='#f7f7f7')

font = ("Open Sans", 12)

source_language_var = tk.StringVar()
source_language_var.set("en")  # default source language
source_language_label = tk.Label(root, text="Quellsprache:", font=font, background='#333333', foreground='#f7f7f7')
source_language_label.pack(pady=10)
source_language_option = ttk.OptionMenu(root, source_language_var, "en", "en", "es", "ru", "fr", "de")
source_language_option.pack(pady=10)

target_language_var = tk.StringVar()
target_language_var.set("de")  # default target language
target_language_label = tk.Label(root, text="Zielsprache:", font=font,background='#333333', foreground='#f7f7f7')
target_language_label.pack(pady=10)
target_language_option = ttk.OptionMenu(root, target_language_var, "de", "en", "es", "ru", "fr", "de")
target_language_option.pack(pady=10)

translate_button = ttk.Button(root, text="Übersetzen und Speichern", command=translate_and_save)
translate_button.pack(pady=20)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
progress_bar.pack(pady=10)

progress_label = tk.Label(root, text="", font=font, background='#333333', foreground='#f7f7f7')
progress_label.pack(pady=10)

text_area = tk.Text(root, width=80, height=20, font=font, background='#333333', foreground='#f7f7f7')
text_area.pack(pady=20)

root.mainloop()