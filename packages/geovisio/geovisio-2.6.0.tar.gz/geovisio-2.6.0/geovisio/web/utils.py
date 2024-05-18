import typing
from dateutil import tz
from datetime import timezone
from dateutil.tz import gettz
from typing import Optional
from functools import wraps
import psycopg
from flask import current_app, url_for, Response, make_response
from geovisio import errors

STAC_VERSION = "1.0.0"


def removeNoneInDict(val):
    """Removes empty values from dictionnary"""
    return {k: v for k, v in val.items() if v is not None}


def cleanNoneInDict(val):
    """Removes empty values from dictionnary, and return None if dict is empty"""
    res = removeNoneInDict(val)
    return res if len(res) > 0 else None


def dbTsToStac(dbts):
    """Transforms timestamp returned by PostgreSQL into UTC ISO format expected by STAC"""
    return dbts.astimezone(tz.gettz("UTC")).isoformat() if dbts is not None else None


def dbTsToStacTZ(dbts, dbtz):
    """Transforms timestamp returned by PostgreSQL into ISO format with timezone"""
    tzSwitches = {"CEST": "CET"}
    if dbtz in tzSwitches:
        dbtz = tzSwitches[dbtz]
    return dbts.astimezone(gettz(dbtz or "UTC") or timezone.utc).isoformat()


def cleanNoneInList(val: typing.List) -> typing.List:
    """Removes empty values from list"""
    return list(filter(lambda e: e is not None, val))


def accountIdOrDefault(account):
    # Get default account ID
    if account is not None:
        return account.id
    with psycopg.connect(current_app.config["DB_URL"]) as conn:
        accountId = conn.execute("SELECT id FROM accounts WHERE is_default").fetchone()
        if accountId is None:
            raise errors.InternalError("No default account defined, please contact your instance administrator")
        return str(accountId[0])


def get_license_link():
    license_url = current_app.config.get("API_PICTURES_LICENSE_URL")
    if not license_url:
        return None
    return {
        "rel": "license",
        "title": f"License for this object ({current_app.config['API_PICTURES_LICENSE_SPDX_ID']})",
        "href": license_url,
    }


def get_root_link():
    return {
        "rel": "root",
        "type": "application/json",
        "title": "Instance catalog",
        "href": url_for("stac.getLanding", _external=True),
    }


def get_mainpage_url():
    if current_app.config["API_MAIN_PAGE"].startswith("http"):
        return current_app.config["API_MAIN_PAGE"]
    else:
        return url_for("index", _external=True)


def get_viewerpage_url():
    if current_app.config["API_VIEWER_PAGE"].startswith("http"):
        return current_app.config["API_VIEWER_PAGE"]
    else:
        return url_for("viewer", _external=True)


def user_dependant_response(flag):
    """Set if a response is user dependant.

    If the response is not user dependant, we can tell that it can be cached by a reverse proxy, even if some authentication headers are set
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask import g

            g.user_dependant_response = flag
            return f(*args, **kwargs)

        return decorated_function

    return decorator
