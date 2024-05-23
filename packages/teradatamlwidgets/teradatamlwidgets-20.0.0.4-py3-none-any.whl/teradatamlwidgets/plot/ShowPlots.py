# -*- coding: utf-8 -*-
'''
Copyright © 2024 by Teradata.
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import os
import sys
import ipywidgets as widgets
from IPython.display import clear_output, HTML, Javascript, display
from teradataml import * 
import teradatamlwidgets.plot.teradata_plot_impl
from teradatamlwidgets.connection_teradataml import *
import IPython


def ShowPlots(plots, nrows=None, ncols=None, grid=None):
    clear_output()
    fig, axes = subplots(nrows=nrows, ncols=ncols, grid=grid)
    index = 0
    for ui_plot in plots:
        current_plot = ui_plot.get_current_plot()
        plot = current_plot.do_plot(ui_plot.get_base_args(), show=False, ax=axes[index], figure=fig)
        index += 1
    plot.show()