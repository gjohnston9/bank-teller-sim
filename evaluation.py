import numpy as np

def get_statistics(lst):
    mean = sum(lst) / float(len(lst))
    std_dev = np.std(lst)
    median = lst[len(lst)/2]

    return "mean: {}\nstandard deviation: {}\nmedian: {}".format(mean, std_dev, median)
