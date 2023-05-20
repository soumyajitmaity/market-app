from flask import Flask, request
from flask_restful import Resource, Api
from pony import orm
import secrets
import string
from functools import wraps 
import datetime
import jwt


#################################################################################################################
app = Flask(__name__)
api = Api(app)
db = orm.Database()

app.config['SECRET_KEY'] = 'thisIsCompletlysecretKey@@@@apwdkpoawkdwoqu'

##############################################################models##############################################


class Catagory(db.Entity):
    catagory_id = orm.Required(str, unique = True)
    catagory_name  = orm.Required(str, unique = True)
    item = orm.Set("Item")
    
class Item(db.Entity):
    item_id = orm.Required(str, unique = True)
    item_name  = orm.Required(str, unique = True)
    item_price = orm.Required(str)
    item_type = orm.Required(lambda : Catagory)

class User(db.Entity):
    user_id = orm.Required(str, unique=True)
    username = orm.Required(str, unique = True)
    password = orm.Required(str)

class Admin(db.Entity):
    admin_name = orm.Required(str,unique = True)
    admin_password = orm.Required(str)


db.bind('sqlite', 'database.sqlite', create_db = True)
db.generate_mapping(create_tables=True)



#################################################################################################################

def gen_id(length: int)->str:
    res = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
              for i in range(length))
    return res

def getCatagoryId(name)->int:
    with orm.db_session():
        c = orm.select(c for c in Catagory if c.catagory_name == name)
        c = [i.to_dict() for i in c]
        if len(c) > 0:
            return(c[0]['id'])
        return 0
    
def get_token(username):
    dt = datetime.datetime.utcnow() + datetime.timedelta(days = 7)
    dt = dt.strftime("%y-%m-%d %H:%M:%S")
    payload = {
        'username' : username,
        'ex_date': dt,
        'role': 'user'
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm = 'HS256')
    return token


def get_admin_token(admin_name):
    dt = datetime.datetime.utcnow() + datetime.timedelta(days = 7)
    dt = dt.strftime("%y-%m-%d %H:%M:%S")
    payload = {
        'username' : admin_name,
        'ex_date': dt,
        'role': 'admin'
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm = 'HS256')
    return token

def token_validator(token: str)->bool:
    data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
    if (data):
        if data['role'] == 'user':
            ex_date = datetime.datetime.strptime(data['ex_date'], "%y-%m-%d %H:%M:%S")
            if datetime.datetime.utcnow() - ex_date <= datetime.timedelta(days=7):
                return True
            
    return False

def admin_token_validator(token:str)->bool:
    data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
    if (data):
        if data['role'] =='admin':
            ex_date = datetime.datetime.strptime(data['ex_date'], "%y-%m-%d %H:%M:%S")
            if datetime.datetime.utcnow() - ex_date <= datetime.timedelta(days=7):
                return True
            
    return False
    

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers['token']
        if token_validator(token) == True:
            return f(*args, **kwargs)
    return wrapper

def login_required_as_admin(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
        token = request.headers['token']
        if admin_token_validator(token) == True:
            return f(*args, **kwargs)
    return wrapper

#########################################################api##################################################################

class All_Items(Resource):
    def get(self):
            with orm.db_session():
                items = orm.select(item for item in Item)
                r = [i.to_dict() for i in items]
                if len(r) ==0: return {'message': 'no items found'}
                return {'result': r}
                


        
class Items(Resource):
    def get(self,item_id):
        with orm.db_session():
            item = Item.get(item_id = item_id)
            if item:
                return {'result': item.to_dict()}
            else: return {'error':'invalid item id'}
                

class UploadItems(Resource):
     @login_required_as_admin
     def post(self):
        new_item = request.json
        try:
            with orm.db_session():
                    item_type = new_item['item_type']
                    if getCatagoryId(item_type)>0:
           
                        Item(
                            item_id = gen_id(10),
                            item_name = new_item['item_name'],
                            item_price = new_item['item_price'],
                            item_type = getCatagoryId(new_item['item_type'])
                            )
                        return {'item': new_item}
                    else: return{'error': 'invalid catagory push'}
        except orm.TransactionIntegrityError as err:
                raise err("item exists")
                
            

            
class All_Catagories(Resource):
    def get(self):
        with orm.db_session():
            catagories = orm.select(c for c in Catagory)
            
            result = [c.to_dict() for c in catagories]
       
            return {'result':result}
        
class Catagories(Resource):
     def get(self, name):
          if (getCatagoryId(name)>0):
            
            with orm.db_session():
                c = Catagory.get(catagory_name = name)
                items = orm.select(i for i in Item if i.item_type == c)
                items = [i.to_dict() for i in items]
            return items
          else:
              return({'error': 'Invalid catagory'}) 
     
    
         

class UploadCatagory(Resource):
    @login_required_as_admin
    def post(self):
        new_catagory = request.json
        try:
            with orm.db_session():
                Catagory(
                    catagory_id = gen_id(10),
                    catagory_name = new_catagory['catagory_name']
                )
                return {'catagory': new_catagory}
        except orm.TransactionIntegrityError as err:
            print(err)
            return {'error': 'catagory already exists'}
            
################################auths###################################


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
                return data
        except orm.TransactionIntegrityError as e:
            return {'error': 'username already exist'}
    

class Login_Admin(Resource):
    def post(self):
        data = request.json
        username = data['admin_name']
        password = data['password']
        if len(username) > 0 and len(password)>0:
           
            with orm.db_session():
                admin =  Admin.get(admin_name = username)
                if (admin):
                    if (admin.to_dict())['admin_password'] == password:
                        return {'token': get_admin_token(username)} 
                    else: return {'error':'Invalid username or password'}
        
class Login_User(Resource):
    def post(self):
        pass
        
        
        
###############################################resource mapping####################################################################################


api.add_resource(All_Items, '/items/')
api.add_resource(Items,'/items/<string:item_id>/')
api.add_resource(UploadItems,'/items/u/')
api.add_resource(All_Catagories,'/catagories/')
api.add_resource(Catagories,'/catagories/<string:name>/')
api.add_resource(UploadCatagory,'/catagories/u')
api.add_resource(Register, '/register')
api.add_resource(Login_Admin, '/admin_login')

###################################################################################################################################################

