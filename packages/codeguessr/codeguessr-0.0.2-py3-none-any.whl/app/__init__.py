"""Shim to provide the Flask application."""
import argparse

from app import app

create_app = app.create_app

def main() -> None:
    """Entry-point to the application on CLI."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root_dir", dest="filename", help="Provide the root path of the directory to guess.", default=None
    )
    parser.add_argument(
        "--host", help="Hostname to bind to.", default="0.0.0.0"
    )
    parser.add_argument(
        "--port", help="Port to bind to.", default=8080
    )

    args = parser.parse_args()
    app = create_app(args.filename)
    app.run(host=args.host, port=args.port)
