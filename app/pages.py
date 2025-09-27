from flask import Blueprint, render_template


pages = Blueprint("pages", __name__)


@pages.get("/")
def home():
    return render_template("index.html")


@pages.get("/login")
def login_page():
    return render_template("auth_login.html")


@pages.get("/register")
def register_page():
    return render_template("auth_register.html")


@pages.get("/quests")
def quests_page():
    return render_template("quests.html")


@pages.get("/leaderboard")
def leaderboard_page():
    return render_template("leaderboard.html")      