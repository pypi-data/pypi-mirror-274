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
from teradatamlwidgets.teradata_analytic_lib.data_transformation import *
from teradatamlwidgets.teradata_analytic_lib.open_ended_query_generator import OpenEndedQueryGenerator
import ipywidgets as widgets
from IPython.display import clear_output, HTML,Javascript, display
from teradatamlwidgets.teradata_analytic_lib.verifyTableColumns import *
from teradatamlwidgets.teradata_analytic_lib.valib_executor import *
from teradatamlwidgets.teradata_analytic_lib.vantage_version import *
import pandas as pd
from teradatamlwidgets.my_tags_input import *
from teradatamlwidgets.connection import *
from teradatamlwidgets.teradata_analytic_lib.uaf_json_converter import * 
import teradataml
from teradataml.analytics.json_parser.utils import func_type_json_version
from teradataml.common.constants import TeradataAnalyticFunctionInfo
from teradataml.common.utils import UtilFuncs
from teradataml.common.constants import TeradataConstants

def isValidFloat(x):
    try:
        f = float(x)
        return True
    except:
        return False

def isValidInteger(x):
    try:
        i = int(x)
        return True
    except:
        return False

show_native_dialog = True # "linux" in sys.platform.lower()


# Internal class
class NotebookUiImpl:
    uiname_to_databyname = {"None" : "None", "Partition": "PartitionByKey", "Hash" : "HashByKey", "Dimension" : "Dimension"}
    databyname_to_uiname = {"None" : "None", "PartitionByKey": "Partition", "HashByKey" : "Hash", "Dimension" : "Dimension"}
    login_info = {}
    
    def __init__(self, connection, outputs, function="", inputs=[], filename=""):

        self.widget_output = widgets.Output()
        self.main_panel = widgets.HBox([])
        display(self.main_panel, self.widget_output)

        ipywidgets_version = widgets.__version__.split(".")
        ipywidgets_version = int(ipywidgets_version[0])*100 + int(ipywidgets_version[1])*10 + int(ipywidgets_version[2])
        NotebookUiImpl.tag_widget_available = ipywidgets_version >= 804
        NotebookUiImpl.TagsInput = MyTagsInput if not NotebookUiImpl.tag_widget_available else widgets.TagsInput

        # If old version then it won't have combobox
        if not hasattr(widgets, "Combobox") or not NotebookUiImpl.tag_widget_available:
            widgets.Combobox = widgets.Dropdown

        # input can be either table name or teradata dataframe
        inputs_table_names = []
        for input in inputs:
            if type(input) == str:
                inputs_table_names.append(input)
            elif type(input) == teradataml.dataframe.dataframe.DataFrame:
                inputs_table_names.append(input._table_name.strip('"'))
        inputs = inputs_table_names

        # Output processing
        if len(outputs) == 0:
            new_table_name = UtilFuncs._generate_temp_table_name(table_type = TeradataConstants.TERADATA_TABLE)
            outputs.append(new_table_name)

        self.function = function
        self.connection = connection
        self.inputs = inputs
        self.outputs = outputs
        self.df = None
        self.login_ui = None
        self.function_ui = None
        self.login_info = {}
        self.filename = filename
        self.folder = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))

        # Load a progress bar when stuff is slow and we need to indicate to user to wait
        with open(os.path.join(self.folder, "progress.gif"), 'rb') as f:
            img = f.read()
        self.loading_bar = widgets.Image(value=img)


        if self.connection.is_logged_in():
            self.login_info['default_db'] = self.connection.get_connection_setting(inputs[0], 'default_db')
            self.login_info['val_location'] = self.connection.get_connection_setting(inputs[0], 'val_location')
            self.open_function_ui()
        else:
            self.login_info['default_db'] = "dssDB"
            self.login_info['val_location'] = "VAL"
            self.create_login_ui()
            # If login was previously a succes then just log in again
            if len(NotebookUiImpl.login_info)>0:
                try:
                    self.login_info = NotebookUiImpl.login_info.copy()
                    self.on_login(self.login)
                except Exception as e:
                    with self.widget_output:
                        print(str(e))
                    pass

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


    def create_login_ui(self):
        self.show_display(self.loading_bar)

        teradata_environment = json.loads(os.environ.get("TERADATA_DEFAULT", "{}"))

        self.host = widgets.Text(
            value= self.login_info.get('host', teradata_environment.get("host", "")),
            placeholder='Enter host URL',
            description='Host:',
        )
        self.username = widgets.Text(
            value= self.login_info.get('username', teradata_environment.get("user", "")),
            placeholder='Enter username',
            description='Username:',
            disabled=False
        )
        self.password = widgets.Password(
            value=self.login_info.get('password', teradata_environment.get("password", "")),
            placeholder='Enter password',
            description='Password:',
            disabled=False
        )
        self.default_db = widgets.Text(
            value=self.login_info.get('default_db', teradata_environment.get("defaultDB", "")),
            placeholder='Enter default database',
            description='Schema:',
            disabled=False
        )
        self.val_loc = widgets.Text(
            value=self.login_info.get('val_location', teradata_environment.get("VAL_LOCATION", "VAL")),
            placeholder='Enter VAL location',
            description='VALIB:',
            disabled=False
        )

        self.login = widgets.Button(description="Login")
        self.login.on_click(lambda x : self.on_login(x))

        self.login_ui = widgets.HBox([widgets.VBox([self.host,self.username,self.password,self.default_db,self.val_loc]), self.login])
        self.show_display(self.login_ui, True)

        
    def on_login(self, b):

        try:
            self.show_display(self.loading_bar)
            self.login_info['host'] = self.host.value
            self.login_info['username'] = self.username.value
            self.login_info['password'] = self.password.value
            self.login_info['default_db'] = self.default_db.value
            self.login_info['val_location'] = self.val_loc.value

            self.connection.login(self.login_info['host'], self.login_info['username'], self.login_info['password'], self.login_info['default_db'], self.login_info['val_location'])
            if not self.connection.is_logged_in():
                return
            self.open_function_ui()
            # Copy last succesful login
            NotebookUiImpl.login_info = self.login_info.copy()
        except Exception as e:
            with self.widget_output:
                print(str(e))


    def get_function_json_path(self, function_category, version):  
        if function_category == "VAL":
           return os.path.join(self.folder, function_category) 
        if function_category == "SQLE" or function_category == "UAF":
           func_type = TeradataAnalyticFunctionInfo.FASTPATH if function_category == "SQLE" else TeradataAnalyticFunctionInfo.UAF
           directory = UtilFuncs._get_data_directory(dir_name="jsons", func_type=func_type)
           path = os.path.join(directory, version) 
           # Check if path exists
           if os.path.exists(path):
                return path
           else:
                # Path doesnt exist so maybe the version doesnt exist so lets try 17.20
                path = os.path.join(directory, "17.20")
                return path 


    def open_function_ui(self):
        self.version = get_vantage_version(  self.connection  )
        self.functions = []
        self.functionJsonFilePaths = {}
        self.function_types = {"SQLE" : [], "VAL" : [], "UAF" : []}
        self.search_json_directory("SQLE")
        self.search_json_directory("VAL")
        self.search_json_directory("UAF")
        self.functions.sort()
        self.functions = [""] + self.functions
        self.create_function_ui()
        if self.filename:
            # When UI first comes up load the user settings JSON if it was provided
            self.on_load(None)

    def search_json_directory(self, function_category):
        try:
            directory_path = self.get_function_json_path(function_category, self.version) 
            directory = os.listdir(directory_path)
            for filename in directory:
                json_file_path = os.path.join(directory_path, filename)
                if not os.path.isfile(json_file_path):
                    continue
                if not json_file_path.endswith(".json"):
                    continue
                name = filename.replace(".json", "")
                self.functions.append(name)
                self.functionJsonFilePaths[name] = json_file_path   
                self.function_types[function_category].append(name)
        except Exception as e:
            with self.widget_output:
                print(e)
            pass


    def on_keyword_changed(self, changed):
        # Combobox needs to be recreated as you cannot dynamically change the options for it
        current_func = self.current_function.value
        self.function_toolbar.children = []
        self.current_function.close()
        self.current_function = widgets.Combobox(
            placeholder='Select a function ...',
            options=self.functions,
            description='Function:',
            ensure_option=True,
            disabled=False,
            layout = {'width': '90%'}
        )  
        self.current_function.value = current_func
        available_functions = []
        if self.keyword['SQLE'].value:
            available_functions.extend(self.function_types["SQLE"])
        if self.keyword['VAL'].value:
            available_functions.extend(self.function_types["VAL"])
        if self.keyword['UAF'].value:
            available_functions.extend(self.function_types["UAF"])
        available_functions.sort()
        self.current_function.options = available_functions
        self.function_toolbar.children = [self.current_function, self.keyword['SQLE'] , self.keyword['VAL'], self.keyword['UAF']]
        self.current_function.observe(lambda x : self.on_current_function(x), names='value')
        

    def create_function_ui(self):
        self.show_display(self.loading_bar, True)

        self.config_json = None
        if self.function_ui:
            self.function_ui.close()
        self.current_function = widgets.Combobox(
            placeholder='Select a function ...',
            options=self.functions,
            ensure_option=True,
            disabled=False,
            layout = {'width': '90%'}
        )  
        self.current_function.observe(lambda x : self.on_current_function(x), names='value')

        self.keyword = {}
        self.keyword['SQLE'] = widgets.Checkbox(value=True, description='Analytics Database')
        self.keyword['SQLE'].observe(lambda x : self.on_keyword_changed(x), names='value')
        self.keyword['VAL'] = widgets.Checkbox(value=True, description='VAL')
        self.keyword['VAL'].observe(lambda x : self.on_keyword_changed(x), names='value')
        self.keyword['UAF'] = widgets.Checkbox(value=True, description='UAF Time Series')
        self.keyword['UAF'].observe(lambda x : self.on_keyword_changed(x), names='value')
        
        
        self.execute = widgets.Button(description="Execute")
        self.execute.on_click(lambda x : self.on_execute(x))

        self.query = widgets.Button(description="Query")
        self.query.on_click(lambda x : self.on_query(x))

        self.reset = widgets.Button(description="Reset")
        self.reset.on_click(lambda x : self.on_reset(x))

        self.main_toolbar = [self.execute, self.query, self.reset]

        if self.filename:
            self.load = widgets.Button(description="Load")
            self.load.on_click(lambda x : self.on_load(x))
            self.main_toolbar.append(self.load)

            self.save = widgets.Button(description="Save")
            self.save.on_click(lambda x : self.on_save(x))
            self.main_toolbar.append(self.save)

        if self.connection.can_log_out():
            self.logout = widgets.Button(description="Log Out")
            self.logout.on_click(lambda x : self.on_logout(x))
            self.main_toolbar.append(self.logout)
 
        self.function_description  = widgets.HTML(value= '<style>p{word-wrap: break-word; max-height:200px}</style> <p></p>')

        self.tabs = widgets.Tab()
        self.tabs.children = []
        
        self.function_toolbar = widgets.HBox([self.current_function, self.keyword['SQLE'] , self.keyword['VAL'], self.keyword['UAF'] ])

        self.function_ui = widgets.VBox([
            widgets.HBox(self.main_toolbar),
            self.function_toolbar,
            self.function_description,
            self.tabs
            ])

        self.show_display(self.function_ui, True)

        self.current_function.value = self.function
        
    
    def on_logout(self, b):
        # Clear the global login info
        NotebookUiImpl.login_info = {}
        self.connection.logout()
        self.create_login_ui()
    
    def on_current_function(self, change):
        self.change_function()

    def change_function(self, file_settings_json = {}):
        if self.current_function.value == "":
            return

        self.show_display(self.loading_bar, False)

        json_file_name = self.functionJsonFilePaths[self.current_function.value]
        with open(json_file_name, 'r') as file:
            data = file.read()

        self.in_db_json = json.loads(data)
             
        # If this is UAF then we need to convert to IN DB format
        if "function_type" not in self.in_db_json:
            self.in_db_json = uaf_to_indb(self.in_db_json)

        self.config_json = {}
        input_table_names = self.connection.get_dataset_name(self.inputs)
        self.config_json['function'] = load_json(self.in_db_json, input_table_names)
        # Load any user changes they saved last time
        if file_settings_json:
            self.load_user_json_settings(file_settings_json)

        self.config_json['function']['inputschemas'] = {}
        # Keep association of parameters that are columns to the tables they represent
        input_index = 0
        input_table_map = {}
        for input in self.config_json["function"]["required_input"]:
            # Making lowercase as JSONs sometimes have mistakes
            name = input['name'].lower()
            input_table_map[name] = input_index
            if len(input.get("alternateNames", []))>0:
                for alternative_name in input["alternateNames"]:
                    input_table_map[alternative_name.lower()] = input_index
            input["column_param_ui"] = []
        for arg in self.config_json["function"]["arguments"]:
            datatype = arg['datatype']
            if datatype == "COLUMNS":
                target_table = arg["targetTable"][0].lower()
                arg['target_input_index'] = input_table_map[target_table]
       

        self.function_description.value = '<style>p{max-width: 100%; overflow-y:scroll; max-height:150px;}</style> <p>'+self.in_db_json['long_description']+'</p>'

        self.param_widgets = {}
        self.table_widgets = {}
        required_ui = self.create_param_ui(required=True)
        optional_ui = self.create_param_ui(required=False)

        # Update the table and columns controls
        for input in self.config_json["function"]["required_input"]:
            self.update_input_tables(input)
            self.update_input_columns(input)

        self.tabs.children = [required_ui, optional_ui]
        self.tabs.set_title(index=0,title="Required")
        self.tabs.set_title(index=1,title="Optional")

        self.show_display(self.function_ui)

    
    def on_value_changed(self, change):
        input = change['owner'].json
        input['value'] = change['owner'].value

    def on_table_changed(self, change):
        table_name = change['owner'].value
        input = change['owner'].json
        input['value'] = table_name
        self.update_input_columns(input)


    def on_data_partition_option_changed(self, change):
        input = change['owner'].json
        input['kind'] = NotebookUiImpl.uiname_to_databyname[change['owner'].value]
        input['partion_hash_ui'].layout.display = "none" if input['kind'] == "None" else "inline"
    
    def on_data_by_changed(self, change):
        value = change['owner'].value
        change['owner'].json['partitionAttributes'] = value
    
    def on_order_by_changed(self, change):
        columns = change['owner'].value
        column_direction = change['owner'].direction
        change['owner'].json['orderByColumn'] = columns
        change['owner'].json['orderByColumnDirection'] = column_direction

    def update_input_tables(self, input):

        # Fix bug where if we change options then the value gets lost
        # So first we keep copy of current value
        original_value = input['table_ui'].value
        # Then we update options
        input['table_ui'].options = self.connection.get_dataset_name(self.inputs)
        # Then we reset back the table value
        try:
            input['table_ui'].value = original_value
        except:
            pass

    def update_columns(self, control, dataset_name):
        columns = self.connection.get_columns_of_dataset(dataset_name)
        if hasattr(control, 'allowed_tags'):
            control.allowed_tags = columns.copy()
        if hasattr(control, 'set_allowed_tags'):
            control.set_allowed_tags(columns.copy())
        if hasattr(control, 'options'):
            # Fix bug where if we change options then the value gets lost
            # So first we keep copy of current value
            original_value = control.value
            # Then we update options
            control.options = columns.copy()
            # Then we reset back the table value
            try:
                control.value = original_value
            except:
                pass

    def update_input_columns(self, input):
        dataset_name = input.get('value','')
        if "data_by_ui" in input:
            self.update_columns(input['data_by_ui'], dataset_name)
        if "order_by_ui" in input:
            self.update_columns(input['order_by_ui'], dataset_name)
        # update associated parameters that represent this table
        for column_param_ui in input["column_param_ui"]:
            self.update_columns(column_param_ui, dataset_name)

    def create_partition_hash_by_ui(self, input, input_items):
        options = ['None', 'Partition', 'Hash']
        if 'Dimension' in input['inputKindChoices']:
            options.append('Dimension')
        data_partition_option = widgets.Dropdown(description="Data Partition Option", options=options, style=dict(description_width='150px'), layout={'width': '90%'})
        data_partition_option.json = input
        data_partition_option.value = NotebookUiImpl.databyname_to_uiname.get(input['kind'], "None")
        data_partition_option.observe(lambda x : self.on_data_partition_option_changed(x), names='value')
        
        partition_value = input['partitionAttributes']
        input['data_by_ui'] = MyTagsInput(value=partition_value, allow_duplicates=False, style=dict(description_width='150px'), layout={'width': '400px'})
        input['data_by_ui'].json = input
        input['data_by_ui'].observe(lambda x : self.on_data_by_changed(x), names='value')
        
        order_by_values = []
        direction_values = []
        for i in range(len(input['orderByColumn'])):
            direction = "ASC"
            if 'orderByColumnDirection' in input and i < len(input['orderByColumnDirection']):
                direction = input['orderByColumnDirection'][i]
            direction_values.append(direction)
            order_by_values.append(input['orderByColumn'][i])   
        input['order_by_ui'] = MyTagsInput(value=order_by_values, allow_duplicates=False, style=dict(description_width='150px'), layout={'width': '600px'}, has_direction=True, direction=direction_values)
        input['order_by_ui'].json = input
        input['order_by_ui'].observe(lambda x : self.on_order_by_changed(x), names='value')
        
        input['partion_hash_ui'] = widgets.VBox([widgets.Label("Data By"), input['data_by_ui'] , widgets.Label("Order By"), input['order_by_ui'] ])
        input['partion_hash_ui'].layout.display = "none" if input['kind'] == "None" else "inline"
        input_items.append(widgets.VBox([data_partition_option, widgets.HBox([widgets.Label("", layout={'width': '150px'}), input['partion_hash_ui'] ])]))
        
    def set_uaf_visibility(self, input):
        input_uaf = input["uaf_ui"]
        uaf_type = input_uaf['uaf_type'].value

        input_uaf['is_row_sequence'].layout.display = "inline" if uaf_type!='ART' and uaf_type!='GENSERIES' and uaf_type!='' else "none"
        input_uaf['row_axis_name'].layout.display = "inline" if uaf_type!='ART' and uaf_type!='GENSERIES' and uaf_type!='' else "none"
    
        input_uaf['is_col_sequence'].layout.display = "inline" if uaf_type=='MATRIX' else "none"
        input_uaf['column_axis_name'].layout.display = "inline" if uaf_type=='MATRIX' else "none"
    
        input_uaf['id_name'].layout.display = "inline" if uaf_type!='ART' and uaf_type!='GENSERIES' and uaf_type!='' else "none"
        input_uaf['id_sequence'].layout.display = "inline" if uaf_type!='GENSERIES' and uaf_type!='' else "none"

        input_uaf['payload_fields'].layout.display = "inline" if uaf_type!='ART' and uaf_type!='GENSERIES' and uaf_type!='' else "none"
        input_uaf['payload_content'].layout.display = "inline" if uaf_type!='ART' and uaf_type!='GENSERIES' and uaf_type!='' else "none"
        
        input_uaf['payload_start_value'].layout.display = "inline" if uaf_type=='GENSERIES' else "none"
        input_uaf['payload_offset_value'].layout.display = "inline" if uaf_type=='GENSERIES' else "none"
        input_uaf['payload_num_entries'].layout.display = "inline" if uaf_type=='GENSERIES' else "none"
    
        input_uaf['layer'].layout.display = "inline" if uaf_type!='GENSERIES' and uaf_type!='' else "none"

        input_uaf['time_duration'].layout.display = "inline" if uaf_type=='SERIES' else "none"
        input_uaf['time_type'].layout.display = "inline" if uaf_type=='SERIES' else "none"
        input_uaf['time_zero'].layout.display = "inline" if uaf_type=='SERIES' else "none"
        input_uaf['seq_zero'].layout.display = "inline" if uaf_type=='SERIES' else "none"

        input_uaf['where'].layout.display = "inline" if uaf_type!='GENSERIES' and uaf_type!='' else "none"

        


    def on_uaf_type_changed(self, change):
        input = change['owner'].json
        input["uafType"] = change['owner'].value
        self.set_uaf_visibility(input)
    def on_is_row_sequence_changed(self, change):
        input = change['owner'].json
        input["uaf"]['is_row_sequence'] = change['owner'].value
    def on_uaf_property_changed(self, param_name, change, split = False):
        input = change['owner'].json
        input["uaf"][param_name] = change['owner'].value.split(" ") if split else change['owner'].value

    def create_uaf_ui(self, input, input_items):
        items = []

        options = ['']
        if 'SERIES' in input['uaf']['requiredUafKind']:
            options.append('SERIES')
        if 'MATRIX' in input['uaf']['requiredUafKind']:
            options.append('MATRIX')
        if 'ART' in input['uaf']['requiredUafKind']:
            options.append('ART')
        if 'GENSERIES' in input['uaf']['requiredUafKind']:
            options.append('GENSERIES')
        
        input_uaf = {}
        input["uaf_ui"] = input_uaf
        input_uaf = input["uaf_ui"]

        #print('row_axis_name=', input['uaf']['row_axis_name'])
        
        param_name = 'uaf_type'
        input_uaf[param_name] = widgets.Dropdown(description="UAF Type", options=options, style=dict(description_width='150px'), layout={'width': '90%'})
        input_uaf[param_name].json = input
        input_uaf[param_name].value = input.get('uafType', '')
        input_uaf[param_name].observe(lambda x : self.on_uaf_type_changed(x), names='value')
        items.append(input_uaf[param_name])

        param_name = 'is_row_sequence'
        input_uaf[param_name] = widgets.Dropdown(description="Row", options=["TIMECODE", "SEQUENCE"], style=dict(description_width='150px'), layout={'width': '90%'})
        input_uaf[param_name].json = input
        input_uaf[param_name].value = input['uaf'][param_name]
        input_uaf[param_name].observe(lambda x : self.on_is_row_sequence_changed(x), names='value')
        items.append(input_uaf[param_name])

        param_name = 'row_axis_name'
        input_uaf[param_name] = widgets.Text(description="Row Axis Name", style=dict(description_width='150px'), layout={'width': '90%'})
        input_uaf[param_name].json = input
        input_uaf[param_name].value = input['uaf'][param_name]
        input_uaf[param_name].observe(lambda x : self.on_uaf_property_changed('row_axis_name', x), names='value')
        items.append(input_uaf[param_name])

        param_name = 'is_col_sequence'
        input_uaf[param_name] = widgets.Dropdown(description="Column", options=["TIMECODE", "SEQUENCE"], style=dict(description_width='150px'), layout={'width': '90%'})
        input_uaf[param_name].json = input
        input_uaf[param_name].value = input['uaf'][param_name]
        input_uaf[param_name].observe(lambda x : self.on_uaf_property_changed('is_col_sequence', x), names='value')
        items.append(input_uaf[param_name])

        param_name = 'column_axis_name'
        input_uaf[param_name] = widgets.Text(description="Column Axis Name", style=dict(description_width='150px'), layout={'width': '90%'})
        input_uaf[param_name].json = input
        input_uaf[param_name].value = input['uaf'][param_name]
        input_uaf[param_name].observe(lambda x : self.on_uaf_property_changed('column_axis_name', x), names='value')
        items.append(input_uaf[param_name])

        #items.append(widgets.Label("ID"))
        param_name = 'id_name'
        #value = input['uaf'][param_name]
        input_uaf[param_name] = widgets.Textarea(description= "ID", style=dict(description_width='150px'), layout={'width': '90%'})

        
        input_uaf[param_name].json = input
        input_uaf[param_name].value = " ".join(input['uaf'][param_name])
        #if type(value) == str:
        #    if value == "":
        #        value = []
        #    else:
        #        value = [value]
        #input_uaf[param_name].value = value
        input_uaf[param_name].observe(lambda x : self.on_uaf_property_changed('id_name', x, True), names='value')
        items.append(input_uaf[param_name])

        param_name = 'id_sequence'
        input_uaf[param_name] = widgets.Textarea(description="Sequence", style=dict(description_width='150px'), layout={'width': '90%'})
        input_uaf[param_name].json = input
        input_uaf[param_name].value = " ".join(input['uaf'][param_name])
        input_uaf[param_name].observe(lambda x : self.on_uaf_property_changed('id_sequence', x, True), names='value')
        items.append(input_uaf[param_name])

        param_name = 'payload_fields'
        input_uaf[param_name] = widgets.Textarea(description="Payload Fields", style=dict(description_width='150px'), layout={'width': '90%'})
        input_uaf[param_name].json = input
        input_uaf[param_name].value = " ".join(input['uaf'][param_name])
        input_uaf[param_name].observe(lambda x : self.on_uaf_property_changed('payload_fields', x, True), names='value')
        items.append(input_uaf[param_name])

        param_name = 'payload_content'
        options = ["", "REAL", "COMPLEX", "AMPL_PHASE", "AMPL_PHASE_RADIANS", "AMPL_PHASE_DEGREES", "MULTIVAR_REAL", "MULTIVAR_COMPLEX", "MULTIVAR_ANYTYPE", "MULTIVAR_AMPL_PHASE", "MULTIVAR_AMPL_PHASE_RADIANS", "MULTIVAR_AMPL_PHASE_DEGREES"]
        input_uaf[param_name] = widgets.Dropdown(description="Payload Content", options=options, style=dict(description_width='150px'), layout={'width': '90%'})
        input_uaf[param_name].json = input
        input_uaf[param_name].value = input['uaf'][param_name]
        input_uaf[param_name].observe(lambda x : self.on_uaf_property_changed('payload_content', x), names='value')
        items.append(input_uaf[param_name])

        param_name = 'payload_start_value'
        input_uaf[param_name] = widgets.Text(description="Payload Start", style=dict(description_width='150px'), layout={'width': '90%'})
        input_uaf[param_name].json = input
        input_uaf[param_name].value = input['uaf'][param_name]
        input_uaf[param_name].observe(lambda x : self.on_uaf_property_changed('payload_start_value', x), names='value')
        items.append(input_uaf[param_name])

        param_name = 'payload_offset_value'
        input_uaf[param_name] = widgets.Text(description="Payload Offset", style=dict(description_width='150px'), layout={'width': '90%'})
        input_uaf[param_name].json = input
        input_uaf[param_name].value = input['uaf'][param_name]
        input_uaf[param_name].observe(lambda x : self.on_uaf_property_changed('payload_offset_value', x), names='value')
        items.append(input_uaf[param_name])

        param_name = 'payload_num_entries'
        input_uaf[param_name] = widgets.Text(description="Payload #Entries", style=dict(description_width='150px'), layout={'width': '90%'})
        input_uaf[param_name].json = input
        input_uaf[param_name].value = input['uaf'][param_name]
        input_uaf[param_name].observe(lambda x : self.on_uaf_property_changed('payload_num_entries', x), names='value')
        items.append(input_uaf[param_name])

        param_name = 'layer'
        input_uaf[param_name] = widgets.Text(description="Layer", style=dict(description_width='150px'), layout={'width': '90%'})
        input_uaf[param_name].json = input
        input_uaf[param_name].value = input['uaf'][param_name]
        input_uaf[param_name].observe(lambda x : self.on_uaf_property_changed('layer', x), names='value')
        items.append(input_uaf[param_name])

        param_name = 'time_duration'
        options = ["", "CAL_YEARS", "CAL_MONTHS", "CAL_DAYS", "WEEKS", "DAYS", "HOURS", "MINUTES", "SECONDS", "MILLISECONDS", "MICROSECONDS"]
        input_uaf[param_name] = widgets.Dropdown(description="Interval", options=options, style=dict(description_width='150px'), layout={'width': '90%'})
        input_uaf[param_name].json = input
        input_uaf[param_name].value = input['uaf'][param_name]
        input_uaf[param_name].observe(lambda x : self.on_uaf_property_changed('time_duration', x), names='value')
        items.append(input_uaf[param_name])

        param_name = 'time_type'
        options = ["", "float", "integer"]
        input_uaf[param_name] = widgets.Dropdown(description="Interval Type", options=options, style=dict(description_width='150px'), layout={'width': '90%'})
        input_uaf[param_name].json = input
        input_uaf[param_name].value = input['uaf'][param_name]
        input_uaf[param_name].observe(lambda x : self.on_uaf_property_changed('time_type', x), names='value')
        items.append(input_uaf[param_name])

        param_name = 'time_zero'
        options = ["", "DATE", "TIMESTAMP", "TIMESTAMP WITH TIME ZONE"]
        input_uaf[param_name] = widgets.Dropdown(description="Zero", options=options, style=dict(description_width='150px'), layout={'width': '90%'})
        input_uaf[param_name].json = input
        input_uaf[param_name].value = input['uaf'][param_name]
        input_uaf[param_name].observe(lambda x : self.on_uaf_property_changed('time_zero', x), names='value')
        items.append(input_uaf[param_name])

        param_name = 'seq_zero'
        input_uaf[param_name] = widgets.Text(description="Sequence Zero", style=dict(description_width='150px'), layout={'width': '90%'})
        input_uaf[param_name].json = input
        input_uaf[param_name].value = input['uaf'][param_name]
        input_uaf[param_name].observe(lambda x : self.on_uaf_property_changed('seq_zero', x), names='value')
        items.append(input_uaf[param_name])

        param_name = 'where'
        input_uaf[param_name] = widgets.Text(description="WHERE", style=dict(description_width='150px'), layout={'width': '90%'})
        input_uaf[param_name].json = input
        input_uaf[param_name].value = input['uaf'][param_name]
        input_uaf[param_name].observe(lambda x : self.on_uaf_property_changed('where', x), names='value')
        items.append(input_uaf[param_name])

        # Hide show
        self.set_uaf_visibility(input)

        input_items.append(widgets.VBox(items))
        

    def camel_case_split(s):
        # use map to add an underscore before each uppercase letter
        modified_string = list(map(lambda x: '_' + x if x.isupper() else x, s))
        # join the modified string and split it at the underscores
        split_string = ''.join(modified_string).split('_')
        # remove any empty strings from the list
        split_string = list(filter(lambda x: x != '', split_string))
        return " ".join(split_string)

    def create_param_ui(self, required):
        items = []
        is_uaf = self.in_db_json.get("function_type", "") == "uaf"
            
        for input in self.config_json["function"]["required_input"]:
            isRequired = input.get('isRequired', False)
            name = input['name']
            value = input.get('value', '')
            description = input.get("description", "")
            
            if isRequired != required:
                continue
            
            input_items = []

            table = widgets.Combobox(description="Table", value=str(value), options=[str(value)], style=dict(description_width='150px'), layout={'width': '90%'})
            table.tooltip = description

            self.table_widgets[name] = table
            table.json = input
            table.observe(lambda x : self.on_table_changed(x), names='value')
            input_items.append(table)
            input['table_ui'] = table

            if len(input.get('inputKindChoices', []))>1:
                self.create_partition_hash_by_ui(input, input_items)
            elif input.get('uafType', ''):
                self.create_uaf_ui(input, input_items)

            # Add Group (Accordian) parent UI for these items
            accordion = widgets.Accordion()
            accordion.children = [widgets.VBox(input_items)]
            accordion.set_title(index=0,title=name)
            items.append(accordion)

        for arg in self.config_json["function"]["arguments"]:
            isRequired = arg.get('isRequired', False)
            if isRequired != required:
                continue
            name = arg['name']
            if not is_uaf:
                name = NotebookUiImpl.camel_case_split(name)
            # TODO User datatype to create the appropriate widget
            datatype = arg['datatype']
            value = arg.get('value', arg.get('defaultValue', ''))
            description = arg.get("description", "")

            item = None
            if arg.get('allowsLists', False):
                if type(value) == str:
                    if value == '':
                        value = []
                if type(value) != list:
                        value = [value]

                control = NotebookUiImpl.TagsInput(value=value, tooltip=description, allow_duplicates=True, style=dict(description_width='150px'), layout={'width': '90%'})
                item = widgets.HBox([widgets.Label(name, layout=widgets.Layout(width="170px", display="flex", justify_content="flex-end")), control])
            elif datatype=="GROUPSTART" or datatype=="GROUPEND":
                # Ignore UAF Group start and End
                continue
            elif datatype=="COLUMNS":
                # Single COLUMN
                # At least have an option which is the value to avoid an error
                options = [str(value)]
                control = widgets.Dropdown(description=name, value=str(value), options=options, style=dict(description_width='150px'), layout={'width': '90%'})
            elif datatype=="BOOLEAN":
                if type(value) == str:
                    value = value.lower() == "true"
                control = widgets.Checkbox(description=name, value=value, style=dict(description_width='150px'))
            elif datatype=="DOUBLE PRECISION" and isValidFloat(value):
                control = widgets.BoundedFloatText(description=name, value=value, style=dict(description_width='150px'))
                lowerBound = arg.get('lowerBound', '')
                if lowerBound:
                    control.min = float(lowerBound)
                upperBound = arg.get('upperBound', '')
                if upperBound:
                    control.max = float(upperBound)
                if lowerBound and upperBound:
                    if lowerBound.lower() == "infinity" or float(lowerBound) < -1000.0:
                        step = 0.001
                    elif upperBound.lower() == "infinity" or float(upperBound) > 1000.0:
                        step = 0.001
                    else:
                        step = (float(upperBound)-float(lowerBound))/10000.0;
                    if step<0.001:
                        step = 0.001
                    step = round(step, 4);
                    control.step = step
            elif datatype=="INTEGER" and isValidInteger(value):
                control = widgets.BoundedFloatText(description=name, value=value, style=dict(description_width='150px'))
                lowerBound = arg.get('lowerBound', '')
                if lowerBound:
                    control.min = float(lowerBound)
                upperBound = arg.get('upperBound', '')
                if upperBound:
                    control.max = float(upperBound)
                control.step = 1
            elif datatype=="STRING" and "permittedValues" in arg and len(arg["permittedValues"])>0:
                control = widgets.Combobox(description=name, value=value, options=[str(value)], style=dict(description_width='150px'))
                if "" not in arg['permittedValues']:
                    arg['permittedValues'] = [""] + arg['permittedValues']
                control.options = arg['permittedValues']
                control.ensure_option = True
            else:
                # Just treat as string textfield
                control = widgets.Text(description=name, value=str(value), style=dict(description_width='150px'), layout={'width': '90%'})

            items.append(control if item==None else item)
            self.param_widgets[name] = control

            # Keep association of table and column parameters so when table is changes the columns can be updated
            if datatype == "COLUMNS":
                target_input_index = arg["target_input_index"]
                input = self.config_json["function"]["required_input"][target_input_index]
                input["column_param_ui"].append(control)

            # Show Tool Tip with description of parameter
            control.tooltip = description

            # Register callback when value changed of parameter widget
            control.json = arg
            control.observe(lambda x : self.on_value_changed(x), names='value')

        return widgets.VBox(items)


    def on_execute(self, change):
        try:
            self.execute_query()
        except Exception as e:
            #self.widget_output.clear_output()
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
            # use display on non-linux to avoid pressing OK twice
            if show_native_dialog:
                self.show_dialog(error_message)
                return
            else:
                display(Javascript(output_value))

            # Hide Progress Bar
            self.show_display(self.function_ui)
            #print(str(e))

    def on_query(self, change):
        try:
            dss_function = self.config_json.get('function', None)
            if dss_function and 'function_type' in dss_function and dss_function['function_type'] == "valib":
                json_contents = json.loads(dss_function["json_contents"])
                query = valib_execution(json_contents, dss_function, valib_query_wrapper=None)
            else:
                sql_generator = OpenEndedQueryGenerator('output', self.config_json)
                query = sql_generator.create_query()
            if not query:
                return
            output_value = '''
                require(
                    ["base/js/dialog"], 
                    function(dialog) {
                        dialog.modal({
                            title: "Query",
                            body: $("<div></div>").append('__BODY__'),
                            buttons: {
                                "OK": {
                                }}
                        });
                    }
                );'''

            query = query.replace("'", '"')
            query = query.replace('\n', '<br>');
            output_value = output_value.replace("__BODY__", query)
            if show_native_dialog:
                self.show_dialog(query)
                return
            else:
                display(Javascript(output_value))

        except Exception as e:
            self.widget_output.clear_output()
            with self.widget_output:
                print(str(e))


    def execute_query(self):
        if not self.config_json:
            return

        self.show_display(self.loading_bar, False)

        input_table_names = []
        output_table_names = []
        inputtables = {}
        inputschemas = {}
        # Gather the inputs (get table and schema from datasets)
        required_inputs = self.config_json["function"]["required_input"]
        for required_input in required_inputs:
            dataset_name = ""
            if "value" in required_input:
                dataset_name = required_input["value"]
            if dataset_name == "":
                if ("isRequired" in required_input) and required_input["isRequired"]:
                    raise RuntimeError("Input is missing - " + required_input["name"])
                # No input set by user, so keep empty
                input_table_names.append({})
                continue
            schema, full_table_name = self.connection.get_schema_table_name(dataset_name, self.inputs)
            if schema == "":
                schema = self.login_info['default_db']
            table_map = {}
            table_map["name"] = full_table_name
            table_map["table"] = full_table_name
            table_map["schema"] = schema
            inputtables[dataset_name] = full_table_name
            inputschemas[full_table_name] = schema
            input_table_names.append(table_map)
        self.config_json["function"]["input_table_names"] = input_table_names
        self.config_json["function"]["inputtables"] = inputtables
        self.config_json["function"]["inputschemas"] = inputschemas

        # Gather the outputs (get table and schema from datasets)
        for output in self.connection.get_dataset_name(self.outputs):
            table_map = {}
            dataset_name = output
            outputDatabaseName, outputTable = self.connection.get_schema_table_name(dataset_name, self.outputs)
            if schema == "":
                schema = self.login_info['default_db']
            table_map["name"] = outputTable
            table_map["table"] = outputTable
            table_map["schema"] = outputDatabaseName
            output_table_names.append(table_map)
        self.config_json["function"]["output_table_names"] = output_table_names

        # Main output is first schema and table
        outputDatabaseName = output_table_names[0]['schema']
        outputTable = output_table_names[0]["table"]

        # Gather connection properties
        autocommit = self.connection.get_connection_setting(self.inputs[0], "autocommitMode", True)
        pre_query = None
        post_query = None
        if not autocommit:
            pre_query = ["BEGIN TRANSACTION;"]
            post_query = ["END TRANSACTION;"]
            tmode = self.connection.get_connection_setting(self.inputs[0], "TMODE", "")
            if tmode == 'ANSI':
                pre_query = [";"]
                post_query = ["COMMIT WORK;"]

        # Setup the Executor
        self.connection.setup_executor(self.inputs[0], autocommit, pre_query, post_query)

        # Drop Outputs
        for output in output_table_names:
            drop_query = "DROP TABLE {outputTablename};".format(outputTablename=verifyQualifiedTableName(output['schema'], output['table']))
            try:
                self.connection.execute(drop_query)
            except:
                pass

        dss_function = self.config_json.get('function', None)
        if dss_function and 'function_type' in dss_function and dss_function['function_type'] == "valib":
            # VALIB     
            dss_function["val_location"] = self.login_info['val_location']
            json_contents = json.loads(dss_function["json_contents"])
            valib_execution(json_contents, dss_function, dropIfExists=dss_function.get('dropIfExists', False), valib_query_wrapper = self.connection)
        else:        
            # SQLE/UAF    
            sql_generator = OpenEndedQueryGenerator(outputTable, self.config_json, verbose=True, outputDatabaseName=outputDatabaseName)
            query = sql_generator.create_query()
            self.connection.execute(query)

        # Set schema
        index = 0
        for output in self.outputs:
            self.connection.set_schema_from_vantage(dataset=output, schema=output_table_names[0]['schema'], table=output_table_names[0]['table'])
            index += 1

        # Display output dataframe
        df = self.get_pandas_dataframe().head()

        try:
            output_value = '''
                require(
                    ["base/js/dialog"], 
                    function(dialog) {
                        dialog.modal({
                            title: "Result",
                            body: $("<div></div>").append('__BODY__'),
                            buttons: {
                                "OK": {
                                }}
                        });
                    }
                );'''
            markup = df.to_html().replace("\n", ' ')
            output_value = output_value.replace("__BODY__", markup)
            if show_native_dialog:
                self.show_dialog(markup)
                return
            else:
                display(Javascript(output_value))
        except:
            with self.widget_output:
                print(str(e))
            pass

        # Clear the progress bar
        self.show_display(self.function_ui)



    def get_output_dataframe(self, output_index=0):
        dataset_name = self.connection.get_dataset_name(self.outputs)[output_index]
        schema, table_name = self.connection.get_schema_table_name(dataset_name, self.outputs)
        return self.connection.get_output_dataframe(verifyQualifiedTableName(schema, table_name), dataset_name)

    def get_pandas_dataframe(self, output_index=0):
        dataset_name = self.connection.get_dataset_name(self.outputs)[output_index]
        schema, table_name = self.connection.get_schema_table_name(dataset_name, self.outputs)
        return self.connection.get_pandas_dataframe(verifyQualifiedTableName(schema, table_name), dataset_name)

    def on_reset(self, change):
        if not self.config_json:
            return
        self.change_function()

    def on_load(self, change):
        if not self.config_json:
            return
        if not os.path.exists(self.filename):
            return
        with open(self.filename, 'r') as file:
            data = file.read()
        dictionary = json.loads(data)
        self.current_function.value = dictionary["function_name"]
        self.change_function(file_settings_json=dictionary)


    def load_user_json_settings(self, dictionary):
        input_index = 0
        for input in self.config_json["function"]["required_input"]:
            input_values = dictionary["required_input"][input_index]
            input['value'] = input_values['value']
            if 'schema' in input_values:
                input['schema'] = input_values['schema']
            if 'partitionAttributes' in input_values:
                input['partitionAttributes'] = input_values['partitionAttributes']
            if 'orderByColumn' in input_values:
                input['orderByColumn'] = input_values['orderByColumn']
            if 'orderByColumnDirection' in input_values:
                input['orderByColumnDirection'] = input_values['orderByColumnDirection']
            if 'kind' in input_values:
                input['kind'] = input_values['kind']
            if 'uaf' in input_values:
                input['uaf'] = input_values['uaf']
            if 'uafType' in input_values:
                input['uafType'] = input_values['uafType']
            input_index += 1
        for arg in self.config_json["function"]["arguments"]:
            name = arg['name']
            if name in dictionary["arguments"]:
                arg['value'] = dictionary["arguments"][name]


    def on_save(self, change):      
        if not self.config_json:
            return
        dictionary = {"required_input" : [], "arguments" : {}}

        dictionary["function_name"] = self.in_db_json['function_name']
        for input in self.config_json["function"]["required_input"]:
            input_values = {}
            input_values['value'] = input['value']
            if 'schema' in input:
                input_values['schema'] = input['schema']
            if 'partitionAttributes' in input:
                input_values['partitionAttributes'] = input['partitionAttributes']
            if 'orderByColumn' in input:
                input_values['orderByColumn'] = input['orderByColumn']
            if 'orderByColumnDirection' in input:
                input_values['orderByColumnDirection'] = input['orderByColumnDirection']
            if 'kind' in input:
                input_values['kind'] = input['kind']
            if 'uaf' in input:
                input_values['uaf'] = input['uaf']
            if 'uafType' in input:
                input_values['uafType'] = input['uafType']
            dictionary["required_input"].append(input_values)
        for arg in self.config_json["function"]["arguments"]:
            name = arg['name']
            if "value" in arg:
                dictionary["arguments"][name] = arg['value']

        json_object = json.dumps(dictionary, indent=4)
        with open(self.filename, "w") as outfile:
            outfile.write(json_object)

        output_value = """
            require(
                ["base/js/dialog"], 
                function(dialog) {
                    dialog.modal({
                        title: 'Confirmation',
                        body: 'Saved',
                        buttons: {
                            'OK': {
                            }}
                    });
                }
            );
        """
        # Linux has no popup dialog
        if show_native_dialog:
            display(Javascript(output_value))


