def create_server(spec_dir, additional_middleware: list = None, debug=False, app_settings=None, **kwargs):
    from connexion import AsyncApp, ConnexionMiddleware
    import os
    import orjson
    import yaml
    from parrot_api.core.common import get_subpackage_paths
    from connexion.middleware import MiddlewarePosition
    from starlette.middleware.cors import CORSMiddleware
    middleware_stack = ConnexionMiddleware.default_middlewares + additional_middleware if additional_middleware else ConnexionMiddleware.default_middlewares

    app = AsyncApp(__name__, middlewares=middleware_stack, jsonifier=orjson, **kwargs)
    if app_settings is None:
        app_settings = dict()
    app.add_middleware(
        CORSMiddleware,
        position=MiddlewarePosition.BEFORE_ROUTING,
        allow_origins=app_settings.get("cors_origins", ['*']),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
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
