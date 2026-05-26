import numpy as np

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