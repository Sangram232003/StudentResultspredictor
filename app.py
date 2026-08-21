from flask import Flask, request, render_template_string
import joblib
import numpy as np
import os

app = Flask(__name__)

# =========================================================
# LOAD MODEL
# =========================================================

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "random_model(1).pkl"
)

try:
    model = joblib.load(MODEL_PATH)
    model_error = None
except Exception as e:
    model = None
    model_error = str(e)


# =========================================================
# HTML + CSS + JAVASCRIPT
# Everything is inside app.py
# =========================================================

HTML = """

<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>Student Performance AI</title>

<style>

/* =====================================================
   RESET
===================================================== */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}


/* =====================================================
   BODY
===================================================== */

body {

    min-height: 100vh;

    font-family:
        "Segoe UI",
        Arial,
        sans-serif;

    color: white;

    background:
        radial-gradient(
            circle at 10% 15%,
            rgba(0, 255, 213, 0.18),
            transparent 27%
        ),

        radial-gradient(
            circle at 90% 15%,
            rgba(139, 92, 246, 0.23),
            transparent 30%
        ),

        radial-gradient(
            circle at 85% 90%,
            rgba(236, 72, 153, 0.18),
            transparent 27%
        ),

        linear-gradient(
            135deg,
            #050816,
            #0b1026,
            #12091f
        );

    overflow-x: hidden;
}


/* =====================================================
   FLOATING BACKGROUND
===================================================== */

body::before {

    content: "";

    position: fixed;

    width: 380px;
    height: 380px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            rgba(0, 255, 213, 0.16),
            transparent 70%
        );

    filter: blur(45px);

    left: -140px;
    top: -120px;

    animation:
        floatOne 8s ease-in-out infinite alternate;

    pointer-events: none;

}


body::after {

    content: "";

    position: fixed;

    width: 450px;
    height: 450px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            rgba(168, 85, 247, 0.17),
            transparent 70%
        );

    filter: blur(50px);

    right: -160px;
    bottom: -180px;

    animation:
        floatTwo 10s ease-in-out infinite alternate;

    pointer-events: none;

}


@keyframes floatOne {

    from {
        transform: translate(0, 0);
    }

    to {
        transform: translate(100px, 70px);
    }

}


@keyframes floatTwo {

    from {
        transform: translate(0, 0);
    }

    to {
        transform: translate(-90px, -70px);
    }

}


/* =====================================================
   CONTAINER
===================================================== */

.container {

    width: min(1150px, 92%);

    margin: auto;

    padding:
        45px 0 60px;

}


/* =====================================================
   HERO
===================================================== */

.hero {

    text-align: center;

    margin-bottom: 35px;

}


.badge {

    display: inline-flex;

    align-items: center;

    gap: 8px;

    padding:
        9px 18px;

    border-radius: 50px;

    background:
        rgba(0,255,213,0.07);

    border:
        1px solid
        rgba(0,255,213,0.25);

    color: #62ffe4;

    font-size: 12px;

    font-weight: 800;

    letter-spacing: 1.2px;

    margin-bottom: 20px;

}


.badge-dot {

    width: 7px;
    height: 7px;

    border-radius: 50%;

    background: #00ffd5;

    box-shadow:
        0 0 14px #00ffd5;

    animation:
        pulse 1.5s infinite;

}


@keyframes pulse {

    0%,100% {
        transform: scale(0.8);
        opacity: .5;
    }

    50% {
        transform: scale(1.2);
        opacity: 1;
    }

}


.hero h1 {

    font-size:
        clamp(40px, 7vw, 75px);

    line-height: 1;

    font-weight: 900;

    letter-spacing: -2px;

    background:

        linear-gradient(
            90deg,
            #ffffff,
            #4fffe0,
            #a78bfa,
            #f472b6,
            #ffffff
        );

    background-size: 300%;

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;

    animation:
        gradientMove 7s linear infinite;

}


@keyframes gradientMove {

    0% {
        background-position: 0%;
    }

    100% {
        background-position: 300%;
    }

}


.hero p {

    max-width: 720px;

    margin:
        20px auto 0;

    color: #9da8c2;

    font-size: 15px;

    line-height: 1.8;

}


/* =====================================================
   MAIN CARD
===================================================== */

.main-card {

    position: relative;

    padding: 32px;

    border-radius: 28px;

    background:
        rgba(15,20,43,0.76);

    border:
        1px solid
        rgba(255,255,255,0.09);

    backdrop-filter:
        blur(20px);

    -webkit-backdrop-filter:
        blur(20px);

    box-shadow:

        0 30px 90px
        rgba(0,0,0,0.38),

        inset 0 1px 0
        rgba(255,255,255,0.05);

    overflow: hidden;

}


.main-card::before {

    content: "";

    position: absolute;

    left: 0;
    right: 0;
    top: 0;

    height: 3px;

    background:

        linear-gradient(
            90deg,
            transparent,
            #00ffd5,
            #6366f1,
            #ec4899,
            transparent
        );

}


/* =====================================================
   TITLE
===================================================== */

.title {

    margin-bottom: 28px;

}


.title h2 {

    font-size: 24px;

    margin-bottom: 7px;

}


.title p {

    color: #78839f;

    font-size: 13px;

}


/* =====================================================
   FORM GRID
===================================================== */

.form-grid {

    display: grid;

    grid-template-columns:
        repeat(2, 1fr);

    gap: 20px;

}


.field {

    position: relative;

}


.field label {

    display: block;

    margin-bottom: 8px;

    font-size: 13px;

    font-weight: 700;

    color: #cbd2e5;

}


input,
select {

    width: 100%;

    padding:
        15px 16px;

    border-radius: 14px;

    border:
        1px solid
        rgba(255,255,255,0.10);

    background:
        rgba(5,9,25,0.78);

    color: white;

    outline: none;

    font-size: 14px;

    transition:
        all .25s ease;

}


input::placeholder {

    color: #5f6982;

}


input:hover,
select:hover {

    border-color:
        rgba(255,255,255,.22);

}


input:focus,
select:focus {

    border-color:
        #00ffd5;

    box-shadow:

        0 0 0 3px
        rgba(0,255,213,.07),

        0 0 25px
        rgba(0,255,213,.08);

    transform:
        translateY(-1px);

}


select option {

    background:
        #10152c;

    color: white;

}


.help {

    display: block;

    margin-top: 6px;

    color: #5f6a85;

    font-size: 10px;

}


/* =====================================================
   COLORED LABELS
===================================================== */

.field:nth-child(1) label {
    color: #67e8f9;
}

.field:nth-child(2) label {
    color: #c4b5fd;
}

.field:nth-child(3) label {
    color: #86efac;
}

.field:nth-child(4) label {
    color: #f9a8d4;
}

.field:nth-child(5) label {
    color: #fde68a;
}

.field:nth-child(6) label {
    color: #93c5fd;
}

.field:nth-child(7) label {
    color: #f0abfc;
}

.field:nth-child(8) label {
    color: #5eead4;
}


/* =====================================================
   PREDICT BUTTON
===================================================== */

.predict-btn {

    position: relative;

    width: 100%;

    margin-top: 28px;

    padding: 17px;

    border: none;

    border-radius: 16px;

    cursor: pointer;

    overflow: hidden;

    color: white;

    font-size: 15px;

    font-weight: 800;

    letter-spacing: .6px;

    background:

        linear-gradient(
            100deg,
            #00c9a7,
            #06b6d4,
            #6366f1,
            #a855f7,
            #ec4899
        );

    background-size: 300%;

    box-shadow:

        0 15px 40px
        rgba(99,102,241,.22);

    transition:
        all .3s ease;

    animation:
        buttonGradient 6s ease infinite;

}


@keyframes buttonGradient {

    0% {
        background-position: 0%;
    }

    50% {
        background-position: 100%;
    }

    100% {
        background-position: 0%;
    }

}


.predict-btn:hover {

    transform:
        translateY(-3px);

    box-shadow:

        0 20px 55px
        rgba(99,102,241,.32),

        0 0 30px
        rgba(0,255,213,.10);

}


.predict-btn:active {

    transform:
        scale(.98);

}


/* =====================================================
   BUTTON SHINE EFFECT
===================================================== */

.predict-btn::before {

    content: "";

    position: absolute;

    top: 0;
    left: -120%;

    width: 70%;
    height: 100%;

    background:

        linear-gradient(
            90deg,
            transparent,
            rgba(255,255,255,.35),
            transparent
        );

    transform:
        skewX(-20deg);

}


.predict-btn:hover::before {

    animation:
        shine .8s ease;

}


@keyframes shine {

    from {
        left: -120%;
    }

    to {
        left: 150%;
    }

}


/* =====================================================
   LOADING STATE
===================================================== */

.predict-btn.loading {

    cursor:
        not-allowed;

    transform:
        scale(.99);

    background:
        linear-gradient(
            90deg,
            #111827,
            #26324f,
            #111827
        );

    background-size:
        200%;

    animation:
        loadingBackground 1.2s linear infinite;

}


@keyframes loadingBackground {

    0% {
        background-position: 0%;
    }

    100% {
        background-position: 200%;
    }

}


.spinner {

    display: inline-block;

    width: 17px;
    height: 17px;

    border-radius: 50%;

    border:
        3px solid
        rgba(255,255,255,.25);

    border-top-color:
        white;

    vertical-align:
        middle;

    margin-right: 9px;

    animation:
        spin .7s linear infinite;

}


@keyframes spin {

    to {
        transform:
            rotate(360deg);
    }

}


/* =====================================================
   RESULT
===================================================== */

.result {

    margin-top: 28px;

    padding: 30px;

    border-radius: 22px;

    text-align: center;

    background:

        linear-gradient(
            135deg,
            rgba(0,255,213,.07),
            rgba(99,102,241,.10),
            rgba(236,72,153,.07)
        );

    border:
        1px solid
        rgba(0,255,213,.22);

    animation:
        resultAppear .7s cubic-bezier(.2,.8,.2,1);

}


@keyframes resultAppear {

    0% {

        opacity: 0;

        transform:
            translateY(35px)
            scale(.90);

    }

    60% {

        transform:
            translateY(-5px)
            scale(1.02);

    }

    100% {

        opacity: 1;

        transform:
            translateY(0)
            scale(1);

    }

}


.result-icon {

    font-size: 52px;

    margin-bottom: 10px;

    animation:
        iconPop .7s ease;

}


@keyframes iconPop {

    0% {
        transform:
            scale(0)
            rotate(-30deg);
    }

    70% {
        transform:
            scale(1.15)
            rotate(5deg);
    }

    100% {
        transform:
            scale(1)
            rotate(0);
    }

}


.result h2 {

    font-size: 29px;

    margin-bottom: 8px;

}


.result p {

    max-width: 600px;

    margin: auto;

    color: #a7b0c7;

    font-size: 13px;

    line-height: 1.7;

}


.prediction-pill {

    display: inline-block;

    margin-top: 17px;

    padding:
        9px 18px;

    border-radius: 50px;

    background:
        rgba(255,255,255,.06);

    border:
        1px solid
        rgba(255,255,255,.08);

    color: #65ffe5;

    font-size: 11px;

    font-weight: 800;

    letter-spacing: 1px;

}


/* =====================================================
   FEATURE CARDS
===================================================== */

.features {

    display: grid;

    grid-template-columns:
        repeat(3,1fr);

    gap: 16px;

    margin-top: 20px;

}


.feature {

    padding: 22px;

    border-radius: 19px;

    background:
        rgba(255,255,255,.035);

    border:
        1px solid
        rgba(255,255,255,.07);

    transition:
        .3s ease;

}


.feature:hover {

    transform:
        translateY(-6px);

    background:
        rgba(255,255,255,.055);

    border-color:
        rgba(0,255,213,.18);

}


.feature-icon {

    font-size: 28px;

    margin-bottom: 12px;

}


.feature h3 {

    font-size: 15px;

    margin-bottom: 7px;

}


.feature p {

    color: #717c97;

    font-size: 12px;

    line-height: 1.6;

}


/* =====================================================
   ERROR
===================================================== */

.error {

    margin-top: 20px;

    padding: 15px;

    border-radius: 14px;

    background:
        rgba(244,63,94,.10);

    border:
        1px solid
        rgba(244,63,94,.25);

    color: #fda4af;

    font-size: 13px;

}


/* =====================================================
   FOOTER
===================================================== */

footer {

    text-align: center;

    margin-top: 30px;

    color: #59637c;

    font-size: 11px;

}


.footer-dot {

    display: inline-block;

    width: 6px;
    height: 6px;

    border-radius: 50%;

    background:
        #00ffd5;

    box-shadow:
        0 0 10px #00ffd5;

    margin-right: 5px;

}


/* =====================================================
   MOBILE
===================================================== */

@media(max-width:760px) {

    .container {

        width: 94%;

        padding-top: 25px;

    }


    .main-card {

        padding: 20px;

        border-radius: 22px;

    }


    .form-grid {

        grid-template-columns:
            1fr;

    }


    .features {

        grid-template-columns:
            1fr;

    }


    .hero h1 {

        font-size: 43px;

        letter-spacing: -1px;

    }

}

</style>

</head>


<body>


<div class="container">


<!-- =====================================================
     HERO
===================================================== -->

<section class="hero">

<div class="badge">

<span class="badge-dot"></span>

AI STUDENT PERFORMANCE ANALYZER

</div>


<h1>

Student Performance<br>

AI Predictor

</h1>


<p>

Enter your academic information and let our
Random Forest Machine Learning model predict
your expected academic outcome instantly.

</p>

</section>



<!-- =====================================================
     MAIN CARD
===================================================== -->

<div class="main-card">


<div class="title">

<h2>
    ✦ Academic Profile
</h2>

<p>
    Enter the information required by the trained model.
</p>

</div>



<form
    method="POST"
    id="predictionForm"
    onsubmit="startPrediction()"
>


<div class="form-grid">


<!-- AGE -->

<div class="field">

<label>
    👤 Age
</label>

<input
    type="number"
    name="Age"
    min="1"
    max="100"
    placeholder="Example: 21"
    required
>

<span class="help">
    Your current age
</span>

</div>



<!-- GENDER -->

<div class="field">

<label>
    ◉ Gender
</label>

<select
    name="Gender"
    required
>

<option value="">
    Select Gender
</option>

<option value="0">
    Male
</option>

<option value="1">
    Female
</option>

</select>

<span class="help">
    Use the encoding from your training data
</span>

</div>



<!-- DEPARTMENT -->

<div class="field">

<label>
    🎓 Department
</label>

<select
    name="Department"
    required
>

<option value="">
    Select Department
</option>

<option value="0">
    Computer Science
</option>

<option value="1">
    Information Technology
</option>

<option value="2">
    Electronics
</option>

<option value="3">
    Mechanical
</option>

<option value="4">
    Civil
</option>

</select>

<span class="help">
    Select your department
</span>

</div>



<!-- STUDY HOURS -->

<div class="field">

<label>
    📚 Study Hours Per Day
</label>

<input
    type="number"
    name="Study_Hours_Per_Day"
    min="0"
    max="24"
    step="0.1"
    placeholder="Example: 6.5"
    required
>

<span class="help">
    Average daily study hours
</span>

</div>



<!-- ATTENDANCE -->

<div class="field">

<label>
    📊 Attendance Percentage
</label>

<input
    type="number"
    name="Attendance_Percentage"
    min="0"
    max="100"
    step="0.1"
    placeholder="Example: 85"
    required
>

<span class="help">
    Attendance percentage
</span>

</div>



<!-- ASSIGNMENTS -->

<div class="field">

<label>
    📝 Assignments Completed
</label>

<input
    type="number"
    name="Assignments_Completed"
    min="0"
    step="1"
    placeholder="Example: 8"
    required
>

<span class="help">
    Number of completed assignments
</span>

</div>



<!-- MIDTERM -->

<div class="field">

<label>
    📖 Midterm Score
</label>

<input
    type="number"
    name="Midterm_Score"
    min="0"
    max="100"
    step="0.1"
    placeholder="Example: 72"
    required
>

<span class="help">
    Midterm examination score
</span>

</div>



<!-- FINAL -->

<div class="field">

<label>
    🏆 Final Score
</label>

<input
    type="number"
    name="Final_Score"
    min="0"
    max="100"
    step="0.1"
    placeholder="Example: 78"
    required
>

<span class="help">
    Final examination score
</span>

</div>


</div>



<!-- =====================================================
     PREDICT BUTTON
===================================================== -->

<button
    type="submit"
    class="predict-btn"
    id="predictButton"
>

<span id="buttonText">

    ✦ PREDICT STUDENT PERFORMANCE

</span>

</button>


</form>



<!-- =====================================================
     RESULT
===================================================== -->

{% if prediction is not none %}

<div class="result">


<div class="result-icon">

{% if prediction == "Pass" %}

🎉

{% else %}

📊

{% endif %}

</div>



{% if prediction == "Pass" %}

<h2>
    🎉 Predicted Result: PASS
</h2>

<p>

Great! Based on the information provided,
the Random Forest model predicts a
<strong>Pass</strong> outcome.

</p>

{% else %}

<h2>
    📊 Predicted Result: FAIL
</h2>

<p>

Based on the academic profile entered,
the Random Forest model predicts a
<strong>Fail</strong> outcome.

</p>

{% endif %}



<div class="prediction-pill">

MODEL OUTPUT: {{ prediction }}

</div>


</div>

{% endif %}



{% if error %}

<div class="error">

⚠ {{ error }}

</div>

{% endif %}


</div>



<!-- =====================================================
     FEATURE CARDS
===================================================== -->

<div class="features">


<div class="feature">

<div class="feature-icon">
    🤖
</div>

<h3>
    Random Forest AI
</h3>

<p>
    Your trained Random Forest model analyzes
    the academic information and generates
    a prediction.
</p>

</div>



<div class="feature">

<div class="feature-icon">
    📈
</div>

<h3>
    Academic Analysis
</h3>

<p>
    Study hours, attendance, assignments,
    midterm and final scores are considered.
</p>

</div>



<div class="feature">

<div class="feature-icon">
    ⚡
</div>

<h3>
    Instant Prediction
</h3>

<p>
    Click the prediction button and receive
    your Machine Learning result instantly.
</p>

</div>


</div>



<footer>

<span class="footer-dot"></span>

Student Performance AI
•
Machine Learning Application

</footer>


</div>



<!-- =====================================================
     JAVASCRIPT
===================================================== -->

<script>

function startPrediction() {

    const button =
        document.getElementById(
            "predictButton"
        );

    const text =
        document.getElementById(
            "buttonText"
        );


    /*
       Prevent double clicking
    */

    button.disabled = true;


    /*
       Add loading class
    */

    button.classList.add(
        "loading"
    );


    /*
       Show spinner + analyzing text
    */

    text.innerHTML = `

        <span class="spinner"></span>

        ANALYZING PERFORMANCE...

    `;


    /*
       The form continues submitting normally.
       Flask will process the prediction.
    */

}

</script>


</body>

</html>

"""


# =========================================================
# FLASK ROUTE
# =========================================================

@app.route("/", methods=["GET", "POST"])
def home():

    prediction = None
    error = None


    if request.method == "POST":

        try:

            if model is None:

                raise Exception(
                    "Model could not be loaded: "
                    + str(model_error)
                )


            # =================================================
            # EXACT FEATURE ORDER FROM THE MODEL
            # =================================================

            features = [

                float(
                    request.form["Age"]
                ),

                float(
                    request.form["Gender"]
                ),

                float(
                    request.form["Department"]
                ),

                float(
                    request.form[
                        "Study_Hours_Per_Day"
                    ]
                ),

                float(
                    request.form[
                        "Attendance_Percentage"
                    ]
                ),

                float(
                    request.form[
                        "Assignments_Completed"
                    ]
                ),

                float(
                    request.form[
                        "Midterm_Score"
                    ]
                ),

                float(
                    request.form[
                        "Final_Score"
                    ]
                )

            ]


            # Convert to NumPy

            input_data = np.array(
                features,
                dtype=float
            ).reshape(
                1,
                -1
            )


            # =================================================
            # PREDICTION
            # =================================================

            prediction = model.predict(
                input_data
            )[0]


            prediction = str(
                prediction
            )


        except Exception as e:

            error = (
                "Prediction Error: "
                + str(e)
            )


    return render_template_string(

        HTML,

        prediction=prediction,

        error=error

    )


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(

        host="0.0.0.0",

        port=port,

        debug=False

    )
