import matplotlib.pyplot as plt

# Data
datasets = ['r_data.csv', 'w_data.csv', 'x_data.csv']
algorithms = ['OsGuard-r', 'OsGuard-r-fs','OsGuard-rwx', 'OsGuard-rwx-fs']

accuracy_data = {
    'OsGuard-r': [82.86, 68.09, 25.00],
    'OsGuard-r-fs': [100, 59.57, 7.22],
    'OsGuard-rwx': [85.71, 72.34, 16.67],
    'OsGuard-rwx-fs': [97.14, 59.57, 41.67]
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
plt.title('Accuracy of Models Evaluting Read on Different Datasets')
plt.xticks([p + 2 * bar_width for p in index], datasets)
plt.legend()

plt.tight_layout()
plt.show()
