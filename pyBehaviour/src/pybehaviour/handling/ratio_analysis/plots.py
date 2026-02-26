# ================================================================
# 0. Section: IMPORTS
# ================================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns

from itertools import combinations
from statannotations.Annotator import Annotator



# ================================================================
# 1. Section: Plot Multiple Parameter
# ================================================================
def plot_multiple_parameters(
    summary_df: pd.DataFrame,
    conditions: np.ndarray | list,
    selected_parameters: np.ndarray | list,
    labels: np.ndarray | list,
    title: str
) -> tuple:

    base_color = '#F03B20'
    alpha = 0.3
    faded_color = [(1 - alpha) * mcolors.to_rgb(base_color)[i] + alpha * mcolors.to_rgb('#FFFFFF')[i] for i in range(3)]
    colors = ['#8E8E8E', base_color, faded_color] # Grey for baseline, red for acute and faded red for chronic

    means = {}
    for condition in conditions:
        condition_data = summary_df[summary_df['condition'] == condition]  # Select data for each condition
        means[condition] = condition_data[selected_parameters].mean() # Calculate means for bar heights

    mean_df = pd.DataFrame(means, index=selected_parameters)

    # X positions for each parameter
    x = np.arange(len(selected_parameters))
    width = 0.2  # Width of each bar
    group_spacing = 0.05  # Space between bar groups

    # Plot setup
    fig, ax = plt.subplots(figsize=(12, 6))

    for i, condition in enumerate(conditions):
        # Bar plots
        ax.bar(x + i * (width + group_spacing), mean_df[condition], width,
               label=f'{condition}', alpha=0.8, color=colors[i])

        # Overlay dots for individual data points
        condition_data = summary_df[summary_df['condition'] == condition]
        for j, parameter in enumerate(selected_parameters):
            data_points = condition_data[parameter].dropna() # type: ignore[union-attr]
            x_positions = np.full(len(data_points), x[j] + i * (width + group_spacing))  # Create an array of x positions
            ax.scatter(x_positions, data_points, color=colors[i], alpha=0.7, s=50, zorder=10)

    # Formatting
    ax.set_xticks(x + (width + group_spacing) * (len(conditions) - 1) / 2)
    ax.set_xticklabels(labels, rotation=0, ha='center', fontsize=14)
    ax.set_ylabel('Ratio Injured/Uninjured', fontsize=16)
    ax.legend(title='Condition', fontsize=12)
    ax.set_title(title, fontsize=18)

    sns.despine(fig=None, ax=None, top=True, right=True)
    plt.tight_layout()
    plt.show(block=False)

    return fig, ax


# ================================================================
# 2. Section: Plot Single Parameter
# ================================================================
def plot_single_parameter(
    summary_df: pd.DataFrame,
    conditions: np.ndarray | list,
    parameter: str,
    title: str,
    ylabel: str,
    figure_name: str,
    direction_ttest
) -> tuple:

    # Colors
    base_color = '#F03B20'
    alpha = 0.3
    faded_color = [(1 - alpha) * mcolors.to_rgb(base_color)[i] + alpha * mcolors.to_rgb('#FFFFFF')[i] for i in range(3)]
    colors = ['#8E8E8E', base_color, faded_color]

    df_plot = summary_df.sort_values('condition', key=lambda s: s.apply(conditions.index)) # type: ignore[union-attr]

    fig = plt.figure(figsize=(2,4.5))
    ax = sns.barplot(data=df_plot, x='condition', y=parameter, hue='condition',
                palette=colors, errorbar=None, alpha=0.7)
    sns.stripplot(data=df_plot, x='condition', y=parameter, hue='condition',
                palette=colors, jitter=False, legend=False, ax=ax, size=7)

    # Stats
    df_plot = df_plot.sort_values('animal')
    x = "condition"
    y = parameter
    order = list(conditions)
    pairs = list(combinations(order, 2))
    annot = Annotator(ax, pairs, data=df_plot, x=x, y=y, order=order)
    annot.new_plot(ax, pairs, data=df_plot, x=x, y=y, order=order)
    annot.configure(test='t-test_paired', verbose=2)
    annot.apply_test(alternative=direction_ttest)
    annot.annotate()

    # Formatting
    ax.set_xlabel("")
    ax.set_xticks(np.arange(len(conditions)))
    ax.set_xticklabels(conditions, rotation=30, ha='right')
    ax.set_ylabel(ylabel)
    plt.title(title)
    sns.despine(fig=None, ax=None, top=True, right=True, left=False, bottom=False, offset=None, trim=False)

    plt.savefig(figure_name, bbox_inches='tight')
    plt.show(block=False)

    return fig, ax
