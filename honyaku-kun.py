import tkinter as tk
import tkinter.ttk as ttk
from deepl_api import translate


def en_trans():
    text = source_text_entry.get(1.0, "end")
    if text == "\n":
        pass
    else:
        target_text_entry.delete(1.0, tk.END)
        target_text_entry.insert(1.0, translate(text, "EN"))


def ja_trans():
    text = source_text_entry.get(1.0, "end")
    if text == "\n":
        pass
    else:
        target_text_entry.delete(1.0, tk.END)
        target_text_entry.insert(1.0, translate(text, "JA"))


def switch():
    text = target_text_entry.get(1.0, "end")
    source_text_entry.delete(1.0, tk.END)
    source_text_entry.insert(1.0, text)


def delete():
    source_text_entry.delete(1.0, tk.END)
    target_text_entry.delete(1.0, tk.END)


# rootメインウィンドウの設定
root = tk.Tk()
root.title("翻訳くん (Ver.1.03)")
root.geometry("750x550")

# Frameを設定
frame1 = ttk.Frame(root)
frame2 = ttk.Frame(root)
frame3 = ttk.Frame(root)

# テキストボックスwidgetを設定
source_text_entry = tk.Text(
    frame1, height=10, width=80, relief="ridge", bd=3,)

target_text_entry = tk.Text(
    frame3, height=10, width=80, relief="ridge", bd=3,)

# ボタンwidgetを設定

button_1 = tk.Button(frame2, text="JA to EN")
button_2 = tk.Button(frame2, text="EN to JA")
button_3 = tk.Button(frame2, text="switch")
button_4 = tk.Button(frame2, text="delete")

# widgetの配置を設定
frame1.pack(pady=5)
frame2.pack(pady=5)
frame3.pack(pady=5)
source_text_entry.pack()
target_text_entry.pack()
button_1.grid(row=0, column=0, padx=5)
button_2.grid(row=0, column=1, padx=5)
button_3.grid(row=0, column=2, padx=5)
button_4.grid(row=0, column=3, padx=5)

# テキストボックスのフォントを設定
source_text_entry.configure(font=("Meiryo", 11))
target_text_entry.configure(font=("Meiryo", 11))

button_1["command"] = en_trans
button_2["command"] = ja_trans
button_3["command"] = switch
button_4["command"] = delete

root.mainloop()
