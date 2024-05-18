import unittest
import numpy as np
from diegoplot.diegoplot import DiegoPlot

class TestDiegoPlot(unittest.TestCase):
    def setUp(self):
        self.dp = DiegoPlot()

    def test_plot_data_no_data(self):
        with self.assertRaises(ValueError):
            self.dp.plot_data()

    def test_plot_data_with_data(self):
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        self.dp.manual_load(x, y, ['X', 'Y'], ['Sine Wave'])
        try:
            self.dp.plot_data()
        except ValueError as e:
            self.fail(f'plot_data 方法引发了一个异常: {e}')

    def test_plot_label(self):
        self.dp.label = ['X', 'Y']
        try:
            self.dp.plot_label()
            self.assertEqual(self.dp.ax.get_xlabel(), 'X')
            self.assertEqual(self.dp.ax.get_ylabel(), 'Y')
        except Exception as e:
            self.fail(f'plot_label 方法引发了一个异常: {e}')
    
    def test_auto_plot(self):
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        label = ['X', 'Y']
        legend = ['Sine Wave']
        tag = '(a)'

        try:
            self.dp.auto_plot(x, y, label=label, legend=legend, tag=tag)
        except Exception as e:
            self.fail(f'auto_plot 方法引发了一个异常: {e}')

    def test_plot_legend(self):
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        self.dp.manual_load(x, y, [], [])
        self.dp.plot_data()
        legend = ['Sine Wave']
        self.dp.legend = legend
        self.dp.plot_legend()
        try:
            self.assertEqual(
                [text.get_text() for text in self.dp.ax.get_legend().get_texts()],
                legend
            )
        except Exception as e:
            self.fail(f'plot_legend 方法引发了一个异常: {e}')

if __name__ == '__main__':
    unittest.main()
