from flask import Flask, abort, redirect, request, jsonify

from model.iban import Iban
from model.iban import IbanInvalidCharactersError, IbanTooLongError


# Application factory method for our endpoint/app
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_pyfile("flask.cfg", silent=True)
    else:
        app.config.from_mapping(test_config)

    @app.route("/")
    def root():
        # Redirect to our default "Hello there!" for the time being
        return redirect("hello", code=302)

    @app.route("/validate", methods=["GET", "POST"])
    def validate():
        if request.method == "GET":
            args = request.args

            if "account" in args:
                # Forcing account_data to be a string will yield None if the parameter isn't of that type
                account_data = request.args.get("account", type=str)

                # Instantiate an Iban object and validate it
                if account_data:
                    try:
                        account = Iban(account_data)
                    except (
                        IbanInvalidCharactersError,
                        IbanTooLongError,
                    ) as iban_error:
                        res = {"error": str(iban_error)}
                    else:
                        if account.is_correct():
                            res = {account.iban: "OK"}
                        else:
                            # TODO: Consider reporting the reason
                            res = {account.iban: "NOTOK"}
            else:
                abort(400, "Parameter account is missing in URL.")

            return jsonify(res)

        elif request.method == "POST":
            abort(405, "Request method not yet supported")
            data = request.get_json()
            if data is not None and "account" in data:
                account_data = data["account"]
                # TODO: Move functionality of "GET" to a function and call it in both places
        else:
            abort(405, "Request method not allowed")

    @app.errorhandler(400)
    def resource_not_found(e):
        return jsonify(error=str(e)), 400

    @app.errorhandler(404)
    def resource_not_found(e):
        return jsonify(error=str(e)), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify(error=str(e)), 405

    @app.route("/hello")
    def hello():
        return "<h1 style='color:red'>Hello there!</h1>"

    return app


app = create_app()
