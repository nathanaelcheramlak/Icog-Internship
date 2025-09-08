from flask import Flask

from auth.routes import auth_bp
from movies.routes import movies_bp
from recommendation.routes import rec_bp

def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(movies_bp, url_prefix="/movies")
    app.register_blueprint(rec_bp, url_prefix="/recommendations")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
