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


class Ui:
    '''
    Teradata's Interactive Notebook Uuser Interface
    '''
    def __init__(self, outputs = [], connection = None, function="", inputs=[], export_settings=""):
        """
        Constructor for the Teradata's Interactive Notebook Uuser Interface.

        @param outputs: Optional Argument. Specifies the output name of the output table.

        @param connection: Optional Argument. Specifies the specific connection; could be teradataml based (i.e. TeradatamlConnection instance) or another platform.

        @param function: Optional Argument. Specifies the name of the function, otherwise list of all functions will show.

        @param inputs: Optional Argument. Specifies the input tables desired allowing for selection in UI, otherwise user must type in input table name.

        @param export_settings: Optional Argument. Specifies the filename user would like to save the JSON out to, that way it can be reloaded in the future. I.e. if it is has information saved in filename, it will be loaded but if it is specified for first time then when user saves out it will save to that filename.

        @return: Instance of the UI class

        """

        # Error checking
        found_correct_version = False
        try:
            from teradataml.common.constants import TeradataAnalyticFunctionInfo
            found_correct_version = hasattr(TeradataAnalyticFunctionInfo, 'VAL')
        except ModuleNotFoundError as err:
            print("Error you do not have teradataml installed")
            return
        if not found_correct_version:
            #print("Error you do not have correct version of teradataml")
            pass
        try:
            import ipywidgets
        except ModuleNotFoundError as err:
            print("Error you do not have ipywidgets installed")
            return


        if not connection:
            connection = Connection()

        self.__notebook = NotebookUiImpl(connection, 
                        outputs,
                        function=function, 
                        inputs=inputs,  
                        filename=export_settings)
    
    def get_output_dataframe(self, output_index=0):
        """
        Access the output dataframe.

        @param output_index: Optional Argument. By default is set to 0, and will show the one output. If there are more than one output dataframe, accordingly this function can be called again with next index. The output is in the form of Teradataml Dataframe (if it is a TeradatamlConnection), or whatever dataframe type is.

        @return: The output dataframe, the type is based on the connection.

        """
        return self.__notebook.get_output_dataframe(output_index)


