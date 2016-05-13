# coding=utf-8

from matplotlib.pyplot import subplots


def plot_steps(x, y, steps, ax=None):
    if not ax:
        fig, ax = subplots()

    plot_retract(x, y, ax)

    for step in steps:
        ax.axvline(x[step], linewidth=2, color='r')


def plot_retract(x, y, ax=None):
    if not ax:
        fig, ax = subplots()

    x *= 10 ** 6
    y *= 10 ** 12

    ax.plot(x, y)
    ax.set_xlabel("height [µm]")
    ax.set_ylabel("force [pN]")
