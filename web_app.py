from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    result = None
    complaint = ""

    if request.method == "POST":

        complaint = request.form.get("complaint", "").strip()

        if complaint:

            # Temporary import from your existing backend
            from backend import analyze_complaint

            result = analyze_complaint(complaint)

    return render_template(
        "index.html",
        result=result,
        complaint=complaint
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )