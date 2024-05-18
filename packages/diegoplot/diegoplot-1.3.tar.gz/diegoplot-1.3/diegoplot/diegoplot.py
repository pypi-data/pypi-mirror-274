#  -*- coding: UTF-8 -*-
#
#  diegoplot.py
#
#  Created by Diego on 2022/08/15 19:25:48.
#  Copyright © Diego. All rights reserved.

import numpy as np
import matplotlib.pyplot as plt
from cycler import cycler
from typing import Sequence, Optional, Iterable


class DiegoPlot:

    def __init__(self, *args, **kwargs) -> None:
        """
        :param (optional) x: x
        :param (optional) y: y
        :param kwargs legend: legend
        :param linestyle: Three kind of line styles are supported, choose by 0, 1, 2.
        """
        self.colors = [
            "#1f77b4",
            "#ff7f0e",
            "#2ca02c",
            "#d62728",
            "#9467bd",
            "#8c564b",
            "#e377c2",
            "#7f7f7f",
            "#bcbd22",
        ]
        self.style_0 = cycler("color", [None] * 10)
        self.style_1 = cycler(
            "marker", ["v", "o", "s", "d", "^", "*", "X", "h", "p", "P"]
        )
        self.style_2 = (
            cycler("linestyle", ["-", "--", ":", "-."])
            * cycler("marker", ["v", "o", "s", "d"])
            * cycler("fillstyle", ["none"])
            * cycler("markeredgewidth", [2])
        )
        self.style = [self.style_0, self.style_1, self.style_2]
        self.current_style: int = 0

        self.data = None
        self.x: Optional[Sequence] = None
        self.y: Optional[Sequence] = None
        self.label: Optional[Sequence] = None
        self.legend: Optional[Sequence] = None

        # Use `rcParams` to control global settings is good.
        # Figure size
        plt.rcParams["figure.figsize"] = kwargs.get("fig_size", (8, 6))
        plt.rcParams["figure.dpi"] = 100

        # Margin
        plt.rcParams["figure.subplot.left"] = 0.135
        plt.rcParams["figure.subplot.right"] = 0.98
        plt.rcParams["figure.subplot.bottom"] = 0.15
        plt.rcParams["figure.subplot.top"] = 0.98

        # Font
        plt.rcParams["font.family"] = "Times New Roman"
        plt.rcParams["mathtext.fontset"] = "stix"
        # Font size: about 12pt, 27 for 10.5 pt, 23 for 9 pt
        # 字体大小：30 = 小四, 27 = 五号, 23 = 小五 （大概）
        plt.rcParams["font.size"] = 30

        plt.rcParams["axes.linewidth"] = 2  # board width

        # Ticks
        plt.rcParams["xtick.direction"] = "in"
        plt.rcParams["ytick.direction"] = "in"
        plt.rcParams["xtick.major.size"] = 4
        plt.rcParams["xtick.major.size"] = 4
        plt.rcParams["xtick.major.width"] = 2
        plt.rcParams["xtick.major.width"] = 2
        plt.rcParams["ytick.major.size"] = 4
        plt.rcParams["ytick.major.size"] = 4
        plt.rcParams["ytick.major.width"] = 2
        plt.rcParams["ytick.major.width"] = 2

        plt.rcParams["lines.linewidth"] = kwargs.get("line_width", 3)
        plt.rcParams["lines.markersize"] = 13

        plt.rcParams["legend.edgecolor"] = "k"

        self.fig, self.ax = plt.subplots()

        if len(args) != 0:
            self.auto_plot(*args, **kwargs)

    def load_npz(self, filename: str) -> None:
        """
        Load data from *.npz.
        Data should be packed with index x, y, label, and legend. Means:
        np.savez(filename, x=x, y=y, label=label, legend=legend)
        """
        self.data = np.load(filename)
        try:
            self.x = self.data["x"]
        except IOError as e:
            print(e)
            self.x = None
        try:
            self.y = self.data["y"]
        except IOError as e:
            print(e)
            self.y = None
        try:
            self.label = self.data["label"]
        except IOError as e:
            print(e)
            self.label = None
        try:
            self.legend = self.data["legend"]
        except IOError as e:
            print(e)
            self.legend = None

    def load_txt(self, filename: str, index: list[str], split: str = " ") -> None:
        """
        A row of the text file should be like: x y_of_curve_1 y_of_curve_2 ...
        :param filename: You don't necessarily add '.txt' since this is build specifically for txt files.
        :param index: A list of column names. This tells the program how many columns you got and which on is x.
        :param split: How you split the data in a row, default space, alternatively you can use ';', ',', et al.
        :return: None.
        """
        with open(filename, "r") as f:
            file = f.readlines()
        file_data = []
        for row in file:
            file_data.append(row.strip("\n").split(split))
        file_data = np.array(file_data, dtype=float)
        data = {}
        for i, column_name in enumerate(index):
            data[column_name] = file_data[:, i]
        if "x" in data:
            self.x = data.pop("x")
        else:
            self.x = data.pop(next(iter(data)))
        self.y = list(data.values())

    def load_csv(self, filename: str):
        """
        Made for my use case only. Of which the beginning 21 lines are bullshit, and last line is empty.
        Data have two columns, x and y.
        :param filename:
        :return:
        """
        import csv

        with open(filename, "r") as f:
            file = list(csv.reader(f))
            file.pop()
            data = file[21:]
        data = np.array(data, dtype=float)
        self.x = data[:, 0]
        self.y = data[:, 1]

    def manual_load(self, x: Sequence, y: Sequence, label: Sequence, legend: Sequence):
        self.x = x
        self.y = y
        self.label = label
        self.legend = legend

    def plot_data(
        self, linestyle: int = 0, cycler: Optional[Iterable] = None, log_y: bool = False
    ) -> None:
        """
        Plot data that loaded before.
        So load before you plot.
        :param linestyle: Three kind of line styles are supported, choose by 0, 1, 2.
        :param cycler:
        :return: None.
        """
        assert linestyle in [0, 1, 2], "Line style should be 0, 1, or 2."
        self.current_style = linestyle
        if cycler is not None:
            line_style_cycle: Iterable = cycler
        else:
            line_style_cycle = self.style[linestyle]

        # Ensure x and y are numpy arrays
        self.x = np.asarray(self.x)
        self.y = np.asarray(self.y)

        # Choose plot function
        plot_function = self.ax.semilogy if log_y else self.ax.plot

        # Check the dimensions of x
        if self.x.ndim == 2:
            for x, y, sty in zip(self.x, self.y, line_style_cycle):
                plot_function(x, y, **sty)
        elif self.x.ndim == 1:
            if self.y.ndim == 1:
                plot_function(self.x, self.y)
            elif self.y.ndim == 2:
                for y, sty in zip(self.y, line_style_cycle):
                    plot_function(self.x, y, **sty)
            else:
                raise ValueError("Unexpected y data dimension.")
        else:
            raise ValueError("Unexpected x data dimension.")

    def plot_label(self, *args) -> None:
        """
        Plot label. Specified label is prior to the loaded one.
        :param args: ['x-axis', 'y-axis']
        :return: None
        """
        # plt.tick_params(direction='in', width=2, length=4)
        if len(args) == 1:
            try:
                self.ax.set_xlabel(args[0][0])
                self.ax.set_ylabel(args[0][1])
            except IndexError:
                raise IndexError("Label should be given by ['x','y']")
            return
        if self.label is not None:
            try:
                self.ax.set_xlabel(self.label[0])
                self.ax.set_ylabel(self.label[1])
            except IndexError:
                raise IndexError("Label should be given by ['x','y']")
            return

    def plot_legend(self, *args):
        if len(args) == 1:
            self.legend = args[0]
        elif len(args) > 1:
            raise RuntimeError(
                "Legend should be given in a list ['line 1', 'line 2', ...]."
            )
        if self.legend is None:
            raise RuntimeError("No legend is given.")
        handle_length = 1 if self.current_style == 0 else 1.9
        self.ax.legend(
            self.legend, handlelength=handle_length, fontsize=23, fancybox=False
        )

    def plot_tag(self, tag: str, loc: int = 2):
        """
        Plot tag like '(a)'.
        :param tag: Tag in string. Don't forget the bracket.
        :param loc: 1 for upper left, 2 for upper right. Tuple (x, y) for custom location.
        :return: None.
        """
        x, y = 0.95, 0.93  # Default upper right
        if type(loc) == tuple:  # custom location
            x, y = loc
        else:
            if loc == 1:  # upper left
                x, y = 0.10, 0.93
        self.ax.text(
            x,
            y,
            tag,
            horizontalalignment="center",
            verticalalignment="center",
            transform=self.ax.transAxes,
        )

    def show(self, auto_tight: bool = True):
        if auto_tight:
            self.fig.tight_layout(pad=0.15)
        plt.show()

    def auto_plot(self, x, y, **kwargs):

        self.x = x
        self.y = y
        self.plot_data(
            linestyle=kwargs.get("linestyle", 0),
            cycler=kwargs.get("cycler", None),
            log_y=kwargs.get("log_y", False),
        )

        if "legend" in kwargs:
            self.legend = kwargs["legend"]
            self.plot_legend()
        if "label" in kwargs:
            self.label = kwargs["label"]
            self.plot_label()
        if "tag" in kwargs:
            self.plot_tag(kwargs["tag"])

        self.show(auto_tight=True)
