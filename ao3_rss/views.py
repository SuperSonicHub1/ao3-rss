from flask import (
	Blueprint,
	render_template,
	Response,
	redirect,
	url_for,
	request
)
from AO3.utils import workid_from_url
from .generator import create_feed

views = Blueprint("views", __name__, url_prefix="/")

@views.route('/')
def index():
	return render_template("index.html")

@views.route('/from/url')
def from_url():
	return redirect(
		url_for(
			'views.feed',
			work_id=workid_from_url(request.args.get("url"))
		)
	)

@views.route('/from/id')
def from_id():
	return redirect(
		url_for(
			'views.feed',
			work_id=int(request.args.get("id"))
		)
	)

@views.route('/feed/<int:work_id>')
def feed(work_id: int):
	feed = create_feed(work_id)
	return Response(feed.rss(), mimetype='application/rss+xml')
