import matplotlib.pyplot as plt

# Data
datasets = ['r_data.csv', 'w_data.csv', 'x_data.csv']
algorithms = ['OsGuard-x', 'OsGuard-x-fs','OsGuard-rwx', 'OsGuard-rwx-fs']

accuracy_data = {
    'OsGuard-x': [77.14, 57.45, 38.89],
    'OsGuard-x-fs': [91.43, 95.74, 44.44],
    'OsGuard-rwx': [88.57, 68.09, 36.11],
    'OsGuard-rwx-fs': [94.29, 97.87, 41.67]
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
plt.title('Accuracy of Models Evaluting execute on Different Datasets')
plt.xticks([p + 2 * bar_width for p in index], datasets)
plt.legend()

plt.tight_layout()
plt.show()
