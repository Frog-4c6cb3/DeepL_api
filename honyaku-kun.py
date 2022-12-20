import tkinter as tk
from tkinter.constants import RIGHT, X
import tkinter.ttk as ttk
from deepl_api import translate, usage_request
import pyperclip


def indicate_limit():
    usage_result = usage_request()
    character_limit = usage_result["character_limit"]
    character_count = character_limit - usage_result["character_count"]
    limit_rate = character_count / character_limit * 100
    limit_text = f"翻訳可能な残文字数: {round(limit_rate,1)}% "\
        f"({character_count} / {character_limit})"
    label1["text"] = limit_text


def en_trans():
    text = source_text_entry.get(1.0, "end")
    if text == "\n":
        pass
    else:
        target_text_entry.delete(1.0, tk.END)
        if check_v.get():
            translate_result = translate(text, "EN", 1)
        else:
            translate_result = translate(text, "EN", 0)
        indicate_limit()
        target_text_entry.insert(1.0, translate_result)


def ja_trans():
    text = source_text_entry.get(1.0, "end")
    if text == "\n":
        pass
    else:
        target_text_entry.delete(1.0, tk.END)
        if check_v.get():
            translate_result = translate(text, "JA", 1)
        else:
            translate_result = translate(text, "JA", 0)
        indicate_limit()
        target_text_entry.insert(1.0, translate_result)


def switch():
    text = target_text_entry.get(1.0, "end")
    source_text_entry.delete(1.0, tk.END)
    source_text_entry.insert(1.0, text)


def delete():
    source_text_entry.delete(1.0, tk.END)
    target_text_entry.delete(1.0, tk.END)


def leftClick_1(event):
    source_text_entry.delete(1.0, tk.END)
    source_text_entry.insert(1.0, clip())


def leftClick_2(event):
    text = target_text_entry.get(1.0, "end")
    pyperclip.copy(text)


def clip():
    add_clip = pyperclip.paste()
    return add_clip


# rootメインウィンドウの設定
root = tk.Tk()
root.title("DeepL翻訳 (Ver.4.1.0)")
root.geometry("750x560")
root.iconbitmap(default="icon.ico")

# Frameを設定
frame1 = ttk.Frame(root)
frame2 = ttk.Frame(root)
frame3 = ttk.Frame(root)
frame4 = ttk.Frame(root)

# テキストボックスwidgetを設定
source_text_entry = tk.Text(
    frame1, height=10, width=80, relief="ridge", bd=3,)

source_text_entry.bind('<Button-3>', leftClick_1)

target_text_entry = tk.Text(
    frame3, height=10, width=80, relief="ridge", bd=3,)

target_text_entry.bind('<Button-3>', leftClick_2)

# ボタンwidgetを設定

button_1 = tk.Button(frame2, text="JA to EN")
button_2 = tk.Button(frame2, text="EN to JA")
button_3 = tk.Button(frame2, text="switch")
button_4 = tk.Button(frame2, text="delete")

# チェックボックス
check_v = tk.BooleanVar()
chk = tk.Checkbutton(
    frame2, text="改行を無視する", variable=check_v, onvalue=True, offvalue=False)

# widgetの配置を設定
frame1.pack(pady=5)
frame2.pack(pady=5)
frame3.pack(pady=5)
frame4.pack(padx=20, pady=1, fill=X)
source_text_entry.pack()
target_text_entry.pack()
button_1.grid(row=0, column=0, padx=5)
button_2.grid(row=0, column=1, padx=5)
button_3.grid(row=0, column=2, padx=5)
button_4.grid(row=0, column=3, padx=5)
chk.grid(row=0, column=4, padx=5)


# テキストボックスのフォントを設定
source_text_entry.configure(font=("Meiryo", 11))
target_text_entry.configure(font=("Meiryo", 11))

button_1["command"] = en_trans
button_2["command"] = ja_trans
button_3["command"] = switch
button_4["command"] = delete

# ラベル
label1 = tk.Label(frame4, text=" ", font=("Meiryo", 8))
label1.pack(side=RIGHT)
indicate_limit()

root.mainloop()
