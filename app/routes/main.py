from flask import Blueprint, render_template, redirect, url_for, flash, request

main_bp = Blueprint("main", __name__,template_folder="../templates")

@main_bp.route("/")
def index():
    return render_template("index.html")