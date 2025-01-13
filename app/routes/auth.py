from flask import Blueprint, render_template, redirect, url_for, flash, request


auth_bp = Blueprint("auth", __name__,template_folder="../templates/auth")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Handle registration form submission
        pass
    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Handle login form submission
        pass
    return render_template("login.html")