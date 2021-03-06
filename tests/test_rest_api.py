"""Test module."""

from flask import current_app, url_for
from f8a_worker.models import OSIORegisteredRepos
from sqlalchemy import create_engine
from f8a_worker.models import Base
from pytest_mock import mocker
from tests.conftest import create_database

import requests
import os
import pytest
import json

payload = {
    "email-ids": "abcd@gmail.com",
    "git-sha": "somesha",
    "git-url": "test"
}


def api_route_for(route):
    """Construct an URL to the endpoint for given route."""
    return '/api/v1/' + route


def get_json_from_response(response):
    """Decode JSON from response."""
    return json.loads(response.data.decode('utf8'))


def test_readiness_endpoint(client):
    """Test the /api/v1/readiness endpoint."""
    response = client.get(api_route_for("readiness"))
    assert response.status_code == 200
    json_data = get_json_from_response(response)
    assert json_data == {}, "Empty JSON response expected"


def test_liveness_endpoint(client):
    """Test the /api/v1/liveness endpoint."""
    response = client.get(api_route_for("liveness"))
    assert response.status_code == 200
    json_data = get_json_from_response(response)


def test_register_api_endpoint(client, mocker):
    """Test function for register endpoint."""
    create_database()
    scan_mock = mocker.patch("src.rest_api.scan_repo")
    scan_mock.return_value = True
    reg_resp = client.post(api_route_for("register"),
                           data=json.dumps(payload), content_type='application/json')
    assert reg_resp.status_code == 200
    jsn = get_json_from_response(reg_resp)
    assert(jsn["success"])
    assert(jsn['data']["data"]["git_sha"] == payload["git-sha"])
    assert(jsn['data']["data"]["git_url"] == payload["git-url"])
    assert(jsn['data']["data"]["email_ids"] == payload["email-ids"])
