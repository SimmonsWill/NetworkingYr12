import os
import ipaddress
from functools import wraps

from flask import (
    Flask, render_template, request,
    redirect, url_for, session
)

app = Flask(__name__)

# Secret key for Flask sessions
app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY",
    "chain-reaction-development-key"
)


# Correct answers stored on the server
STAGE_1_ANSWERS = {
    "q1": "a",
    "q2": "a",
    "q3": "b",
    "q4": "c",
    "q5": "b"
}

STAGE_2_ANSWER = "skibidi6767"
STAGE_3_ANSWER = "KFC"
STAGE_4_ANSWER = "192.0.2.10"


# Stage access protection
def stage_required(stage_number):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            unlocked_stage = session.get("unlocked_stage", 1)

            if unlocked_stage < stage_number:
                return redirect(url_for("index"))

            return function(*args, **kwargs)

        return wrapper
    return decorator


# HOME PAGE
@app.route("/")
def index():
    session.setdefault("unlocked_stage", 1)
    return render_template("index.html")


# STAGE 1
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


# STAGE 2
@app.route("/stage/2")
@stage_required(2)
def stage2():
    return render_template("stage2.html")


@app.route("/stage/2/submit", methods=["POST"])
@stage_required(2)
def stage2_submit():

    answer = request.form.get("answer", "").strip().lower()

    if answer == STAGE_2_ANSWER.lower():
        session["unlocked_stage"] = max(
            session.get("unlocked_stage", 1), 3
        )

        return redirect(url_for("stage3"))

    return render_template(
        "stage2.html",
        error="Incorrect, try again."
    )


# STAGE 3
@app.route("/stage/3")
@stage_required(3)
def stage3():
    return render_template("stage3.html")


@app.route("/stage/3/submit", methods=["POST"])
@stage_required(3)
def stage3_submit():

    answer = request.form.get("answer", "").strip().upper()

    if answer == STAGE_3_ANSWER.upper():
        session["unlocked_stage"] = max(
            session.get("unlocked_stage", 1), 4
        )

        return redirect(url_for("stage4"))

    return render_template(
        "stage3.html",
        error="Incorrect, try again."
    )


# STAGE 4
@app.route("/stage/4")
@stage_required(4)
def stage4():
    return render_template("stage4.html")


@app.route("/stage/4/submit", methods=["POST"])
@stage_required(4)
def stage4_submit():

    answer = request.form.get("answer", "").strip()

    try:
        ipaddress.ip_address(answer)
    except ValueError:
        return render_template(
            "stage4.html",
            error="Please enter a valid IP address."
        )

    if answer == STAGE_4_ANSWER:
        return render_template(
            "stage4.html",
            success="Correct! You found the destination IP address. Stage 4 complete!"
        )

    return render_template(
        "stage4.html",
        error="Incorrect IP address. Analyse the packets and try again."
    )


if __name__ == "__main__":
    app.run(debug=True)
