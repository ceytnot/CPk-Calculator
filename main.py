# C:\Users\NewHorizon\Documents\PythonProjects\cpk_calculator\venv\Scripts\Activate.ps1
import tkinter as tk
from tkinter import ttk

from support_funct import upload_template_cpk, upload_template_heatmap, download_template

# ############## APP STARTS HERE #############################################################

root = tk.Tk()
root.title("CPk Calculator")
root.geometry("400x250")

# Styles
style_btn = ttk.Style()
style_btn.configure("main_btns.TButton", font=("Arial", 11), padding=10)


# Short Instruction
label_instruction = ttk.Label(root, text=
                  "1.Выгрузите шаблон в .xlsx\n" \
                  "2.Откройте его с помощью Excel\n" \
                  "3.Введите в шаблон имеющиеся данные\n" \
                  "4.Загрузите шаблон в программу для расчета\n   и постороения графиков с помощью одной из кнопок")
label_instruction.pack(pady=10, padx=10)

# Frame for btns
button_frame = ttk.Frame(root)
button_frame.pack(pady=20)
status_label = ttk.Label(root, text="", font=("Arial", 10))
status_label.pack(pady=10)

# Buttons
submit_btn = ttk.Button(button_frame, text="Выгрузить\n Шаблон", style="main_btns.TButton", command=lambda: download_template(root, status_label))
submit_btn.pack(side='left', padx=5)

cpk_btn = ttk.Button(button_frame, text="Рассчитать\n CP/CPk", style="main_btns.TButton", command=lambda: upload_template_cpk(root))    #lambda is required for argument in funct
cpk_btn.pack(side='left', padx=5)

heatmap_btn = ttk.Button(button_frame, text="Тепловая\n Карта", style="main_btns.TButton", command=lambda: upload_template_heatmap(root))
heatmap_btn.pack(side='left', padx=5)

root.mainloop()