import matplotlib.pyplot as plt
import numpy as np

def setup_chart(title: str, xlabel: str, ylabel: str):
    '''Create chart axes and set common title and labels.'''

    axes = plt.axes()  # create axes

    axes.set_title(title)  # set chart title
    axes.set_xlabel(xlabel)  # set x-axis label
    axes.set_ylabel(ylabel)  # set y-axis label

    axes.grid(True)  # add grid to improve readability

    return axes  # return axes


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