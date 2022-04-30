__version__ = '0.1.0'

from flask import Flask

def create_app():
	app = Flask(__name__)

	from .views import views
	app.register_blueprint(views)

	return app
