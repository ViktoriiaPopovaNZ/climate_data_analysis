from pathlib import Path        # Import Path for working with file paths
import pandas as pd             # Import pandas for reading CSV files
import matplotlib.pyplot as plt # Import matplotlib for charts
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

MONTH_NAMES = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

DATA_DIR = Path("data")    # Path to the folder containing CSV files

def extract_year_from_filename(file_path: Path) -> int:
    '''Extract year from a rainfall CSV filename.'''
    return int(file_path.stem.split()[0]) # Get the year from the filename
                                          # Example: "2020 rain.csv" -> "2020 rain" -> "2020" -> 2020

def get_integer_input(text): 
    '''Read an integer from the user.'''
    while True:
        try:
            user_input = input(text) #
            return int(user_input)
        except ValueError:
            print("Invalid format. Please enter a whole year number.")


def read_years(valid_years):
    '''Read and validate selected years from the user.'''

    year_input = input(  # Ask the user to enter one or more years
        "Enter years separated by commas "
        "(example: 2020,2021,2022) or 0 for all years: "
    )

    if year_input == "0":  # Check if the user selected all years
        return valid_years  # Return all available years

    selected_years = []  # Create an empty list for selected years

    split_years = year_input.split(",")  # Split the input by commas

    for year in split_years:  # Loop through entered years

        year = int(year.strip())  # Remove spaces and convert text to integer

        if year in valid_years:  # Check if the year exists in the data
            selected_years.append(year)  # Add valid year to the list

        else:
            print(f"No data available for {year}.")  # Display error message

    return selected_years  # Return selected years

def read_single_year(valid_years):
    '''Read one valid year from the user.'''  # Read only one year from the user

    year = get_integer_input("Enter year: ")  # Ask user to enter a year

    while year not in valid_years:  # Check if the year is not available
        print(f"No data available for {year}.")  # Display error message
        year = get_integer_input("Enter year: ")  # Ask user to enter year again

    return year  # Return valid selected year


def read_months():
    '''Read selected months from the user.'''

    print("Available months:")  # Display available months

    month_number = 1  # Start numbering from 1

    for month_name in MONTH_NAMES:  # Loop through month names
        print(f"[{month_number}] {month_name}")  # Display month number and name
        month_number += 1  # Move to the next month

    month_input = input(     # Read month input
        "Enter month numbers separated by commas "
        "(example: 1,3,7) or 0 for all months: "
    )  

    if month_input == "0":  # Check if the user selected all months
        return [1,2,3,4,5,6,7,8,9,10,11,12]  # Return all months

    selected_months = []  # Create an empty list for selected months

    split_months = month_input.split(",")  # Split the input by commas

    for month in split_months:  # Loop through entered months

        month = int(month)  # Convert text to an integer

        if month >= 1 and month <= 12:  # Check if the month is valid
            selected_months.append(month)  # Add valid month to the list

        else:
            print("Invalid month.")  # Display an error message

    return selected_months  # Return selected months

def read_csv_data(filenames: list[str], columns: list[str]) -> list[tuple]:
    '''
    IMPORTANT NOTE:
      When completing Part one and Part Two of the project
      you do NOT need to understand how this function works.

    Reads in data from a list of csv files.
    Returns columns of data requested, in the order given.
    '''

    df = pd.concat(
        [pd.read_csv(filename) for filename in filenames],
        ignore_index=True
    )

    report_on_dataframe(df, "Loaded CSV data")

    desired_columns = df[columns]

    return list(desired_columns.itertuples(index=False, name=None))

def report_on_dataframe(df, stage_name: str):
    '''Print basic information about a DataFrame.'''

    print(f"\nData inspection: {stage_name}")
    print(f"Shape: {df.shape}")
    print("Columns:")
    print(df.columns)
    print("Missing values:")
    print(df.isna().sum())


def menu_select(options: list[str]) -> int:
    '''
    - Prints a list of enumerated options and collects the users
    - The user is prompted until they enter a valid selection
    '''
    prompt = f"0-{len(options) - 1}:: "
    i = 0
    while i < len(options):
        print(f'[{i}] {options[i]}')
        i += 1

    selection = get_integer_input(prompt)
    while selection < 0 or selection >= len(options):
        print(f'{selection} is not a valid option\nTry again')
        selection = get_integer_input(prompt)

    return selection

def read_report_mode():
    '''Read selected report mode from the user.'''  # Read which type of report the user wants

    options = ["Compare years", "Compare stations", "Rainfall histogram", "Rainfall vs temperature"]  # Create list of report mode options
    
    print("Select report mode:")  # Display message for the user

    return menu_select(options)  # Use existing menu function and return selected mode

def read_one_station(stations: list[tuple]):
    '''Read one station or all stations from the user.'''  # Read one station for year comparison mode

    station_names = []  # Create empty list for station names

    for station_id, station_name in stations:  # Loop through station records
        station_names.append(station_name)  # Add station name to the list

    station_names.append("All stations")  # Add All stations option

    print("Select a location:")  # Ask user to select location

    option = menu_select(station_names)  # Read one selected option

    if option == len(station_names) - 1:  # Check if user selected All stations
        return None, "All stations"  # Return special value for all stations

    return stations[option]  # Return selected station record

def read_temperature_station(stations: list[tuple]):
    '''Read one weather station for temperature analysis.'''

    station_options = []

    for station_number, station_name in stations:
        station_options.append(f"{station_name}")

    print("\nSelect one station:")

    selection = menu_select(station_options)

    return stations[selection]


def read_multiple_stations(stations: list[tuple]):
    '''Read multiple stations or all stations from the user.'''

    print("\nSelect one or more locations:")

    i = 0
    while i < len(stations):
        print(f"[{i}] {stations[i][1]}")
        i += 1

    print(f"[{len(stations)}] All stations")

    user_input = input(
        "\nEnter station numbers separated by commas "
        "(example: 0,2,4): "
    )

    selected_numbers = user_input.split(",")

    selected_stations = []

    for number in selected_numbers:
        number = int(number.strip())

        if number == len(stations):
            return stations

        selected_stations.append(stations[number])

    return selected_stations


def extract_year_and_month(date: str) -> tuple[int, int]:
    '''
    Given a timestamp of the form:
        YYYYMMDD:HHmm
    Extract the year and YYYY (Year digits) and MM (Month digits),
    and return them.
    '''
    date_str, _ = date.split(":")
    year = date_str[:4]
    month = date_str[4:6]

    return int(year), int(month)


def monthly_rain_data(station_number: int, month: int, rain_data: list[tuple], year: int) -> list[float]:
    '''
    Retrieves all rain readings for a given station, and month.
    '''
    out = []

    for station, date_str, reading in rain_data:
        reading_year, reading_month = extract_year_and_month(date_str)
        if station == station_number and reading_month == month and reading_year == year:
            out.append(reading)

    return out

def monthly_temperature_data(month_name: str, year: int,
                             temperature_data: list[tuple]):
    '''Return monthly temperature value for a selected month and year.'''

    for period, temp_year, temperature in temperature_data:
        if period == month_name and int(temp_year) == year:
            return float(temperature)

    return None

def all_stations_rain_data(month: int, rain_data: list[tuple], year: int) -> list[float]:
    '''
    Retrieves all rain readings for all stations for a given month and year.
    '''
    out = []

    for station, date_str, reading in rain_data:
        reading_year, reading_month = extract_year_and_month(date_str)
        if reading_month == month and reading_year == year:
            out.append(reading)

    return out

def print_summary_statistics(rainfall_totals: list[float]):
    '''Print average, minimum, maximum, and standard deviation.'''

    if len(rainfall_totals) == 0:
        print("\nSummary Statistics: No data")
        return

    valid_totals = []

    for total in rainfall_totals:
        if total > 0:
            valid_totals.append(total)

    if len(valid_totals) == 0:
        print("\nSummary Statistics: No valid rainfall data")
        return

    rainfall_array = np.array(valid_totals)

    print("\nSummary Statistics:")
    print(f"Average rainfall: {np.mean(rainfall_array):.2f} mm")
    print(f"Minimum rainfall: {np.min(rainfall_array):.2f} mm")
    print(f"Maximum rainfall: {np.max(rainfall_array):.2f} mm")
    print(f"Standard deviation: {np.std(rainfall_array):.2f} mm")


def print_temperature_correlation(temperatures: list[float],
                                  rainfall_totals: list[float]):
    '''Print and return correlation between temperature and rainfall.'''

    if len(temperatures) < 2 or len(rainfall_totals) < 2:
        print("\nCorrelation: Not enough data")
        return None

    correlation_matrix = np.corrcoef(
        temperatures,
        rainfall_totals
    )

    correlation = correlation_matrix[0, 1]

    print("\nRainfall and Temperature Analysis:")
    print(f"Correlation: {correlation:.2f}")

    return correlation


def get_summary_statistics_lines(rainfall_totals: list[float]) -> list[str]:
    '''Return rainfall summary statistics as report lines.'''

    valid_totals = []  # Store valid rainfall totals

    for total in rainfall_totals:  # Loop through rainfall totals
        if total > 0:  # Ignore zero values
            valid_totals.append(total)  # Add valid value

    if len(valid_totals) == 0:  # Check if no valid data
        return ["Summary Statistics: No valid rainfall data"]  # Return message

    rainfall_array = np.array(valid_totals)  # Convert list to NumPy array

    return [  # Return statistics lines
        "Summary Statistics:",
        f"Average rainfall: {np.mean(rainfall_array):.2f} mm",
        f"Minimum rainfall: {np.min(rainfall_array):.2f} mm",
        f"Maximum rainfall: {np.max(rainfall_array):.2f} mm",
        f"Standard deviation: {np.std(rainfall_array):.2f} mm"
    ]

def export_comparison_report_to_csv(months: list[str], labels: list,
                                    rainfall_totals: list[list[float]], #f'output/{filename}'
                                    report_name: str):
    '''Export comparison rainfall report to a CSV file.'''

    report_data = {"Month": months}

    i = 0
    while i < len(labels):
        report_data[str(labels[i])] = [
            f"{total:.2f}" for total in rainfall_totals[i]
        ]
        i += 1

    report_df = pd.DataFrame(report_data)

    filename = f"output/{report_name}.csv"

    report_df.to_csv(filename, index=False)

    print(f"\nReport exported to {filename}")

def rain_report(rain_data: list[tuple], stations: list[tuple],
                years: list[int], report_mode: int):
    '''Generate a rainfall report based on selected report mode.'''

    if report_mode == 0:
        year_comparison_report(rain_data, stations, years)

    elif report_mode == 1:
        station_comparison_report(rain_data, stations, years)

    elif report_mode == 2:
        rainfall_histogram_report(rain_data, stations, years)

    else:
        rainfall_vs_temperature_report(rain_data, stations, years)


def year_comparison_report(rain_data: list[tuple], stations: list[tuple],
                           years: list[int]):
    '''Generate rainfall report comparing multiple years.'''

    selected_years = read_years(years)
    print("\nSelect one station or All stations for year comparison.")
    station_number, station_name = read_one_station(stations)

    selected_months = read_months()
    selected_month_names = []

    for month in selected_months:
        selected_month_names.append(MONTH_NAMES[month - 1])

    report_lines = []  # Store text for PDF export
    report_lines.append("Rainfall Year Comparison Report")
    report_lines.append("")
    report_lines.append(f"Station: {station_name}")  # Add station name
    report_lines.append(f"Years: {selected_years}")  # Add selected years

    report_lines.append("Months:")  # Add months heading

    for month_name in selected_month_names:  # Loop through month names
        report_lines.append(f"- {month_name}")  # Add one month per line

    report_lines.append("")  # Add empty line

    all_year_totals = []

    for year in selected_years:
        month_totals = []

        heading = f"Monthly Rain Total: {year} - {station_name}"
        print(f"\n{heading}")
        report_lines.append(heading)

        for month in selected_months:
            month_name = MONTH_NAMES[month - 1]

            if station_name == "All stations":
                month_data = all_stations_rain_data(month, rain_data, year)
            else:
                month_data = monthly_rain_data(
                    station_number,
                    month,
                    rain_data,
                    year
                )

            if len(month_data) == 0:
                line = f"{month_name:10}No data"
                print(line)
                report_lines.append(line)
                month_totals.append(0)
            else:
                monthly_total = sum(month_data)
                line = f"{month_name:10}{monthly_total:5.2f} mm"
                print(line)
                report_lines.append(line)
                month_totals.append(monthly_total)

        print_summary_statistics(month_totals)

        report_lines.append("")

        report_lines.extend(
            get_summary_statistics_lines(month_totals)
        )

        report_lines.append("")
        all_year_totals.append(month_totals)

    export_comparison_report_to_csv(
        selected_month_names,
        selected_years,
        all_year_totals,
        "year_comparison_report"
    )

    figure = plot_year_comparison_chart(
        all_year_totals,
        selected_years,
        station_name,
        selected_month_names
    )

    export_report_to_pdf(
        report_lines,
        "year_comparison_report.pdf",
        figure
    )

def station_comparison_report(rain_data: list[tuple], stations: list[tuple],
                              years: list[int]):
    '''Generate rainfall report comparing multiple stations for one year.'''  # Compare selected stations for one year

    selected_stations = read_multiple_stations(stations)  # Read multiple selected stations

    print("\nSelect one year for station comparison.")  # Ask user to select one year

    selected_year = read_single_year(years)  # Read only one year

    selected_months = read_months()  # Read selected months
    selected_month_names = []  # Create empty list for selected month names

    for month in selected_months:  # Loop through selected months
        selected_month_names.append(MONTH_NAMES[month - 1])  # Add month name to list

    all_station_totals = []  # Create empty list for all station totals
    station_names = []  # Create empty list for station names
    report_lines = []  # Store report text for PDF export

    report_lines.append("Rainfall Station Comparison Report")  # Add report title
    report_lines.append("")  # Add empty line
    report_lines.append(f"Year: {selected_year}")  # Add selected year
    report_lines.append("")  # Add empty line

    report_lines.append("Stations:")  # Add stations heading

    for station_number, station_name in selected_stations:  # Loop through stations
        report_lines.append(f"- {station_name}")  # Add station name

    report_lines.append("")  # Add empty line
    report_lines.append("Months:")  # Add months heading

    for month_name in selected_month_names:  # Loop through month names
        report_lines.append(f"- {month_name}")  # Add month name

    report_lines.append("")  # Add empty line

    for station_number, station_name in selected_stations:  # Loop through selected stations
        month_totals = []  # Create empty list for this station's monthly totals

        heading = f"Monthly Rain Total: {selected_year} - {station_name}"  # Create heading
        print(f"\n{heading}")  # Print report heading
        report_lines.append(heading)  # Add heading to PDF report

        for month in selected_months:  # Loop through selected months
            month_name = MONTH_NAMES[month - 1]  # Get month name

            month_data = monthly_rain_data(  # Get rainfall data for station
                station_number,
                month,
                rain_data,
                selected_year
            )

            if len(month_data) == 0:  # Check if there is no data
                line = f"{month_name:10}No data"  # Create no data line
                print(line)  # Print no data line
                report_lines.append(line)  # Add line to PDF report
                month_totals.append(0)  # Add zero for chart

            else:
                monthly_total = sum(month_data)  # Calculate total rainfall
                line = f"{month_name:10}{monthly_total:5.2f} mm"  # Create total line
                print(line)  # Print rainfall total
                report_lines.append(line)  # Add line to PDF report
                month_totals.append(monthly_total)  # Add total to list

        print_summary_statistics(month_totals)  
        report_lines.append("")  # Add spacing before statistics

        report_lines.extend(
            get_summary_statistics_lines(month_totals)
        )
        report_lines.append("")  # Add empty line between stations

        all_station_totals.append(month_totals)  # Add this station's totals to main list
        station_names.append(station_name)  # Add station name to labels

    export_comparison_report_to_csv(  # Export comparison data to CSV
        selected_month_names,
        station_names,
        all_station_totals,
        f"station_comparison_report_{selected_year}"
    )

    figure = plot_station_comparison_chart(  # Draw chart and get figure
        all_station_totals,
        station_names,
        selected_year,
        selected_month_names
    )

    export_report_to_pdf(  # Export report text and chart to PDF
        report_lines,
        f"station_comparison_report_{selected_year}.pdf",
        figure
    )


def rainfall_histogram_report(rain_data: list[tuple],
                              stations: list[tuple],
                              years: list[int]):
    '''Generate rainfall histogram report.'''  # Generate histogram report

    print("\nSelect one station or All stations for histogram analysis.")  # Ask user to select station

    station_number, station_name = read_one_station(stations)  # Read station selection

    print("\nSelect one year for histogram analysis.")  # Ask user to select year

    selected_year = read_single_year(years)  # Read selected year

    rainfall_totals = []  # Store monthly rainfall totals
    report_lines = []  # Store report text for PDF export

    report_lines.append("Rainfall Histogram Report")  # Add report title
    report_lines.append("")  # Add empty line
    report_lines.append(f"Station: {station_name}")  # Add station name
    report_lines.append(f"Year: {selected_year}")  # Add selected year
    report_lines.append("")  # Add empty line

    heading = f"Rainfall Histogram Report: {selected_year} - {station_name}"  # Create heading
    print(f"\n{heading}")  # Print heading
    report_lines.append(heading)  # Add heading to PDF report

    for month in range(1, 13):  # Loop through all months
        month_name = MONTH_NAMES[month - 1]  # Get month name

        if station_name == "All stations":  # Check if all stations selected
            month_data = all_stations_rain_data(  # Get all-stations rainfall data
                month,
                rain_data,
                selected_year
            )
        else:
            month_data = monthly_rain_data(  # Get selected-station rainfall data
                station_number,
                month,
                rain_data,
                selected_year
            )

        if len(month_data) == 0:  # Check if no rainfall data exists
            line = f"{month_name:10}No data"  # Create no data line
            print(line)  # Print no data line
            report_lines.append(line)  # Add line to PDF report
            rainfall_totals.append(0)  # Add zero for chart

        else:
            monthly_total = sum(month_data)  # Calculate monthly rainfall total
            line = f"{month_name:10}{monthly_total:5.2f} mm"  # Create rainfall line
            print(line)  # Print rainfall total
            report_lines.append(line)  # Add line to PDF report
            rainfall_totals.append(monthly_total)  # Add total to list

    print_summary_statistics(rainfall_totals) # Print summary statistics

    report_lines.append("")  # Add spacing before statistics

    report_lines.extend(
        get_summary_statistics_lines(rainfall_totals)
    )

    report_lines.append("")  # Add spacing after statistics

    wettest_total = max(rainfall_totals)  # Find highest rainfall total
    driest_total = min(rainfall_totals)  # Find lowest rainfall total

    wettest_index = rainfall_totals.index(wettest_total)  # Find index of wettest month
    driest_index = rainfall_totals.index(driest_total)  # Find index of driest month

    wettest_month = MONTH_NAMES[wettest_index]  # Get wettest month name
    driest_month = MONTH_NAMES[driest_index]  # Get driest month name

    wettest_line = f"Wettest month: {wettest_month} ({wettest_total:.2f} mm)"  # Create wettest line
    driest_line = f"Driest month: {driest_month} ({driest_total:.2f} mm)"  # Create driest line

    print(f"\n{wettest_line}")  # Print wettest month
    print(driest_line)  # Print driest month

    report_lines.append("")  # Add empty line
    report_lines.append(wettest_line)  # Add wettest month to PDF report
    report_lines.append(driest_line)  # Add driest month to PDF report

    figure = plot_rainfall_histogram(  # Draw histogram and get figure
        rainfall_totals,
        station_name,
        selected_year
    )

    export_report_to_pdf(  # Export report text and chart to PDF
        report_lines,
        f"rainfall_histogram_report_{selected_year}.pdf",
        figure
    )

def rainfall_vs_temperature_report(rain_data: list[tuple],
                                   stations: list[tuple],
                                   years: list[int]):
    '''Generate rainfall vs temperature scatter plot report.'''  # Generate rainfall vs temperature report

    print("\nSelect one station for rainfall vs temperature analysis.")  # Ask user to select station

    station_number, station_name = read_temperature_station(stations)  # Read selected station

    temperature_file = DATA_DIR / f"{station_number}_temperature.csv"  # Create temperature file path

    temperature_data = read_csv_data(  # Read temperature CSV data
        [temperature_file],
        ["PERIOD", "YEAR", "STATS_VALUE"]
    )

    print("\nSelect one year for rainfall vs temperature analysis.")  # Ask user to select year

    selected_year = read_single_year(years)  # Read selected year

    rainfall_totals = []  # Store matching rainfall totals
    temperatures = []  # Store matching temperature values
    report_lines = []  # Store report text for PDF export

    report_lines.append("Rainfall vs Temperature Report")  # Add report title
    report_lines.append("")  # Add empty line
    report_lines.append(f"Station: {station_name}")  # Add station name
    report_lines.append(f"Year: {selected_year}")  # Add selected year
    report_lines.append("")  # Add empty line

    heading = f"Rainfall vs Temperature Report: {selected_year} - {station_name}"  # Create heading
    print(f"\n{heading}")  # Print heading
    report_lines.append(heading)  # Add heading to PDF report

    for month in range(1, 13):  # Loop through all months
        month_name = MONTH_NAMES[month - 1]  # Get month name

        month_data = monthly_rain_data(  # Get monthly rainfall data
            station_number,
            month,
            rain_data,
            selected_year
        )

        temperature = monthly_temperature_data(  # Get monthly temperature data
            month_name,
            selected_year,
            temperature_data
        )

        if len(month_data) > 0 and temperature is not None:  # Check if both values exist
            monthly_total = sum(month_data)  # Calculate monthly rainfall total

            line = (  # Create report line
                f"{month_name:10}"
                f"Rainfall: {monthly_total:7.2f} mm   "
                f"Temperature: {temperature:5.2f} °C"
            )

            print(line)  # Print matched rainfall and temperature
            report_lines.append(line)  # Add line to PDF report

            rainfall_totals.append(monthly_total)  # Add rainfall total to list
            temperatures.append(temperature)  # Add temperature to list

        else:
            line = f"{month_name:10}No matching rainfall/temperature data"  # Create no data line
            print(line)  # Print no data line
            report_lines.append(line)  # Add line to PDF report

    if len(rainfall_totals) == 0:  # Check if no matching data exists
        line = "\nNo matching data available for scatter plot."  # Create no data message
        print(line)  # Print message
        report_lines.append(line)  # Add message to PDF report
        export_report_to_pdf(  # Export text-only PDF report
            report_lines,
            f"rainfall_temperature_report_{selected_year}.pdf"
        )
        return  # Stop function

    correlation = print_temperature_correlation(
        temperatures,
        rainfall_totals
    )

    if correlation is not None:
        report_lines.append("")
        report_lines.append("Rainfall and Temperature Analysis:")
        report_lines.append(f"Correlation: {correlation:.2f}")
    
    figure = plot_rainfall_temperature_scatter(  # Draw scatter plot and get figure
        temperatures,
        rainfall_totals,
        station_name,
        selected_year
    )

    export_report_to_pdf(  # Export report text and chart to PDF
        report_lines,
        f"rainfall_temperature_report_{selected_year}.pdf",
        figure
    )
    
def setup_chart(title: str, xlabel: str, ylabel: str):
    '''Create chart axes and set common title and labels.'''

    axes = plt.axes()  # create axes

    axes.set_title(title)  # set chart title
    axes.set_xlabel(xlabel)  # set x-axis label
    axes.set_ylabel(ylabel)  # set y-axis label

    axes.grid(True)  # add grid to improve readability

    return axes  # return axes

def export_report_to_pdf(report_lines: list[str],
                         filename: str,
                         figure=None):
    '''Export rainfall report text and optional chart to a PDF file.'''

    with PdfPages(f'output/{filename}') as pdf:  # Create PDF file

        text_figure = plt.figure(figsize=(8.27, 11.69))  # Create A4 page

        y_position = 0.95  # Starting vertical position

        for line in report_lines:  # Loop through report lines

            if y_position < 0.05:  # Check if page is full
                pdf.savefig(text_figure)  # Save current page

                plt.close(text_figure)  # Close current figure

                text_figure = plt.figure(figsize=(8.27, 11.69))  # Create new page

                y_position = 0.95  # Reset vertical position

            text_figure.text(
                0.05,  # X position
                y_position,  # Y position
                line,  # Text line
                va="top",  # Align text from top
                fontsize=8,  # Font size
                family="monospace"  # Use monospace font
            )

            y_position -= 0.02  # Move down for next line

        pdf.savefig(text_figure)  # Save final text page

        if figure is not None:  # Check if chart exists
            pdf.savefig(figure)  # Save chart page

        plt.close(text_figure)  # Close figure

    print(f"PDF report exported to {filename}")  # Confirm export



def plot_year_comparison_chart(all_year_totals: list[list[float]],
                               years: list[int],
                               station_name: str,
                               selected_month_names: list[str]):
    '''Plot rainfall totals for multiple years.'''

    axes = setup_chart(
        f"Rainfall Year Comparison for {station_name}",
        "Month",
        "Rainfall (mm)"
    )

    i = 0  # Start from first year

    while i < len(years):  # Loop through selected years
        axes.plot(
            selected_month_names,  # X-axis values
            all_year_totals[i],  # Y-axis values
            marker="o",  # Add markers
            label=str(years[i])  # Add year label
        )

        i += 1  # Move to next year

    axes.tick_params(axis="x", rotation=45)  # Rotate month names
    axes.legend()  # Show legend

    plt.tight_layout()  # Adjust layout
    figure = plt.gcf()
    
    return figure


def plot_station_comparison_chart(all_station_totals: list[list[float]],
                                  station_names: list[str],
                                  year: int,
                                  selected_month_names: list[str]):
    '''Plots rainfall totals for multiple stations using a grouped bar chart.'''  # Plot grouped bar chart

    axes = setup_chart(  # Create chart and labels
        f"Rainfall Station Comparison in {year}",
        "Month",
        "Rainfall (mm)"
    )

    x_positions = list(range(len(selected_month_names)))  # Create x positions for months

    bar_width = 0.8 / len(station_names)  # Calculate width of each bar

    i = 0  # Start from first station

    while i < len(station_names):  # Loop through selected stations

        bar_positions = []  # Create empty list for shifted bar positions

        for x in x_positions:  # Loop through month positions
            bar_positions.append(x + i * bar_width)  # Shift bars sideways

        axes.bar(  # Draw grouped bars for this station
            bar_positions,  # X positions
            all_station_totals[i],  # Rainfall totals
            width=bar_width,  # Width of bars
            label=station_names[i]  # Station label for legend
        )

        i += 1  # Move to next station

    middle_positions = []  # Create empty list for centered month labels

    for x in x_positions:  # Loop through month positions
        middle_positions.append(
            x + bar_width * (len(station_names) - 1) / 2  # Centre labels
        )

    axes.set_xticks(middle_positions)  # Set tick positions
    axes.set_xticklabels(selected_month_names, rotation=45)  # Add month labels

    axes.legend()  # Show legend

    plt.tight_layout()  # Adjust spacing

    figure = plt.gcf()  # Get current chart figure

    return figure  # Return figure for PDF export


def plot_rainfall_histogram(rainfall_totals: list[float],
                            station_name: str,
                            selected_year: int):
    '''Plot a histogram of rainfall totals.'''  # Plot histogram chart

    valid_totals = []  # Create empty list for valid rainfall totals

    for total in rainfall_totals:  # Loop through rainfall totals
        if total > 0:  # Keep only positive rainfall values
            valid_totals.append(total)  # Add valid total to list

    if len(valid_totals) == 0:  # Check if list is empty
        print("\nNo valid rainfall data to plot.")  # Display message
        return  # Stop function

    axes = setup_chart(  # Create chart and labels
        f"Rainfall Distribution: {station_name} ({selected_year})",
        "Monthly Rainfall Total (mm)",
        "Number of Months"
    )

    axes.hist(valid_totals, bins=5)  # Plot histogram

    plt.tight_layout()  # Adjust layout spacing
    figure = plt.gcf()  # Get current chart figure

    return figure


def plot_rainfall_temperature_scatter(temperatures: list[float],
                                      rainfall_totals: list[float],
                                      station_name: str,
                                      selected_year: int):
    '''Plot rainfall totals against mean temperature.'''  # Plot scatter chart

    axes = setup_chart(  # Create chart and labels
        f"Rainfall vs Temperature: {station_name} ({selected_year})",
        "Mean Air Temperature (°C)",
        "Monthly Rainfall Total (mm)"
    )

    axes.scatter(  # Plot scatter points
        temperatures,
        rainfall_totals
    )

    trend = np.polyfit(  # Calculate linear trend line
        temperatures,
        rainfall_totals,
        1
    )

    trend_line = np.poly1d(trend)  # Create trend line equation

    axes.plot(  # Plot trend line
        temperatures,
        trend_line(temperatures)
    )

    plt.tight_layout()  # Adjust layout spacing
    figure = plt.gcf()  # Get current chart figure

    return figure  # Display chart


def main():
    '''Run the rainfall report program.'''

    rain_files = sorted(DATA_DIR.glob("* rain.csv"))  # Find all rainfall CSV files in the data folder

    years = []  # Create an empty list for available years

    for file_path in rain_files:  # Loop through all rainfall files
        years.append(extract_year_from_filename(file_path))  # Extract year from filename

    report_mode = read_report_mode()  # Read selected report mode

    rain_data = read_csv_data(  # Read rainfall data from all rainfall CSV files
        rain_files,
        ["Station", "Date(NZST)", "Amount(mm)"]
    )

    station_data = read_csv_data(  # Read weather station information
        [DATA_DIR / "stations.csv"],
        ["Agent Number", "Name"]
    )

    rain_report(  # Generate and display rainfall report
        rain_data,
        station_data,
        years,
        report_mode
    )

main()  # Call the main function to start the program