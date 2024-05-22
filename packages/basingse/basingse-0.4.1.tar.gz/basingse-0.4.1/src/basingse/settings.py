import dataclasses as dc
from typing import Any

import humanize
import structlog
from bootlace import as_tag
from bootlace import Bootlace
from bootlace import render
from flask import Flask
from flask_attachments import Attachments

from . import attachments as attmod  # noqa: F401
from . import svcs
from .admin.settings import AdminSettings
from .assets import Assets
from .auth.extension import Authentication
from .customize.settings import CustomizeSettings
from .logging import Logging
from .markdown import MarkdownOptions
from .models import Model
from .models import SQLAlchemy
from .page.settings import PageSettings
from .resources.settings import AssetBundles
from .resources.settings import builtin_bundles
from .utils.urls import rewrite_endpoint
from .utils.urls import rewrite_update
from .utils.urls import rewrite_url
from .views import CoreSettings


logger = structlog.get_logger()


@dc.dataclass(frozen=True)
class Context:

    def init_app(self, app: Flask) -> None:
        app.context_processor(context)


def context() -> dict[str, Any]:
    return {
        "humanize": humanize,
        "rewrite": rewrite_url,
        "endpoint": rewrite_endpoint,
        "update": rewrite_update,
        "as_tag": as_tag,
        "render": render,
    }


@dc.dataclass
class BaSingSe:

    assets: Assets | None = dc.field(default_factory=Assets)
    auth: Authentication | None = Authentication()
    attachments: Attachments | None = Attachments(registry=Model.registry)
    bundles: AssetBundles | None = dc.field(default_factory=AssetBundles)
    customize: CustomizeSettings | None = CustomizeSettings()
    page: PageSettings | None = PageSettings()
    core: CoreSettings | None = CoreSettings()
    sqlalchemy: SQLAlchemy | None = SQLAlchemy()
    logging: Logging | None = Logging()
    markdown: MarkdownOptions | None = MarkdownOptions()
    context: Context | None = Context()
    bootlace: Bootlace | None = Bootlace()
    admin: AdminSettings | None = AdminSettings()

    initailized: dict[str, bool] = dc.field(default_factory=dict)

    def init_app(self, app: Flask) -> None:
        svcs.init_app(app)

        config = app.config.get_namespace("BASINGSE_")

        if self.assets is not None and self.bundles is not None:
            builtin_bundles(self.bundles, self.assets)

        for field in dc.fields(self):
            attr = getattr(self, field.name)
            if attr is None:
                continue

            if dc.is_dataclass(attr):
                cfg = config.get(field.name, {})
                if any(cfg):
                    attr = dc.replace(attr, **cfg)

            if hasattr(attr, "init_app"):
                if self.initailized.get(field.name, False):
                    raise RuntimeError(f"{field.name} already initialized")

                attr.init_app(app)
                self.initailized[field.name] = True
