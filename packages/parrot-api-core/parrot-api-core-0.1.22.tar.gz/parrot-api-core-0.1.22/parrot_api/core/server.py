from connexion.middleware.abstract import SpecMiddleware
from connexion.middleware.context import ContextMiddleware
from connexion.middleware.exceptions import ExceptionMiddleware
from connexion.middleware.lifespan import Lifespan, LifespanMiddleware
from connexion.middleware.request_validation import RequestValidationMiddleware
from connexion.middleware.response_validation import ResponseValidationMiddleware
from connexion.middleware.routing import RoutingMiddleware
from connexion.middleware.security import SecurityMiddleware
from connexion.middleware.swagger_ui import SwaggerUIMiddleware
from functools import partialmethod, partial


def create_server(spec_dir, additional_middleware: list = None, debug=False, app_settings=None, **kwargs):
    from connexion import AsyncApp, ConnexionMiddleware
    import os
    import orjson
    import yaml
    from parrot_api.core.common import get_subpackage_paths
    from connexion.middleware import MiddlewarePosition
    from starlette.middleware.cors import CORSMiddleware
    if app_settings is None:
        app_settings = dict()
    middleware_stack = [
        partial(CORSMiddleware,
            allow_origins=app_settings.get("cors_origins", ['*']),
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"]
        ),
        ExceptionMiddleware,
        SwaggerUIMiddleware,
        RoutingMiddleware,
        SecurityMiddleware,
        RequestValidationMiddleware,
        ResponseValidationMiddleware,
        LifespanMiddleware,
        ContextMiddleware,
    ]
    if additional_middleware:
        middleware_stack.extend(additional_middleware)
    app = AsyncApp(__name__, middlewares=middleware_stack, jsonifier=orjson, **kwargs)

    for spec in os.listdir(spec_dir):
        app.add_api(specification=os.path.join(spec_dir, spec), validate_responses=debug)

    for path in get_subpackage_paths():
        schema_directory = os.path.join(path, 'schemas/')
        if os.path.isdir(schema_directory):
            for spec_file in [i for i in os.listdir(schema_directory) if i.endswith('yaml') or i.endswith("yml")]:
                with open(os.path.join(schema_directory, spec_file), 'rt') as f:
                    spec = yaml.safe_load(f)
                app.add_api(specification=spec, validate_responses=debug)
    return app


async def healthcheck():
    return dict(status='ok')


async def hello():
    return dict(status='ok')
