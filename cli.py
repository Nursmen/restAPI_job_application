import sqlite3

def get_db():
    conn = sqlite3.connect("sales.db", check_same_thread=False)
    return conn

def delete_all_items():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Images")
    cursor.execute("DELETE FROM Item")
    conn.commit()
    conn.close()
    print("\n✅ All items (and their images) deleted.\n")

def delete_all_comments_and_likes():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Comment")
    cursor.execute("DELETE FROM UserLikedItems")
    conn.commit()
    conn.close()
    print("\n✅ All comments and likes deleted.\n")

def create_category():
    name = input("Enter new category name: ").strip()
    if not name:
        print("⚠️ Category name cannot be empty.\n")
        return
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Type (name) VALUES (?)", (name,))
        conn.commit()
        print(f"\n✅ Category '{name}' created.\n")
    except sqlite3.IntegrityError:
        print(f"\n⚠️ Category '{name}' already exists.\n")
    conn.close()

def main():
    ascii_art = r"""
  _   _                       __      
 | \ | |                     / _|     
 |  \| |_   _ _ __ ___  ___ | |_ ___  
 | . ` | | | | '__/ __|/ _ \|  _/ _ \ 
 | |\  | |_| | |  \__ \ (_) | || (_) |
 |_| \_|\__,_|_|  |___/\___/|_| \___/                            
    """
    print(ascii_art)
    while True:
        print("Choose an action:")
        print("1. Delete all items (and images)")
        print("2. Delete all comments and likes")
        print("3. Create a new category")
        print("0. Exit")
        choice = input("Enter a number: ").strip()

        if choice == "1":
            delete_all_items()
        elif choice == "2":
            delete_all_comments_and_likes()
        elif choice == "3":
            create_category()
        elif choice == "0":
            print("👋 Goodbye!")
            break
        else:
            print("⚠️ Invalid choice, try again.\n")

if __name__ == "__main__":
    main()
