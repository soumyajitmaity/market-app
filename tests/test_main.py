import os 
os.path.abspath("..")
from functools import wraps
from mock import patch

####################writing auth bypass decorator########################### 

def mock_decorator():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            return f(*args, **kwargs)
        return decorated_function
    return decorator


patch('app.login_required', mock_decorator)

from src.app import *



##########################tests####################################


def test_gen_ID() -> None:
    lenth = 10
    assert len(gen_id(length=lenth)) > 0

def test_get_token() -> None:
    assert len(get_token("testUser")) > 0

def test_get_admin_token() -> None:
    assert len(get_admin_token("testAdmin")) > 0

def test_token_validator() -> None:
    token = get_token("test_user")
    if token:
        assert token_validator(token)

def test_admin_token_validator() -> None:
    admin_token = get_admin_token("testAdmin")
    if (admin_token):
        assert admin_token_validator(admin_token)

def test_getting_all_items() -> None:
    items = All_Items()
    x = items.get()
    assert type(x) == type({"hello":"world"})


def test_getting_all_catagory() -> None:
    catagory = All_Catagories()
    x = catagory.get()
    assert type(x) == type({"hello":"world"})



def test_upload_items() -> None:
    pass    







