import numpy as np
import matplotlib.patches as patches
import matplotlib.pyplot as plt; plt.switch_backend('agg')

def get_statistics(lst):
    mean = sum(lst) / float(len(lst))
    median = lst[len(lst)/2]
    std_dev = np.std(lst)

    return "mean: {:.1f}\nmedian: {:.1f}\nstandard deviation: {:.1f}\n".format(mean, median, std_dev)


def save_plot(xy, title, xlabel, ylabel, file_name, lunch_break_times, lunch_break_length):
	x, y = zip(*xy)
	fig, ax = plt.subplots(nrows=1, ncols=1)
	plt.scatter(x, y, s=4)
	axes = plt.gca()
	axes.set_xlim([0, max(x)])
	axes.set_ylim([0, max(y)])
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)

	### rectangles for rush periods
	for x_start in (2, 8):
		ax.add_patch(patches.Rectangle((x_start, 0), 2, max(y), 0, alpha=0.1, color="red"))

	### rectangles indicating lunch break times
	for x_start in lunch_break_times:
		ax.add_patch(patches.Rectangle((x_start, 0), lunch_break_length, max(y), 0, alpha=0.1, color="blue"))

	plt.title(title)
	plt.savefig(file_name)
	plt.clf()
