from os import environ as env
from urllib.parse import quote_plus, urlencode

from flask import Flask, session, request
from flask import render_template, redirect, url_for, flash

from authlib.integrations.flask_client import OAuth

import db
import validation
from util import requires_auth
from util import is_uuid
from util import dict_snake_to_camelCase
from const import NOT_LOGGED_IN


# Main App
app = Flask(__name__,
            static_url_path="",
            static_folder="static")
app.secret_key = env["APP_SECRET_KEY"]

with app.app_context():
    db.setup()

oauth = OAuth(app)
oauth.register(
    "auth0",
    client_id=env["AUTH0_CLIENT_ID"],
    client_secret=env["AUTH0_CLIENT_SECRET"],
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{env["AUTH0_DOMAIN"]}/.well-known/openid-configuration",
)


"""
Page Routes
"""
@app.route("/")
def index():
    isLoggedIn, userId = (True if "user_id" in session else False, session.get("user_id"))

    # if not isLoggedIn:
    #     return redirect(url_for("login"))

    vehicles = list(map(dict_snake_to_camelCase, db.select_all_vehicles(userId)))
    gasStations = list(map(dict_snake_to_camelCase, db.select_all_stations()))

    return render_template("index.html", isLoggedIn=isLoggedIn, vehicles=vehicles, gasStations=gasStations)

@app.route("/profile")
@requires_auth
def profile():
    if not "user_id" in session:
        flash(NOT_LOGGED_IN)

        return redirect("/")

    return render_template("my_profile.html", isLoggedIn=True)

@app.route("/vehicles")
@requires_auth
def vehicle():
    if not "user_id" in session:
        flash(NOT_LOGGED_IN)

        return redirect("/")

    return render_template("my_vehicles.html", isLoggedIn=True)


"""
Auth Routes
"""
@app.get("/login-test")
def test_login():
    session["user_id"] = "00000000-0000-0000-0000-000000000000"

    return redirect("/")

@app.get("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()

    session["user_id"] = token["userinfo"]["sub"]

    return redirect("/")

@app.get("/logout")
def logout():
    session.clear()

    print("https://" + env["AUTH0_DOMAIN"]
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("index", _external=True),
                "client_id": env["AUTH0_CLIENT_ID"],
            },
            quote_via=quote_plus,
        ))

    return redirect(
        "https://" + env["AUTH0_DOMAIN"]
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("index", _external=True),
                "client_id": env["AUTH0_CLIENT_ID"],
            },
            quote_via=quote_plus,
        )
    )


"""
API Routes
"""
# Receipt Resources
@app.post("/api/receipts")
@requires_auth
def create_receipt():
    """
    Handler for POSTing new receipt

    This function needs a

    Request Body Format:

    {
        vehicleId: string,
        stationId: number,
        gallons: number,
        pricePerGallon, number,
    }

    Returns:
        tuple: ID of created receipt and HTTP Status Code
    """

    # Data
    body = dict(request.get_json())

    valid, message = validation.validate_receipt_post(body)
    if not valid:
        return message, 400

    # Database
    try:
        receipt = db.insert_receipt(
            user_id=session["user_id"],
            vehicle_id=body["vehicleId"],
            station_id=body["stationId"],
            gallons=body["gallons"],
            price_per_gallon=body["pricePerGallon"]
        )
    except Exception as e:
        app.logger.error(e)

        return "Internal Server Error", 500

    return receipt, 201

@app.get("/api/receipts/<receiptId>")
@requires_auth
def retrieve_receipt(receiptId):
    """
    TODO: docs
    """

    # Data
    valid, message = validation.validate_receipt_get(receiptId)
    if not valid:
        return message, 400

    # Database
    try:
        receipt = db.select_receipt(receipt_id=receiptId)
        if receipt is None:
            return "Not found", 404
    except Exception as e:
        app.logger.error(e)

        return "Internal Server Error", 500

    return dict_snake_to_camelCase(receipt), 200

@app.patch("/api/receipts/<receiptId>")
@requires_auth
def update_receipt(receiptId):
    """
    TODO: docs
    """

    # Data
    body = dict(request.get_json())

    valid, message = validation.validate_receipt_patch(receiptId, body)
    if not valid:
        return message, 400

    # Database
    try:
        succ = db.update_receipt(
            receipt_id=receiptId,
            vehicle_id=body.get("vehicleId"),
            station_id=body.get("stationId"),
            gallons=body.get("gallons"),
            price_per_gallon=body.get("pricePerGallon"),
            deleted=body.get("deleted"),
        )
        if not succ:
            return "Failed to updated receipt", 500
    except Exception as e:
        app.logger.error(e)

        return "Internal Server Error", 500

    receipt = db.select_receipt(receipt_id=receiptId)

    return dict_snake_to_camelCase(receipt), 200

@app.delete("/api/receipts/<receiptId>")
@requires_auth
def delete_receipt(receiptId):
    """
    TODO: docs
    """

    # Data

    # Database
    try:
        succ = db.delete_receipt(receipt_id=receiptId)
        if not succ:
            return "Failed to remove receipt", 500
    except Exception as e:
        app.logger.error(e)

        return "Internal Server Error", 500

    return "", 204

@app.get("/api/receipts")
@requires_auth
def query_receipts():
    """
    TODO: docs
    """

    # Data
    vehicleId = request.args.get("vehicleId")

    valid, message = validation.validate_receipt_query(vehicleId)
    if not valid:
        return message, 400

    # Database
    try:
        receipts = db.select_all_receipts(
            user_id=session["user_id"],
            vehicle_id=vehicleId,
        )
    except Exception as e:
        app.logger.error(e)

        return "Internal Server Error", 500

    return list(map(dict_snake_to_camelCase, receipts)), 200
