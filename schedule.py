import schedule, time
from flask import Flask, render_template, request
import pandas as pd
from Scrape import run_scraper

app = Flask(__name__)

# Run scraper every 10 minutes
schedule.every(10).minutes.do(run_scraper)

def scheduler_loop():
    while True:
        schedule.run_pending()
        time.sleep(1)

@app.route("/", methods=["GET", "POST"])
def index():
    product_choice = None
    data = None
    if request.method == "POST":
        product_choice = request.form.get("product")
        df = pd.read_csv("cosmetic_offers.csv")
        data = df[df["Category"].str.contains(product_choice, case=False)]
    return render_template("index.html", data=data, product_choice=product_choice)

if __name__ == "__main__":
    # Start Flask
    app.run(debug=True)

