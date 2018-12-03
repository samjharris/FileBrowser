from flask import Flask, flash, render_template


class VueFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(variable_start_string="((", variable_end_string="))"))


app = VueFlask(__name__)
app.config["WTF_CSRF_METHODS"] = []


@app.route("/")
def test():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
