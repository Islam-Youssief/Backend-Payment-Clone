from flask import Flask
from routes.payments_getaway import payments_bp
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(payments_bp, url_prefix="/api/v1")


@app.route("/")
def home():
    return {"message": "Mock Payment Gateway is running"}


if __name__ == "__main__":
    app.run(debug=True)