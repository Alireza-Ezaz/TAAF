
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import matplotlib.patheffects as path_effects

# ----------------------
# Data
# ----------------------
models = [
    'Gemini 2.5 Flash',
    'Gemini 2.5 Pro (Reasoning)',
    'Claude Haiku 4.5',
    'Claude Opus 4.1 (Reasoning)',
    'GPT-4o',
    'GPT o4-mini (Reasoning)',
    'GPT-4.1 nano (small)'
]

accuracy = np.array([89.50, 95.83, 73.67, 87.67, 79.83, 95.50, 67.33])
families = np.array(['Gemini','Gemini','Claude','Claude','GPT','GPT','GPT'])
is_reasoning = np.array([False, True, False, True, False, True, False])

# Colors: Gemini stays blue; Claude = good yellow; GPT = good purple
family_colors = {
    'Gemini': '#1f77b4',  # blue
    'Claude': '#FFC300',  # good yellow
    'GPT':    '#7B61FF',  # good purple
}

# ----------------------
# Geometry
# ----------------------
N = len(models)
angles = np.linspace(0, 2*np.pi, N, endpoint=False)

# ----------------------
# Figure / Axes
# ----------------------
fig = plt.figure(figsize=(10, 9.8))
ax = plt.subplot(111, polar=True)

# Family-colored fills only within family blocks
rmin = 60.0
for fam in ['Gemini', 'Claude', 'GPT']:
    idx = np.where(families == fam)[0]
    idx_sorted = np.sort(idx)
    fam_angles = angles[idx_sorted]
    fam_values = accuracy[idx_sorted]
    fill_angles = np.concatenate([[fam_angles[0]], fam_angles, [fam_angles[-1]]])
    fill_values = np.concatenate([[rmin],         fam_values,   [rmin]])
    ax.fill(fill_angles, fill_values, color=family_colors[fam], alpha=0.15, zorder=0)

# Spokes and markers
for ang, val, fam, reasoning in zip(angles, accuracy, families, is_reasoning):
    col = family_colors[fam]
    lw = 3.0 if reasoning else 2.0
    ms = 85 if reasoning else 70
    ax.plot([ang, ang], [rmin, val], color=col, linewidth=lw, zorder=3)
    ax.scatter([ang], [val], s=ms, facecolor=col, edgecolor='black', linewidth=0.8, zorder=4)

# Connecting segments; dashed when crossing families, solid within family
for i in range(N):
    j = (i + 1) % N
    a_i, a_j = angles[i], angles[j]
    v_i, v_j = accuracy[i], accuracy[j]
    same_family = (families[i] == families[j])
    style = '-' if same_family else '--'
    ax.plot([a_i, a_j], [v_i, v_j], linestyle=style, color='0.5', linewidth=1.2, zorder=2)

# Axis limits, ticks
ax.set_ylim(rmin, 100)
ax.set_yticks([60, 70, 80, 90, 100])
ax.set_yticklabels(['60','70','80','90','100'], fontsize=12)
ax.set_rlabel_position(0)
ax.set_xticks(angles)
ax.set_xticklabels([])

# Outside labels (single break before "(Reasoning)" only)
def format_label(name, reasoning_flag):
    if reasoning_flag and "(Reasoning)" in name:
        return name.replace(" (Reasoning)", "\n(Reasoning)")
    return name

label_radius = 104.0
for ang, name, fam, reasoning in zip(angles, models, families, is_reasoning):
    txt = format_label(name, reasoning)
    ang_centered = ((ang + np.pi) % (2*np.pi)) - np.pi
    ha = 'left' if (-np.pi/2 <= ang_centered <= np.pi/2) else 'right'
    lbl = ax.text(ang, label_radius, txt, ha=ha, va='center',
                  color=family_colors[fam],
                  fontweight='bold' if reasoning else 'normal',
                  fontsize=13, zorder=10)
    lbl.set_path_effects([path_effects.withStroke(linewidth=2, foreground="white")])

# Numeric annotations with a bit more radial margin
for i, (ang, val) in enumerate(zip(angles, accuracy)):
    roff = 1.7
    aoff = 0.03 if (-np.pi/4 <= ang <= np.pi/4) else 0.0
    if i == 0:  # Gemini 2.5 Flash
        roff = 4.4
        aoff = 0.055
    if i == 4 or i == 6:  # GPT-4o and GPT-4.1 nano
        roff = 4.6
    if i == 5:  # GPT o4-mini (Reasoning)
        roff = 3

    num = ax.text(ang + aoff, val + roff, f"{val:.2f}%",
                  ha='center', va='bottom', fontsize=11.5, color='black', zorder=9)
    num.set_path_effects([path_effects.withStroke(linewidth=2, foreground="white")])

# Title moved up a bit more
ax.set_title("TAAF accuracy by model families (1 s, mid)", fontsize=17, fontweight='bold', y=1.15)

# Legend
family_handles = [
    Patch(facecolor=family_colors['Gemini'], edgecolor='black', label='Gemini'),
    Patch(facecolor=family_colors['Claude'], edgecolor='black', label='Claude'),
    Patch(facecolor=family_colors['GPT'],    edgecolor='black', label='GPT')
]
reasoning_handle = Line2D([0], [0], color='black', lw=3, label='Reasoning emphasis')
ax.legend(handles=family_handles + [reasoning_handle],
          loc='upper right', bbox_to_anchor=(1.14, 1.15), fontsize=12)

plt.tight_layout()

plt.savefig("../evaluation_outputs/RQ8.png")
plt.savefig("../evaluation_outputs/RQ8.pdf")

plt.show()

