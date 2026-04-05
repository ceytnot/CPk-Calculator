import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import numpy as np

import math

def calculate_cpk(data_values: dict) -> tuple[dict, list[float]]:
    """Returns results (cp, cpk, mean and so on...) and measurements"""
    
    usl = data_values['usl']
    lsl = data_values['lsl']
    measurements = data_values.get('values', [])
    
    if not measurements:
        messagebox.showerror("Ошибка", "Нет данных измерений")
    
    if usl is None and lsl is None:
        messagebox.showerror("Ошибка", "Не указаны USL и LSL - должен быть хотя бы один предел")
    
    # Mean (среднее)
    n = len(measurements)
    mean = sum(measurements) / n
    
    # Standard deviation
    variance = sum((x - mean) ** 2 for x in measurements) / (n - 1)
    std_dev = math.sqrt(variance)
    
    # Indexes

    if usl is None:
        cp = 'Односторонний допуск'
        cpl = (mean - lsl) / (3 * std_dev) if std_dev > 0 else float('inf')
        cpk = cpl

    elif lsl is None:
        cp = 'Односторонний допуск'
        cpu = (usl - mean) / (3 * std_dev) if std_dev > 0 else float('inf')
        cpk = cpu

    else:
        cp = (usl - lsl) / (6 * std_dev) if std_dev > 0 else float('inf')
        cpu = (usl - mean) / (3 * std_dev) if std_dev > 0 else float('inf')
        cpl = (mean - lsl) / (3 * std_dev) if std_dev > 0 else float('inf')
        cpk = min(cpu, cpl)

    # Target (Целевое значение)
    if usl is None or lsl is None:
        target = "НЕТ"
    else:
        target = (usl + lsl) / 2 
    
    # Результаты
    results = {
        'n': n,
        'mean': mean,
        'std_dev': std_dev,
        'usl': usl,
        'lsl': lsl,
        'cp': cp,
        'cpk': cpk,
        'target': target
    }
    
    return results, measurements