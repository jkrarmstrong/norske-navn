# --- Imports ---
from flask import render_template, request
from app import app
from app.plots import name_trend_chart, top_names_chart
from app.data import df


# --- Routes ---
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/name_trend", methods=["GET", "POST"])
def name_trend_view():
    plot_path = None
    feilmelding = None

    if request.method == "POST":
        navn = request.form["navn"].capitalize()

        if set(["fornavn", "år", "antall"]).issubset(df.columns):
            success = name_trend_chart(df, navn)
            if success:
                plot_path = "plot.html"
            else:
                feilmelding = f"Could not find the name '{navn}' in this dataset."
        else:
            feilmelding = "Dataset is missing required columns (fornavn, år, antall)."

    return render_template("name_trend.html", plot_path=plot_path, feilmelding=feilmelding)


@app.route("/top_names", methods=["GET", "POST"])
def top_names_view():
    plot_path = None
    feilmelding = None

    if request.method == "POST":
        try:
            år = int(request.form["år"])
            success = top_names_chart(df, år)
            if success:
                plot_path = "top_names.html"
            else:
                feilmelding = f"No data found for the year {år}."
        except ValueError:
            feilmelding = "Please enter a valid year."

    return render_template("top_names.html", plot_path=plot_path, feilmelding=feilmelding)

