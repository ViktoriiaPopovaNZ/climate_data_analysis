

from constants import (
    DATA_DIR,
    MONTH_NAMES,
    REPORT_MODES
)

from exporters import (
    export_comparison_report_to_csv,
    export_report_to_pdf
)

from charts import (
    plot_year_comparison_chart,
    plot_station_comparison_chart,
    plot_rainfall_histogram,
    plot_rainfall_temperature_scatter
)

from rainfall_statistics import (
    print_summary_statistics,
    print_temperature_correlation,
    get_summary_statistics_lines
)

from rainfall_data import (
    extract_year_from_filename,
    read_csv_data,
    extract_year_and_month,
    monthly_rain_data,
    monthly_temperature_data,
    all_stations_rain_data
)


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

    options = REPORT_MODES

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