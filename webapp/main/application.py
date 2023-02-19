from fastapi import FastAPI

from .interfaces import user_controller, auth_controller, redis_controller
from webapp.main.interfaces.something import router
from .containers import Container
from webapp import main

def create_app():
    container = Container()
    container.config.from_yaml("config.yml")
    container.config.redis_host.from_env("REDIS_HOST", "localhost")
    container.config.redis_password.from_env("REDIS_PASSWORD", "password")

    container.wire(
        packages=[main],
    )

    fastapi_app = FastAPI(openapi_prefix="/vi")
    fastapi_app.container = container
    fastapi_app.include_router(user_controller.router)
    fastapi_app.include_router(auth_controller.router)
    fastapi_app.include_router(redis_controller.router)
    fastapi_app.include_router(prefix="/v1", router=router)

    return fastapi_app, container


app, container = create_app()


@app.get(app.root_path + "/openapi.json")
def custom_swagger_ui_html():
    return app.openapi()
