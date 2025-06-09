# --- Imports ---
from flask import render_template, request, jsonify
from app import app
from app.plots import *
from app.data import df


# --- Routes ---

# Index/Home
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate_charts", methods=["POST"])
def generate_charts():
    # Extract data from frontend
    name = request.form.get("name-search", "").strip()
    selected_graphs = request.form.getlist("selected-graphs[]")
    year = request.form.get("year")
    start_year = request.form.get("start-year")
    end_year = request.form.get("end-year")

    # List will store the filnames of generated charts
    chart_files = []

    # Loop through selected graph types and generate charts
    for graph in selected_graphs:
        if graph == "trend" and name:
            if name_trend_chart(df, name):
                chart_files.append("plot.html")

        elif graph == "top10" and year:
            if top_names_chart(df, int(year)):
                chart_files.append("top_names.html")

        elif graph == "rising" and start_year and end_year:
            if fastest_growing_names_chart(df, int(start_year), int(end_year)):
                chart_files.append("fastest_growth.html")

        elif graph == "total":
            if named_individuals_chart(df):
                chart_files.append("named_individuals.html")

        elif graph == "prefix" and name:
            if starts_with_chart(df, name, int(year) if year else None):
                chart_files.append("starts_with.html")

    # Return list of generated chart filenames as JSON
    return jsonify({"charts": chart_files})


@app.route("/name_trend", methods=["GET", "POST"])
def name_trend_view():
    plot_path = None
    feilmelding = None

    # Get submitted name and standardize capitalization
    if request.method == "POST":
        navn = request.form["navn"].capitalize()

        # Ensure columns are present
        if set(["fornavn", "år", "antall"]).issubset(df.columns):
            # Try to generate chart
            success = name_trend_chart(df, navn)
            if success:
                plot_path = "plot.html"
            else:
                feilmelding = f"Could not find the name '{navn}' in this dataset."
        else:
            feilmelding = "Dataset is missing required columns (fornavn, år, antall)."

    # Render chart or error message
    return render_template("name_trend.html", plot_path=plot_path, feilmelding=feilmelding)


@app.route("/top_names", methods=["GET", "POST"])
def top_names_view():
    plot_path = None
    feilmelding = None

    # Get submitted year
    if request.method == "POST":
        try:
            år = int(request.form["år"])
            # Try to generate chart
            success = top_names_chart(df, år)
            if success:
                plot_path = "top_names.html"
            else:
                feilmelding = f"No data found for the year {år}."
        except ValueError:
            feilmelding = "Please enter a valid year."

    # Render chart or error message
    return render_template("top_names.html", plot_path=plot_path, feilmelding=feilmelding)


@app.route("/fastest_growth", methods=["GET", "POST"])
def fastest_growth_view():
    plot_path = None
    feilmelding = None

    # Get submitted years
    if request.method == "POST":
        try:
            year_from = int(request.form["year_from"])
            year_to = int(request.form["year_to"])

            # Handle faulty user input
            if year_from >= year_to:
                feilmelding = "Start year must be earlier than end year."
            else:
                # Try to generate chart
                success = fastest_growing_names_chart(df, year_from, year_to)
                if success:
                    plot_path = "fastest_growth.html"
                else:
                    feilmelding = f"No data found for {year_from} or {year_to}."
        except ValueError:
            feilmelding = "Please enter valid years."

    # Render chart og error message
    return render_template("fastest_growth.html", plot_path=plot_path, feilmelding=feilmelding)


@app.route("/named_individuals", methods=["GET", "POST"])
def named_individuals_view():
    plot_path = "named_individuals.html"
    success = named_individuals_chart(df)

    return render_template("named_individuals.html", plot_path=plot_path)


@app.route("/starts_with", methods=["GET", "POST"])
def starts_with():
    plot_path = None
    feilmelding = None

    # Get submitted name and year
    if request.method == "POST":
        start_str = request.form["start_str"].strip()
        year_str = request.form["year"].strip()

        # Check if user interacted
        if not start_str:
            feilmelding = "Please enter a starting string."
        else:
            year = None
            if year_str:
                try:
                    year = int(year_str)
                except ValueError:
                    feilmelding = "Year must be a number."

            if feilmelding is None:
                # Try to generate chart
                success = starts_with_chart(df, start_str, year)
                if success:
                    plot_path = "starts_with.html"
                else:
                    feilmelding = "No matching names found."

    # Render template or error message
    return render_template("starts_with.html", plot_path=plot_path, feilmelding=feilmelding)
