# The intro from the following code is from CS psets 7 and 8
import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

# Configure application
app = Flask(__name__, static_url_path='/static')

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("quiz.html")

# Determine the user's spirit Vine
@app.route("/form", methods=["POST"])
def post_form():
    # Uses the answers to the first three questions to determine introversion or extroversion
    # The rest of the Vine deciding is a series of for loops, structured according to our magical formula
    # Starts with a pool of eight vines, and future questions go down a binary tree we've predetermined
    i_count = 0;
    if request.form.get("q1")== "i":
        i_count += 1
    if request.form.get("q2")== "i":
        i_count += 1
    if request.form.get("q3")== "i":
        i_count += 1
    # Introverted path
    if i_count > 1:
        if request.form.get("q5") == "cut":
            if request.form.get("q7") == "croissant":
                # I COULD HAVE DROPPED MY CROISSANT
                return render_template("results.html", title="I could have dropped my croissant!", url="hRFUZBXOWZI", description="You are kind and caring and always look out for others before yourself. You are extremely precious and it is hard to come by people like you in this world. You care deeply about others and the world and is secretly an introvert.")
            else:
                # I'M SENSITIVE, AUBREY
                return render_template("results.html", title="I'M SENSITIVE, AUBREY!", url="7xZDaw2H9GU", description= "You are typically a sensitive person that takes into account everything others say, sometimes too personally. You are also somewhat clumsy and most likely have a true age somewhere between 13-17, those darn angsty teenage years.")
        elif request.form.get("q8") == "road":
            # ROAD WORK AHEAD
            return render_template("results.html", title="Road work ahead!", url="6AYv6rV3NXE", description= "You are sassy, but down to Earth, and everyone loves being around you. You have an uncomparable sense of humor, but sometimes, you come off as too sarcastic. However, with the correct audience you are the life of the party and always a loyal friend. You will grow up to wield an arsenal of dad jokes in which you will use at every opportunity.")
        else:
            # GOOD EVENING
            return render_template("results.html", title="Good evening!", url="OyBmEeojfKo", description= "You are smooth in both actions and words and others often look at you in envy because of your mad stylishness. Sliding in and out and those dms are no problem for you and you can strike up a conversation with almost anyone. Your sense of humor is unique in its own special way.")
    # Extroverted path
    else:
        if request.form.get("q6") == "bump":
            #KING BACH
            if request.form.get("q9") == "kb":
                return render_template("results.html", title="What's up, brah!", url="kNsYxYOcSwc", description= "You act hard and possess so much swagger but when adversity presents itself, you react with gentleness. You hit the gym often and people can be intimidated by you but you're actually a gentle giant inside. You like to wear tight shirts to flex on em and sometimes you're guilty of saying you got a woman at home when you really don't.")

            else:
            #ASK ALL MY FRIENDS IF I'M THE NICEST...
                return render_template("results.html", title="Ask all my friends...", url="UGTNAnQFpUE", description= "You are a protective and caring soul and their are a lot of things on this Earth that are precious to you and worth protecting. Yet sometimes you take things too seriously and come off as overprotective when others are just joking. You're also extremely patriotic and probably own at least three American flags.")

        elif request.form.get("q10") == "be me":
            #IT'S GONNA BE ME
            return render_template("results.html", title="It's Gonna Be Me!", url="t0R13Ix2630", description= "You're the type to pull up at red lights, roll down your windows, and serenade the other drivers around you. You listen to the good ol bops and quality music and everyone claims that you have a good music taste. You're playlist is absolute fire and you carry your aux cord and speakers with you wherever you go. Furthermore, you have little grooves to whip out to every song you listen to.")

        else:
            #ARKANSAS AND KANSAS
            return render_template("results.html", title= "I am confusion!", url="BXt6NwKGJW0", description="You take everything as they come quite literally and often question other's thoughts when they don't align with your own. Sometimes, you come off as incredibly funny to your friends because you are lost by something that should seem obvious. You are most likely active in the Subtle Asian traits Facebook page.")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return render_template("error.html", message="Not all fields were filled in")


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)