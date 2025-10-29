import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# -------------------------------------------------
# 1) Load the CSV you uploaded
# -------------------------------------------------
csv_path = "../extra_documents/TAAF Aggregated Results.csv"
df = pd.read_csv(csv_path)

# -------------------------------------------------
# 2) Helper – compute accuracy for any three-column set
# -------------------------------------------------
def add_accuracy(frame, zero_col, half_col, one_col, new_name):
    frame['Total_tmp'] = frame[[zero_col, half_col, one_col]].sum(axis=1)
    frame[new_name] = (
        0.5 * frame[half_col] + 1 * frame[one_col]
    ) / frame['Total_tmp'] * 100
    frame.drop(columns='Total_tmp', inplace=True)
    return frame

# Apply for RAW (no KG) and KG-Powered counts
add_accuracy(df, 'Raw 0s',          'Raw 0.5',          'Raw 1s',          'Acc_NoKG')
add_accuracy(df, 'KG-Powered 0s',   'KG-Powered 0.5s',  'KG-Powered 1s',   'Acc_KG')

# -------------------------------------------------
# 3) Aggregate by Query-Type & Graph-Structure
# -------------------------------------------------
agg = (
    df.groupby(['Question Category Type', 'Question Graph Type'])
      [['Acc_NoKG', 'Acc_KG']]
      .mean()
      .reset_index()
)

# Two pivot tables for the two heatmaps
heat_no  = agg.pivot(index='Question Category Type', columns='Question Graph Type', values='Acc_NoKG')
heat_yes = agg.pivot(index='Question Category Type', columns='Question Graph Type', values='Acc_KG')

# -------------------------------------------------
# 4) Plot with shared color scale (vmin/vmax)
# -------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(14, 5.2), sharey=True)

# Shared color range
vmin = min(heat_no.min().min(), heat_yes.min().min())
vmax = max(heat_no.max().max(), heat_yes.max().max())

# Heatmap: WITHOUT KG
sns.heatmap(
    heat_no, ax=axes[0],
    annot=True, fmt=".2f",
    cmap=sns.light_palette("blue", as_cmap=True),
    cbar_kws={'label': 'Accuracy (%)'},
    vmin=vmin, vmax=vmax
)
axes[0].set_title("Accuracy by Query & Graph (No KG)")
axes[0].set_xlabel("Graph Structure")
axes[0].set_ylabel("Query Type")

# Heatmap: WITH KG
sns.heatmap(
    heat_yes, ax=axes[1],
    annot=True, fmt=".2f",
    cmap=sns.light_palette("blue", as_cmap=True),
    cbar_kws={'label': 'Accuracy (%)'},
    vmin=vmin, vmax=vmax
)
axes[1].set_title("Accuracy by Query & Graph (With KG)")
axes[1].set_xlabel("Graph Structure")
axes[1].set_ylabel("")

# -------------------------------------------------
# 5) Save and show
# -------------------------------------------------
plt.tight_layout()
plt.savefig("../evaluation_outputs/RQ5-1.pdf", format="pdf")
plt.show()
