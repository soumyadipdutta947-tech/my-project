from flask import Flask, render_template, request
import pandas as pd
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

# dataset load
data = pd.read_csv("student_data.csv")

# inputs
X = data[[
    "study_hours",
    "attendance",
    "internal_marks",
    "assignment_marks",
    "previous_marks"
]]

# output
y = data["result"]

# model
model = LinearRegression()

# training
model.fit(X, y)

@app.route("/", methods=["GET", "POST"])

def home():

    prediction = ""
    grade = ""
    status = ""

    if request.method == "POST":

        study = float(request.form["study"])
        attendance = float(request.form["attendance"])
        internal = float(request.form["internal"])
        assignment = float(request.form["assignment"])
        previous = float(request.form["previous"])

        result = model.predict([[
            study,
            attendance,
            internal,
            assignment,
            previous
        ]])

        prediction = round(result[0],2)

        # pass fail
        if prediction >= 40:
            status = "PASS"
        else:
            status = "FAIL"

        # grade
        if prediction >= 90:
            grade = "A+"

        elif prediction >= 80:
            grade = "A"

        elif prediction >= 70:
            grade = "B"

        elif prediction >= 60:
            grade = "C"

        elif prediction >= 40:
            grade = "D"

        else:
            grade = "F"

    return render_template(
        "index.html",
        prediction=prediction,
        grade=grade,
        status=status
    )

if __name__ == "__main__":
    app.run(debug=True)