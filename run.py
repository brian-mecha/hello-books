from api import app, routes

app.register_blueprint(routes.mod)

if __name__ == '__main__':
    app.run(debug=True)
