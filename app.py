from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from pathlib import Path
import archiver
from pprint import pprint

app = Flask(__name__)
CORS(app)


class LoggingMiddleware(object):
    def __init__(self, app):
        self._app = app

    def __call__(self, env, resp):
        errorlog = env['wsgi.errors']
        pprint(('REQUEST', env), stream=errorlog)

        def log_response(status, headers, *args):
            pprint(('RESPONSE', status, headers), stream=errorlog)
            return resp(status, headers, *args)

        return self._app(env, log_response)


@app.route("/")
def homepage():
    logs_path = Path("logs", "archiver.log")
    if not logs_path.exists():
        return render_template("homepage.html", data=None)
    with Path("logs", "archiver.log").open(mode="r") as f:
        lines = f.read().splitlines()
    data = []
    for line in lines:
        columns = [col.strip() for col in line.split(" - ") if col]
        data.append(columns)
    return render_template("homepage.html", data=data)


@app.post("/archive")
def archive_post():
    values = request.get_json()
    if not values:
        response = {
            "message": "No data found."
        }
        return jsonify(response), 400
    if "url" not in values:
        response = {
            "message": "No URL data found."
        }
        return jsonify(response), 400
    archive_url = values.get("url")
    if archive_url == "about:blank":
        response = {
            "message": "URL is about:blank"
        }
        return jsonify(response), 400
    archiver.archive_url(archive_url)
    return f"Archived url at {archive_url}"


if __name__ == "__main__":
    # app.wsgi_app = LoggingMiddleware(app.wsgi_app)
    app.run(debug=True, host="127.0.0.1", port=5000)
    # app.run(debug=True, host="192.168.56.1",)
