import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import Handling_helpers as Handling_helpers

# === SETUP ===
control_dir = r'C:\Users\paoli\OneDrive\Documenti\A_PARIGI\AAA_InternshipEPFL\DataXThesis\46_untreatedCtrl\Handling\Analysed\Analysed_CerealHandling_AllVideos'
vsx2_dir = r'C:\Users\paoli\OneDrive\Documenti\A_PARIGI\AAA_InternshipEPFL\DataXThesis\44ABl\Handling\CSV_files\RetrainedModel'
conditions = ['handling-postablation', '7', '28']

# === LOAD DATA ===
summary_control = Handling_helpers.compute_feature_per_animal(control_dir, conditions, threshold=0.8)
summary_control['group'] = 'Control'

summary_vsx2 = Handling_helpers.compute_feature_per_animal(vsx2_dir, conditions, threshold=0.8)
summary_vsx2['group'] = 'Vsx2-ablated'

# === COMBINE DATA ===
summary_all = pd.concat([summary_control, summary_vsx2], ignore_index=True)

# === PARAMETERS TO PLOT ===
selected_parameters = [
    'ratio_avg_dist_fingers_tip',
    'ratio_range_dist_tip',
    'ratio_var_dist_tip',
    'ratio_avg_dist_cereal_tip',
    'ratio_min_dist_cereal_tip'
]

labels = [
    'Distance between\nfingers',
    'Fingers range\nof motion',
    'Finger position\nvariance',
    'Average distance\nfrom cereal',
    'Closest finger\ndistance from cereal'
]



# === PLOTTING FUNCTION ===
def plot_group_comparison(summary, conditions, selected_parameters, labels, title):
    colors = {
        'Control': '#8E8E8E',
        'Vsx2-ablated': '#F03B20'
    }

    width = 0.35
    group_spacing = 0.15
    condition_positions = np.arange(len(conditions))

    fig, axes = plt.subplots(1, len(selected_parameters), figsize=(18, 5), sharey=True)
    if len(selected_parameters) == 1:
        axes = [axes]

    for i, param in enumerate(selected_parameters):
        ax = axes[i]
        for j, condition in enumerate(conditions):
            for k, group in enumerate(['Control', 'Vsx2-ablated']):
                x_pos = j + (k - 0.5) * width + (j * group_spacing)
                data = summary[(summary['condition'] == condition) & (summary['group'] == group)][param].dropna()
                mean_val = data.mean()
                ax.bar(x_pos, mean_val, width=width, color=colors[group], label=group if j == 0 and k == 0 else "")

                # Add scatter for individual animals
                #ax.scatter(np.full(len(data), x_pos), data, color=colors[group], edgecolor='black', alpha=0.7, zorder=10)
                jitter_strength = 0.08  # adjust if needed
                jittered_x = x_pos + np.random.uniform(-jitter_strength, jitter_strength, size=len(data))
                ax.scatter(jittered_x, data, color=colors[group], edgecolor='black', alpha=0.7, zorder=10)



        ax.set_title(labels[i], fontsize=14)
        ax.set_xticks(condition_positions)
        ax.set_xticklabels(['PostAblation', 'D7', 'D28'], rotation=30)
        ax.set_xlabel("Condition")
        if i == 0:
            ax.set_ylabel("Ratio Injured / Uninjured")
        ax.grid(True, axis='y', linestyle='--', alpha=0.5)

    handles = [plt.Rectangle((0, 0), 1, 1, color=colors[group]) for group in colors]
    fig.legend(handles, colors.keys(), loc='upper right', fontsize=12)
    fig.suptitle(title, fontsize=16)
    sns.despine()
    plt.tight_layout()
    plt.show()

# === CALL THE PLOT ===
plot_group_comparison(summary_all, conditions, selected_parameters, labels, title="Control vs Vsx2-Ablated: Injury Ratios")
