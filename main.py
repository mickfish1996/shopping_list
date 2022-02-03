import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from get_key import Get_key

"""
Initialize Data Base:
This function will create an instance of Get_key, it will then call return_key()
and will set that valse as cred. it will initialize the app and return the 
database
"""
def init_database():
    gk = Get_key()

    cred = gk.return_key()
    
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db

"""
View in list:
This function will only display the items that the user has in the list, 
and it will only display the items that have a value greater than 0 
assciated with them.
"""    
def view_in_list(db,id):
    result = db.collection("users").document(id).get()
    data = result.to_dict()
    
    items = data["items"]
    i = 1
    print("\nShopping List")
    print("___________________________________")
    for item in items:
        if items[item] > 0:
            print(f"{i}. {item}: {items[item]}")
            i += 1
        
    print("___________________________________\n")

"""
Add Items:
This function will take items that the user would like to add to the list and will
send it up to the cloud data base.
"""        
def add_items(db,id):
    results = db.collection("users").document(id).get()
    
    data = results.to_dict()
    items = data["items"]
    print("___________________________________")
    item = input("Name of item to add: ")
    num = int(input("Number of item: "))
    print("___________________________________")
    
    items[item.capitalize()] = num
    data["items"] = items
    
    db.collection("users").document(id).set(data)  
    
"""
Remove items:
This function will display the items in the list and will prompt the user for the Item
that they would like to set the value associated with the item to zero.
"""
def remove_items(db,id):
    results = db.collection("users").document(id).get()
    
    data = results.to_dict()
    items = data["items"]
    
    i = 1
    print("___________________________________")
    for item in items:
        if items[item] > 0:
            print(f"{i}. {item}: {items[item]}")
            
            i+=1
    keep_going = False
    while not keep_going:    
        choice = input("What item would you like to remove: ")
        if choice not in items:
            print("Please choose an item in the list")
        else:
            keep_going = True
            
    print("___________________________________")
    
    items[choice] = 0
    
    data["items"] = items
    
    db.collection("users").document(id).set(data)

"""
Create Account:
This function will create a dictionary with the values that the user input earlier,
and will set them as the user name and password that are being used. and will then
return the id of that new document item.
"""
def create_account(email, password, db):
    data = {}
    data["email"] = email
    data["password"] = password
    data["items"] = {}

    try:
        db.collection("users").add(data)

        results = db.collection("users").where("email", "==", email).where("password", "==", password).get()


        id = None
        for result in results:
            id = result.id

        result = db.collection("users").document(id).get()
        return id
    except: 
        print("Failed to create user")

"""
Get User Info:
This function will prompt the user for their email and password, it will then 
see if it is in the database. if it is it will return the users id, if it is not
it will ask the user if they would like to create an account. 
"""   
def get_user_info(db):
    keep_going = False
    while not keep_going: 
        email = None
        password = None
        try:
            email = input("Email: ")
            password = input("Password: ")
        
            results = db.collection("users").where("email", "==", email).where("password", "==", password).get()
            id = None
            data = None
            for result in results:
                id = result.id
                data = db.collection("users").document(id).get()
                keep_going = True

            if data.exists:
                return id
            
        except:
            print("Error: user not in the system!")
            create = input("Would you like to create an account? [y/n]: ")

            if create == "y":
                id = create_account(email, password, db)
                return id


    
"""
Main:
This function will prompt the user for what they would like to do
it will also call in the db from init_database. it will then pass
that db to what ever function wants to access.
"""    
def main():
    db = init_database()
    id = get_user_info(db)
    keep_going = True
    while keep_going:
        print("\n\t   SHOPPING LIST")
        print("___________________________________")
        print("What would you like to do?")
        
        try:
            choice = int(input("1. View list\n2. Add to list\n3. Remove From list\n4. Exit\n\nChoice: "))
            if choice == 1:
                view_in_list(db,id)
            
            elif choice == 2:
                add_items(db,id)
                
            elif choice == 3:
                remove_items(db,id)
                
            elif choice == 4:
                keep_going = False
            
            else:
                print("incorrect number enterd.")
                
        except:
            print("Error: Please enter a valid number")
    

if __name__ == "__main__":
    main()
    

