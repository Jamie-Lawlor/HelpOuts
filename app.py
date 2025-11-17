from flask import Flask
import os
from db.database import db
from db.modals import Users
from initial_screen.index import index_blueprint
from nav_bar.nav_bar import navbar_blueprint
from add_post.add_post import add_post_blueprint
from home_page.home import home_blueprint
from inbox.inbox import inbox_blueprint
from settings.settings import settings_blueprint
from user_profile.user_profile import user_profile_blueprint
from register_account.register_account import register_account_blueprint
from helper_register_account.helper_register_account import (
    helper_register_account_blueprint,
)


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URL")

app.secret_key = "TODO_BAD_SECRET_KEY"


# migrate = Migrate(app.db)
app.register_blueprint(index_blueprint)
app.register_blueprint(navbar_blueprint)
app.register_blueprint(add_post_blueprint, url_prefix="/add_post")
app.register_blueprint(home_blueprint, url_prefix="/home_page")
app.register_blueprint(inbox_blueprint, url_prefix="/inbox")
app.register_blueprint(settings_blueprint, url_prefix="/settings")
app.register_blueprint(user_profile_blueprint, url_prefix="/user_profile")
app.register_blueprint(register_account_blueprint, url_prefix="/register_page")
app.register_blueprint(
    helper_register_account_blueprint, url_prefix="/helper_register_page"
)


if __name__ == "__main__":
    app.run(debug=True)
