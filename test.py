import requests as r 
from main import getCatagoryId
catagory_list =['Furniture',' Hand & Power Tools', 'Veterinary & Pet Items', 'kitchen appliences', 'books']

for c in catagory_list:
    try:
        x= r.post(
        url = 'http://127.0.0.1:5000/catagories/u',
        json = {'catagory_name':c}
        
        )
        print(x.text)
    except:
        print('new catagory added ::::: %s' %c)



i1 =  {
        'item_name':'sofa',
        'item_price':'30000rs',
        'item_type':'Furniture',
}
    


i2 = {  
        'item_name':'chair',
        'item_price' : '50000rs',
        'item_type' : 'Furniture',

    }

i3 = {  
        'item_name':'dog food',
        'item_price' : '500rs',
        'item_type' : 'Veterinary & Pet Items',

    }

items = [i1,i2,i3]

for i in items:
    x = r.post(
        url='http://127.0.0.1:5000/items/u',
        json = i
    )
    print(x.text)


print(r.get(url='http://127.0.0.1:5000/items').text)