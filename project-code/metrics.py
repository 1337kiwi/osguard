#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

perms = ["r", "w", "x"]
datasets = ["r", "w", "x"]
modelfiles = ["r", "r-fs", "w", "w-fs", "x", "x-fs", "rwx", "rwx-fs"]

all_prints = []
all_metrics = []


def check_metrics(perm: str, modelfile: str):

    TP = 0
    TN = 0
    FP = 0
    FN = 0
    for dataset in datasets:
        filename = f"results/results_{modelfile}-{perm}-{dataset}.csv"
        results = pd.read_csv(filename)
        results["filename"] = results["filename"].fillna("")
        print(
            f"----- Evaluating {modelfile} {perm} ratios on dataset {dataset}_data.csv -----"
        )

        results_groups = (
            results.groupby(["id"])
            .apply(lambda x: x.to_dict("records"), include_groups=False)
            .to_dict()
        )

        # print(f"Results_groups: {results_groups}")

        for id, actual_rows in results_groups.items():
            expected_df = pd.read_csv(
                f"../Dataset-Generation/expected/{perm}_model-{dataset}_data.csv"
            )
            expected_df["filename"] = expected_df["filename"].fillna("")
            expected_groups = (
                expected_df.groupby("id")
                .apply(lambda x: x.to_dict("records"), include_groups=False)
                .to_dict()
            )

            # print(f"Expected_groups: {expected_groups}")

            expected_rows = expected_groups.get(id, [])

            actual_rows = [
                {k: v for k, v in row.items() if k != "perm"} for row in actual_rows
            ]

            actual_rows = sorted(
                actual_rows, key=lambda x: (x["required"], x["filename"])
            )
            expected_rows = sorted(
                expected_rows, key=lambda x: (x["required"], x["filename"])
            )

            for actual_row, expected_row in zip(actual_rows, expected_rows):
                if actual_row["required"] == "yes" and expected_row["required"] == "yes":
                    if actual_row["filename"] == expected_row["filename"]:
                        TP += 1
                    else:
                        FP += 1
                elif (actual_row["required"] == "yes" and expected_row["required"] == "no"):
                    FP += 1
                elif actual_row["required"] == "no" and expected_row["required"] == "no":
                    TN += 1
                elif actual_row["required"] == "no" and expected_row["required"] == "yes":
                    FN += 1

    # TPR = TP / (TP + FN) if TP + FN > 0 else 0
    # TNR = TN / (TN + FP) if TN + FP > 0 else 0
    # FPR = FP / (FP + TN) if FP + TN > 0 else 0
    # FNR = FN / (FN + TP) if FN + TP > 0 else 0

    # rates = f"TPR: {TPR:.2%}, TNR: {TNR:.2%}, FPR: {FPR:.2%}, FNR: {FNR:.2%}"
    ratios = f"TP: {TP}, TN: {TN}, FP: {FP}, FN: {FN}"

    print(f"----- Ratios: {ratios} -----")

    # all_prints.append(f"{modelfile} has {ratios} and {rates} on perm {perm} on all datasets")
    all_prints.append(f"{modelfile} has {ratios} on perm {perm} on all datasets")
    
    return {'TP': TP, 'TN': TN, 'FP': FP, 'FN': FN}


for modelfile in modelfiles:
    perm = modelfile.split("-")[0]
    modelfile = f"OsGuard-{modelfile}"
    all_metrics = []  # Reset the all_metrics list for each modelfile
    if perm == "rwx":
        for p in perm:
            metrics = check_metrics(p, modelfile)
            all_metrics.append((p, metrics))
    # else:
    #     metrics = check_metrics(perm, modelfile)
    #     all_metrics.append((perm, metrics))

    # Create confusion matrix
    perms = ["r", "w", "x"]
    metric_labels = ["TP", "TN", "FP", "FN"]

    values = {
        perm: [
            next(
                (
                    metric[1][label]
                    for metric in all_metrics
                    if metric[0] == perm and label in metric[1]
                ),
                0,
            )
            for label in metric_labels
        ]
        for perm in perms
    }

    confusion_matrix = [
        values[perm] if perm in values else [0, 0, 0, 0] for perm in perms
    ]

    plt.figure(figsize=(10, 7))
    sns.heatmap(
        confusion_matrix,
        annot=True,
        cmap="YlGnBu",
        xticklabels=metric_labels,
        yticklabels=perms,
    )
    plt.xlabel("Actual")
    plt.ylabel("Predicted")
    plt.title(f"Confusion Matrix for {modelfile}")
    plt.savefig(f"{modelfile}-confusion_matrix.png")
    plt.clf()  # Clear the current figure


print("----- Final Results -----")
for prints in all_prints:
    print(prints)
