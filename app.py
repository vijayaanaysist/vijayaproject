from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    data = None
    product_choice = None

    if request.method == "POST":
        product_choice = request.form.get("product")
        df = pd.read_csv("cosmetic_offers.csv")

        data = df[df["Product"].str.contains(product_choice, case=False, na=False)]

    return render_template("index.html", data=data, product_choice=product_choice)

if __name__ == "__main__":
    app.run(debug=True)