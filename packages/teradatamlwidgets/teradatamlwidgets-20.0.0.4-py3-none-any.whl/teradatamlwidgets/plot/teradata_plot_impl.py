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
import json
import pprint
import sys
import ipywidgets
from IPython.display import clear_output, HTML,Javascript, display
import pandas as pd
import teradataml

show_native_dialog = True # "linux" in sys.platform.lower()


class BasePlot:

    NUM_Y_SERIES = 16

    def __init__(self, base, df):
        self.base = base
        self.df = df
        
    def get_ui(self):
        return self.plot_ui

    def get_columns_of_type(self, valid_types):
        result = []
        for column_name, column_type in self.df.dtypes._column_names_and_types:
            if column_type not in valid_types:
                if column_type == "datetime.date" and "int" in valid_types:
                    pass
                elif column_type == "datetime.date" and "float" in valid_types:
                    pass
                else:
                    continue
            result.append(column_name)
        return result

    def show_plot(self, base):
        try:
            # Currently we save this to a file
            self.plot.save("plot")
            # Then we load the save image
            file = open("plot.png", "rb")
            # Read the loaded image
            image = file.read()
            # And then show in ipwidgets
            base.image.value = image
            # Show ipwidgets Image widget
            base.image.layout.visibility = "visible"
        except Exception as e:
            print("Plot failed", e)
            output_value = '''
                require(
                    ["base/js/dialog"], 
                    function(dialog) {
                        dialog.modal({
                            title: "Error",
                            body: $("<div></div>").append('__BODY__'),
                            buttons: {
                                "OK": {
                                }}
                        });
                    }
                );'''
            error_message = str(e)
            error_list = error_message.split("\n")
            filter_error_list = [line for line in error_list if not line.strip(" ").startswith("at")]
            error_message = "\n".join(filter_error_list)
            error_message = error_message.replace("'", '"')
            error_message = error_message.replace('\n', '<br>');
            output_value = output_value.replace("__BODY__", error_message)
            if show_native_dialog:
                display(HTML(error_message))
            else:
                display(Javascript(output_value))


    def get_num_series_visible(self):
        result = 1
        for index in range(1, BasePlot.NUM_Y_SERIES):
            if self.Y[index].value != "" and self.Y[index].layout.visibility == "visible":
                result += 1
        return result

    def create_y_series(self, columns):
        self.Y = {}
        result = []

        arguments = []
        # Check is series is in constructor arguments
        if 'series' in self.base.kwargs:
            arguments = self.base.kwargs['series']
            if type(arguments)==str:
                # Make it into an array
                arguments = [arguments]
        for index in range(BasePlot.NUM_Y_SERIES):
            value = arguments[index] if index < len(arguments) else ""
            if value not in columns:
                columns.append(value)
            self.Y[index] = ipywidgets.Dropdown(
                options=[""] + columns,
                value= value,
                description="Series[{}]".format(index),
                disabled=False)
            if index <= len(arguments):
                self.Y[index].layout.visibility = "visible"
            else:
                self.Y[index].layout.visibility = "hidden"
            self.Y[index].y_index = index
            self.Y[index].observe(lambda change : self.update_y_series(change.owner.y_index), names='value')
            result.append(self.Y[index])
        return result
        

    def update_y_series(self, index):
        # Hide all series to right
        if self.Y[index].value == "":
            for i in range(index+1, BasePlot.NUM_Y_SERIES):
                self.Y[i].layout.visibility = "hidden"
                self.Y[i].value = ""
        else:
            # Show the series just to right
            if index+1 < BasePlot.NUM_Y_SERIES:
                self.Y[index+1].layout.visibility = "visible"
        self.base.change_plot()


    def get_y_series(self):
        y = []
        for index in range(BasePlot.NUM_Y_SERIES):
            if self.Y[index].value != "" and self.Y[index].layout.visibility == "visible":
                y.append(self.df[self.Y[index].value])
        return y


    def create_ui(self, x_columns, y_columns, is_scale=False):
        rows = []
        # Get the X value from constructor arguments
        X = self.base.kwargs.get('x', x_columns[0])
        # Make sure the X value is in the columns choices
        if X not in x_columns:
            x_columns.append(X)
        self.X = ipywidgets.Dropdown(
            options=x_columns,
            value=X,
            description='X:',
            disabled=False)
        rows.append(self.X)
        if is_scale:
            scale = self.base.kwargs.get('scale', x_columns[0])
            if scale not in x_columns:
                x_columns.append(scale)
            self.Scale = ipywidgets.Dropdown(
                value=scale,
                options=x_columns,
                description='Scale:',
                disabled=False)
            rows.append(self.Scale)
        # Arrange 4 in a row
        y_series = self.create_y_series(y_columns)
        for i in range(0, BasePlot.NUM_Y_SERIES, 4):
            series_row = []
            series_row.append(y_series[i])
            series_row.append(y_series[i+1])
            series_row.append(y_series[i+2])
            series_row.append(y_series[i+3])
            rows.append(ipywidgets.HBox(series_row))
        return rows


class LinePlot(BasePlot):
    def __init__(self, base, df):
        super().__init__(base, df)
        self.create_ui()
        
    def do_plot(self, base_args, show=True, ax=None, figure=None):
        y = self.get_y_series()

        self.plot =  self.df.plot(kind='line', x=self.df[self.X.value], y=y, 
            title = self.base.title.value if self.base.title.value else None,
            heading = self.base.heading.value if self.base.heading.value else None, 
            ax=ax,
            figure=figure,
            **base_args)
        if show:
            self.show_plot(self.base)
        return self.plot

    def create_ui(self):
        x_columns = self.get_columns_of_type(['float'])
        y_columns = self.get_columns_of_type(['float'])
        rows = BasePlot.create_ui(self, x_columns, y_columns)
        self.plot_ui = ipywidgets.VBox(rows)



class BarPlot(BasePlot):
    def __init__(self, base, df):
        super().__init__(base, df)
        self.create_ui()
        
    def do_plot(self, base_args, show=True, ax=None, figure=None):

        y = self.get_y_series()

        self.plot =  self.df.plot(kind='bar', x=self.df[self.X.value], y=y, 
            title = self.base.title.value if self.base.title.value else None,
            heading = self.base.heading.value if self.base.heading.value else None, 
            ax=ax,
            figure=figure,
            **base_args)

        if show:
            self.show_plot(self.base)
        return self.plot

    def create_ui(self):
        x_columns = self.get_columns_of_type(['float', 'int'])
        y_columns = self.get_columns_of_type(['float', 'int'])
        rows = BasePlot.create_ui(self, x_columns, y_columns)
        self.plot_ui = ipywidgets.VBox(rows)

class ScatterPlot(BasePlot):
    def __init__(self, base, df):
        super().__init__(base, df)
        self.create_ui()
        
    def do_plot(self, base_args, show=True, ax=None, figure=None):

        y = self.get_y_series()

        self.plot =  self.df.plot(kind='scatter', x=self.df[self.X.value], y=y, 
            title = self.base.title.value if self.base.title.value else None,
            heading = self.base.heading.value if self.base.heading.value else None, 
            ax=ax,
            figure=figure,
            **base_args)

        if show:
            self.show_plot(self.base)
        return self.plot

    def create_ui(self):
        x_columns = self.get_columns_of_type(['float', 'int'])
        y_columns = self.get_columns_of_type(['float', 'int'])
        rows = BasePlot.create_ui(self, x_columns, y_columns)
        self.plot_ui = ipywidgets.VBox(rows)

class CorrPlot(BasePlot):
    def __init__(self, base, df):
        super().__init__(base, df)
        self.create_ui()
        
    def do_plot(self, base_args, show=True, ax=None, figure=None):

        y = self.get_y_series()

        self.plot =  self.df.plot(kind='corr', x=self.df[self.X.value], y=y, 
            title = self.base.title.value if self.base.title.value else None,
            heading = self.base.heading.value if self.base.heading.value else None, 
            ax=ax,
            figure=figure,
            **base_args)

        if show:
            self.show_plot(self.base)
        return self.plot

    def create_ui(self):
        x_columns = self.get_columns_of_type(['float', 'int'])
        y_columns = self.get_columns_of_type(['float', 'int'])
        rows = BasePlot.create_ui(self, x_columns, y_columns)
        self.plot_ui = ipywidgets.VBox(rows)

class WigglePlot(BasePlot):
    def __init__(self, base, df):
        super().__init__(base, df)
        self.create_ui()
        
    def do_plot(self, base_args, show=True, ax=None, figure=None):

        y = self.get_y_series()

        self.plot =  self.df.plot(
            kind='wiggle', 
            x=self.df[self.X.value], 
            y=y, 
            scale = self.df[self.Scale.value],
            title = self.base.title.value if self.base.title.value else None,
            heading = self.base.heading.value if self.base.heading.value else None, 
            ax=ax,
            figure=figure,
            **base_args)

        if show:
            self.show_plot(self.base)
        return self.plot

    def create_ui(self):
        x_columns = self.get_columns_of_type(['float', 'int'])
        y_columns = self.get_columns_of_type(['float', 'int'])
        rows = BasePlot.create_ui(self, x_columns, y_columns, True)
        wiggle_row = []
        self.wiggle_fill = ipywidgets.ToggleButton(
            value=False,
            description='Wiggle Fill',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Fill Wiggle Area',
            icon='check' # (FontAwesome names without the `fa-` prefix)
        )       
        wiggle_row.append(self.wiggle_fill)
        self.wiggle_scale = ipywidgets.ToggleButton(
            value=False,
            description='Wiggle Scale',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Specifies the scale of the wiggle',
            icon='check' # (FontAwesome names without the `fa-` prefix)
        )
        wiggle_row.append(self.wiggle_scale)
        self.plot_ui = ipywidgets.VBox([ipywidgets.HBox(wiggle_row)] + rows)

class MeshPlot(BasePlot):
    def __init__(self, base, df):
        super().__init__(base, df)
        self.create_ui()
        
    def do_plot(self, base_args, show=True, ax=None, figure=None):

        y = self.get_y_series()

        self.plot =  self.df.plot(kind='mesh', 
            x=self.df[self.X.value], 
            y=y, 
            scale = self.df[self.Scale.value],
            title = self.base.title.value if self.base.title.value else None,
            heading = self.base.heading.value if self.base.heading.value else None, 
            ax=ax,
            figure=figure,
            **base_args)

        if show:
            self.show_plot(self.base)
        return self.plot

    def create_ui(self):
        x_columns = self.get_columns_of_type(['float', 'int'])
        y_columns = self.get_columns_of_type(['float', 'int'])
        rows = BasePlot.create_ui(self, x_columns, y_columns, True)
        wiggle_row = []
        self.wiggle_scale = ipywidgets.ToggleButton(
            value=False,
            description='Wiggle Scale',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Specifies the scale of the wiggle',
            icon='check' # (FontAwesome names without the `fa-` prefix)
        )
        wiggle_row.append(self.wiggle_scale)
        #rows.append(self.wiggle_scale)
        self.plot_ui = ipywidgets.VBox([ipywidgets.HBox(wiggle_row)] + rows)

class GeomPlot(BasePlot):
    def __init__(self, base, df):
        super().__init__(base, df)
        self.create_ui()
        
    def do_plot(self, base_args, show=True, ax=None, figure=None):

        y = self.get_y_series()

        self.plot =  self.df.plot(kind='geometry', 
            # Dont need x
            #x=self.df[self.X.value], 
            y=y, 
            title = self.base.title.value if self.base.title.value else None,
            heading = self.base.heading.value if self.base.heading.value else None, 
            ax=ax,
            figure=figure,
            **base_args)

        if show:
            self.show_plot(self.base)
        return self.plot

    def create_ui(self):
        x_columns = self.get_columns_of_type(['float', 'int'])
        y_columns = self.get_columns_of_type(['float', 'int'])
        rows = BasePlot.create_ui(self, x_columns, y_columns)
        self.plot_ui = ipywidgets.VBox(rows)





