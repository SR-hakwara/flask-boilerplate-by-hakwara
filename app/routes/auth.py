from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required, login_user, logout_user
from app.forms import RegisterForm, LoginForm, UserProfileForm
from app.services import AuthService, ProfileService
from flask import session

auth_bp = Blueprint("auth", __name__, template_folder="../templates/auth")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        result = AuthService.register(form.data)
        if result.success:
            flash("Registration successful", "success")
            return redirect(url_for("auth.login"))
        flash(result.error, "warning")
    return render_template("register.html",form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        result = AuthService.login(form.data)
        if result.user:
            login_user(result.user)
            session["last_login"] = (
                result.user.last_login.strftime("%d/%m/%Y %H:%M")
                if result.user.last_login
                else "Première connexion"
            )
            result.user.update_last_login()
            return redirect(url_for("main.index"))

        flash(result.error, "warning")
    return render_template("login.html", form=form)

@auth_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = UserProfileForm()

    if form.validate_on_submit():
        # Récupère les données du formulaire
        form_data = {
            "username": form.username.data,
            "email": form.email.data,
            "password": form.password.data if form.password.data else None,
        }

        # Met à jour le profil via le service
        result = ProfileService.update_profile(current_user.id, form_data)

        if result.success:
            flash("Profil mis à jour avec succès", "success")
            return redirect(url_for("auth.profile"))
        else:
            flash(result.error, "warning")

    # Pré-remplit le formulaire avec les données actuelles de l'utilisateur
    form.username.data = current_user.username
    form.email.data = current_user.email

    return render_template("profile.html", form=form, user=current_user)

@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))