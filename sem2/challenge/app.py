from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Set FLASK_SECRET_KEY in your environment before starting Flask.
app.secret_key = os.environ.get("FLASK_SECRET_KEY")

if not app.secret_key:
    raise RuntimeError(
        "Please set the FLASK_SECRET_KEY environment variable."
    )

# Correct answers stay on the server.
STAGE_1_ANSWERS = {
    "q1": "a",
    "q2": "a",
    "q3": "b",
    "q4": "c",
    "q5": "b"
}

STAGE_2_ANSWER = "skibidi6767"
STAGE_3_ANSWER = "KFC"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/stage/1")
@stage_required(1)
def stage1():
    return render_template("stage1.html")


@app.route("/stage/1/submit", methods=["POST"])
@stage_required(1)
def stage1_submit():
    for question in STAGE_1_ANSWERS:
        answer = request.form.get(question, "").lower()

        if answer != correct_answer:
            return render_template(
                "stage1.html",
                error="One or more answers are incorrect. Try again."
            )

    session["unlocked_stage"] = max(
        session.get("unlocked_stage", 1), 2
    )
    return redirect(url_for("stage2"))



@app.route("/stage/2")
@stage_required(2)
def stage2():
    return render_template("stage2.html")


@app.route("/stage/2/submit", methods=["POST"])
@stage_required(2)
def stage2_submit():
    answer = request.form.get("answer", "").strip().lower()

    if answer == STAGE_2_ANSWER:
        session["unlocked_stage"] = max(
            session.get("unlocked_stage", 1), 3
        )
        return redirect(url_for("stage3"))

    return render_template(
        "stage2.html",
        error="Incorrect, try again."
    )


@app.route("/stage/3")
def stage3():
    return render_template("stage3.html")


@app.route("/stage/3/submit", methods=["POST"])
@stage_required(3)
def stage3_submit():
    answer = request.form.get("answer", "").strip().upper()

    if answer == STAGE_3_ANSWER:
        return redirect(url_for("stage3"))

    return render_template(
        "stage3.html",
        error="Incorrect, try again."
    )

if __name__ == "__main__": 
    app.run(debug=True)


