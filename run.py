import os

from api import create_app, routes

config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)

app.register_blueprint(routes.mod)

if __name__ == '__main__':
    app.run()
