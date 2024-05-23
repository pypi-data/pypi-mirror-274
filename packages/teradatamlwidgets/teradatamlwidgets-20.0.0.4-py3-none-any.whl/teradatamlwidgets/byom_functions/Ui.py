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
from teradatamlwidgets.analytic_functions.teradata_notebook_impl import NotebookUiImpl
from teradatamlwidgets.connection_teradataml import Connection
import ipywidgets as widgets
from IPython.display import clear_output, HTML,Javascript, display
import teradataml
from teradataml import get_connection, DataFrame
from teradataml import save_byom, retrieve_byom, load_example_data
from teradataml import configure, display_analytic_functions, execute_sql
from teradataml import DataRobotPredict


class DataRobotPredictUi:
    
    def __init__(self):
        self.connection = Connection()

        self.widget_output = widgets.Output()
        self.main_panel = widgets.HBox([])
        display(self.main_panel, self.widget_output)
        
                
        self.byom_install_location = widgets.Text(
            value='',
            placeholder='Type BYOM install location.',
            description='BYOM Install:',
            layout={'width': '600px'},
            disabled=False   
        )

        self.newdata = widgets.Text(
            value='',
            placeholder='Type the input teradataml DataFrame that contains the data to be scored.',
            description='newdata:',
            layout={'width': '600px'},
            disabled=False   
        )
        self.newdata.observe(lambda x : self.on_newdata_changed(x), names='value')

        self.modeldata_id = widgets.Text(
            value='',
            placeholder='Type the model id to be used for scoring.',
            description='modeldata:',
            layout={'width': '600px'},
            disabled=False   
        )
        self.modeldata_table_name = widgets.Text(
            value='',
            placeholder='Type the model table name to be used for scoring.',
            description='modeldata:',
            layout={'width': '600px'},
            disabled=False   
        )

        columns = []
        self.accumulate = widgets.SelectMultiple(
            options=[''],
            value=[''],
            description='Accumulate:',
            disabled=False
        )
        columns.append(self.accumulate)

        self.model_output_fields = widgets.SelectMultiple(
            options= [''],
            value=[''],
            description='Model Output:',
            disabled=False,
        )
        columns.append(self.model_output_fields)

        self.overwrite_cached_models = widgets.Dropdown(
            options=['', 'true', 'false', '*', 'current_cached_model'],
            value='',
            description='Overwrite:',
            disabled=False,
        )

        generic_arguments = []

        self.is_debug = widgets.Checkbox(
            value=False,
            description='Debug',
            disabled=False,
            layout={'width': '200px'},
            indent=True
        )
        generic_arguments.append(self.is_debug)

        self.persist = widgets.Checkbox(
            value=False,
            description='Persist',
            disabled=False,
            layout={'width': '200px'},
            indent=True
        )
        generic_arguments.append(self.persist)

        self.volatile = widgets.Checkbox(
            value=False,
            description='Volatile',
            disabled=False,
            layout={'width': '200px'},
            indent=True
        )
        generic_arguments.append(self.volatile)

        columns_row = widgets.HBox(columns)

        generic_arguments_row = widgets.HBox(generic_arguments)
        self.execute = widgets.Button(description="Execute")
        self.execute.on_click(lambda x : self.on_execute(x))
        
        self.function_ui = widgets.VBox([self.byom_install_location, self.newdata, self.modeldata_id, self.modeldata_table_name, columns_row, self.overwrite_cached_models, generic_arguments_row, self.execute])

        self.show_display(self.function_ui, True)

        
    def on_newdata_changed(self, widget):
        try:
            columns = self.connection.get_columns_of_dataset(self.newdata.value)
            self.accumulate.options = [''] + columns
            self.model_output_fields.options = [''] + columns
            
        except:
            pass
        
    def on_execute(self, widget):
        if not self.modeldata_id.value or not self.modeldata_table_name.value:
            self.show_dialog("Error: You need to specify the modeldata")
            return
        if not self.byom_install_location.value:
            self.show_dialog("Error: You need to specify the BYOM Install")
            return
        
        try:
            configure.byom_install_location = self.byom_install_location.value
            modeldata = retrieve_byom(self.modeldata_id.value, table_name=self.modeldata_table_name.value)

            self.output_dataframe = DataRobotPredict(newdata=DataFrame(self.newdata.value),
                                                  modeldata=modeldata,
                                                  accumulate=list(self.accumulate.value),
                                                  model_output_fields = list(self.model_output_fields.value) if self.model_output_fields.value else None,
                                                  overwrite_cached_models=self.overwrite_cached_models.value).result
            
            markup = self.output_dataframe.to_pandas().head().to_html().replace("\n", ' ')
            self.show_dialog(markup)
            
        except Exception as e:
            self.show_dialog(str(e))

    def show_display(self, item, clear=True):
        if clear:
            self.widget_output.clear_output(wait=True)
        with self.widget_output:
            display(item)
            
    def show_dialog(self, html):
        html = widgets.HTML(value=html)
        close_button = widgets.Button(description="Close")
        close_button.on_click(lambda x : self.show_display(self.function_ui, True))
        container = widgets.VBox([html, close_button])
        self.show_display(container, True)
        


