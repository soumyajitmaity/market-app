from pony import orm

db = orm.Database()

class Admin(db.Entity):
    admin_name = orm.Required(str,unique = True)
    admin_password = orm.Required(str)


db.bind('sqlite', 'database.sqlite', create_db = True)
db.generate_mapping(create_tables=True)


def create_admin():
    name = input('enter the admin name: ')
    password = input('enter password: ')
    cp = input('confirm password: ')
    if cp == password:
    
        with orm.db_session():
            Admin(
                admin_name = name,
                admin_password = password
            )
            print('admin created')
        
    
if __name__ =='__main__':
    create_admin()