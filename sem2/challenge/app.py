
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Correct answers live here, server-side only.

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


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/stage/1", methods=["GET"])
def stage1():
    return render_template("stage1.html")


@app.route("/stage/1/submit", methods=["POST"])
def stage1_submit():
    for question in STAGE_1_ANSWERS:
        answer = request.form.get(question, "").strip().lower()

        if answer != STAGE_1_ANSWERS[question]:
            return render_template(
                "stage1.html",
                error="One or more answers are incorrect. Try again."
            )

    return redirect(url_for("stage2"))



@app.route("/stage/2", methods=["GET"])
def stage2():
    return render_template("stage2.html")


@app.route("/stage/2/submit", methods=["POST"])
def stage2_submit():
    answer = request.form.get("answer", "").strip().lower()

    if answer == STAGE_2_ANSWER:
        return redirect(url_for("stage3"))

    return render_template(
        "stage2.html",
        error="Incorrect, try again."
    )



@app.route("/stage/3", methods=["GET"])
def stage3():
    return render_template("stage3.html")


@app.route("/stage/3/submit", methods=["POST"])
def stage3_submit():
    answer = request.form.get("answer", "").strip().upper()

    if answer == STAGE_3_ANSWER:
        return redirect(url_for("stage4"))

    return render_template(
        "stage3.html",
        error="Incorrect, try again."
    )


@app.route("/stage/4", methods=["GET"])
def stage4():
    return render_template("stage4.html")


@app.route("/stage/4/submit", methods=["POST"])
def stage4_submit():
    answer = request.form.get("answer", "").strip()

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
