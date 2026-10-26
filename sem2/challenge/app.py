
import os
from functools import wraps
from flask import (
    Flask, render_template, request,
    redirect, url_for, session
)

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
STAGE_3_ANSWER = "kfc"


# Prevent access to stages that haven't been unlocked.
def stage_required(stage_number):
    def decorator(view_function):
        @wraps(view_function)
        def wrapper(*args, **kwargs):
            unlocked_stage = session.get("unlocked_stage", 1)

            if unlocked_stage < stage_number:
                return redirect(url_for("index"))

            return view_function(*args, **kwargs)

        return wrapper
    return decorator


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
    for question, correct_answer in STAGE_1_ANSWERS.items():
        answer = request.form.get(question, "").strip().lower()

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
@stage_required(3)
def stage3():
    return render_template("stage3.html")


@app.route("/stage/3/submit", methods=["POST"])
@stage_required(3)
def stage3_submit():
    answer = request.form.get("answer", "").strip().lower()

    if answer == STAGE_3_ANSWER:
        # Stage 4 is not implemented yet.
        session["unlocked_stage"] = max(
            session.get("unlocked_stage", 1), 4
        )
        return "Stage 3 complete! Stage 4 is coming soon."

    return render_template(
        "stage3.html",
        error="Incorrect, try again."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
