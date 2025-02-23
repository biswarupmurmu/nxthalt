import os
from flask import Flask, request, render_template
from flask_pymongo import PyMongo
from .the_graph import create_graph, dijkstra
from .forms import TravelForm


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['MONGO_URI'] = os.getenv('MONGO_URI')

    print(app.config)

    mongo = PyMongo(app)

    with app.app_context():
        graph = create_graph(mongo=mongo)
        app.config['GRAPH'] = graph

    @app.route("/")
    def index():
        src = request.args.get('source', '')
        des = request.args.get('destination', '')
        h = request.args.get('hour', 0, type=int)
        m = request.args.get('minutes', 0, type=int)
        h *= 60
        t=h+m
        src = src.strip().lower()
        des = des.strip().lower()
        res = dijkstra(app.config['GRAPH'], src, des, t)
        return res

    @app.route("/ui", methods=["GET", "POST"])
    def find_route():
        form = TravelForm()
        res = ""
        if form.validate_on_submit():
            source = form.source.data
            destination = form.destination.data
            h = form.data.get('hour', 0)
            m = form.data.get('minutes', 0)
            h *= 60
            time = h+m

            res = dijkstra(app.config['GRAPH'], source, destination, time)

        return render_template('form.html', form=form, result=res)

    return app
