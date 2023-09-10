#!/usr/bin/env python
from __future__ import print_function  # Code should work with Python 2 or 3

# from flask import Flask, escape, request, render_template
import flask
import datetime
import platform
import os, json, logging, uuid
from flask_cors import CORS
import watchtower

from rds import RDS


logging.basicConfig(level=logging.INFO)

app = flask.Flask(__name__)
cors = CORS(app)


def json_log(res, status="info"):
    log = {
        "status": status,
        "headers": res.headers["Access-Control-Allow-Origin"],
    }
    app.logger.info(json.dumps(log))


def row_log(row):
    log = {
        "status": "info",
        "row": " ".join(row),
    }
    app.logger.info(json.dumps(log))


def add_headers(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Headers"] = "*"
    resp.headers["Access-Control-Allow-Credentials"] = True
    resp.headers["Content-Type"] = "application/json"
    resp.headers["Referrer-Policy"] = "no-referrer"
    return resp


@app.route("/", methods=["GET"])
def init():
    return "ok"


@app.route("/sales", methods=["GET"])
def get_sales():
    # get data from rds
    data = rds.get_sales()
    if data is None:
        return flask.make_response("Not found", 404)
    resp = flask.make_response(json.dumps(data), 200)
    return resp
    # return flask.make_response("Unauthorized", 401)


@app.route("/products", methods=["GET"])
def get_products():
    username = flask.request.args.get("username", "")
    data = rds.get_products(username)
    if data is None:
        return flask.make_response(json.dumps({"error": "Not found"}), 404)
    resp = flask.make_response(json.dumps(data, default=str), 200)
    return resp


@app.after_request
def after_request(response):
    response = add_headers(response)
    # json_log(response)
    return response


if __name__ == "__main__":
    try:
        rds = RDS()
        handler = watchtower.CloudWatchLogHandler(
            log_group="fargate-service",
        )
        app.logger.addHandler(handler)
    except Exception as e:
        print("Couldn't start CW Logging")
        print(e)
    app.run(debug=True, host="0.0.0.0", port=5000)
