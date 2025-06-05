# --- Imports ---
import plotly.express as px
import plotly.io as pio
import os

# File to work with
output_file = os.path.join(os.path.dirname(__file__), "static", "plot.html")

def name_trend_chart(df, name, output_file=output_file):
    """
    Generates a line plot showing the popularity of a given name over time.
    Returns True if the plot was successfully generated. False if name not found.
    """
    name_df = df[df["fornavn"] == name]

    if name_df.empty:
        return False

    fig = px.line(
        name_df,
        x="år",
        y="antall",
        markers=True,
        title=f"Name trend for: {name}",
        labels={"år": "Year", "antall": "Count"}
    )

    pio.write_html(fig, file=output_file, auto_open=False)
    return True


def top_names_chart(df, year, output_file="app/static/top_names.html", n=10):
    """
    Generates a bar chart of the top n names for the given year.
    Returns True if data exists, False if year not found.
    """
    year_df = df[df["år"] == year]

    # Exit function if no data exists for given year
    if year_df.empty:
        return False

    # Sort the year. Highest n rows will be the most popular names
    top = year_df.sort_values(by="antall", ascending=False).head(n)

    # Create plotly chart
    fig = px.bar(
        top,
        x="fornavn",
        y="antall",
        text="antall",
        title=f"Top {n} names in {year}",
        labels={"fornavn": "Name", "antall": "Count"}
    )

    # Move text outside pillars
    fig.update_traces(textposition="outside")

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    pio.write_html(fig, file=output_file, auto_open=False)
    return True

