import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from constants import OUTPUT_DIR

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

    filename = OUTPUT_DIR / f"{report_name}.csv"

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


def export_report_to_pdf(report_lines: list[str],
                         filename: str,
                         figure=None):
    '''Export rainfall report text and optional chart to a PDF file.'''

    with PdfPages(OUTPUT_DIR / filename) as pdf: # Create PDF file

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