# Climate Data Analysis
## Tasks
- [ ] Download the initial project files from the LMS
- [ ] Write your first commit adding these files in your repository
- [ ] Inspect the code in `main.py`
- Fill in missing sections of `readme.md`
  - [ ] Fill in *Initial Program Behavior* section
  - [ ] Fill in the *Future Development* sections
- [ ] Commit the changes to `readme.md` and push the changes to your eng-git repository

## Initial Program Behavior

Initially, the program read precipitation data from CSV files and generated a monthly rainfall report for a selected weather station.

The program extracted the year and month from the date format `YYYYMMDD:HHmm`. It filtered the data by station, month, and a fixed year (2020 only).

It then calculated the total precipitation (mm) for each month and displayed the results for the selected weather station in the terminal.

Inputs:
- 3 CSV files of precipitation amounts (rain_files), each file representing a different year: 2020, 2021, and 2022. Each file contains the following columns: Station, Date (NZST), Amount (mm)
- stations.csv file of the weather station, containing the following columns: Agent Number, Name
- User selects a station from the list

Outputs:
- Displays the summed precipitation amount by month at the selected station for 2020 and month from the date type (YYYYMMDD:HHmm).
It filters data by weather station, month, and precipitation data for 2020 only.
The program summarizes precipitation by month for the selected station.
Generates a report on precipitation amount (mm) by month.

## Current Program Behavior

The program now supports multiple rainfall analysis and comparison modes.

In Compare Years mode, the user selects one weather station (or all stations combined), one or more years, and one or more months. The program compares rainfall totals across the selected years using a line chart.

In Compare Stations mode, the user selects one year, multiple weather stations (or all stations), and one or more months. The program compares rainfall totals between the selected stations using a grouped bar chart.

In Rainfall Histogram mode, the user selects one weather station (or all stations combined) and one year. The program analyses rainfall totals across the full year and displays a histogram to show the distribution of monthly rainfall totals.

In Rainfall vs Temperature mode, the user selects one weather station and one year. The program combines monthly rainfall totals with monthly mean air temperature data, calculates a correlation value, and displays a scatter plot with a trend line. This helps show whether there is a visible relationship between temperature and rainfall for the selected station and year.

At the start, the user selects the report mode from an interactive menu. The program then displays different input options depending on the selected analysis type.

The program automatically detects available rainfall CSV files from the data folder using pathlib. It extracts the year from each filename and loads rainfall data from all available CSV files.

The program also prints basic information about loaded CSV files. This includes the DataFrame size, column names, and missing values. This helps check that the datasets were loaded correctly before analysis.

Temperature datasets for selected weather stations have also been added to the project data folder for future climate comparison and scatter plot analysis.

For comparison reports, the user can select one or more months. The program displays a list of available months, and the user can enter a single month, multiple months separated by commas, or 0 to select all months.

For each selected year, station, and month, the program retrieves relevant precipitation records. If data is available, it calculates and displays the total rainfall in millimetres. If no data is found, it displays "No data" to clearly indicate missing records.

If rainfall data is unavailable for a selected month or station, the program uses 0 values in charts to maintain consistent visualisation.

The Sugar Loaf AWS station was removed from the project because the dataset had very little rainfall data and many missing records. This made the results less reliable for rainfall comparison, charts, and statistical analysis.

The program also calculates rainfall summary statistics for generated reports, including:

- Average rainfall
- Minimum rainfall
- Maximum rainfall
- Standard deviation

The summary statistics are calculated from the generated monthly rainfall totals using NumPy functions.

The program can export generated comparison reports to CSV files. The exported CSV files contain:

- selected month names
- rainfall totals in millimetres
- rainfall comparison data for selected years or selected weather stations

The program can also automatically export generated rainfall reports to PDF files stored in the output folder.

The exported PDF reports include:
- rainfall totals
- rainfall summary statistics
- generated charts and visualisations
- multi-page report support for large reports

Rainfall values are formatted to two decimal places before export.

Different chart types are automatically selected depending on the report mode. Line charts are used for year comparison, grouped bar charts are used for station comparison, and histograms are used for rainfall distribution analysis.

Graph visualisation has also been improved by using reusable plotting helper functions. Common chart setup logic such as titles, axis labels, grid display, rotated month labels, legends, and layout spacing is now managed through shared helper functions. This reduces duplicated plotting code and improves chart readability and maintainability.

Inputs:
- Multiple precipitation CSV files, each representing a different year
- Temperature CSV files for selected weather stations
- User input for selecting a report mode
- User input for selecting one or more years
- `stations.csv` containing weather station information
- User input for selecting one or more stations
- User input for selecting one or more months in comparison reports

Outputs:
- Monthly rainfall report displayed in the terminal
- Rainfall summary statistics
- "No data" shown for months with missing records
- Line chart for year comparison
- Grouped bar chart for station comparison
- Histogram for rainfall distribution analysis
- Scatter plot with trend line for rainfall vs temperature analysis
- CSV comparison report exported for generated comparison reports
- Data inspection information for loaded CSV files
- PDF rainfall reports exported to the output folder
- Correlation analysis for rainfall and temperature data


## Dependencies

This program requires the following Python libraries:

- pandas
- matplotlib
- pathlib
- numpy
- matplotlib.backends.backend_pdf

## How to Run
To execute this program run following command from a terminal:

`python3 main.py`

## Future Development

- Add humidity and wind speed analysis if more data becomes available

- Add scatter plot analysis such as:
  - Rainfall vs Humidity

- Continue improving data cleaning and validation using Pandas

- Add the ability to export rainfall reports to:
  - TXT

- Continue improving the menu system and user input validation.

- Explore a future object-oriented programming (OOP) structure using custom classes for rainfall observations and weather stations.


### Basic Analysis Feature
You will need to outline at least one analysis that you plan to implement. Please include details on sources of new data required to complete this analysis.

This analysis must feature at least one [matplotlib](https://matplotlib.org/) graph.

Examples of basic analysis:
- correlating two weather metrics
- forming box plots of weather metric(s)
- ...

Tip: [NIWA DataHub](https://data.niwa.co.nz ) is a really useful source of historical weather data.

### Student Lead Features
You are to provide a set of features research and developed by you. They need to integrate the use of libraries **not** presented in the course.

For example you could:
- develop a weather dashboard using libraries like [streamlit](https://pypi.org/project/streamlit/), [panel](https://pypi.org/project/panel/) or [dash](https://dash.plotly.com/)
- generate Choropleths using [plotly](https://plotly.com/python/choropleth-maps/) that display weather information on a map
- Application Programming Interface (API) using [requests](https://pypi.org/project/requests/) to integrate live data into your program.
## Citations

As you develop your project you will use a variety of resources. Cite and reference each as using the APA 7th format.
