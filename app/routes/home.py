from flask import render_template


def register_home_routes(app):

    @app.route("/")
    def home():
        return render_template("home.html")