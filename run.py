# -------------------------------------------------
# Entry point that creates the Flask app, registers
# the UI blueprint (client) and the API blueprint
# (server), then runs the development server.
# -------------------------------------------------
from flask import Flask
from app.blueprints.router import client_bp

def create_app() -> Flask:
    app = Flask(__name__, static_folder="app/static", template_folder="app/templates")
    app.secret_key = "replace‑this‑with‑a‑secure‑random‑value"
    # Register blueprints
    # app.register_blueprint(app_bp)     # Health check endpoints (/ping, /active)
    app.register_blueprint(client_bp)  # UI routes (ETL wizard)
    return app

if __name__ == "__main__":
    # Debug mode is fine for local development
    create_app().run(host="127.0.0.1", port=5001, debug=True)