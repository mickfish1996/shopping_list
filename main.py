import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from get_key import Get_key

def init_database():
    gk = Get_key()

    cred = gk.return_key()
    
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db
    
def view_in_list(db):
    result = db.collection("shopping_list").document("food").get()
    data = result.to_dict()
    
    items = data["items"]
    i = 1
    print("\nShopping List")
    print("____________________________________")
    for item in items:
        if items[item] != 0:
            print(f"{i}. {item}: {items[item]}")
            i += 1
        
    print("____________________________________\n")
        
def add_items(db):
    results = db.collection("shopping_list").document("food").get()
    
    data = results.to_dict()
    items = data["items"]
    
    
    
    
    
    

def main():
    db = init_database()
    keep_going = True
    while keep_going:
        print("\n\t   SHOPPING LIST")
        print("____________________________________")
        print("What would you like to do?")
        
        try:
            choice = int(input("1. View list\n2. Add to list\n3. Remove From list\n4. View all items\n5. Exit\n\nChoice: "))
            if choice == 1:
                view_in_list(db)
            
            elif choice == 2:
                add_items(db)
                
            elif choice == 5:
                keep_going = False
            
            else:
                print("incorrect number enterd.")
                
        except:
            print("Error: Please enter a number")
    

if __name__ == "__main__":
    main()
    

