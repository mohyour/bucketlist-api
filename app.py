import os
from src import create_app


config_name = os.getenv("APP_SETTINGS")
app = create_app(config_name)


@app.route("/")
def home():
    return "Welcome to bucket list api"


if __name__ == "__main__":
    app.run()
