import sys
import os

from flask import Flask, flash, request, render_template, url_for, redirect

from .task import Item


def create_app(test_config=None):

    from .task import Item

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DB_NAME='flasktodo',
        DB_USER='flasktodo_user',
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


 #------------------------------------------------------------------------------------------------------------  

    @app.route('/')
    def root():
        return redirect(url_for('index'))
 #------------------------------------------------------------------------------------------------------------  
                        #LIST ALL 
    @app.route('/todo', methods=["GET", "POST"])
    def index():
        tasks = [
            Item('test task')
        ]

        if request.method == 'POST':
            new_item = Item(request.form['task'])
            tasks.append(new_item)
            return redirect(url_for('index'))

        filter_option = request.args.get('filter')
        if filter_option == 'completed':
            tasks = list(filter(lambda t: t.completed, tasks))
        elif filter_option == 'active':
            tasks = list(filter(lambda t: not t.completed, tasks))


        print(len(tasks))
        return render_template('index.html', filter_option=filter_option, tasks=tasks)

 #------------------------------------------------------------------------------------------------------------  
                        #CREATE
    @app.route('/todo/create', methods=["GET", "POST"])
    def create():
        print('/create')
        return render_template('create.html')
    
 #------------------------------------------------------------------------------------------------------------  
                        #UPDATE
    methods_route_allows = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE']

    @app.route('/todo/update', methods=methods_route_allows)
    def method_route():
        if request.method == ['GET']:
            new_item = Item(request.form['task'])
            tasks.append(new_item)
            return redirect(url_for('index'))
        return render_template('update.html', allowed=methods_route_allows, method=request.method, tasks=tasks)


 #------------------------------------------------------------------------------------------------------------  
    @app.route('/status')
    def status_route():
        code = request.args.get('c', 200)
        response = make_response(f"status: {code}", code)

        return response
    
 #------------------------------------------------------------------------------------------------------------  
   #from . import db
   # db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)
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



























