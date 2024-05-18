## Teradata Widgets

teradatamlwidgets makes available to Python users a user interface to a collection of analytic functions and plot functions that reside on Teradata Vantage. This package provides Data Scientists and Teradata users a simple UI experience within a Jupyter Notebook to perform analytics and visualization on Teradata Vantage with no SQL coding and limited python coding required.

For documentation and tutorial notebooks please visit [Documentation](https://docs.teradata.com/r/Teradataml-Widgets/March-2024).

For Teradata customer support, please visit [Teradata Support](https://support.teradata.com/csm).

Copyright 2024, Teradata. All Rights Reserved.

### Table of Contents
* [Release Notes](#release-notes)
* [Installation and Requirements](#installation-and-requirements)
* [Using the Teradata Widgets Package](#using-the-teradata-python-package)
* [Documentation](#documentation)
* [License](#license)

## Release Notes:
#### teradatamlwidgets 20.0.0.3
* ##### New Features/Functionality
  * None
* ###### New APIs:
  * None
* ##### Bug Fixes
  * Using native dialog boxes
  * Parameter name change for Plot (color)

#### teradatamlwidgets 20.0.0.2
* ##### New Features/Functionality
  * Updated documentation
* ###### New APIs:
  * None
* ##### Bug Fixes
  * Initialized default database

#### teradatamlwidgets 20.0.0.1
* ##### New Features/Functionality
  * Updated documentation
* ###### New APIs:
  * None
* ##### Bug Fixes
  * None

#### teradatamlwidgets 20.0.0.0
* ##### New Features/Functionality
* ###### New APIs:
    * Analytic functions
      * `teradatamlwidgets.analytic_functions.Ui()`:
      * `teradatamlwidgets.analytic_functions.get_output_dataframe()`:
    * Plotting
      * `teradatamlwidgets.plot.ShowPlots()`:
* ##### Bug Fixes
  * None


## Installation and Requirements

### Package Requirements:
* Python 3.5 or later

Note: 32-bit Python is not supported.

### Minimum System Requirements:
* Windows 7 (64Bit) or later
* macOS 10.9 (64Bit) or later
* Red Hat 7 or later versions
* Ubuntu 16.04 or later versions
* CentOS 7 or later versions
* SLES 12 or later versions
* Teradata Vantage Advanced SQL Engine:
    * Advanced SQL Engine 16.20 Feature Update 1 or later
* For a Teradata Vantage system with the ML Engine:
    * Teradata Machine Learning Engine 08.00.03.01 or later

### Installation

Use pip to install the Teradata Widgets Package for Advanced Analytics.

Platform       | Command
-------------- | ---
macOS/Linux    | `pip install teradatamlwidgets`
Windows        | `py -3 -m pip install teradatamlwidgets`

When upgrading to a new version of the Teradata Widgets Package, you may need to use pip install's `--no-cache-dir` option to force the download of the new version.

Platform       | Command
-------------- | ---
macOS/Linux    | `pip install --no-cache-dir -U teradatamlwidgets`
Windows        | `py -3 -m pip install --no-cache-dir -U teradatamlwidgets`

## Using the Teradata Python Package

Your Python script must import the `teradatamlwidgets` package in order to use the Teradata Widgets Package:

```
>>> from teradataml import *
>>> Load the example data.
>>> load_example_data("movavg", ["ibm_stock"])
>>> load_example_data("teradataml", "titanic")
>>> inputs = ["ibm_stock"]
>>> outputs = ["Project_OutMovingAverageTest"]
>>> ui = Ui(function= 'MovingAverage',
        outputs=outputs, 
        inputs=inputs)
```
```
>>> from teradataml import *
>>> from teradatamlwidgets.plot.Login import *
>>> from teradatamlwidgets.plot.Ui import *
>>> from teradatamlwidgets.plot.ShowPlots import *
>>> # Load the example data.
>>> load_example_data("movavg", "ibm_stock")
>>> load_example_data("teradataml", "iris_input")
>>> # Plot
>>> plot1 = Ui(
	    table_name="ibm_stock", 
	    current_plot="Line", 
	    x='period', 
	    series='stockprice', 
	    style='green')
>>> plot2 = Ui(
	    table_name="iris_input", 
	    current_plot="Scatter", 
	    x='sepal_length', 
	    series='petal_length', 
	    xlabel='sepal_length',
	    ylabel='petal_length',
	    grid_color='black',
	    grid_linewidth=1, 
	    grid_linestyle="-",
	    style='red', 
	    title='Scatter Plot of sepal_length vs petal_length',
	    heading= 'Scatter Plot Example')
>>> # Combine Plots
>>> ShowPlots([plot1, plot2], nrows=1, ncols=2) 
```


+ Details

	+ This package is useful to Data Scientists and Teradata users and provides following:
	
		+ A simple UI experience within Jupyter Notebook.

		+ Access to In-DB analytics
                
		+ Visualizations

		+ Integration with teradataml

		+ Enable simple and easy integration with 3rd party workbenches


	+ teradatamlwidgets.analytic_functions.Ui Class
		+ Purpose
			+ Opens the function UI dialog in the notebook for the analytic functions (subset of the Analytics Database analytic functions, Vantage Analytics Library (VAL) functions, Unbounded Array Framework (UAF) time series functions).
		+ Syntax
			+ teradatamlwidgets.analytic_functions.Ui(outputs=[], inputs=[], function = '', export_settings = '')
		+ Arguments
			+ outputs:
				+ Optional Argument.
				+ A list with output table(s) name. Specify it as a schema_name.table_name or just table_name. If not specified, a name will be generated at random.
				+ Ex: outputs = [“dssDB.my_output”, “dssDB.my_test”] 
				+ Types: List String

			+ inputs:
				+ Required Argument.
				+ Option 1: A list with whichever input table(s) is desired. The tables that are listed will be the options for you to choose from when you choose the function. It is written as schema_name.table_name
				+ Ex: inputs = [“company1_stock”, “titanic”] 

				+ Option 2: A teradataml dataframe. It is written as DataFrame(“df_name”)
				+ Ex: inputs = [DataFrame(“company1_stock”), DataFrame(”titanic”)] 
				+ Types: List String or List teradataml.DataFrame

			+ function:
				+ Optional Argument.
				+ If a specific function is desired to be selected immediately when the UI shows up, then include the function name.
				+ Ex: function = "Linear Regression VAL" 
				+ Types: String

			+ export_settings:
				+ Optional Argument.
				+ In order to load and save your chosen parameters to a file, then set this filename.
				+ Ex: filename="LinReg.json"
				+ Types: String

		+ Function Output 
			+ This function will return instance of notebook UI interface.
		+ Usage Considerations
			+ The first time this is called, the “Login” user interface will be displayed so the user can log into a Teradata instance which creates the internal instance.

	+ teradatamlwidgets.analytic_functions.get_output_dataframe Method
		+ Purpose
			+ Gets the DataFrame of the executed function.
		+ Syntax
			+ ui.get_output_dataframe(output_index = 0)
		+ Arguments
			+ output_index:
				+ Optional Argument.
				+ Use this function to get the full output result table. Default is 0.
				+ Types: Int

		+ Function Output 
			+ Return Value: teradataml.DataFrame. Returns the output of the function as a teradataml DataFrame.
		+ Usage Considerations
			+ NA

	+ teradatamlwidgets.plot.Ui Class
		+ Purpose
			+ Allows a user interface for plotting that allows the user to set plotting parameters and then visualize the plots. The internal implementation uses the functionality of TD_PLOT exposed in teradataml DataFrame.
		+ Syntax
			+ teradatamlwidgets.plot.Ui(table_name = '', df = None, current_plot = '', ...all other parameter arguments...)
		+ Arguments
			+ table_name:
				+ Required Argument (IF df argument is not set).
				+ An input table name to use for plotting. 
				+ Ex: teradatamlwidgets.plot.Ui(table_name = "titanic")
				+ Types: String

			+ df:
				+ Required Argument (IF table_name argument is not set).
				+ An input teradataml dataframe to use for plotting. 
				+ Ex: teradatamlwidgets.plot.Ui(df = DataFrame("titanic"))
				+ Types: teradataml.DataFrame

			+ current_plot:
				+ Optional Argument.
				+ If you want chart type pre-selected.
				+ Ex: teradatamlwidgets.plot.Ui(table_name = "titanic", current_plot = "Bar")
				+ Possible Values: Line, Bar, Scatter, Corr, Wiggle, Mesh, Geom
				+ Types: String

			+ ..all other parameter arguments..:
				+ Optional Argument(s).
				+ If you want any other parameters pre-selected, see their argument name in description.
				+ Ex: teradatamlwidgets.plot.Ui(table_name = "titanic", current_plot = "Bar", style='green')
				+ Types: String 
			+ Refer to full list of parameter options in TD_PLOT teradataml documentation (https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/Teradata-Package-for-Python-User-Guide-17.20/Plotting-in-teradataml).

		+ Function Output 
			+ This function will return instance of notebook UI interface for TD_PLOT.
		+ Usage Considerations
			+ The first time this is called, the “Login” user interface will be displayed so the user can log into a Teradata instance which creates the internal instance.

	+ teradatamlwidgets.plot.ShowPlots Method
		+ Purpose
			+ ShowPlots combines multiple plots together into one figure.
		+ Syntax
			+ teradatamlwidgets.plot.ShowPlots(plots, nrows, ncols, grid=None)
		+ Arguments
			+ plots:
				+ Required Argument.
				+ List of UI Plot instances you want to combine into one figure.
				+ Types: List of plot.Ui

			+ nrows:
				+ Required Argument (IF grid argument not supplied).
				+ Number of rows. 
				+ Types: int

			+ ncols:
				+ Required Argument (IF grid argument not supplied).
				+ Number of columns. 
				+ Types: int

			+ grid:
				+ Optional Argument.
				+ Grid layout. 
				+ Types: map of tuples
				+ Example: Generates a figure with 2 subplots in the first row and a first column and second colum respectively and 1 sublpot in the second row (refer to the teradataml subplot documentation)
					+ grid={(1,1): (1, 1), (1,2): (1,1), (2, 1): (1, 2)}
				


## Documentation

General product information, including installation instructions, is available in the [Teradata Documentation website](https://docs.teradata.com/search/documents?query=package+python+-lake&filters=category~%2522Programming+Reference%2522_%2522User+Guide%2522*prodname~%2522Teradata+Package+for+Python%2522_%2522Teradata+Python+Package%2522&sort=last_update&virtual-field=title_only&content-lang=)

## License

Use of the Teradata Widgets Package is governed by the *License Agreement for the Teradata Widgets Package for Advanced Analytics*. 
After installation, the `LICENSE` and `LICENSE-3RD-PARTY` files are located in the `teradata_widget` directory of the Python installation directory.





