#!/usr/bin/env python3

import pandas as pd

perms = ["r", "w", "x"]
datasets = ["r", "w", "x"]
modelfiles = ["r", "r-fs", "w", "w-fs", "x", "x-fs", "rwx", "rwx-fs"]

all_accuracies = []


def check_accuracy(perm: str, dataset: str, modelfile: str):
    filename = f"results/results_{modelfile}-{perm}-{dataset}.csv"
    results = pd.read_csv(filename)
    results["filename"] = results["filename"].fillna("")

    total = 0
    correct = 0

    print(
        f"----- Evaluating {modelfile} {perm} accuracy on dataset {dataset}_data.csv -----"
    )

    # Group by 'id' and 'dataset' and convert each group to a list of dictionaries
    results_groups = (
        results.groupby(["id"])
        .apply(lambda x: x.to_dict("records"), include_groups=False)
        .to_dict()
    )

    for id, actual_rows in results_groups.items():
        # Read the expected CSV for the current dataset
        expected_df = pd.read_csv(
            f"../Dataset-Generation/expected/{perm}_model-{dataset}_data.csv"
        )
        expected_df["filename"] = expected_df["filename"].fillna("")
        expected_groups = (
            expected_df.groupby("id")
            .apply(lambda x: x.to_dict("records"), include_groups=False)
            .to_dict()
        )

        expected_rows = expected_groups.get(id, [])

        actual_rows = [
            {k: v for k, v in row.items() if k != "perm"} for row in actual_rows
        ]

        # Sort the rows before comparing to ensure order doesn't matter
        if sorted(actual_rows, key=lambda x: (x["required"], x["filename"])) == sorted(
            expected_rows, key=lambda x: (x["required"], x["filename"])
        ):
            print(f"Dataset {dataset}, id {id} correct")
            correct += 1
        else:
            print(f"Dataset {dataset}, id {id} NOT correct")
            print(f"  Expected: {expected_rows}")
            print(f"  Actual: {actual_rows}")
        total += 1

    print(f"----- Accuracy: {correct}/{total} ({correct/total:.2%}) -----")

    all_accuracies.append(
        f"{modelfile} {perm} accuracy on dataset {dataset}_data.csv: {correct}/{total} ({correct/total:.2%})"
    )


for modelfile in modelfiles:
    perm = modelfile.split("-")[0]
    modelfile = f"OsGuard-{modelfile}"
    if perm == "rwx":
        for p in perm:
            for dataset in datasets:
                check_accuracy(p, dataset, modelfile)
    else:
        for dataset in datasets:
            check_accuracy(perm, dataset, modelfile)

print("----- Final Results -----")
for accuracy in all_accuracies:
    print(accuracy)
