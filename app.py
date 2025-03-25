from flask import Flask, render_template, request
>>>>>>> 8e00a57a29a99e17edd8713522a1f48c40927478
import os

app = Flask(__name__)

# MLT Grade Calculation
def calculate_mlt(GAA, Qz1, Qz2, bonus=0):
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


# BDM Grade Calculation with GA Eligibility Check
def calculate_bdm(GA1, GA2, GA3, GA4, Qz2, ROE):
    grades = {"S": 90, "A": 80, "B": 70, "C": 60, "D": 50, "E": 40}
    results = {}

    # Sort and select the best 3 GA scores
    best_3_ga = sorted([GA1, GA2, GA3, GA4], reverse=True)[:3]
    GA_avg = sum(best_3_ga) / 3

    # ❌ Eligibility Check: GA average must be ≥ 40
    if GA_avg < 40:
        return "ineligible", GA_avg

    # ✅ Proceed with grade calculation if eligible
    for grade, threshold in grades.items():
        found = False
        for F in range(101):  # Checking from 0 to 100
            T = 0.3 * GA_avg + 0.2 * Qz2 + 0.2 * ROE + 0.3 * F
            if T >= threshold:
                results[grade] = F
                found = True
                break
        if not found:
            results[grade] = "Not possible"

    return results, GA_avg


@app.route("/", methods=["GET", "POST"])
def index():
    results = {}
    eligibility_message = ""
    subject = "MLT"  # Default subject

    if request.method == "POST":
        subject = request.form.get("subject")

        if subject == "MLT":
            GAA = float(request.form.get("GAA", 0))
            Qz1 = float(request.form.get("Qz1", 0))
            Qz2 = float(request.form.get("Qz2", 0))
            bonus = float(request.form.get("bonus", 0))
            results = calculate_mlt(GAA, Qz1, Qz2, bonus)

        elif subject == "BDM":
            GA1 = float(request.form.get("GA1", 0))
            GA2 = float(request.form.get("GA2", 0))
            GA3 = float(request.form.get("GA3", 0))
            GA4 = float(request.form.get("GA4", 0))
            Qz2 = float(request.form.get("Qz2", 0))
            ROE = float(request.form.get("ROE", 0))

            calculation_result = calculate_bdm(GA1, GA2, GA3, GA4, Qz2, ROE)

            # Handle eligibility check
            if calculation_result[0] == "ineligible":
                eligibility_message = f"❌ You are NOT eligible for the End Term Exam. GA Average: {calculation_result[1]:.2f}"
                results = {}
            else:
                results, GA_avg = calculation_result
                eligibility_message = f"✅ You are eligible for the End Term Exam. GA Average: {GA_avg:.2f}"

        # ✅ Redirect to clear form data after POST
        return redirect(url_for("index", subject=subject))

    return render_template("index.html", results=results, subject=subject, eligibility_message=eligibility_message)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
