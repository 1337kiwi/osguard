import matplotlib.pyplot as plt

# Data
datasets = ['r_data.csv', 'w_data.csv', 'x_data.csv']
algorithms = ['OsGuard-w', 'OsGuard-w-fs','OsGuard-rwx', 'OsGuard-rwx-fs']

accuracy_data = {
    'OsGuard-w': [97.14, 87.23, 97.22],
    'OsGuard-w-fs': [97.14, 97.87, 94.44],
    'OsGuard-rwx': [85.71, 80.85, 38.89],
    'OsGuard-rwx-fs': [100.00, 82.98, 97.22]
}

# Plotting
bar_width = 0.15
opacity = 0.8
index = range(len(datasets))

fig, ax = plt.subplots()

for i, algorithm in enumerate(algorithms):
    plt.bar([p + i * bar_width for p in index], accuracy_data[algorithm], bar_width,
            alpha=opacity, label=algorithm)

plt.xlabel('Datasets')
plt.ylabel('Accuracy Percentage')
plt.title('Accuracy of Models Evaluting Write on Different Datasets')
plt.xticks([p + 2 * bar_width for p in index], datasets)
plt.legend()

plt.tight_layout()
plt.show()
