import flask

from statistics import calculate_results

application = flask.Flask(__name__)


@application.route("/")
def index():
    return flask.render_template("index.html")


@application.route("/results", methods=["POST", "GET"])
def results():
    if flask.request.method == "GET":
        # user tries to access results URL directly
        return flask.render_template("results_unavailable.html")
    if flask.request.method == "POST":
        # user tries to access results URL through data submission form
        form_data = flask.request.form.copy()
        results = calculate_results(form_data)
        return flask.render_template("results.html", results=results)


if __name__ == "__main__":
    application.run(debug=True, host="0.0.0.0", port=5000)
