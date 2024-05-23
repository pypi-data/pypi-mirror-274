# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2024 TU Wien.
#
# Invenio-Theme-TUW is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Pytest configuration.

See https://pytest-invenio.readthedocs.io/ for documentation on which test
fixtures are available.
"""

import os
import shutil

import pytest
from flask import Flask
from flask_babelex import Babel
from flask_limiter import Limiter
from flask_webpackext.manifest import (
    JinjaManifest,
    JinjaManifestEntry,
    JinjaManifestLoader,
)
from invenio_access import InvenioAccess
from invenio_accounts import InvenioAccounts
from invenio_accounts.models import User
from invenio_app.helpers import ThemeJinjaLoader
from invenio_app_rdm.config import APP_RDM_ROUTES
from invenio_app_rdm.records_ui.views import create_blueprint as create_app_rdm_bp
from invenio_assets import InvenioAssets
from invenio_cache import InvenioCache
from invenio_communities import InvenioCommunities
from invenio_communities.communities.records.api import Community
from invenio_db import InvenioDB, db
from invenio_files_rest import InvenioFilesREST
from invenio_files_rest.models import Location
from invenio_formatter import InvenioFormatter
from invenio_i18n import InvenioI18N
from invenio_indexer import InvenioIndexer
from invenio_jsonschemas import InvenioJSONSchemas
from invenio_pidstore import InvenioPIDStore
from invenio_rdm_records import InvenioRDMRecords
from invenio_rdm_records.records.api import RDMRecord
from invenio_records import InvenioRecords
from invenio_records_rest import InvenioRecordsREST
from invenio_records_rest.utils import PIDConverter
from invenio_records_rest.views import create_blueprint_from_app
from invenio_search import InvenioSearch, current_search, current_search_client
from invenio_search_ui import InvenioSearchUI
from invenio_search_ui.views import blueprint as search_ui_bp
from invenio_theme import InvenioTheme
from invenio_vocabularies import InvenioVocabularies
from invenio_vocabularies.records.api import Vocabulary
from invenio_vocabularies.records.models import VocabularyType
from pytest_invenio.user import UserFixtureBase

from invenio_theme_tuw import InvenioThemeTUW


#
# Mock the webpack manifest to avoid having to compile the full assets.
#
class MockJinjaManifest(JinjaManifest):
    """Mock manifest."""

    def __getitem__(self, key):
        """Get a manifest entry."""
        return JinjaManifestEntry(key, [key])

    def __getattr__(self, name):
        """Get a manifest entry."""
        return JinjaManifestEntry(name, [name])


class MockManifestLoader(JinjaManifestLoader):
    """Manifest loader creating a mocked manifest."""

    def load(self, filepath):
        """Load the manifest."""
        return MockJinjaManifest()


#
# Class for loading testing configuration.
#
class TestConfig:
    """Testing Configuration."""

    APP_RDM_DEPOSIT_FORM_TEMPLATE = "invenio_app_rdm/records/deposit.html"
    APP_RDM_ROUTES = APP_RDM_ROUTES
    DB_VERSIONING = False
    RDM_REQUESTS_ROUTES = {
        "user-dashboard-request-details": "/me/requests/<request_pid_value>",
        "community-dashboard-request-details": "/communities/<pid_value>/requests/<request_pid_value>",
        "community-dashboard-invitation-details": "/communities/<pid_value>/invitations/<request_pid_value>",
    }
    RECORDS_REFRESOLVER_CLS = "invenio_records.resolver.InvenioRefResolver"
    RECORDS_REFRESOLVER_STORE = "invenio_jsonschemas.proxies.current_refresolver_store"
    REQUESTS_FACETS = {}
    SECRET_KEY = "super_secret_key"
    SECURITY_PASSWORD_SALT = "test-secret-key"
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI") or "sqlite:///"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    WEBPACKEXT_MANIFEST_LOADER = MockManifestLoader


def _db_create_fill_tables(db):
    """Creates db tables and fills specific vocabularies."""
    db.create_all()
    # create dummy vocabularies for deposit page. They have to have
    # the real id fields though.
    dummy_vocs = [
        VocabularyType(id="titletypes", pid_type="pid_type1"),
        VocabularyType(id="resourcetypes", pid_type="pid_type2"),
        VocabularyType(id="creatorsroles", pid_type="pid_type3"),
        VocabularyType(id="descriptiontypes", pid_type="pid_type4"),
        VocabularyType(id="datetypes", pid_type="pid_type5"),
        VocabularyType(id="contributorsroles", pid_type="pid_type6"),
        VocabularyType(id="relationtypes", pid_type="pid_type7"),
    ]
    db.session.add_all(dummy_vocs)
    db.session.commit()


def _es_create_indexes(current_search, current_search_client):
    """Creates all registered Elasticsearch indexes."""
    to_create = [RDMRecord.index._name, Vocabulary.index._name, Community.index._name]
    # list to trigger iter
    list(current_search.create(ignore_existing=True, index_list=to_create))
    current_search_client.indices.refresh()
    return to_create


def _create_files_loc(db):
    """Creates app location for testing."""
    loc_path = "testing_data_location"

    if os.path.exists(loc_path):
        shutil.rmtree(loc_path)
    os.makedirs(loc_path)
    loc = Location(name="local", uri=loc_path, default=True)
    db.session.add(loc)
    db.session.commit()
    return loc_path


def _register_exts_bps(app):
    """Registers extensions and blueprints to given application."""
    Babel(app)
    InvenioAccess(app)
    InvenioAccounts(app)
    InvenioAssets(app)
    InvenioCache(app)
    InvenioCommunities(app)
    InvenioDB(app)
    InvenioFilesREST(app)
    InvenioFormatter(app)
    InvenioI18N(app)
    InvenioIndexer(app)
    InvenioJSONSchemas(app)
    InvenioPIDStore(app)
    InvenioRecords(app)
    InvenioRecordsREST(app)
    InvenioRDMRecords(app)
    InvenioSearch(app)
    InvenioSearchUI(app)
    # NOTE: Our extension needs to be initialized before InvenioTheme
    # so that our custom templates are picked up
    InvenioThemeTUW(app)
    InvenioTheme(app)
    InvenioVocabularies(app)
    Limiter(app)

    # Register Invenio Search UI routes #
    app.register_blueprint(search_ui_bp)

    # Register Invenio app RDM Records UI routes #
    app.register_blueprint(create_app_rdm_bp(app))

    # Register Invenio Records REST routes #
    app.register_blueprint(create_blueprint_from_app(app))


@pytest.fixture()
def minimal_record():
    """Minimal record for creation during tests."""
    return {
        "access": {
            "record": "public",
            "files": "public",
        },
        "files": {"enabled": False},  # Most tests don't care about file upload
        "metadata": {
            "publication_date": "2022-02-09",
            "creators": [
                {
                    "person_or_org": {
                        "type": "personal",
                        "name": "Doe, John",
                        "given_name": "John Doe",
                        "family_name": "Doe",
                    }
                }
            ],
            "title": "This is the record title",
        },
    }


@pytest.fixture()
def user(base_app):
    """User creation and login fixture."""
    test_user = UserFixtureBase(
        email="user@example.org",
        password="super_secure_password",
        username="pytest_user",
    )
    test_user.create(base_app, db)
    test_user.app_login()
    return test_user


@pytest.fixture()
def base_app():
    """Base application fixture."""
    app = Flask("test_app")
    app.config.from_object(TestConfig)

    # Jinja env loader that seeks the templates in the custom directory
    app.jinja_env.loader = ThemeJinjaLoader(app, app.jinja_env.loader)

    # pid converter
    app.url_map.converters["pid"] = PIDConverter

    return app


@pytest.fixture()
def app(base_app):
    """Application fixture with extensions, db, es."""
    # attach essential extensions and their blueprints to the app
    _register_exts_bps(base_app)

    # push app ctx
    base_app.app_context().push()

    # create db, es & location
    _db_create_fill_tables(db)
    indexes = _es_create_indexes(current_search, current_search_client)
    loc = _create_files_loc(db)

    yield base_app

    # teardown db, es indexes & location
    db.session.remove()
    db.drop_all()
    current_search.delete(index_list=indexes)
    shutil.rmtree(loc)
