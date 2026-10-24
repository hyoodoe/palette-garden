import json
import customtkinter as ctk
from tkinter import colorchooser, filedialog, messagebox


app = ctk.CTk()
app.title("Palette Garden")
app.geometry("760x560")

colors = []


# interface

title = ctk.CTkLabel(
    app,
    text="Palette Garden",
    font=ctk.CTkFont(size=30, weight="bold")
)
title.pack(pady=(20, 10))

toolbar = ctk.CTkFrame(app)
toolbar.pack(fill="x", padx=20, pady=10)

name_entry = ctk.CTkEntry(
    toolbar,
    placeholder_text="Palette Name"
)
name_entry.pack(side="left", padx=10, pady=10, expand=True, fill="x")

palette_frame = ctk.CTkScrollableFrame(
    app,
    label_text="Palette Colors"
)
palette_frame.pack(fill="both", expand=True, padx=20, pady=10)


# app features

def refresh_palette():
    for widget in palette_frame.winfo_children():
        widget.destroy()

    for color in colors:
        row = ctk.CTkFrame(palette_frame)
        row.pack(fill="x", padx=5, pady=5)

        swatch = ctk.CTkFrame(
            row,
            width=45,
            height=35,
            fg_color=color
        )
        swatch.pack(side="left", padx=10, pady=8)
        swatch.pack_propagate(False)

        color_label = ctk.CTkLabel(row, text=color)
        color_label.pack(side="left", padx=10, expand=True, anchor="w")

        copy_button = ctk.CTkButton(
            row,
            text="Copiar",
            width=80,
            command=lambda value=color: copy_color(value)
        )
        copy_button.pack(side="right", padx=5)

        remove_button = ctk.CTkButton(
            row,
            text="Quitar",
            width=80,
            fg_color="#8f3f45",
            hover_color="#713238",
            command=lambda value=color: remove_color(value)
        )
        remove_button.pack(side="right", padx=5)


def choose_color():
    result = colorchooser.askcolor(
        title="Choose a Color",
        parent=app
    )
    color = result[1]

    if color is None:
        return

    if color in colors:
        messagebox.showinfo("Repeated Color", "This color is already in the Palette")
        return

    colors.append(color)
    refresh_palette()


def remove_color(color):
    colors.remove(color)
    refresh_palette()


def copy_color(color):
    app.clipboard_clear()
    app.clipboard_append(color)
    app.update()


def save_palette():
    filepath = filedialog.asksaveasfilename(
        title="Save Palette",
        defaultextension=".json",
        filetypes=[("JSON", "*.json")],
        parent=app
    )

    if not filepath:
        return

    palette_data = {
        "name": name_entry.get().strip() or "Unnamed Palette",
        "colors": colors
    }

    try:
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(palette_data, file, indent=2, ensure_ascii=False)
        messagebox.showinfo("Saved", "Palette has been saved")
    except OSError as error:
        messagebox.showerror("An error occured while saving", str(error))


def load_palette():
    filepath = filedialog.askopenfilename(
        title="Open Palette",
        filetypes=[("JSON", "*.json")],
        parent=app
    )

    if not filepath:
        return

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            palette_data = json.load(file)

        loaded_colors = palette_data["colors"]
        if not isinstance(loaded_colors, list):
            raise ValueError("'Colors' field must be a list.")

        colors.clear()
        colors.extend(loaded_colors)

        name_entry.delete(0, "end")
        name_entry.insert(0, palette_data.get("name", "Unnamed Palette"))

        refresh_palette()

    except (OSError, json.JSONDecodeError, KeyError, ValueError, TypeError) as error:
        messagebox.showerror("Unable to open Palette", str(error))


# buttons

add_button = ctk.CTkButton(
    toolbar,
    text="Choose and add a Color",
    command=choose_color
)
add_button.pack(side="left", padx=10, pady=10)

save_button = ctk.CTkButton(
    toolbar,
    text="Save",
    command=save_palette
)
save_button.pack(side="left", padx=(0, 5), pady=10)

load_button = ctk.CTkButton(
    toolbar,
    text="Open",
    command=load_palette
)
load_button.pack(side="left", padx=(0, 10), pady=10)


app.mainloop()
