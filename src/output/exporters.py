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