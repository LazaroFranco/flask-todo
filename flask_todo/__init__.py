import sys
import os

from flask import Flask, request, render_template, url_for, redirect

from .task import Item


def create_app(test_config=None):

    from .task import Item
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    tasks = []

    @app.route('/')
    def root():
        return redirect(url_for('index'))
    
    @app.route('/todo', methods=["GET", "POST"])
    def index():
        if request.method == 'POST':
            new_item = Item(request.form['task'])
            tasks.append(new_item)
            return redirect(url_for('index'))
        return render_template('index.html', tasks=tasks)

    @app.route('/todo/create', methods=['POST'])
    def create():
        return render_template('create.html') 


    @app.route('/status')
    def status_route():
        code = request.args.get('c', 200)
        response = make_response(f"status: {code}", code)

        return response

    return app
   
  ## @app.route('/calculate', methods=['GET', 'POST'])
  # def calculate():
  #     if request.method == 'GET':
  #         return render_template('calculate.html', action="Add")
  #     elif request.method == 'POST':
  #         x = float(request.form['x'])
  #         y = float(request.form['y'])
  #         action = request.form['action']

  #         if action == "Add":
  #             result = x + y
  #         elif action == "Subtract":
  #             result = x - y
  #         elif action == "Multiply":
  #             result = x * y
  #         elif action == "Divide":
  #             result = x / y

  #         return render_template('calculate.html', result=result, x=x, y=y)

  # methods_route_allows = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE']

  # @app.route('/method', methods=methods_route_allows)
  # def method_route():
  #     return render_template('method.html', allowed=methods_route_allows, method=request.method)



























