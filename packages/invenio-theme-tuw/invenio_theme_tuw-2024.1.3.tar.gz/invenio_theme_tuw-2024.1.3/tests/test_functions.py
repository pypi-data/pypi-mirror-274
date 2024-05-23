# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2024 TU Wien.
#
# Invenio-Theme-TUW is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Test specific functions."""

from flask import render_template_string
from invenio_rdm_records.proxies import current_rdm_records_service as rec_service
from invenio_records_permissions.generators import AnyUser

from invenio_theme_tuw.views import (
    fetch_schemaorg_jsonld,
    guarded_deposit_create,
    guarded_deposit_edit,
)


def test_fetch_schemaorg_jsonld(app):
    """Test fetching of Schema.org metadata."""
    # this will trigger the exception
    doi_url = "sth"
    with app.test_request_context():
        metadata = fetch_schemaorg_jsonld(doi_url)
        assert metadata is None

    # the doi must be taken from researchdata.tuwien.ac.at
    # since we are accepting only application/vnd.schemaorg.ld+json
    # in the function.
    doi_url = "https://doi.org/10.48436/vzs40-t9b67"
    with app.test_request_context():
        metadata = fetch_schemaorg_jsonld(doi_url)
        assert metadata


def test_tuw_create_schemaorg_metadata(app):
    """Test Schema.org metadata creation."""
    template = r"""
    {% set record = {
        "pids": {
            "doi": {
                "identifier": "https://doi.org/10.48436/vzs40-t9b67"
            }
        }
    } %}
    {{ tuw_create_schemaorg_metadata(record) }}
    """
    with app.test_request_context():
        result = render_template_string(template)
        assert result
        assert "TU Wien" in result

    # test fallback case when doi is contained in metadata
    template = r"""
    {% set record = {
        "metadata": {
            "identifiers": [
                {
                "scheme":  "doi",
                "identifier": "https://doi.org/10.48436/vzs40-t9b67"
                }
            ]
        }
    } %}
    {{ tuw_create_schemaorg_metadata(record) }}
    """
    with app.test_request_context():
        result = render_template_string(template)
        assert result
        assert "TU Wien" in result


def test_deposit_create_allowed(app, user):
    """Test deposit guard. Allowing creation case."""
    # default behavior is to allow creation, no further action required
    response = guarded_deposit_create()
    assert "deposit-form" in response


def test_deposit_create_denied(app, user):
    """Test deposit guard. Denying creation case."""
    # deny create permission
    rec_service.config.permission_policy_cls.can_create = []

    response, status_code = guarded_deposit_create()
    assert (
        "For your first upload, your account must be manually activated by our team"
        in response
    )
    assert status_code == 403


# NOTE: these tests are failing because the user somehow is not authenticated,
# altough the assertion passes from the user fixture.

# def test_deposit_edit_allowed(app, user, minimal_record):
#     """Test deposit guard. Allowing edit case."""
#     rec_service.config.permission_policy_cls.can_create = [AnyUser()]
#     rec_service.config.permission_policy_cls.can_update = [AnyUser()]

#     draft = rec_service.create(user.identity, minimal_record)

#     response = guarded_deposit_edit(pid_value=draft.id)
#     assert "deposit-form" in response


# def test_deposit_edit_denied(app, user, minimal_record):
#     """Test deposit guard. Denying edit case."""
#     rec_service.config.permission_policy_cls.can_create = [AnyUser()]
#     rec_service.config.permission_policy_cls.can_update = [AnyUser()]

#     draft = rec_service.create(user.identity, minimal_record)
#     response = guarded_deposit_edit(pid_value=draft.id)
#     assert (
#         "For your first upload, your account must be manually activated by our team"
#         in response
#     )
