from pony import orm
from flask_restful import Resource,Api
from flask import request
db = orm.Database()
db.bind('sqlite', 'database.sqlite', create_db = True)
db.generate_mapping(create_tables=True)
from main import User,gen_id
from flask import render_template



class Register(Resource):
    def post(self):
        data = request.json
        try:
            with orm.db_session():
                User(
                    user_id = gen_id(10),
                    username = data['username'],
                    password = data['password']
                )
        except orm.TransactionIntegrityError as e:
            return {'error': 'username already exist'}
    
    def get(self):
        return render_template('register.html')
