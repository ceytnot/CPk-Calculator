import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np

import math

def normal_pdf(x, mean, std):
    """Probability Density Function (PDF) of Normal Distribution"""
    if std <= 0:
        return np.zeros_like(x)
    return (1.0 / (std * math.sqrt(2.0 * math.pi))) * np.exp(-((x - mean) ** 2) / (2.0 * std ** 2))

def show_drawings_cpk(results, values):
    """Counts parameters based on values and shows drawing in Matplotlib"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

    # Histogram
    n, bins, patches = ax1.hist(values, bins=10, edgecolor='black', alpha=0.6, 
                               color='skyblue', label='Данные')
    
    # Get parameters
    mean = results['mean']
    std = results['std_dev']
    usl = results['usl']
    lsl = results['lsl']
    
    # Target value
    if usl is None or lsl is None:
        target = "НЕТ"
    else:
        target = results.get('target', (usl + lsl) / 2)
    
    # Curve of Probability Density Function (PDF)
    x_min_values = [mean - 3.5 * std, min(values) - 1]
    x_max_values = [mean + 3.5 * std, max(values) + 1]

    x_min = min(x_min_values)
    x_max = max(x_max_values)

    max_width = 10 * std  # или любое другое значение
    center = (x_min + x_max) / 2
    x_min = max(x_min, center - max_width/2)
    x_max = min(x_max, center + max_width/2)


    x = np.linspace(x_min, x_max, 500)
    
    # SCALE the normal distribution curve to fit the histogram
    bin_width = bins[1] - bins[0]
    y_scaled = normal_pdf(x, mean, std) * len(values) * bin_width
    ax1.plot(x, y_scaled, 'r-', linewidth=2.5, label='Нормальное распределение')

    # get max_y
    max_y = max(y_scaled)

    # Central line of PDF
    ax1.axvline(mean, color='red', linestyle='-', linewidth=2, 
               label=f"Центр НР (μ): {mean:.3f}", alpha=0.7)
    
    # Target central line
    try:
        target_float = float(target)
        ax1.axvline(target_float, color='purple', linestyle='-.', linewidth=3, 
                label=f"Целевое значение (Target): {target_float:.3f}", alpha=0.8)
    except (TypeError, ValueError):
        pass
    
    # USL and LSL
    if usl is not None:
        ax1.axvline(usl, color='green', linestyle='--', linewidth=1.5, 
                label=f"USL: {usl}", alpha=0.7)
    if lsl is not None:
        ax1.axvline(lsl, color='green', linestyle='--', linewidth=1.5, 
                label=f"LSL: {lsl}", alpha=0.7)

    # Levels for Sigma
    #colors = ['orange', 'gold', 'lightcoral']
    colors = ["#bfffb2", "#c3ff8a", "#f1ff72"]
  

    alphas = [0.3, 0.2, 0.1]
    
    for i in range(1, 4):
        # vertical lines for sigma
        ax1.axvline(mean + i*std, color='gray', linestyle=':', linewidth=1, alpha=0.5)
        ax1.axvline(mean - i*std, color='gray', linestyle=':', linewidth=1, alpha=0.5)
        
        # Fill areas for sigma
        if i == 1:
            ax1.axvspan(mean - std, mean + std, alpha=alphas[0], color=colors[0], 
                       label=f'±1σ (68.3%)')
            
            # Label 1σ inside area
            ax1.text(mean, max_y * 0.5, '1σ', fontsize=10, 
                   ha='center', va='center', color='black', fontweight='bold',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
            
        elif i == 2:
            ax1.axvspan(mean - 2*std, mean - std, alpha=alphas[1], color=colors[1])
            ax1.axvspan(mean + std, mean + 2*std, alpha=alphas[1], color=colors[1])
            ax1.fill_between([], [], [], color=colors[1], alpha=alphas[1], 
                           label=f'±2σ (95.5%)')
            
            # Label 2σ inside area
            ax1.text(mean - 1.5*std, max_y * 0.3, '2σ', fontsize=9, 
                   ha='center', va='center', color='black', fontweight='bold',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
            ax1.text(mean + 1.5*std, max_y * 0.3, '2σ', fontsize=9, 
                   ha='center', va='center', color='black', fontweight='bold',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
            
        elif i == 3:
            ax1.axvspan(mean - 3*std, mean - 2*std, alpha=alphas[2], color=colors[2])
            ax1.axvspan(mean + 2*std, mean + 3*std, alpha=alphas[2], color=colors[2])
            ax1.fill_between([], [], [], color=colors[2], alpha=alphas[2], 
                           label=f'±3σ (99.7%)')
            
            # Label 3σ inside area
            ax1.text(mean - 2.5*std, max_y * 0.15, '3σ', fontsize=8, 
                   ha='center', va='center', color='black', fontweight='bold',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
            ax1.text(mean + 2.5*std, max_y * 0.15, '3σ', fontsize=8, 
                   ha='center', va='center', color='black', fontweight='bold',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))

    # Vertical line - Center of PDF
    ax1.plot([mean, mean], [0, max_y], color='blue', linestyle=':', linewidth=1, alpha=0.5)

    # Defect areas
    defect_values = []
    if lsl is not None and usl is not None:
        defect_values = [v for v in values if v < lsl or v > usl]
    elif lsl is not None:
        defect_values = [v for v in values if v < lsl]
    elif usl is not None:
        defect_values = [v for v in values if v > usl]

    if defect_values:
        ax1.scatter(defect_values, [0] * len(defect_values), 
                  color='red', s=50, zorder=5, marker='v', 
                  label=f'Брак ({len(defect_values)} шт.)')

    # Labels and titles
    ax1.set_xlabel('Значения', fontsize=12)
    ax1.set_ylabel('Частота', fontsize=12)
    ax1.set_title('Нормальное распределение', 
                 fontsize=14, fontweight='bold')
    ax1.legend(loc='upper right', fontsize=9)
    ax1.grid(True, alpha=0.3)

    # SECOND GRAPH
    # count indices for horizontal axis
    x_indices = list(range(1, len(values) + 1))
    
    # linear graph
    ax2.plot(x_indices, values, 'b-', linewidth=2, marker='o', 
             markersize=4, label='Измерения')
    
    # Horizontal line of limits
    if usl is not None:
        ax2.axhline(y=usl, color='green', linestyle='--', linewidth=1.5, 
                    label=f'USL: {usl}', alpha=0.7)
    if lsl is not None:
        ax2.axhline(y=lsl, color='green', linestyle='--', linewidth=1.5, 
                    label=f'LSL: {lsl}', alpha=0.7)
    
    # Horizontal line of Mean
    ax2.axhline(y=mean, color='red', linestyle='-', linewidth=2, 
                label=f'Среднее: {mean:.3f}', alpha=0.7)
    
    # horizontal line of Target value
    try:
        target_float = float(target)
        ax2.axhline(y=target, color='purple', linestyle='-.', linewidth=2, 
                    label=f'Целевое значение: {target:.3f}', alpha=0.8)
    except (TypeError, ValueError):
        pass        
    
    # Sigma levels (areas) colors = ["#bfffb2", "#d7ffb2", "#deffb2"]
    ax2.fill_between(x_indices, mean - std, mean + std, alpha=0.2, color=colors[0], 
                     label=f'±1σ ({mean-std:.3f} - {mean+std:.3f})')
    ax2.fill_between(x_indices, mean - 2*std, mean + 2*std, alpha=0.1, color=colors[1], 
                     label=f'±2σ ({mean-2*std:.3f} - {mean+2*std:.3f})')
    ax2.fill_between(x_indices, mean - 3*std, mean + 3*std, alpha=0.05, color=colors[2], 
                     label=f'±3σ ({mean-3*std:.3f} - {mean+3*std:.3})')
    
    # Higlights for defects
    defect_indices = []
    defect_values_list = []

    for i, val in enumerate(values):
        is_defect = False
        if lsl is not None and val < lsl:
            is_defect = True
        if usl is not None and val > usl:
            is_defect = True
        
        if is_defect:
            defect_indices.append(x_indices[i])
            defect_values_list.append(val)

    if defect_indices:
        ax2.scatter(defect_indices, defect_values_list, color='red', s=80, 
                zorder=5, marker='v', label=f'Брак ({len(defect_indices)} шт.)')
    
    # Properties of second graph
    ax2.set_xlabel('Номер измерения', fontsize=12)
    ax2.set_ylabel('Значение', fontsize=12)
    ax2.set_title('Линейный график измерений', fontsize=14, fontweight='bold')
    ax2.legend(loc='upper right', fontsize=9)
    ax2.grid(True, alpha=0.3)
    
    y_min = min(values)*1.1
    y_max = max(values)*1.1

    y_min = y_min*1.1 if y_min < 0 else y_min - y_min*0.1
    y_max = y_max*1.1 if y_min > 0 else y_max +  y_max*0.1

    # add limits if available
    if lsl is not None and lsl < y_min:        
        y_min = lsl*1.1 if lsl < 0 else lsl - lsl*0.1

    if usl is not None and usl > y_max:
        y_max = usl*1.1 if usl > 0 else usl +  usl*0.1

    ax2.set_ylim(y_min, y_max)

    # COMMON TEXT AND LABELS
    cp_text = f'Cp = {results["cp"]:.3f}\n' if results["cp"] != "Односторонний допуск" else f'Cp = {results["cp"]}\n'
    labels_PDF = (f'{cp_text}'
               f'Cpk = {results["cpk"]:.3f}\n'
               #f'μ = {mean:.2f}\n'
               f'σ = {std:.3f}\n'
               #f'Target = {target:.2f}\n'
               f'Значений = {results["n"]}')

    
    # text block with statistic
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.9)
    ax1.text(0.02, 0.98, labels_PDF, transform=ax1.transAxes, fontsize=9,
            verticalalignment='top', bbox=props)

    plt.tight_layout()
    plt.show(block=False)


    
def drawing_heatmap(data_values: dict, sigma_threshold: float = 2.0):
    """Heatmap and Scatter Matrix (support from 2 to 3 columns)"""
    keys = list(data_values.keys())
    n_elements = len(keys)
    n_samples = len(data_values[keys[0]])
    
    # check numbers of graphs
    if n_elements == 2:
        n_scatter = 1 
        n_outliers = 1  
        scatter_pairs = [(0, keys[0], keys[1])]
    else:  # n_elements >= 3
        n_scatter = 3
        n_outliers = 3
        scatter_pairs = [(0, keys[0], keys[1]), (1, keys[0], keys[2]), (2, keys[1], keys[2])]
    

    if n_scatter == 1:
        # grid 1x2
        fig1 = plt.figure(figsize=(10, 5))
        gs = GridSpec(1, 2, figure=fig1, hspace=0.3, wspace=0.3)
    else:
        # grid 3x2 сетка
        fig1 = plt.figure(figsize=(14, 12))
        gs = GridSpec(3, 2, figure=fig1, hspace=0.3, wspace=0.3)
    
    # ==================== SCATTER MATRIX ====================
    for idx, (row, name_x, name_y) in enumerate(scatter_pairs):
        if n_scatter == 1:
            ax = fig1.add_subplot(gs[0, 0])  # one graph only
        else:
            ax = fig1.add_subplot(gs[row, 0])
        
        x = data_values[name_x]
        y = data_values[name_y]
        
        ax.scatter(x, y, alpha=0.7, s=50, c='steelblue', edgecolors='black', linewidth=0.8)
        
        # Regression line
        if len(np.unique(x)) > 1 and len(np.unique(y)) > 1:
            z = np.polyfit(x, y, 1)
            p = np.poly1d(z)
            x_line = np.linspace(min(x), max(x), 100)
            y_line = p(x_line)
            ax.plot(x_line, y_line, 'r--', linewidth=1.5, label='Регрессия')
            r = np.corrcoef(x, y)[0, 1]
            equation = f'{name_y} = {z[0]:.2f}·{name_x} + {z[1]:.4f}'
        else:
            r = np.nan
            equation = 'Недостаточно данных'
        
        ax.text(0.05, 0.95, f'r = {r:.3f}\n{equation}', transform=ax.transAxes,
                verticalalignment='top', fontsize=9,
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        ax.set_xlabel(f'{name_x}, %', fontsize=10)
        ax.set_ylabel(f'{name_y}, %', fontsize=10)
        ax.grid(True, alpha=0.3, linestyle=':')
        if 'Регрессия' in equation:
            ax.legend(loc='lower right', fontsize=8)
    
    sample_nums = np.arange(1, n_samples + 1)
    
    # ==================== ANOMALY GRAPHS ====================
    if n_elements == 2:
        # One graph (2 columns in input data)
        ax_out = fig1.add_subplot(gs[0, 1])
        
        x = np.array(data_values[keys[1]])
        y = np.array(data_values[keys[0]])
        
        if len(np.unique(x)) > 1:
            z = np.polyfit(x, y, 1)
            y_pred = z[0] * x + z[1]
            residuals = y - y_pred
            std_res = np.std(residuals)
        else:
            residuals = np.zeros_like(y)
            std_res = 0
        
        colors = ['red' if abs(r) > sigma_threshold * std_res else 'steelblue' 
                  for r in residuals] if std_res > 0 else ['steelblue'] * n_samples
        
        ax_out.scatter(sample_nums, residuals, c=colors, alpha=0.7, s=50, edgecolors='black')
        ax_out.axhline(0, color='black', linestyle='-', linewidth=0.8)
        if std_res > 0:
            ax_out.axhline(sigma_threshold * std_res, color='red', linestyle='--', 
                          linewidth=1, label=f'+{sigma_threshold}σ')
            ax_out.axhline(-sigma_threshold * std_res, color='red', linestyle='--', 
                          linewidth=1, label=f'-{sigma_threshold}σ')
        
        ax_out.set_xlabel('Номер образца')
        ax_out.set_ylabel(f'Отклонение {keys[0]} от регрессии по {keys[1]}')
        ax_out.set_title(f'Выбросы: {keys[0]}-{keys[1]}')
        ax_out.grid(True, alpha=0.3, linestyle=':')
        if std_res > 0:
            ax_out.legend(loc='upper right', fontsize=8)
        
        for i, r in enumerate(residuals):
            if std_res > 0 and abs(r) > sigma_threshold * std_res:
                ax_out.annotate(f'{sample_nums[i]}', (sample_nums[i], r),
                               textcoords="offset points", xytext=(0, 10), ha='center', fontsize=8,
                               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    else:  # 3 columns in input data

        # first
        ax_cp = fig1.add_subplot(gs[0, 1])
        x_cp = np.array(data_values[keys[1]])
        y_cp = np.array(data_values[keys[0]])
        z_cp = np.polyfit(x_cp, y_cp, 1)
        y_pred_cp = z_cp[0] * x_cp + z_cp[1]
        res_cp = y_cp - y_pred_cp
        std_cp = np.std(res_cp)
        colors_cp = ['red' if abs(r) > sigma_threshold * std_cp else 'steelblue' for r in res_cp]
        
        ax_cp.scatter(sample_nums, res_cp, c=colors_cp, alpha=0.7, s=50, edgecolors='black')
        ax_cp.axhline(0, color='black', linestyle='-', linewidth=0.8)
        ax_cp.axhline(sigma_threshold * std_cp, color='red', linestyle='--', linewidth=1, label=f'+{sigma_threshold}σ')
        ax_cp.axhline(-sigma_threshold * std_cp, color='red', linestyle='--', linewidth=1, label=f'-{sigma_threshold}σ')
        ax_cp.set_xlabel('Номер образца')
        ax_cp.set_ylabel(f'Отклонение {keys[0]} от регрессии по {keys[1]}')
        ax_cp.set_title(f'Выбросы: {keys[0]}-{keys[1]}')
        ax_cp.grid(True, alpha=0.3, linestyle=':')
        ax_cp.legend(loc='upper right', fontsize=8)
        for i, r in enumerate(res_cp):
            if abs(r) > sigma_threshold * std_cp:
                ax_cp.annotate(f'{sample_nums[i]}', (sample_nums[i], r),
                               textcoords="offset points", xytext=(0, 10), ha='center', fontsize=8,
                               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
        
        # second
        ax_cs = fig1.add_subplot(gs[1, 1])
        x_cs = np.array(data_values[keys[2]])
        y_cs = np.array(data_values[keys[0]])
        z_cs = np.polyfit(x_cs, y_cs, 1)
        y_pred_cs = z_cs[0] * x_cs + z_cs[1]
        res_cs = y_cs - y_pred_cs
        std_cs = np.std(res_cs)
        colors_cs = ['red' if abs(r) > sigma_threshold * std_cs else 'steelblue' for r in res_cs]
        
        ax_cs.scatter(sample_nums, res_cs, c=colors_cs, alpha=0.7, s=50, edgecolors='black')
        ax_cs.axhline(0, color='black', linestyle='-', linewidth=0.8)
        ax_cs.axhline(sigma_threshold * std_cs, color='red', linestyle='--', linewidth=1, label=f'+{sigma_threshold}σ')
        ax_cs.axhline(-sigma_threshold * std_cs, color='red', linestyle='--', linewidth=1, label=f'-{sigma_threshold}σ')
        ax_cs.set_xlabel('Номер образца')
        ax_cs.set_ylabel(f'Отклонение {keys[0]} от регрессии по {keys[2]}')
        ax_cs.set_title(f'Выбросы: {keys[0]}-{keys[2]}')
        ax_cs.grid(True, alpha=0.3, linestyle=':')
        ax_cs.legend(loc='upper right', fontsize=8)
        for i, r in enumerate(res_cs):
            if abs(r) > sigma_threshold * std_cs:
                ax_cs.annotate(f'{sample_nums[i]}', (sample_nums[i], r),
                               textcoords="offset points", xytext=(0, 10), ha='center', fontsize=8,
                               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
        
        # third
        ax_ps = fig1.add_subplot(gs[2, 1])
        x_ps = np.array(data_values[keys[2]])
        y_ps = np.array(data_values[keys[1]])
        z_ps = np.polyfit(x_ps, y_ps, 1)
        y_pred_ps = z_ps[0] * x_ps + z_ps[1]
        res_ps = y_ps - y_pred_ps
        std_ps = np.std(res_ps)
        colors_ps = ['red' if abs(r) > sigma_threshold * std_ps else 'steelblue' for r in res_ps]
        
        ax_ps.scatter(sample_nums, res_ps, c=colors_ps, alpha=0.7, s=50, edgecolors='black')
        ax_ps.axhline(0, color='black', linestyle='-', linewidth=0.8)
        ax_ps.axhline(sigma_threshold * std_ps, color='red', linestyle='--', linewidth=1, label=f'+{sigma_threshold}σ')
        ax_ps.axhline(-sigma_threshold * std_ps, color='red', linestyle='--', linewidth=1, label=f'-{sigma_threshold}σ')
        ax_ps.set_xlabel('Номер образца')
        ax_ps.set_ylabel(f'Отклонение {keys[1]} от регрессии по {keys[2]}')
        ax_ps.set_title(f'Выбросы: {keys[1]}-{keys[2]}')
        ax_ps.grid(True, alpha=0.3, linestyle=':')
        ax_ps.legend(loc='upper right', fontsize=8)
        for i, r in enumerate(res_ps):
            if abs(r) > sigma_threshold * std_ps:
                ax_ps.annotate(f'{sample_nums[i]}', (sample_nums[i], r),
                               textcoords="offset points", xytext=(0, 10), ha='center', fontsize=8,
                               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    # Titles
    if n_elements == 2:
        fig1.suptitle(f'Диаграммы рассеивания и выбросы: {keys[0]} vs {keys[1]} (порог {sigma_threshold}σ)',
                      fontsize=12, fontweight='bold', y=0.98)
    else:
        fig1.suptitle(f'Матрица диаграмм рассеивания (порог {sigma_threshold}σ)',
                      fontsize=14, fontweight='bold', y=0.98)
    
    fig1.tight_layout()
    
    # ==================== Heatmap ====================
    fig2, ax_corr = plt.subplots(figsize=(8, 7))
    
    corr_matrix = np.zeros((n_elements, n_elements))
    for i in range(n_elements):
        for j in range(n_elements):
            corr_matrix[i, j] = np.corrcoef(data_values[keys[i]], data_values[keys[j]])[0, 1]
    
    im = ax_corr.imshow(corr_matrix, cmap='RdBu_r', vmin=-1, vmax=1, aspect='equal')
    
    ax_corr.set_xticks(np.arange(n_elements))
    ax_corr.set_yticks(np.arange(n_elements))
    ax_corr.set_xticklabels(keys, fontsize=12)
    ax_corr.set_yticklabels(keys, fontsize=12)
    
    for i in range(n_elements):
        for j in range(n_elements):
            color = 'white' if abs(corr_matrix[i, j]) > 0.6 else 'black'
            ax_corr.text(j, i, f'{corr_matrix[i, j]:.2f}', ha='center', va='center',
                         fontsize=14, fontweight='bold', color=color)
    
    plt.colorbar(im, ax=ax_corr, label='Коэффициент корреляции (r)')
    ax_corr.set_title(f'Тепловая карта', fontsize=12, fontweight='bold')
    fig2.tight_layout()
    
    plt.show(block=False)
    plt.show()
