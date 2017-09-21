import os

import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import SimpleCookieStorage
from aiohttp_session import setup as setup_cookiestore
from jinja2 import FileSystemLoader

from config import load_config
from db import init_pg, close_pg, init_login, close_login
from decrypt import init_blowfish
from routes import setup_routes
from scheduling import setup as setup_scheduler


def main() -> None:
    """
    Launch the app

    :return:
    """
    global app
    app = web.Application()
    setup_routes(app)

    conf = load_config(os.path.join("config", "config.yaml"))
    app["db_config"] = conf["db"]
    app["deadlines"] = conf["deadlines"]
    app["login_db"] = conf["login_db"]

    aiohttp_jinja2.setup(app, loader=FileSystemLoader("./template/"))
    app.router.add_static("/static/", "./static")

    setup_cookiestore(app, SimpleCookieStorage())
    app["webserver"] = conf["webserver"]
    app["permissions"] = conf["permissions"]
    app["misc_config"] = conf["misc"]
    app["email"] = conf["email"]
    app["email"]["from_"] = app["email"]["from"]
    del app["email"]["from"]

    app.on_startup.append(init_pg)
    app.on_startup.append(setup_scheduler)
    app.on_startup.append(init_blowfish)
    app.on_startup.append(init_login)
    app.on_cleanup.append(close_pg)
    app.on_cleanup.append(close_login)
    web.run_app(app,
                host=conf["webserver"]["host"],
                port=conf["webserver"]["port"])

if __name__ == '__main__':
    main()
