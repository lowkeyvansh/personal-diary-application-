import tkinter as tk
from tkinter import messagebox, filedialog
import os
import time

def setup_window():
    root = tk.Tk()
    root.title("Personal Diary")
    root.geometry("600x400")
    return root

def create_text_area(root):
    text_area = tk.Text(root, wrap="word")
    text_area.pack(fill="both", expand=True)
    return text_area

def create_buttons(root, text_area):
    button_frame = tk.Frame(root)
    button_frame.pack(fill="x")
    
    new_button = tk.Button(button_frame, text="New Entry", command=lambda: new_entry(text_area))
    new_button.pack(side="left", padx=10, pady=10)
    
    save_button = tk.Button(button_frame, text="Save Entry", command=lambda: save_entry(text_area))
    save_button.pack(side="left", padx=10, pady=10)
    
    view_button = tk.Button(button_frame, text="View Past Entries", command=view_entries)
    view_button.pack(side="left", padx=10, pady=10)

def new_entry(text_area):
    text_area.delete(1.0, tk.END)

def save_entry(text_area):
    entry_content = text_area.get(1.0, tk.END).strip()
    if entry_content:
        with open(f"diary_{int(time.time())}.txt", "w") as file:
            file.write(entry_content)
        messagebox.showinfo("Success", "Diary entry saved successfully!")
    else:
        messagebox.showwarning("Warning", "Diary entry is empty. Please write something before saving.")

def view_entries():
    entries = [f for f in os.listdir() if f.startswith("diary_") and f.endswith(".txt")]
    if not entries:
        messagebox.showinfo("No Entries", "No past entries found.")
        return
    
    view_window = tk.Toplevel()
    view_window.title("Past Entries")
    view_window.geometry("400x300")
    
    listbox = tk.Listbox(view_window)
    listbox.pack(fill="both", expand=True)
    
    for entry in entries:
        listbox.insert(tk.END, entry)
    
    listbox.bind("<<ListboxSelect>>", lambda event: display_entry(event, view_window))

def display_entry(event, view_window):
    listbox = event.widget
    selection = listbox.curselection()
    if selection:
        entry_name = listbox.get(selection[0])
        with open(entry_name, "r") as file:
            content = file.read()
        
        entry_window = tk.Toplevel(view_window)
        entry_window.title(entry_name)
        entry_window.geometry("400x300")
        
        text_area = tk.Text(entry_window, wrap="word")
        text_area.pack(fill="both", expand=True)
        text_area.insert(tk.END, content)
        text_area.config(state=tk.DISABLED)

def main():
    root = setup_window()
    text_area = create_text_area(root)
    create_buttons(root, text_area)
    root.mainloop()

if __name__ == "__main__":
    main()
