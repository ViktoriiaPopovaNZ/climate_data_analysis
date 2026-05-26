import pandas as pd
from pathlib import Path

def extract_year_from_filename(file_path: Path) -> int:
    '''Extract year from a rainfall CSV filename.'''
    return int(file_path.stem.split()[0]) # Get the year from the filename
                                          # Example: "2020 rain.csv" -> "2020 rain" -> "2020" -> 2020


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