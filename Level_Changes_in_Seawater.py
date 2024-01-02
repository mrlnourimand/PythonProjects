"""
COMP.CS.100
Week 06, Second project. title: Project: Level Changes in Seawater.

(This program gets the user inputs, calculates their maximum, minimum,
    median, mean and standard deviation. Then print them out.)

Creator: Maral Nourimand
"""

from math import sqrt


def read_measurements():
    """ this function asks the user for a series of inputs, make them a list and return the list

    :return: list, list of the inputs that are entered by the user one by one.
    """
    measurements_list = []
    print("Enter seawater levels in centimeters one per line.\nEnd by entering an empty line.")
    while True:
        entry = input()
        if entry != "":
            measurements_list.append(float(entry))
        else:
            return measurements_list


def median_finder(sample_list):
    """ This function receives a list of numbers, calculate the median of the series
        and returns the median to where it was called.

    :param sample_list: list, an ALREADY-SORTED list of numbers
    :return: float, the median of the series of numbers.
    """
    sample_list.sort()
    length = len(sample_list)
    if length % 2 == 0:
        two_middle = sample_list[int(length / 2)] + sample_list[int(length / 2) - 1]
        return two_middle / 2
    else:
        return sample_list[int((length - 1) / 2)]


def mean_finder(samples):
    """ This function receives a list of numbers, calculates the average(mean) of them and return it.

    :param samples: list, list of numbers.
    :return: float, the mean(average) of the given list.
    """
    return sum(samples) / len(samples)


def variance_finder(series_num):
    """ This function receives a list of numbers, calculates their variance and returns it.

    :param series_num: list, a list of numbers.
    :return: float, variance of the numbers which are in the list.
    """
    differ_list = []
    ave = mean_finder(series_num)  # average of the numbers
    for item in series_num:
        differ_list.append((item - ave) ** 2)
    return sum(differ_list) / (len(differ_list) - 1)


def main():
    # read the inputs
    measurements = read_measurements()
    # measurements = [
        # August 2022, Pohnpei, Federal States of Micronesia

      #  877, 893, 899, 906, 908, 896, 884, 874,
      #  867, 882, 892, 888, 889, 886, 895, 902,
      #  892, 887, 876, 860, 865, 877, 867, 865,
      #  892, 901, 916, 922, 925, 947, 962
    # ]

    # check the entry errors
    if len(measurements) < 2 :
        print("Error: At least two measurements must be entered!")

    else:
         # find the min/max
        maximum = max(measurements)
        minimum = min(measurements)

        # find median
        median = median_finder(measurements)

        # find mean
        mean = mean_finder(measurements)

        # find variance
        variance = variance_finder(measurements)

        # find standard deviation
        deviation = sqrt(variance)

        print(f"Minimum: {minimum:>10.2f} cm\nMaximum: {maximum:>10.2f} cm\nMedian: {median:>11.2f} cm\n"
        f"Mean: {mean:>13.2f} cm\nDeviation: {deviation:>8.2f} cm")

if __name__ == "__main__":
    main()
