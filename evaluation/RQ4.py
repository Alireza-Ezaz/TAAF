# -------------------- RQ4: FINAL VERSION WITH LABELS + FOCUSED Y-AXIS --------------------

import pandas as pd
import matplotlib.pyplot as plt

# Construct the dataset
data_rq3 = {
    'Model': ['GPT 4.1 nano', 'GPT 4o', 'GPT o4-mini'] * 3,
    'Time Interval': ['1s'] * 3 + ['10s'] * 3 + ['100s'] * 3,
    '0s_no_graph': [125, 111, 55, 166, 119, 92, 148, 137, 108],
    '0.5s_no_graph': [54, 29, 47, 43, 41, 26, 48, 40, 30],
    '1s_no_graph': [121, 160, 198, 91, 140, 182, 104, 123, 162],
    '0s_graph': [102, 56, 8, 140, 54, 16, 136, 61, 23],
    '0.5s_graph': [33, 9, 11, 17, 16, 16, 20, 17, 13],
    '1s_graph': [165, 235, 281, 143, 230, 268, 144, 222, 264]
}

df_rq3 = pd.DataFrame(data_rq3)

# Accuracy calculations
df_rq3['Acc_no_graph'] = (df_rq3['0.5s_no_graph'] * 0.5 + df_rq3['1s_no_graph']) / 300 * 100
df_rq3['Acc_graph'] = (df_rq3['0.5s_graph'] * 0.5 + df_rq3['1s_graph']) / 300 * 100

# Ensure Time Interval order
df_rq3['Time Interval'] = pd.Categorical(df_rq3['Time Interval'], categories=['1s', '10s', '100s'], ordered=True)
df_rq3.sort_values(by=['Model', 'Time Interval'], inplace=True)

# Color palette per model
color_palette = {
    'GPT 4.1 nano': '#1f77b4',  # blue
    'GPT 4o': '#ff7f0e',        # orange
    'GPT o4-mini': '#2ca02c'    # green
}

# -------------------- Plotting --------------------
plt.figure(figsize=(13, 8))

for model in df_rq3['Model'].unique():
    subset = df_rq3[df_rq3['Model'] == model]
    color = color_palette[model]

    # No KG
    plt.plot(subset['Time Interval'], subset['Acc_no_graph'], linestyle='--', marker='s', color=color,
             label=f"{model} (No KG)")
    for x, y in zip(subset['Time Interval'], subset['Acc_no_graph']):
        plt.text(x, y - 2.5, f"{y:.2f}%", ha='center', fontsize=13, color=color)

    # With KG
    plt.plot(subset['Time Interval'], subset['Acc_graph'], linestyle='-', marker='o', color=color,
             label=f"{model} (With KG)")
    for x, y in zip(subset['Time Interval'], subset['Acc_graph']):
        plt.text(x, y + 1.5, f"{y:.2f}%", ha='center', fontsize=13, color=color)

# Adjust y-axis to better show downward trends
plt.ylim(35, 105)  # focus on upper 2/3 where the data lies

plt.title("TAAF Accuracy Across Time Intervals and Models (With and Without Knowledge Graph)", fontsize=13)
plt.xlabel("Time Interval")
plt.ylabel("Accuracy (%)")
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(title="Model + KG Condition", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()
plt.savefig("../evaluation_outputs/RQ4.pdf", format="pdf")  # Save as vector PDF
plt.show()

