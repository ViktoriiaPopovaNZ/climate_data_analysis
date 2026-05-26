# Part Two Features
Below are a list of features that are to be completed for the second part of the assignment. Refer to the Project section of the course page for more detail on each feature.

Please fill in the section for each feature, replace all text below each heading.

## 1. Allow User to Select Year for Monthly Rain Report

I added a function that allows the user to select a year to generate a monthly rainfall report. At the beginning of the program, the user is prompted to enter a year ("Enter year:"). This value is converted to an integer and stored in the `year` variable.

The goal was to create a function that could support additional rainfall data files without manually updating the program each time a new year is added.

To achieve this, I used the pathlib library to automatically search the data folder for rainfall CSV files. The program extracts the year directly from each filename and stores the available years in a list.

This approach improves flexibility because the program can automatically detect new rainfall files such as "2023 rain.csv" or "2024 rain.csv" without requiring hard-coded file paths or manual updates.

I chose this solution because it simplifies maintenance and makes the program easier to expand in the future.

This feature increases the program's flexibility, as it is no longer limited to a single fixed year. It also improves usability by allowing the user to choose which available year they want to generate a report for.

## 2. User Input Validation
I added validation for the year entered by the user.

I created the get_integer_input() function. This function checks whether the user is entering a number. If the user enters something that isn't a number, the program displays an error message and prompts for more input.

Then I created the read_year() function. This function checks whether the entered year is in the list of available years. If the year isn't in the data, the program notifies the user and prompts for another year.

I also improved the station selection. The program already checked the range but didn't check the input format. I added a check to ensure the user is entering a number.

I used separate functions for the validation because it makes the code more readable and reusable.

## 3. Warn the user if no records found
I added text indicating if precipitation records are missing.

The rain_report() function first saves monthly data to a variable named month_data. It then checks for data availability using len(month_data) == 0. If there are no records, the program displays "No data" for that month. If records are available, the program sums the total precipitation and displays the value in millimeters.

I chose this solution because displaying 0.00 mm can be interpreted as meaning there was no precipitation in the selected month, when in reality, there is simply no data. Displaying "No data" makes the report clearer and easier for the user.

## 4. Rainfall Data Visualisation
I added visualisation features to display rainfall data using matplotlib charts.

To implement this feature, I created separate plotting functions for different types of rainfall analysis. The program now automatically selects different chart types depending on the selected report mode.

For year comparison, the program uses a line chart. This chart compares rainfall totals across multiple years for a selected weather station or all stations combined. Each line on the chart represents a different year, making it easier to identify rainfall trends over time.

For station comparison, the program uses a grouped bar chart. This chart compares rainfall totals between multiple weather stations for a selected year. Each group of bars represents a month, while each bar within the group represents a different station.

The program stores calculated rainfall totals in lists before generating the charts. If rainfall data is unavailable for a selected month, the program uses 0 values in the chart to maintain consistent visualisation.

I chose this approach because different chart types are better suited for different types of analysis. Line charts are more effective for showing trends over time, while grouped bar charts are better for comparing rainfall between locations.

These visualisations make the rainfall reports easier to understand and help users compare rainfall data more clearly.

## 5. All Stations Option
I added the ability for the user to select precipitation data from all stations simultaneously.

I added an "All Stations" option to the station selection menu in the rain_report() function. If the user selects this option, the program uses the all_stations_rain_data() function instead of the monthly_rain_data() function.

The all_stations_rain_data() function collects precipitation data from all stations for the selected month and year. The program then calculates the total for each month using all available station data.

I chose this approach because it is simple and easy to implement. It allows the user to see a general precipitation summary from all stations.

In the future, I plan to improve this function to allow the user to select multiple stations and compare their data individually.

## 6. Multiple Month Selection

I added a new feature that allows the user to select one or more months for the rainfall report.

To implement this, I created a new function named `read_months()`. This function displays a numbered list of all months from January to December. The user can enter one month number, several month numbers separated by commas, or enter 0 to select all months.

For example, if the user enters `1,3,7`, the program generates the report for January, March, and July. If the user enters `0`, the program includes all twelve months.

I updated the `main()` function so that it calls `read_months()` and stores the selected months in the `selected_months` variable. This list is then passed into the `rain_report()` function.

I also updated the `rain_report()` function so it loops through only the selected months instead of all twelve months. The program calculates rainfall totals only for those months and stores the selected month names for the chart.

Finally, I updated the `plot_rainfall_chart()` function so the bar chart displays only the selected months rather than always showing all twelve months.

This feature improves usability because users can focus on specific months instead of always viewing the full yearly report. It also makes the program more flexible because users can compare non-consecutive months, such as January, March, and July.


## 7. Multiple Year Selection

The user can now select one year, multiple years separated by commas, or 0 to select all available years. The program validates the selected years and displays an error message if rainfall data for a year is unavailable.

The program now loads rainfall data from all available CSV files and filters the data based on the user’s selected years.

The rainfall report is displayed separately for each selected year, making it easier to compare rainfall totals across different time periods.

## 8. Multiple Station Selection and Comparison

I added a new feature that allows the user to compare rainfall totals between multiple weather stations.

To implement this feature, I created a new function named `read_multiple_stations()`. This function displays a list of available weather stations and allows the user to select multiple stations by entering station numbers separated by commas.

For example, the user can enter `0,2,4` to compare rainfall data from three different weather stations.

I also created a new function named `station_comparison_report()`. This function calculates rainfall totals for each selected station and stores the totals in separate lists for comparison.

The program uses a grouped bar chart to display the comparison results. Each group of bars represents a month, while each individual bar represents a different weather station.

I chose this solution because grouped bar charts make it easier to compare rainfall totals between locations.

This feature improves the flexibility of the program and allows users to analyse rainfall differences across multiple weather stations.

## 9. Multiple Report Modes

I added support for multiple rainfall analysis modes.

To implement this feature, I created a new function named `read_report_mode()`. This function allows the user to select the type of rainfall analysis at the beginning of the program.

The program now supports two different report modes: Compare Years and Compare Stations.

In Compare Years mode, the user selects one weather station (or all stations combined), one or more years, and one or more months. The program compares rainfall totals across the selected years using a line chart.

In Compare Stations mode, the user selects one year, multiple weather stations, and one or more months. The program compares rainfall totals between the selected stations using a grouped bar chart.

I chose this approach because displaying multiple years and multiple stations in the same chart made the visualisation difficult to read. Separating the analysis into different modes improved both the readability of the charts and the overall program structure.

This feature improves usability and allows the program to support different types of rainfall analysis more effectively.

## 10. Rainfall Summary Statistics

I added a rainfall summary statistics feature to improve the analytical capabilities of the program.

After generating rainfall totals, the program now calculates and displays:

- Average rainfall
- Minimum rainfall
- Maximum rainfall
- Standard deviation

The statistics are calculated using NumPy functions such as:

- np.mean()
- np.min()
- np.max()
- np.std()

The program also ignores zero rainfall totals when calculating statistics. This prevents months with missing data or no rainfall records from incorrectly affecting the results.

## 11. Export Comparison Reports to CSV

I added a CSV export feature so that generated rainfall comparison reports can be saved and reused outside the program.

The export feature works with both report modes:

- Compare Years
- Compare Stations

In Compare Years mode, the program exports one CSV file called `year_comparison_report.csv`. This file contains the selected months and one column for each selected year.

In Compare Stations mode, the program exports one CSV file for the selected year, such as `station_comparison_report_2022.csv`. This file contains the selected months and one column for each selected station.

I created a reusable helper function called `export_comparison_report_to_csv()` to keep the export logic separate from the report logic.

The function creates a Pandas DataFrame from the selected months, report labels, and rainfall totals. It then saves the DataFrame as a CSV file using `to_csv()`.

Rainfall values are formatted to two decimal places before export. This makes the exported report easier to read and consistent with the terminal output.

This feature improves the program by allowing users to save, share, and further analyse rainfall comparison results in spreadsheet software.

## 12. Rainfall Histogram Analysis

I added a new rainfall histogram report mode to introduce rainfall distribution analysis to the program.

In this mode, the user selects:

- one weather station or all stations
- one year

The program automatically analyses rainfall totals for all twelve months of the selected year.

I created a new helper function called `plot_rainfall_histogram()` using Matplotlib histogram visualisation.

The histogram shows how monthly rainfall totals are distributed across the selected year. The x-axis shows rainfall total ranges in millimetres, and the y-axis shows how many months fall into each range.

The histogram report also displays rainfall summary statistics in the terminal. It also identifies the wettest and driest months for the selected year.

This feature extends the program beyond comparison reports and introduces a new type of rainfall data visualisation and analysis.

## 13. Rainfall vs Temperature Scatter Plot

I added a new rainfall vs temperature report mode to compare monthly rainfall totals with monthly mean air temperature data.

In this mode, the user selects:

- one weather station
- one year

The program reads the matching temperature CSV file for the selected weather station. The file name is based on the station number, for example `4843_temperature.csv`.

For each month of the selected year, the program matches:

- monthly rainfall total
- monthly mean air temperature

The program then prints the matched rainfall and temperature values in the terminal.

I created a new scatter plot function called `plot_rainfall_temperature_scatter()` using Matplotlib.

The scatter plot shows:

- mean air temperature on the x-axis
- monthly rainfall total on the y-axis

I also added a trend line using NumPy to make the overall relationship easier to see.

This feature extends the project from rainfall-only reporting into basic climate relationship analysis.

## 14. Data Inspection Using Pandas

I added a new helper function called `report_on_dataframe()`.

This function prints basic information about loaded CSV files, including:

- DataFrame size
- column names
- missing values

The function is automatically called when CSV data is loaded.

This helps check that the datasets were loaded correctly before the program continues with rainfall analysis and visualisation.

## 15. Reusable Plotting Functions and Improved Graph Visualisation

I improved the graph visualisation system by creating reusable plotting helper functions for Matplotlib charts.

I created a new helper function called `setup_chart()`. This function automatically creates chart axes and applies common chart settings such as:

- chart titles
- x-axis labels
- y-axis labels
- grid lines

I updated all chart functions to use this shared helper function instead of repeating the same plotting code in multiple places.

I also improved graph readability by adding:

- rotated month labels
- legends
- automatic layout spacing using `tight_layout()`

I chose this approach because it reduces duplicated code and makes the chart functions easier to maintain and extend.

This feature improves both the visual quality of the charts and the overall structure of the program.

## 16. PDF Report Export

I added a new PDF export system for rainfall analysis reports.

The program can now automatically generate PDF reports for all rainfall analysis modes, including:

- Compare Years
- Compare Stations
- Rainfall Histogram Analysis
- Rainfall vs Temperature Analysis

Each PDF report includes:

- selected stations
- selected years
- selected months
- rainfall totals
- rainfall summary statistics
- generated charts and visualisations

To implement this feature, I created a reusable helper function called `export_report_to_pdf()` using Matplotlib PDF export tools.

The PDF export system automatically creates multi-page reports when the report content becomes too large for a single page.

I also updated the chart functions so chart figures can be reused directly inside exported PDF reports.

All exported PDF reports are automatically saved to the `output` folder.

I chose this approach because PDF reports make the rainfall analysis easier to save, share, and present outside the Python program.

This feature improves both the usability and professionalism of the project by turning the rainfall analysis into a complete reporting system.

## 17. Rainfall and Temperature Correlation Analysis

I added a correlation analysis to the Rainfall vs Temperature report.

The program now calculates the correlation between monthly mean air temperature and monthly rainfall totals for the selected station and year.

The correlation value is displayed in the terminal and also included in the exported PDF report.

This helps show whether there is a possible relationship between temperature and rainfall. A value close to 1 shows a positive relationship, a value close to -1 shows a negative relationship, and a value close to 0 means there is no clear relationship.

This feature improves the rainfall vs temperature analysis by adding a simple statistical measure alongside the scatter plot and trend line.