"""Main app/routing file for Twitoff."""

from os import getenv

from flask import Flask, render_template

from .models import DB, User, insert_example_users


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    DB.init_app(app)

    @app.route('/')
    def root():
        DB.drop_all()
        DB.create_all()
        insert_example_users()
        return render_template(
            'base.html', title="Home", users=User.query.all()
        )

    @app.route('/goodbye')
    def goodbye():
        return "Goodbye, Twitoff!"

    return app
