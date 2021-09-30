"""
This file (test_login.py) contains the functional tests for
the `login` blueprint.

These tests use GETs and POSTs to different endpoints to check
for the proper behavior of the `login` blueprint.
"""
from flask import url_for
from flask import request
import pytest


class TestDashboardInvalidAccess:
    """
    Test all dashboard routes for correct user authentication
    """

    routes_get = [
        "/dashboard/",
    ]

    @pytest.mark.parametrize("route", routes_get)
    def test_redirect_if_not_logged_in_get(self, test_client, route, auth):
        auth.logout()
        response = test_client.get(route, follow_redirects=True)

        assert response.status_code == 200
        assert request.path == url_for("auth.login")

    @pytest.mark.usefixtures("login_unconfirmed_user")
    @pytest.mark.parametrize("route", routes_get)
    @pytest.mark.skip(reason="No mail confirmation flow for conf")
    def test_redirect_if_email_not_confirmed(self, test_client, route):
        response = test_client.get(route, follow_redirects=True)

        assert response.status_code == 200
        assert request.path == url_for("auth.unconfirmed")

