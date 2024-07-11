import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# Create 3 x 3 subplot
fig, axes = plt.subplots(3, 3, figsize=(12, 8), sharex=True)

COLORS = ["r", "b", "g"]

for WITHIN_OR_BETWEEN in ["within", "between"]:

    # Import csv file
    ci_df = pd.read_csv(
        f"data_scripts/analysis/confidence_interval/confidence_interval_researchers_{WITHIN_OR_BETWEEN}_group.csv")

    # Plot WITHIN groups
    if WITHIN_OR_BETWEEN == "within":
        axes_indices = [[0, 0], [1, 1], [2, 2]]
        groups = [2, 3, 4]
        groups_series = [filename.split("_")[0]
                         for filename in list(ci_df["filename"])]

        y_list = [0.5, 0, -0.5]

    else:
        axes_indices = [[1, 0], [2, 0], [2, 1]]
        groups = ["23", "24", "34"]
        BASE_Y_LIST = [1, 0, -1]  # Base y location for each category
        OFFSET = 0.25  # offset between each annotator pair bar
        offset_half = OFFSET/2
        y_list = []
        for base_y in BASE_Y_LIST:
            temp_list = []
            min_val = base_y - OFFSET - offset_half
            for i in range(4):
                temp_list.append(min_val + OFFSET * i)

            y_list.append(temp_list)

        # Create a column for groups
        # Create a column for categories
        groups_series = [filename.split("_")[0] + filename.split("_")[1]
                         for filename in list(ci_df["filename"])]

    categories_series = [filename.split("_")[-1][:-4]
                         for filename in list(ci_df["filename"])]
    ci_df["group"] = pd.Series(groups_series)
    ci_df["category"] = pd.Series(categories_series)

    app_df = ci_df[ci_df["category"] == "Appropriateness"]
    info_df = ci_df[ci_df["category"] == "Information content of outputs"]
    humanlikeness_df = ci_df[ci_df["category"] == "Humanlikeness"]

    df_list = [app_df, info_df, humanlikeness_df]
    labels = ["D", "^", "s"]

    for group_idx, group in enumerate(groups):
        for category_idx, df in enumerate(df_list):
            ax = axes[axes_indices[group_idx][0]][axes_indices[group_idx][1]]
            ax.set_ylim(-1.5, 1.5)
            ax.set_xlim(-0.1, 0.8)
            ax.set_yticks([])  # Remove y-ticks
            df_group = df[df["group"] == str(group)]

            y = y_list[category_idx]
            ax.barh(y, left=df_group["lwr"],
                    width=df_group["upr"]-df_group["lwr"], height=0.1, align="center",  color=COLORS[category_idx])
            ax.plot(
                df_group["kappa"], y, linestyle='None', marker=labels[category_idx], markersize=7, color=COLORS[category_idx], label=df["category"].iloc[0],)


# Turn off unused axes
for i in range(3):
    for j in range(3):
        if j == 0:
            axes[i][j].set_ylabel(f"Group {i + 2}", fontsize=13)
        if i == 2:
            axes[i][j].set_xlabel(f"Group {j + 2}", fontsize=13)
        if i < j:
            axes[i, j].axis('off')

handles, labels = ax.get_legend_handles_labels()
fig.legend(handles, labels, loc='upper right')
# fig.text(0.5, 0.04, "Cohen's Kappa", ha='center', va='center')
fig.suptitle("Cohen's Kappa with Confidence Intervals")
fig.tight_layout()
fig.show()
# plt.yticks(groups)
# plt.xlabel("Cohen's Kappa")

# plt.show()
