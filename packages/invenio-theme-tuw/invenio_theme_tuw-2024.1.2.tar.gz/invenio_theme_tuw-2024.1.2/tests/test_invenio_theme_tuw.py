# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2024 TU Wien.
#
# Invenio-Theme-TUW is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Module tests."""

from flask import render_template_string

from invenio_theme_tuw import InvenioThemeTUW


def test_version():
    """Test version import."""
    from invenio_theme_tuw import __version__

    assert __version__


def test_init(base_app):
    """Test application initialization."""
    InvenioThemeTUW(base_app)

    assert base_app.config["TESTING"] is True
    assert "THEME_SITENAME" in base_app.config
    assert "invenio_theme_tuw" in base_app.blueprints.keys()


def test_init_app(base_app):
    """Test application initialization."""
    theme_tuw = InvenioThemeTUW()
    assert "invenio-theme-tuw" not in base_app.extensions
    theme_tuw.init_app(base_app)
    assert "invenio-theme-tuw" in base_app.extensions
    assert "THEME_SITENAME" in base_app.config


def test_tuw_theme_bp_before_theme(app):
    """
    Test if invenio_theme_tuw is registered before invenio_theme.
    This is essential so that our custom templates are rendered when testing.
    This would work only for Python 3.6+ where dicts preserve insertion order.
    """
    bps_names_list = list(app.blueprints.keys())
    assert bps_names_list.index("invenio_theme_tuw") < bps_names_list.index(
        "invenio_theme"
    )


def test_render_template(app):
    """Test rendering of template."""
    template = r"""
    {% extends 'invenio_theme_tuw/overrides/page.html' %}
    {% block body %}{% endblock %}
    """
    with app.test_request_context():
        assert render_template_string(template)


def test_frontpage_does_not_exist(base_app):
    """Test the frontpage that doesn't exist since our module is not registered."""
    response = base_app.test_client().get("/")
    assert response.status_code == 404
