# --- Imports ---
import plotly.express as px
import plotly.io as pio
import pandas as pd
import os


# --- Global color ---
PRIMARY_COLOR = "#F4D03F"

def name_trend_chart(df, name, output_file="app/static/plot.html"):
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

    # Styling
    fig.update_traces(
        line=dict(color=PRIMARY_COLOR, width=3),
        marker=dict(size=8, color=PRIMARY_COLOR)
    )

    fig.update_layout(
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white", family="Arial", size=14),
        title_font=dict(size=22),
        margin=dict(t=50, b=40, l=40, r=40)
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

    # Style the bars
    fig.update_traces(
        marker_color=PRIMARY_COLOR,
        textposition="outside",
        textfont_size=14
    )

    # Layout styling
    fig.update_layout(
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white", family="Arial", size=14),
        title_font=dict(size=22),
        margin=dict(t=60, l=40, r=40, b=40)
    )

    # Store chart and return True
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    pio.write_html(fig, file=output_file, auto_open=False)
    return True


def fastest_growing_names_chart(df, year_from, year_to, output_file="app/static/fastest_growth.html", n=10):
    """
    Finds the top n names with the highest growth in usage from year_from to year_to.
    Returns True if success. False if not.
    """

    # Filter for the two years
    df_from = df[df["år"] == year_from]
    df_to = df[df["år"] == year_to]

    # If data does not exist
    if df_from.empty or df_to.empty:
        return False
    
    # Count by name
    from_counts = df_from.groupby("fornavn")["antall"].sum()
    to_counts = df_to.groupby("fornavn")["antall"].sum()

    # Combine and calculate
    growth_df = pd.DataFrame({
        "from": from_counts,
        "to": to_counts
    }).fillna(0)

    growth_df["growth"] = growth_df["to"] - growth_df["from"]
    top = growth_df.sort_values(by="growth", ascending=False).head(n).reset_index()

    # Create plotly chart
    fig = px.bar(
        top,
        x="fornavn",
        y="growth",
        text="growth",
        title=f"Top {n} fastest-growing names from {year_from} to {year_to}",
        labels={"fornavn": "Name", "growth": "Growth"}
    )

    # Styling
    fig.update_traces(
        marker_color=PRIMARY_COLOR,
        textposition="outside",
        textfont_size=14
    )

    fig.update_layout(
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white", family="Arial", size=14),
        title_font=dict(size=22),
        margin=dict(t=60, l=40, r=40, b=40)
    )

    # Store chart and return True
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    pio.write_html(fig, file=output_file, auto_open=False)
    return True


def named_individuals_chart(df, output_file="app/static/named_individuals.html"):
    """
    Generates a line chart showing total name usage per year.
    """

    totals = df.groupby("år")["antall"].sum().reset_index()

    # Create chart
    fig = px.line(
        totals,
        x="år",
        y="antall",
        markers=True,
        title="Named individuals per year",
        labels={"år": "Year", "antall": "Total count"}
    )

    # Styling
    fig.update_traces(
        line=dict(color=PRIMARY_COLOR, width=3),
        marker=dict(size=8, color=PRIMARY_COLOR)
    )

    fig.update_layout(
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white", family="Arial", size=14),
        title_font=dict(size=22),
        margin=dict(t=60, l=40, r=40, b=40)
    )

    # Store chart and return True
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    pio.write_html(fig, file=output_file, auto_open=False)
    return True


def starts_with_chart(df, start_str, year=None, output_file="app/static/starts_with.html", n=10):
    """
    Generates a bar chart of the top n names starting with a given string.
    Optionally filters by year.
    """

    # Filter names starting with the given string
    filtered = df[df["fornavn"].str.lower().str.startswith(start_str.lower())]

    # Optional
    if year is not None:
        filtered = filtered[filtered["år"] == year]

    # Exit if no data
    if filtered.empty:
        return False
    
    # Group by name and sum counts
    top = filtered.groupby("fornavn")["antall"].sum().sort_values(ascending=False).head(n).reset_index()

    # Create chart
    fig = px.bar(
        top,
        x="fornavn",
        y="antall",
        text="antall",
        title=f"Top {n} names starting with '{start_str}'" + (f"in {year}" if year else ""),
        labels={"fornavn": "Name", "antall": "Count"}
    )

    # Styling
    fig.update_traces(
        marker_color=PRIMARY_COLOR,
        textposition="outside",
        textfont_size=14
    )

    fig.update_layout(
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white", family="Arial", size=14),
        title_font=dict(size=22),
        margin=dict(t=60, l=40, r=40, b=40)
    )

    # Store dchart
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    pio.write_html(fig, file=output_file, auto_open=False)
    return True