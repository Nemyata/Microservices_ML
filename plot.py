import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time

while True:
    metric_log = pd.read_csv('./logs/metric_log.csv')

    plt.figure(figsize=(10, 5))
    sns.histplot(metric_log['absolute_error'], kde=True, color='orange')
    plt.xlabel('absolute_error')
    plt.ylabel('Count')

    plt.savefig('./logs/error_distribution.png')
    plt.close()

    time.sleep(10)
