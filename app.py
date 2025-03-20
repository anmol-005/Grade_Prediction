from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_required_marks(GAA, Qz1, Qz2, bonus=0):
    grades = {"S": 90, "A": 80, "B": 70, "C": 60, "D": 50, "E": 40}
    results = {}

    for grade, threshold in grades.items():
        found = False
        for F in range(101):  # Checking from 0 to 100
            T = 0.1 * GAA + 0.4 * F + max(0.25 * Qz1 + 0.25 * Qz2, 0.4 * max(Qz1, Qz2)) + bonus
            if T >= threshold:
                results[grade] = F
                found = True
                break
        if not found:
            results[grade] = "Not possible"

    return results

@app.route("/", methods=["GET", "POST"])
def index():
    results = {}
    if request.method == "POST":
        GAA = float(request.form.get("GAA", 0))
        Qz1 = float(request.form.get("Qz1", 0))
        Qz2 = float(request.form.get("Qz2", 0))
        bonus = float(request.form.get("bonus", 0))

        results = calculate_required_marks(GAA, Qz1, Qz2, bonus)

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
