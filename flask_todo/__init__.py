import sys
import os
import psycopg2
import datetime
from flask import Flask, flash, request, render_template, make_response,  url_for, redirect

from .task import Item


def create_app(test_config=None):

    from .task import Item

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DB_NAME='task_list',
        DB_USER='csetuser',
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

    from . import db
    db.init_app(app)


 #------------------------------------------------------------------------------------------------------------  

    @app.route('/')
    def root():
        return redirect(url_for('index'))
 #------------------------------------------------------------------------------------------------------------  
                        #LIST ALL 
    @app.route('/todo', methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            item_id = request.form["id"]
            
            if item_id:
                con = db.get_db()
                cur = con.cursor()
                cur.execute(
                        "UPDATE items SET completed = True WHERE id = %s",
                        (item_id,)
                )
                con.commit()

        filter_option = request.args.get('filter')


        #if request.method == 'POST':
        #    new_item = Item(request.form['task'])
        #    tasks.append(new_item)
        #    return redirect(url_for('index'))

        con = db.get_db()
        cur = con.cursor()

        if filter_option == 'completed':
            cur.execute("SELECT * FROM items WHERE completed = True")
        elif filter_option == 'active':
            cur.execute("SELECT * FROM items WHERE completed = False")
        else:
            cur.execute("SELECT * FROM items")

        task_results = cur.fetchall()
        cur.close()

        tasks = []
        for result in task_results:
            tasks.append({
                "id": result[0],
                "task": result[1],
                "task_timestamp": result[2],
                "completed": result[3],
            })

        return render_template('index.html', filter_option=filter_option, tasks=tasks)

 #------------------------------------------------------------------------------------------------------------  
                        #CREATE
    @app.route('/todo/create', methods=["GET", "POST"])
    def create():
        if request.method == "GET":
            return render_template('create.html', task=None)

        elif request.method == "POST":
            new_task = request.form.get('task', False)

            if new_task:
                dt = datetime.datetime.now()

                # Save to database
                con = db.get_db()
                cur = con.cursor()
                cur.execute(
                        "INSERT INTO items (task, task_timestamp, completed) VALUES (%s, %s, %s)",
                        (new_task, dt, False)
                )
                con.commit()
                cur.close()

                # TODO: If error, flash it to the screen

                flash('To-Do item was added. Want to add another?', 'success')
            else:
                flash('You need to add some text first.', 'error')

        return render_template('create.html', new_task=new_task)

    
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



























