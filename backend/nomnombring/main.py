#!/usr/bin/env python

import json
import configparser
import os

from flask_cors import CORS
from flask import Flask, jsonify, request

from .add_to_bring import add_recipes_by_id


def get_recipes(path):
    with open(path, "r") as f:
        data = json.load(f)
    return data

# configuration
DEBUG = True

def create_app(config=None):
    # Running locally
    if os.path.isfile("config.ini"):
        config = "config.ini"

    fil = config or os.environ.get("NOMNOMBRING_BACKEND_SETTINGS")
    if fil is None or (not os.path.isfile(fil)):
        raise Exception("Unable to read config file!")

    config = configparser.ConfigParser()
    config.read(fil)
    global available_recipes
    available_recipes = get_recipes(config["DEFAULT"]["recipe_file"])
    print("Available recipes: " + str(len(available_recipes)))


    # instantiate the app
    app = Flask(__name__)
    app.config.from_object(__name__)

    # enable CORS
    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.route("/recipes", methods=["GET", "POST"])
    def all_recipes():
        response_object = {"status": "success"}
        if request.method == "POST":
            selected_ids = request.get_json()
            print(f"Received POST request: {selected_ids}")

            if not isinstance(selected_ids, list):
                raise ValueError(f"Data must be list of integers, got '{selected_ids}'")
            for id in selected_ids:
                if not isinstance(id, int):
                    raise ValueError(
                        f"Data must be list of integers, got non-integer '{id}'"
                    )

            add_recipes_by_id(config, available_recipes, selected_ids)
        else:
            response_object["recipes"] = available_recipes
        return jsonify(response_object)

    return app


def main(config=None):
    app = create_app(config=None)
    app.run(host='0.0.0.0', port=8080)  # debugging server for development


if __name__ == '__main__':
    main()
