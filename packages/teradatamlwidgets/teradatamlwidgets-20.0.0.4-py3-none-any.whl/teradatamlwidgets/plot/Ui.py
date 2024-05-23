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
import ipywidgets
from IPython.display import clear_output, HTML, Javascript, display
from teradataml import * 
from teradatamlwidgets.plot.teradata_plot_impl import *
from teradatamlwidgets.connection_teradataml import *
import IPython

class Ui:

    ui_plots = []
    login_info = {}
    connection = None

    '''
    Teradata's Interactive Notebook Plot Interface
    '''
    def __init__(self, current_plot = "Line", table_name="", df=None, connection = None, **kwargs):
        """
        Constructor for the Teradata's Interactive Notebook Plot Interface.

        @param df: Name of database table

        @param current_plot: type of plot

        @param connection: Optional Argument. Specifies the specific connection; could be teradataml based (i.e. TeradatamlConnection instance) or another platform.

        """

        self.widget_output = ipywidgets.Output()
        self.main_panel = ipywidgets.HBox([])
        IPython.display.display(self.main_panel, self.widget_output)

        self.kwargs = kwargs
        self.database_table_name = table_name
        self.current_plot = current_plot
        self.plot_map = {}
        self.df = df

        if connection:
            self.connection = connection
        else:
            if not Ui.connection:
                if not connection:
                    connection = Connection()     
                Ui.connection = connection
                self.connection = Ui.connection

        self.folder = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))
        # Load a progress bar when stuff is slow and we need to indicate to user to wait
        with open(os.path.join(self.folder, "progress.gif"), 'rb') as f:
            img = f.read()
        self.loading_bar = ipywidgets.Image(value=img)
        self.show_display(self.loading_bar, False)

        if self.connection.is_logged_in():
            self.open_ui()
        else:
            self.login_info['default_db'] = "dssDB"
            self.login_info['val_location'] = "VAL"
            self.create_login_ui()
            # If login was previously a succes then just log in again
            if len(Ui.login_info)>0:
                try:
                    self.login_info = Ui.login_info.copy()
                    self.on_login(self.login)
                except Exception as e:
                    with self.widget_output:
                        print(str(e))
                    pass

    def show_display(self, item, clear=True):
        if clear:
            self.widget_output.clear_output(wait=True)
        with self.widget_output:
            IPython.display.display(item)

    def create_login_ui(self):
        self.show_display(self.loading_bar)

        teradata_environment = json.loads(os.environ.get("TERADATA_DEFAULT", "{}"))

        self.host = ipywidgets.Text(
            value= self.login_info.get('host', teradata_environment.get("host", "")),
            placeholder='Enter host URL',
            description='Host:',
        )
        self.username = ipywidgets.Text(
            value= self.login_info.get('username', teradata_environment.get("user", "")),
            placeholder='Enter username',
            description='Username:',
            disabled=False
        )
        self.password = ipywidgets.Password(
            value=self.login_info.get('password', teradata_environment.get("password", "")),
            placeholder='Enter password',
            description='Password:',
            disabled=False
        )
        self.default_db = ipywidgets.Text(
            value=self.login_info.get('default_db', teradata_environment.get("defaultDB", "")),
            placeholder='Enter default database',
            description='Schema:',
            disabled=False
        )
        self.val_loc = ipywidgets.Text(
            value=self.login_info.get('val_location', teradata_environment.get("VAL_LOCATION", "VAL")),
            placeholder='Enter VAL location',
            description='VALIB:',
            disabled=False
        )
        self.output = ipywidgets.Output(layout={})

        self.login = ipywidgets.Button(description="Login")
        self.login.on_click(lambda x : self.on_login(x))

        self.login_ui = ipywidgets.HBox([ipywidgets.VBox([self.host,self.username,self.password,self.default_db,self.val_loc, self.output]), self.login])
        self.show_display(self.login_ui)

    def on_login(self, b):
        try:
            self.login_info['host'] = self.host.value
            self.login_info['username'] = self.username.value
            self.login_info['password'] = self.password.value
            self.login_info['default_db'] = self.default_db.value
            self.login_info['val_location'] = self.val_loc.value

            self.connection.login(self.login_info['host'], self.login_info['username'], self.login_info['password'], self.login_info['default_db'], self.login_info['val_location'])
            if not self.connection.is_logged_in():
                return
            self.open_ui()
            # Copy last succesful login
            Ui.login_info = self.login_info.copy()
        except Exception as e:
            with self.widget_output:
                print(str(e))

    def on_logout(self, b):
        # Clear the global login info
        Ui.login_info = {}
        self.connection.logout()
        self.create_login_ui()

    def get_base_args(self):
        base_args = {}
        if self.grid_color.value:
            base_args["grid_color"] = self.grid_color.value 
        if self.grid_format.value:
            base_args["grid_format"] = self.grid_format.value
        if self.grid_linewidth.value:
            base_args["grid_linewidth"] = self.grid_linewidth.value
        if self.grid_linestyle.value:
            base_args["grid_linestyle"] = self.grid_linestyle.value
        base_args["xlabel"] = self.xlabel.value if self.xlabel.value else None
        base_args["xrange"] = (self.xmin.value, self.xmax.value) if self.xrange.value else None
        if self.xtick_format.value:
            base_args["xtick_format"] = self.xtick_format.value
        base_args["reverse_xaxis"] = self.reverse_xaxis.value
        base_args["ylabel"] = self.ylabel.value if self.ylabel.value else None
        base_args["yrange"]  = (self.ymin.value, self.ymax.value) if self.yrange.value else None
        if self.ytick_format.value:
            base_args["ytick_format"] = self.ytick_format.value
        base_args["reverse_yaxis"] = self.reverse_yaxis.value
        if self.cmap.value:
            base_args["cmap"] = self.cmap.value
        if self.legend.value:
            base_args["legend"] = self.legend.value.split(",")
            base_args["legend_style"] = self.legend_style.value
        if self.vmin.value:
            base_args["vmin"] = self.vmin.value
        if self.vmax.value:
            base_args["vmax"] = self.vmax.value
        if self.width.value != 640 or self.height.value != 480:
            base_args["figsize"] = (self.width.value, self.height.value)
        
        # Series values are lists
        base_args["color"] = []
        base_args["linestyle"] = []
        base_args["linewidth"] = []
        base_args["marker"] = []
        base_args["markersize"] = []
        
        for y_index in range(self.get_num_series_visible()):
            if self.color[y_index].value:
                base_args["color"].append(self.color[y_index].value)
            if self.linestyle[y_index].value:
                base_args["linestyle"].append(self.linestyle[y_index].value)
            if self.linewidth[y_index].value:
                base_args["linewidth"].append(self.linewidth[y_index].value)
            if self.marker[y_index].value:
                base_args["marker"].append(self.marker[y_index].value)
            if self.markersize[y_index].value:
                base_args["markersize"].append(self.markersize[y_index].value)

        if len(base_args["color"]) == 0:
            del base_args["color"]
        if len(base_args["linestyle"]) == 0:
            del base_args["linestyle"]
        if len(base_args["linewidth"]) == 0:
            del base_args["linewidth"]
        if len(base_args["marker"]) == 0:
            del base_args["marker"]
        if len(base_args["markersize"]) == 0:
            del base_args["markersize"]
            
        return base_args


    def get_num_series_visible(self):
        return self.get_current_plot().get_num_series_visible()

    def do_plot(self):
        error_message = ""
        try:
            self.show_display(self.loading_bar)
            self.contents = self.get_current_plot().get_ui()
            self.get_current_plot().do_plot(self.get_base_args())
        except Exception as e:
            error_message = str(e)
        self.widget_output.clear_output()
        if error_message:
            with self.widget_output:
                print(error_message)
        tab_selected_index = self.tab.selected_index
        self.create_tab()
        self.tab.selected_index = tab_selected_index
        
    def change_plot(self):
        self.widget_output.clear_output()
        self.contents = self.get_current_plot().get_ui()
        tab_selected_index = self.tab.selected_index
        self.create_tab()
        self.tab.selected_index = tab_selected_index
        
    def get_current_plot(self):
        return self.plot_map[self.plot_menu.value]


    def update_range(self):
        self.xmin.disabled = not self.xrange.value
        self.xmax.disabled = not self.xrange.value
        self.ymin.disabled = not self.yrange.value
        self.ymax.disabled = not self.yrange.value


    def get_series_value(self, name, default_value, index):
        value = default_value
        if name in self.kwargs:
            if type(self.kwargs[name])==list and index<len(self.kwargs[name]):
                value = self.kwargs[name][index]
            elif type(self.kwargs[name])==str:
                value = self.kwargs[name]
        return value

    def create_series_tabs(self):
        self.color = []
        self.linestyle = []
        self.linewidth = []
        self.marker = []
        self.markersize = []
        
        
        self.series_tabs = []
        for y_index in range(BasePlot.NUM_Y_SERIES):
            rows = []
            style_rows = []

            self.color.append(ipywidgets.Text(
                value=self.get_series_value('color', 'blue', y_index),
                tooltip='Specifies the color for the plot. argument: color',
                layout={'width': '200px'},
                description='Style Color:',
                disabled=False   
            ))
            style_rows.append(self.color[-1])


            self.linestyle.append(ipywidgets.Dropdown(
                options=['', '-', '--', '-.', ":"], 
                value=self.get_series_value('linestyle', '', y_index),
                tooltip='Specifies the line style for the plot. argument: linestyle',
                layout={'width': '200px'},
                description='Line Style:',
                disabled=False,
            ))
            style_rows.append(self.linestyle[-1])

            self.linewidth.append(ipywidgets.BoundedFloatText(
                value=self.get_series_value('linewidth', 0.8, y_index),
                tooltip='Specifies the line width for the plot. argument: linewidth',
                description='Line Width:',
                min=0.5,
                max=10,
                step = 0.1,
                layout={'width': '200px'},
                disabled=False
            ))

            style_rows.append(self.linewidth[-1])

            self.marker.append(ipywidgets.Text(
                value=self.get_series_value('marker', '', y_index),
                tooltip='Specifies the type of the marker to be used. argument: marker',
                description='Marker:',
                layout={'width': '200px'},
                disabled=False
            ))

            style_rows.append(self.marker[-1])

            self.markersize.append(ipywidgets.FloatText(
                value=self.get_series_value('markersize', 6, y_index),
                tooltip='Specifies the size of the marker.. argument: markersize',
                description='Marker Size:',
                layout={'width': '200px'},
                disabled=False
            ))

            style_rows.append(self.markersize[-1])

            rows.append(ipywidgets.HBox(style_rows))
            

            self.series_tabs.append(ipywidgets.VBox(rows))



    def create_format_tab(self):
        rows = []
        self.title = ipywidgets.Text(
            value=self.kwargs.get('title', ''),
            tooltip='Specifies the title for the Axis. argument: title',
            placeholder='Enter your chart title',
            description='Title:',   
            layout={'width': '800px'},
            disabled=False   
        )
        rows.append(self.title)

        self.heading = ipywidgets.Text(
            value=self.kwargs.get('heading', ''),
            tooltip='Specifies the heading for the plot. argument: heading',
            placeholder='Enter your chart heading',
            layout={'width': '800px'},
            description='Heading:',
            disabled=False   
        )
        rows.append(self.heading)

        self.xlabel = ipywidgets.Text(
            value=self.kwargs.get('xlabel', ''),
            tooltip='Specifies the label for x-axis. argument: xlabel',
            layout={'width': '800px'},
            description='X Label:',
            disabled=False   
        )
        rows.append(self.xlabel)

        self.ylabel = ipywidgets.Text(
            value=self.kwargs.get('ylabel', ''),
            tooltip='Specifies the label for y-axis. argument: ylabel',
            layout={'width': '800px'},
            description='Y Label:',
            disabled=False)  
        rows.append(self.ylabel)


        grid_rows = []
        self.grid_color = ipywidgets.Text(
            value=self.kwargs.get('grid_color', 'gray'),
            tooltip='Specifies the color of the grid. argument: grid_color',
            layout={'width': '200px'},
            description='Grid Color:',
            disabled=False   
        )
        grid_rows.append(self.grid_color)

        self.grid_format = ipywidgets.Text(
            value=self.kwargs.get('grid_format', ''),
            tooltip='Specifies the format for the grid. argument: grid_format',
            layout={'width': '200px'},
            description='Grid Format:',
            disabled=False   
        )
        grid_rows.append(self.grid_format)

        self.grid_linewidth = ipywidgets.BoundedFloatText(
            value=self.kwargs.get('grid_linewidth', 0.8),
            tooltip='Specifies the line width of the grid. argument: grid_linewidth',
            description='Grid Width:',
            layout={'width': '200px'},
            min=0.4,
            max=10,
            step = 0.1,
            disabled=False
        )
        grid_rows.append(self.grid_linewidth)

        self.grid_linestyle = ipywidgets.Dropdown(
                options=['-', '--', '-.', ":"],
                value=self.kwargs.get('grid_linestyle', '-'),
                tooltip='Specifies the line style of the grid. argument: grid_linestyle',
                layout={'width': '200px'},
                description='Grid Style:',
                disabled=False,
            )
        grid_rows.append(self.grid_linestyle)


        rows.append(ipywidgets.HBox(grid_rows))

        color_map_row = []
        self.cmap = ipywidgets.Text(
            value=self.kwargs.get('cmap', ''),
            tooltip='Specifies the name of the colormap to be used for plotting. argument: cmap',
            layout={'width': '200px'},
            description='Color Map:',
            disabled=False   
        )
        color_map_row.append(self.cmap)
        
        self.vmin = ipywidgets.FloatText(
                description='Min:', 
                value=self.kwargs.get('vmin', 0),
                tooltip='Specifies the lower range of the color map. argument: vmin',
                layout={'width': '200px'},
                disabled=False
            )
        color_map_row.append(self.vmin)

        self.vmax = ipywidgets.FloatText(
                description='Max:',
                value=self.kwargs.get('vmax', 0),
                tooltip='Specifies the upper range of the color map. argument: vmax',
                layout={'width': '200px'},
                disabled=False
            )
        color_map_row.append(self.vmax)
        
        rows.append(ipywidgets.HBox(color_map_row))

        legend_row = []
        self.legend = ipywidgets.Textarea(
            value=self.kwargs.get('legend', ''),
            tooltip='Specifies the legend(s) for the Plot. argument: legend',
            layout={'width': '400px'},
            description='Legend:',
            disabled=False   
        )
        legend_row.append(self.legend)

        self.legend_style = ipywidgets.Dropdown(
            options=['upper right', 'upper left', 'lower right', 'lower left', 'right', 'center left', 'center right', 'lower center', 'upper center', 'center'],
            value=self.kwargs.get('legend_style', 'upper right'),
            tooltip='Specifies the location for legend to display on Plot image. By default, legend is displayed at upper right corner. argument: legend_style',
            description='Placement:',
            layout={'width': '200px'},
            disabled=False,
        )
        legend_row.append(self.legend_style)


        self.width = ipywidgets.BoundedIntText(
            value=self.kwargs.get('width', 640),
            tooltip='Specifies the figure size width. argument: width',
            description='Width:',
            layout={'width': '200px'},
            min=640,
            max=1200,
            step = 1,
            disabled=False
        )
        legend_row.append(self.width)

        self.height = ipywidgets.BoundedIntText(
            value=self.kwargs.get('height', 480),
            tooltip='Specifies the figure size height. argument: height',
            description='Height:',
            layout={'width': '200px'},
            min=480,
            max=1200,
            step = 1,
            disabled=False
        )
        legend_row.append(self.height)


        rows.append(ipywidgets.HBox(legend_row))

        # Final UI is a vertical layout of all rows
        return ipywidgets.VBox(rows)

    def create_range_tab(self):
        rows = []

        x_axis = []
        self.xtick_format = ipywidgets.Text(
            value=self.kwargs.get('xticks', ''),
            tooltip='Specifies whether to format tick values for x-axis or not. argument: xticks',
            layout={'width': '400px'},
            description='X Ticks:',
            disabled=False   
        )
        x_axis.append(self.xtick_format)

        self.reverse_xaxis = ipywidgets.Checkbox(
            value=self.kwargs.get('reverse_xaxis', False),
            tooltip='Specifies whether to reverse tick values on x-axis or not. argument: reverse_xaxis',
            description='Reverse Ticks',
            disabled=False,
            indent=False
        )
        x_axis.append(self.reverse_xaxis)

        rows.append(ipywidgets.HBox(x_axis))


        x_axis_range = []
        self.xrange = ipywidgets.ToggleButton(
            value=self.kwargs.get('xrange', False),
            tooltip='Click if you want to change x-range. argument: xrange',
            description='Change X Range',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            layout={'width': '150px'},
        )
        self.xrange.observe(lambda x : self.update_range(), names='value')
        x_axis_range.append(self.xrange)

        self.xmin = ipywidgets.FloatText(
            value=self.kwargs.get('xmin', -100),
            tooltip='Specify minimum for x-range. argument: xmin',
            description='Min:',
            layout={'width': '200px'},
            disabled=True
        )
        x_axis_range.append(self.xmin)

        self.xmax = ipywidgets.FloatText(
            value=self.kwargs.get('xmax', 100),
            tooltip='Specify maximum for x-range. argument: xmax',
            description='Max:',
            layout={'width': '200px'},
            disabled=True
        )
        x_axis_range.append(self.xmax)

        rows.append(ipywidgets.HBox(x_axis_range))


        y_axis = []
        self.ytick_format = ipywidgets.Text(
            value=self.kwargs.get('yticks', ''),
            tooltip='Specifies whether to format tick values for y-axis or not. argument: yticks',
            layout={'width': '400px'},
            description='Y Ticks:',
            disabled=False   
        )
        y_axis.append(self.ytick_format)
        self.reverse_yaxis = ipywidgets.Checkbox(
            value=self.kwargs.get('reverse_yaxis', False),
            tooltip='Specifies whether to reverse tick values on y-axis or not. argument: reverse_yaxis',
            description='Reverse Ticks',
            disabled=False,
            indent=False
        )
        y_axis.append(self.reverse_yaxis)

        rows.append(ipywidgets.HBox(y_axis))


        y_axis_range = []
        self.yrange = ipywidgets.ToggleButton(
            value=self.kwargs.get('yrange', False),
            tooltip='Click if you want to change y-range. argument: yrange',
            description='Change Y Range',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            layout={'width': '150px'},
        )
        self.yrange.observe(lambda x : self.update_range(), names='value')
        y_axis_range.append(self.yrange)
        self.ymin = ipywidgets.FloatText(
            value=self.kwargs.get('ymin', -100),
            tooltip='Specify minimum for y-range. argument: ymin',
            description='Min:',
            layout={'width': '200px'},
            disabled=True
        )
        y_axis_range.append(self.ymin)
        self.ymax = ipywidgets.FloatText(
            value=self.kwargs.get('ymax', 100),
            tooltip='Specify maximum for x-range. argument: ymax',
            description='Max:',
            layout={'width': '200px'},
            disabled=True
        )
        y_axis_range.append(self.ymax)
        rows.append(ipywidgets.HBox(y_axis_range))

        return ipywidgets.VBox(rows)

    def open_ui(self):
        if self.df == None and self.database_table_name == "":
            self.widget_output.clear_output(wait=True)
            with self.widget_output:
                print("You are logged in")
            return
        try:
            if self.df == None:
                df = DataFrame(self.database_table_name)
                self.df = df
            else:
                df = self.df
        except:
            self.on_logout(True)
            with self.widget_output:
                print("Error cannot load table", self.database_table_name)
            return
        self.plot_map["Line"] = LinePlot(self, df)
        self.plot_map["Bar"] = BarPlot(self, df)
        self.plot_map["Scatter"] = ScatterPlot(self, df)
        self.plot_map["Corr"] = CorrPlot(self, df)
        self.plot_map["Wiggle"] = WigglePlot(self, df)
        self.plot_map["Mesh"] = MeshPlot(self, df)
        self.plot_map["Geom"] = GeomPlot(self, df)
        self.widget_output.clear_output(wait=True)
        self.create_ui()


    def create_ui(self):

        self.plot_menu = ipywidgets.Dropdown(
            options=self.plot_map.keys(),
            value=self.current_plot,
            description='Chart Type:',
            disabled=False)
        self.plot_menu.observe(lambda x : self.change_plot(), names='value')
        
        self.plot_button = ipywidgets.Button(
            description='Plot',
            disabled=False,
            button_style='success',
            tooltip='Create Plot',
        )
        self.plot_button.on_click(lambda x : self.do_plot())
        self.logout_button = ipywidgets.Button(
            description='Logout',
            disabled=False,
            tooltip='Log out of connection',
        )
        self.logout_button.on_click(lambda x : self.on_logout(x))

        self.top_row = ipywidgets.HBox([self.plot_menu, self.plot_button, self.logout_button])

        self.contents = self.get_current_plot().get_ui()
        self.image = ipywidgets.Image(format='png')
        # Hide it by Default
        self.image.layout.visibility = "hidden"
        # base ui
        self.format_tab = self.create_format_tab()
        self.range_tab = self.create_range_tab()
        self.create_series_tabs()
        self.create_tab()

    def create_tab(self):
        self.tab = ipywidgets.Tab()
        children = [self.contents, self.format_tab, self.range_tab]
        titles = ['Chart', 'Format', 'Range']
        for y_index in range(self.get_num_series_visible()):
            children.append(self.series_tabs[y_index])
            titles.append('Series[{}]'.format(y_index))
        self.tab.children = children
        for index in range(len(titles)):
            self.tab.set_title(title=titles[index], index=index)
        
        self.plot_ui = ipywidgets.VBox([self.top_row, self.tab, self.image])
        self.show_display(self.plot_ui, False)
    
