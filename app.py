from flask import Flask, render_template_string, request, redirect, jsonify

app = Flask(__name__)

# Temporary queue - server restart aana fresh ah start aagum
queue = []
token_number = 0


HTML = """
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>QueueLess</title>

<style>

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: Arial, Helvetica, sans-serif;
    background: #f4faf7;
    color: #17231d;
    min-height: 100vh;
}

/* NAVBAR */

.navbar {
    height: 76px;
    background: white;
    border-bottom: 1px solid #e4eee8;

    display: flex;
    align-items: center;
    justify-content: space-between;

    padding: 0 6%;
    position: sticky;
    top: 0;
    z-index: 10;
}

.logo {
    font-size: 27px;
    font-weight: 800;
    letter-spacing: -1px;
}

.logo span {
    color: #16a36b;
}

.status {
    display: flex;
    align-items: center;
    gap: 8px;

    padding: 9px 15px;
    border-radius: 30px;

    background: #ecfaf3;
    color: #16885b;

    font-size: 13px;
    font-weight: 600;
}

.dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #18b874;
}

/* MAIN */

.container {
    width: 88%;
    max-width: 1250px;
    margin: auto;
}

/* HERO */

.hero {
    padding: 70px 0 45px;
}

.hero h1 {
    font-size: clamp(45px, 7vw, 78px);
    line-height: 0.98;
    letter-spacing: -4px;
    max-width: 850px;
}

.hero h1 span {
    color: #16a36b;
}

.hero p {
    margin-top: 22px;
    max-width: 680px;

    color: #718078;
    font-size: 18px;
    line-height: 1.7;
}

/* DASHBOARD */

.dashboard {
    display: grid;
    grid-template-columns: 380px 1fr;
    gap: 25px;
    padding-bottom: 50px;
}

/* CARD */

.card {
    background: white;
    border: 1px solid #e1ebe5;
    border-radius: 24px;
    padding: 30px;

    box-shadow: 0 15px 45px rgba(30, 80, 55, 0.07);
}

.card-title {
    font-size: 22px;
    font-weight: 750;
}

.card-subtitle {
    color: #87948d;
    font-size: 14px;
    margin-top: 7px;
    margin-bottom: 25px;
}

/* FORM */

label {
    display: block;
    margin-top: 18px;
    margin-bottom: 8px;

    color: #52625a;
    font-size: 13px;
    font-weight: 600;
}

input,
select {
    width: 100%;

    padding: 16px;

    border: 1px solid #dce7e1;
    border-radius: 13px;

    background: #fbfdfc;
    color: #17231d;

    font-size: 15px;
    outline: none;
}

input:focus,
select:focus {
    border-color: #20b477;
    box-shadow: 0 0 0 4px rgba(32,180,119,0.10);
}

/* BUTTON */

button {
    width: 100%;

    border: none;
    border-radius: 13px;

    padding: 16px;
    margin-top: 22px;

    background: #16a36b;
    color: white;

    font-size: 15px;
    font-weight: 700;

    cursor: pointer;

    transition: 0.2s;
}

button:hover {
    background: #108957;
    transform: translateY(-2px);
}

/* QUEUE HEADER */

.queue-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    margin-bottom: 22px;
}

.people-count {
    background: #ecfaf3;
    color: #16885b;

    border: 1px solid #d2f0e1;

    padding: 8px 14px;
    border-radius: 30px;

    font-size: 12px;
    font-weight: 700;
}

/* QUEUE ITEM */

.person {
    display: grid;
    grid-template-columns: 90px 1fr 150px;

    align-items: center;
    gap: 20px;

    padding: 18px;

    margin-bottom: 13px;

    border: 1px solid #e4eee8;
    border-radius: 18px;

    background: #fbfdfc;

    transition: 0.2s;
}

.person:hover {
    border-color: #b9dfcc;
    box-shadow: 0 8px 25px rgba(30,100,65,0.06);
}

/* TOKEN */

.token {
    background: #eaf9f1;
    color: #128457;

    border-radius: 14px;

    padding: 11px 5px;

    text-align: center;

    border: 1px solid #d1efdf;
}

.token small {
    display: block;
    font-size: 9px;
    color: #67907c;
}

.token-number {
    font-size: 23px;
    font-weight: 800;
    margin-top: 3px;
}

/* INFO */

.name {
    font-size: 17px;
    font-weight: 750;
}

.service {
    color: #7a8981;
    font-size: 13px;
    margin-top: 5px;
}

.position {
    color: #16a36b;
    font-size: 12px;
    margin-top: 7px;
    font-weight: 600;
}

/* WAIT */

.wait {
    text-align: right;
}

.wait-number {
    color: #16a36b;
    font-size: 18px;
    font-weight: 800;
}

.wait-label {
    color: #9aa69f;
    font-size: 10px;
    margin-top: 4px;
}

/* FINISH */

.finish-btn {
    margin-top: 10px;

    padding: 9px 12px;

    background: white;
    color: #dc665d;

    border: 1px solid #f0cbc7;

    font-size: 12px;

    box-shadow: none;
}

.finish-btn:hover {
    background: #fff4f3;
    color: #c94d44;
}

/* EMPTY */

.empty {
    text-align: center;
    padding: 70px 20px;
    color: #91a099;
}

.empty-icon {
    font-size: 45px;
    margin-bottom: 12px;
}

/* SAVE AREA */

.save-area {
    display: flex;
    gap: 12px;
    margin-top: 20px;
}

.save-area button {
    margin-top: 0;
}

.new-btn {
    background: white;
    color: #16a36b;
    border: 1px solid #bde4d0;
}

.new-btn:hover {
    background: #ecfaf3;
}

/* FOOTER */

.footer {
    text-align: center;
    padding: 25px;

    color: #8b9992;
    font-size: 12px;
}


/* MOBILE */

@media (max-width: 850px) {

    .dashboard {
        grid-template-columns: 1fr;
    }

    .hero {
        padding-top: 50px;
    }

}

@media (max-width: 600px) {

    .container {
        width: 92%;
    }

    .navbar {
        padding: 0 4%;
    }

    .hero h1 {
        letter-spacing: -2px;
    }

    .person {
        grid-template-columns: 70px 1fr;
    }

    .wait {
        grid-column: 2;
        text-align: left;
    }

}

</style>

</head>


<body>


<!-- NAVBAR -->

<div class="navbar">

    <div class="logo">
        Queue<span>Less</span>
    </div>

    <div class="status">
        <div class="dot"></div>
        System Live
    </div>

</div>


<div class="container">


<!-- HERO -->

<section class="hero">

    <h1>
        Skip the queue.<br>
        <span>Save your time.</span>
    </h1>

    <p>
        Book your digital token remotely, track your queue position,
        and arrive when it's your turn.
    </p>

</section>


<!-- DASHBOARD -->

<div class="dashboard">


<!-- BOOK TOKEN -->

<div class="card">

    <div class="card-title">
        🎟️ Book a Token
    </div>

    <div class="card-subtitle">
        Join the queue in a few seconds.
    </div>


    <form method="POST">

        <label>Your Name</label>

        <input
            type="text"
            name="name"
            placeholder="Enter your name"
            required
        >


        <label>Select Service</label>

        <select name="service" required>

            <option value="">
                Select a service
            </option>

            <option value="Hospital">
                🏥 Hospital
            </option>

            <option value="Bank">
                🏦 Bank
            </option>

            <option value="College Office">
                🎓 College Office
            </option>

            <option value="Government Office">
                🏛️ Government Office
            </option>

            <option value="Service Centre">
                🔧 Service Centre
            </option>

        </select>


        <button type="submit">
            Get My Token →
        </button>

    </form>

</div>


<!-- LIVE QUEUE -->

<div class="card">

    <div class="queue-header">

        <div>

            <div class="card-title">
                Live Queue
            </div>

            <div class="card-subtitle"
                 style="margin-bottom:0;">
                People currently waiting
            </div>

        </div>

        <div class="people-count">
            {{ queue|length }} PEOPLE
        </div>

    </div>


    {% if queue %}

        {% for person in queue %}

        <div class="person">


            <div class="token">

                <small>TOKEN</small>

                <div class="token-number">
                    #{{ person.token }}
                </div>

            </div>


            <div>

                <div class="name">
                    {{ person.name }}
                </div>

                <div class="service">
                    {{ person.service }}
                </div>

                <div class="position">
                    Position #{{ loop.index }}
                </div>

            </div>


            <div class="wait">

                <div class="wait-number">
                    {{ loop.index * 5 }} min
                </div>

                <div class="wait-label">
                    EST. WAIT
                </div>


                <form
                    method="POST"
                    action="/finish/{{ person.token }}"
                >

                    <button
                        type="submit"
                        class="finish-btn"
                    >
                        ✓ Finish
                    </button>

                </form>

            </div>


        </div>

        {% endfor %}

    {% else %}

        <div class="empty">

            <div class="empty-icon">
                🎟️
            </div>

            <div>
                No active tokens
            </div>

            <small>
                Book a token to start the queue.
            </small>

        </div>

    {% endif %}


    <!-- SAVE / NEW -->

    <div class="save-area">

        <button
            type="button"
            onclick="saveQueue()"
        >
            💾 Save Queue
        </button>

        <button
            type="button"
            class="new-btn"
            onclick="newSession()"
        >
            🆕 New Session
        </button>

    </div>

</div>

</div>


<div class="footer">
    QueueLess • Smart Queue Management System
</div>


</div>


<script>

/*
    SAVE QUEUE

    Browser localStorage-la current queue save pannum.
*/

function saveQueue() {

    const queueData = {{ queue | tojson }};

    localStorage.setItem(
        "queueless_saved_queue",
        JSON.stringify(queueData)
    );

    localStorage.setItem(
        "queueless_saved",
        "true"
    );

    alert("Queue saved successfully! 💾");

}


/*
    NEW SESSION

    Saved data-a delete pannitu
    fresh session start pannum.
*/

function newSession() {

    const confirmNew = confirm(
        "Start a new session? Saved queue will be removed."
    );

    if (confirmNew) {

        localStorage.removeItem(
            "queueless_saved_queue"
        );

        localStorage.removeItem(
            "queueless_saved"
        );

        window.location.href = "/new";

    }

}

</script>


</body>

</html>
"""


# HOME

@app.route("/", methods=["GET", "POST"])
def home():

    global token_number

    if request.method == "POST":

        name = request.form.get("name")
        service = request.form.get("service")

        token_number += 1

        queue.append({
            "token": token_number,
            "name": name,
            "service": service
        })

        return redirect("/")

    return render_template_string(
        HTML,
        queue=queue
    )


# FINISH TOKEN

@app.route("/finish/<int:token>", methods=["POST"])
def finish_token(token):

    global queue

    queue = [
        person
        for person in queue
        if person["token"] != token
    ]

    return redirect("/")


# NEW SESSION

@app.route("/new")
def new_session():

    global queue
    global token_number

    queue = []
    token_number = 0

    return redirect("/")


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )