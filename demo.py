import sqlite3
import pandas as pd
from tkinter import *
from tkinter import messagebox, simpledialog, scrolledtext
from datetime import datetime


root = Tk()
root.title("Library System")

conn = sqlite3.connect('library_database.db')
cursor = conn.cursor()
 
#   create table
def create_table():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Books (
        book_id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL
    )
    ''')
 
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Members (
        member_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE
    )
    ''')
 
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Borrowing_Records (
        borrow_id INTEGER PRIMARY KEY,
        book_id INTEGER,
        member_id INTEGER,
        borrow_date DATE,
        return_date DATE,
        is_returned BOOLEAN,
        FOREIGN KEY (book_id) REFERENCES Books (book_id),
        FOREIGN KEY (member_id) REFERENCES Members (member_id)
    )
    ''')
 
    # # Insert sample data into Books table
    # cursor.execute('''
    # INSERT INTO Books (title, author) VALUES
    # ('The Great Gatsby', 'F. Scott Fitzgerald'),
    # ('1984', 'George Orwell'),
    # ('To Kill a Mockingbird', 'Harper Lee')
    # ''')
 
    # # Insert sample data into Members table
    # cursor.execute('''
    # INSERT INTO Members (name, email) VALUES
    # ('John Doe', 'john.doe@example.com'),
    # ('Jane Smith', 'jane.smith@example.com'),
    # ('Alice Johnson', 'alice.johnson@example.com')
    # ''')
 
    conn.commit()
    conn.close()
    
#personal record csv
def download_personal_record():
    
    member_id = simpledialog.askstring("Input", "member_id ?")
    conn = sqlite3.connect('library_database.db')
    cursor = conn.cursor()
    sql_query = pd.read_sql_query(f"SELECT borrowed.book_id, b.title, b.author FROM Books AS b INNER JOIN (SELECT book_id FROM Borrowing_records WHERE member_id = {member_id} AND is_returned = False) AS borrowed on b.book_id = borrowed.book_id",conn)
    conn.close()
    df = pd.DataFrame(sql_query)
    df.to_csv('./personal_records.csv')
    print(f"Download member with ID '{member_id}' borrowed book list successfully.")
    messagebox.showinfo("",f"Download member with ID '{member_id}' borrowed book list successfully.")

#book list csv

    
def download_books():
    conn = sqlite3.connect('library_database.db')
    cursor = conn.cursor()
    sql_query = pd.read_sql_query('SELECT b.book_id, b.title, b.author, COALESCE(br.is_returned,True) AS storage FROM Books AS b LEFT JOIN (SELECT book_id, MAX(borrow_id) as latest_borrow_id, is_returned FROM Borrowing_records GROUP BY book_id) AS br ON b.book_id = br.book_id',conn)
    conn.close()
    df = pd.DataFrame(sql_query, columns=["book_id", "title", "author", "storage"])
    df.to_csv('./book_list.csv')
    print(f"Download book list successfully.")
    messagebox.showinfo("",f"Download book list successfully.")

#member list csv

def download_members():
    conn = sqlite3.connect('library_database.db')
    cursor = conn.cursor()
    sql_query = pd.read_sql_query('SELECT b.book_id, b.title, b.author, COALESCE(br.is_returned,True) AS storage FROM Books AS b LEFT JOIN (SELECT book_id, MAX(borrow_id) as latest_borrow_id, is_returned FROM Borrowing_records GROUP BY book_id) AS br ON b.book_id = br.book_id',conn)
    conn.close()
    df = pd.DataFrame(sql_query, columns=["book_id", "title", "author", "storage"])
    df.to_csv('./member_list.csv')
    print(f"Download member list successfully.")
    messagebox.showinfo("",f"Download member list successfully.")

 
# view borrow_return list
def view_records():
    conn = sqlite3.connect('library_database.db')
    cursor = conn.cursor()
    sql_query = pd.read_sql_query('SELECT * FROM Borrowing_records',conn)
    conn.close()
    df = pd.DataFrame(sql_query)
    print(df.to_string(index=False))
    output.insert(END, f'{df}\n\n')
 
# view books list
def view_books():
    conn = sqlite3.connect('library_database.db')
    cursor = conn.cursor()
    # get the latest status of books
    sql_query = pd.read_sql_query('SELECT b.book_id, b.title, b.author, COALESCE(br.is_returned,True) AS storage FROM Books AS b LEFT JOIN (SELECT book_id, MAX(borrow_id) as latest_borrow_id, is_returned FROM Borrowing_records GROUP BY book_id) AS br ON b.book_id = br.book_id',conn)
    conn.close()
    # convert to df
    df = pd.DataFrame(sql_query, columns=["book_id", "title", "author", "storage"])
    if df.empty:
        print("No book.")
        messagebox.showinfo('',"No book.")
    else:
        #print(df.to_string(index=False))
        output.insert(END, f'{df}\n\n')  
        print("")
        




 
 
# view members list
def view_members():
    conn = sqlite3.connect('library_database.db')
    cursor = conn.cursor()
#     cursor.execute('SELECT * FROM Members')
#     rows = cursor.fetchall()
#     conn.close()
 
#     if rows:
#         for row in rows:
#             print(f"ID: {row[0]}, Name: {row[1]}, Email: {row[2]}")
#     else:
#         print("No members found.")
    sql_query = pd.read_sql_query('SELECT Members.member_id, name ,email, COALESCE(no,0) AS no_of_borrowed FROM Members LEFT JOIN (SELECT member_id, COUNT(*) AS no FROM Borrowing_Records WHERE is_returned = False group by member_id) AS count_borrow ON Members.member_id = count_borrow.member_id' ,conn)
    conn.close()
    df = pd.DataFrame(sql_query, columns=["member_id","name","email","no_of_borrowed"])
    if df.empty:
        print("No Member.")
        messagebox.showinfo('',"No Member")
    else:
        print(df.to_string(index=False))
        
        output.insert(END, f'{df}\n\n')
 
# add book
def add_book():
    
    title = simpledialog.askstring("Input", "Enter book title:")
    author = simpledialog.askstring("Input", "Enter book author:")
    
    conn = sqlite3.connect('library_database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Books (title, author) VALUES (?, ?)', (title, author))
    conn.commit()
    conn.close()
    print(f"Book '{title}' added successfully.")
    messagebox.showinfo("",f"Book '{title}' added successfully.")
 
# update book
def update_book():
    
   
    
    conn = sqlite3.connect('library_database.db')
    cursor = conn.cursor()
    
    book_id = simpledialog.askstring("Input", "Enter book ID: ")
    cursor.execute('SELECT * FROM Books WHERE book_id = ?', (book_id))
    is_book_id = cursor.fetchone()
    
    if not is_book_id:
        print("not member")
        messagebox.showinfo("","Book NOT found")
        
    if is_book_id:
        title = simpledialog.askstring("Input", "Enter new title (Press ENTER directly if no changes on title)")
        author = simpledialog.askstring("Input", "Enter new author (Press ENTER directly if no changes on author)")
    
    
    
    if is_book_id != 0:
        if title == "" and author == "":
            pass
        elif title == "":
            cursor.execute('UPDATE Books SET author = ? WHERE book_id = ?', (author, book_id))
        elif author == "":
            cursor.execute('UPDATE Books SET title = ? WHERE book_id = ?', (title, book_id))
        else:
            cursor.execute('UPDATE Books SET title = ?, author = ? WHERE book_id = ?', (title, author, book_id))
        conn.commit()
        cursor.execute('''
        SELECT title FROM Books WHERE book_id = ?
        ''', (book_id,))
        updated_book = cursor.fetchone()
        conn.close()
        if title == "" and author == "":
            print(f"Info of book '{updated_book[0]}' remains unchanged")
            messagebox.showinfo('',f"Info of book '{updated_book[0]}' remains unchanged")
        else:
            print(f"Info of book '{updated_book[0]}' updated successfully.")
            messagebox.showinfo('success',f"Info of book '{updated_book[0]}' updated successfully.")
    else:
        conn.close()
        print(f"Book with ID {book_id} does not exist.")
 
# update memeber
def update_member():
    member_id = simpledialog.askstring("Input", "Enter member ID")
    
    
    
    
    conn = sqlite3.connect('library_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Members WHERE member_id = ?', (member_id))
    is_member_id = cursor.fetchone()
    
    if not is_member_id:
        print("not member")
        messagebox.showinfo("","Member NOT found")
        return
    
    
    if is_member_id:
        name = simpledialog.askstring("Input", "Enter new name (Press ENTER directly if no changes on name):")
        email = simpledialog.askstring("Input", "Enter new email (Press ENTER directly if no changes on email):")
    
    
    if is_member_id != 0:
        if name == "" and email == "":
            pass
        elif name == "":
            cursor.execute('UPDATE Members SET email = ? WHERE member_id = ?', (email, member_id))
        elif email == "":
            cursor.execute('UPDATE Members SET name = ? WHERE member_id = ?', (name, member_id))
        else:
            cursor.execute('UPDATE Members SET name = ?, email = ? WHERE member_id = ?', (name, email, member_id))
        conn.commit()
        cursor.execute('''
        SELECT name FROM Members WHERE member_id = ? 
        ''', (member_id,))
        updated_member = cursor.fetchone()
        conn.close()
        if name == "" and email == "":
            print(f"Info of member '{updated_member[0]}' remains unchanged")
            messagebox.showinfo('',f"Info of member '{updated_member[0]}' remains unchanged")
        else:
            print(f"Info of member '{updated_member[0]}' updated successfully.")
            messagebox.showinfo('',f"Info of member '{updated_member[0]}' updated successfully.")
    else:
        conn.close()
        print(f"Member with ID {member_id} does not exist.")
        messagebox.showinfo('',f"Member with ID {member_id} does not exist.")
        
 
# add member
def add_member():
    name = simpledialog.askstring("Input", "Enter member name: ")
    email = simpledialog.askstring("Input", "Enter member email")
    conn = sqlite3.connect('library_database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Members (name, email) VALUES (?, ?)', (name, email))
    conn.commit()
    conn.close()
    print(f"Member '{name}' added successfully.")
    messagebox.showinfo("Input", f"Member '{name}' added successfully.")
    
def is_valid_date(date_str):
  try:
      datetime.strptime(date_str, '%Y-%m-%d')
      return True
  except ValueError:
      return False

 
# borrow book
def borrow_book():
    
    member_id = simpledialog.askstring("Input", "member_id")
    book_id = simpledialog.askstring("Input", "book_id")
    borrow_date = simpledialog.askstring("Input", "borrow_date YYYY-MM-DD")

    conn = sqlite3.connect('library_database.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT is_returned FROM Borrowing_Records WHERE book_id = ? ORDER BY borrow_id desc LIMIT 1
    ''', (book_id,))
    is_returned = cursor.fetchone()
    cursor.execute('''
    SELECT title FROM Books WHERE book_id = ?
    ''', (book_id,))
    book_name = cursor.fetchone()
    cursor.execute('''
    SELECT name FROM Members WHERE member_id = ?
    ''', (member_id,))
    member_name = cursor.fetchone()

    # check if date valid
    if not is_valid_date(borrow_date):
        conn.close()
        print(f"Borrow Date Format is not valid.")
        messagebox.showinfo('',f"Borrow Date Format is not valid.")
    # check if book/member exists
    elif book_name is not None and member_name is not None:
        #check if it is borrowed
        if is_returned is not None and is_returned[0] != 1:
            conn.close()
            print(f"'{book_name[0]} ({member_id})' is already borrowed.")
            messagebox.showinfo('',f"'{book_name[0]} ({member_id})' is already borrowed.")

        else:
          cursor.execute('''
          SELECT COUNT(*) AS no_of_borrowed FROM Borrowing_Records WHERE is_returned = False AND member_id = ?
          ''', (member_id,))
          count_borrowed = cursor.fetchone()
          if count_borrowed[0] <= 1:
            borrow_date = datetime.strptime(borrow_date, '%Y-%m-%d').date()
            cursor.execute('''
            INSERT INTO Borrowing_Records (book_id, member_id, borrow_date, is_returned) VALUES (?, ?, ?, False)
            ''', (book_id, member_id, borrow_date))
            conn.commit()
            conn.close()
            print(f"'{member_name[0]} ({member_id})' borrowed '{book_name[0]}' successfully.")
            messagebox.showinfo('',f"'{member_name[0]} ({member_id})' borrowed '{book_name[0]}' successfully.")
          else:
            conn.close()
            print(f"{member_name[0]} ({member_id})' borrowed too many books(>= 2)")
            messagebox.showinfo('',f"{member_name[0]} ({member_id})' borrowed too many books(>= 2)")

    else:
        conn.close()
        print(f"Book with ID {book_id} / Member with ID {member_id} does not exist.")
        messagebox.showinfo('',f"Book with ID {book_id} / Member with ID {member_id} does not exist.")

 
# return book
def return_book():
    
    member_id = simpledialog.askstring("Input", "member_id")
    book_id = simpledialog.askstring("Input", "book_id")
    return_date = simpledialog.askstring("Input", "return_date YYYY-MM-DD ")
    
    conn = sqlite3.connect('library_database.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT is_returned FROM Borrowing_Records WHERE book_id = ? AND member_id = ? ORDER BY borrow_id desc LIMIT 1
    ''', (book_id, member_id))
    is_returned = cursor.fetchone()
    cursor.execute('''
    SELECT title FROM Books WHERE book_id = ?
    ''', (book_id,))
    book_name = cursor.fetchone()
    cursor.execute('''
    SELECT name FROM Members WHERE member_id = ?
    ''', (member_id,))
    member_name = cursor.fetchone()

    # check if date valid
    if not is_valid_date(return_date):
        conn.close()
        print(f"Return Date Format is not valid.")
        messagebox.showinfo('',f"Return Date Format is not valid.")
    
    elif book_name is not None and member_name is not None:
        if is_returned[0] == 1:
            conn.close()
            print(f"No record of '{book_name[0]} {book_id}' being borrowed by member with ID {member_id}.")
            messagebox.showinfo('',f"No record of '{book_name[0]} {book_id}' being borrowed by member with ID {member_id}.")
        else:

            return_date = datetime.strptime(return_date, '%Y-%m-%d').date()
            cursor.execute('''
            UPDATE Borrowing_Records SET is_returned = True, return_date = ? WHERE book_id = ? AND member_id = ?
            ''', (return_date, book_id, member_id))
            conn.commit()
            cursor.execute('''
            SELECT julianday(return_date)-julianday(borrow_date) AS days_borrowed FROM Borrowing_Records WHERE book_id = ? AND member_id = ? AND return_date = ? ORDER BY borrow_id desc LIMIT 1
            ''', (book_id, member_id, return_date))
            date_diff = cursor.fetchone()
            conn.close()
            if date_diff[0] <= 6:
                print(f"'{book_name[0]}' returned successfully. No extra charge.")
                messagebox.showinfo('',f"'{book_name[0]}' returned successfully. No extra charge.")

            else:
                print(f"'{book_name[0]}' returned successfully.")
                messagebox.showinfo('',f"'{book_name[0]}' returned successfully.")
                print(f"Member with ID '{member_id}' returns {str(date_diff[0]-6)} days late. ${str((date_diff[0]-6)*0.5)} should be charged")
                messagebox.showinfo('',f"Member with ID '{member_id}' returns {str(date_diff[0]-6)} days late. ${str((date_diff[0]-6)*0.5)} should be charged")
    else:
        conn.close()
        print(f"Book with ID {book_id} / Member with ID {member_id} does not exist.")
        messagebox.showinfo('',f"Book with ID {book_id} / Member with ID {member_id} does not exist.")


def search_book_id():

    id = simpledialog.askstring("Input", "Search book with enter the ID ")
    conn = sqlite3.connect('library_database.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM Books WHERE book_id = ?', (id,))
    have_book = cursor.fetchall()
    
    if not have_book:
        print("No book is found.")
        messagebox.showinfo('',"No book is found.")
        return
    
    if id is not None and id != '':
        sql_query = pd.read_sql_query(f"SELECT * FROM Books WHERE book_id = {id}",conn)
        conn.close()
        # convert to df
        df = pd.DataFrame(sql_query, columns=["book_id", "title", "author"])
        if df.empty:
            print("No book is found.")
            messagebox.showinfo('',"No book is found.")
        else:
            print(df.to_string(index=False))
            output.insert(END, f'{df}\n\n')
    else:
        conn.close()
        print('Search should not be empty.')
        messagebox.showinfo('',"Search should not be empty.")

def search_book_info():
    info = simpledialog.askstring("Input", "Enter related book detail ")

    conn = sqlite3.connect('library_database.db')
    cursor = conn.cursor()
    if info is not None and info != '':
        sql_query = pd.read_sql_query(f"SELECT * FROM Books WHERE LOWER(title) LIKE '%{info.lower()}%' or author LIKE '%{info.lower()}%'",conn)
        conn.close()
        # convert to df
        df = pd.DataFrame(sql_query, columns=["book_id", "title", "author"])
        if df.empty:
            print("No book is found.")
            messagebox.showinfo('',"No book is found.")

        else:
            print(df.to_string(index=False))
            output.insert(END, f'{df}\n\n')
    else:
        conn.close()
        print('Search should not be empty.')
        messagebox.showinfo('',"Search should not be empty.")
        
def search_member_id():

    id = simpledialog.askstring("Input", "Search member with enter the ID ") 
    conn = sqlite3.connect('library_database.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM Members WHERE member_id = ?', (id,))
    have_member = cursor.fetchall()
    
    if not have_member:
        print("No member is found.")
        messagebox.showinfo('',"No member is found.")
        return
    
    sql_query = pd.read_sql_query(f"SELECT * FROM Members WHERE member_id = {id}",conn)
    conn.close()
    
   
    
    if id is not None and id != '':
        
        # convert to df
        df = pd.DataFrame(sql_query, columns=["member_id", "name", "email"])
        if df.empty:
            print("No member is found.")
            messagebox.showinfo('',"No member is found.")
        else:
            print(df.to_string(index=False))
            output.insert(END, f'{df}\n\n')
    else:
        conn.close()
        print('Search should not be empty.')
        messagebox.showinfo('',"Search should not be empty.")

def search_member_info():
    info = simpledialog.askstring("Input", "Enter related member detail ")

    conn = sqlite3.connect('library_database.db')
    cursor = conn.cursor()
    if info is not None and info != '':
        sql_query = pd.read_sql_query(f"SELECT * FROM Members WHERE LOWER(name) LIKE '%{info.lower()}%' or email LIKE '%{info.lower()}%'",conn)
        conn.close()
        # convert to df
        df = pd.DataFrame(sql_query, columns=["member_id", "name", "email"])
        if df.empty:
            print("No Member is found.")
            messagebox.showinfo('',"No Member is found.")

        else:
            print(df.to_string(index=False))
            output.insert(END, f'{df}\n\n')
    else:
        conn.close()
        print('Search should not be empty.')
        messagebox.showinfo('',"Search should not be empty.")
 

def test():
    
    conn = sqlite3.connect('library_database.db')
    cursor = conn.cursor()
    
    
    cursor.execute('SELECT * FROM Books WHERE book_id = ?', (2,))
    have_book = cursor.fetchall()
 
    sql_query = pd.read_sql_query('SELECT b.book_id, b.title, b.author, COALESCE(br.is_returned,True) AS storage FROM Books AS b LEFT JOIN (SELECT book_id, MAX(borrow_id) as latest_borrow_id, is_returned FROM Borrowing_records GROUP BY book_id) AS br ON b.book_id = br.book_id',conn)

    df = pd.DataFrame(sql_query, columns=["storage"])
    
    first_value = df['storage']
    
    int1 = first_value.fillna(0).astype(int)
    
    output.insert(END, f'{type(int1)}]  {int1}\n\n')
    



def remove_book():
    book_id = simpledialog.askstring("Input", "Book ID that you want to remove")
    conn = sqlite3.connect('library_database.db')
    cursor = conn.cursor()
    
    
    cursor.execute('SELECT * FROM Books WHERE book_id = ?', (book_id,))
    have_book = cursor.fetchall()
 
    sql_query = pd.read_sql_query('SELECT b.book_id, b.title, b.author, COALESCE(br.is_returned,True) AS storage FROM Books AS b LEFT JOIN (SELECT book_id, MAX(borrow_id) as latest_borrow_id, is_returned FROM Borrowing_records GROUP BY book_id) AS br ON b.book_id = br.book_id',conn)

    df = pd.DataFrame(sql_query, columns=["storage"])
    
    
    if have_book :
        cursor.execute('DELETE FROM Books WHERE book_id = ?', (book_id,))
        print(f"Book with ID {book_id} is removed.")
        messagebox.showinfo('',f"Book with ID {book_id} is removed.")
    else:
        print('No book found.')
        messagebox.showinfo('',f"No book found")
        #messagebox.showinfo('',f"No book found/ Book not return")
    conn.commit()
    conn.close()
 
 
def remove_member():
    member_id = simpledialog.askstring("Input", "member_id that you want to remove:")
    conn = sqlite3.connect('library_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Members WHERE member_id = ?', (member_id,))
    have_member = cursor.fetchall()
    
    sql_query = pd.read_sql_query('SELECT b.book_id, b.title, b.author, COALESCE(br.is_returned,True) AS storage FROM Books AS b LEFT JOIN (SELECT book_id, MAX(borrow_id) as latest_borrow_id, is_returned FROM Borrowing_records GROUP BY book_id) AS br ON b.book_id = br.book_id',conn)

    df = pd.DataFrame(sql_query, columns=["storage"])
    
    
    
    
 
    if have_member :
        cursor.execute('DELETE FROM Members WHERE member_id = ?', (member_id,))
        print(f"Member with ID {member_id} is removed.")
        messagebox.showinfo('',f"Member with ID {member_id} is removed.")
    else:
        print("Member not found.")
        messagebox.showinfo('',"Member not found.")
        #messagebox.showinfo('',"Member not found./Member Not return book")
    conn.commit()
    conn.close()    
 
def main():
    create_table()
 
    while True:
        print("\n1. Add book")
        print("2. Update book")
        print("3. Delete book")
        print("4. View books")
        print("5. Add member")
        print("6. Update member")
        print("7. Delete member")
        print("8. View members")
        print("9. Borrow Book")
        print("10. Return Book")
        print("11. Search Book")
        print("12. View record")
        print("0. Exit")
 
        choice = input("Choose an option: ")
 
        if choice == '1':
            title = input("Enter title: ")
            author = input("Enter author: ")
            add_book(title, author)
        elif choice == '2':
            book_id = input("Enter book ID: ")
            title = input("Enter new title (Press ENTER directly if no changes on title): ")
            author = input("Enter new author (Press ENTER directly if no changes on author): ")
            update_book(book_id, title, author)
        elif choice == '3':
            book_id =input("Book ID that you want to remove: ")
            remove_book(book_id)
        elif choice == '4':
            view_books()
        elif choice == '5':
            name = input("Enter member name: ")
            email = input("Enter member email: ")
            add_member(name, email)
            view_members()
        elif choice == '6':
            member_id = input("Enter member ID: ")
            name = input("Enter new name (Press ENTER directly if no changes on name): ")
            email = input("Enter new email (Press ENTER directly if no changes on email): ")
            update_member(member_id, name, email)
        elif choice == '7':
            member_id =input("Book ID that you want to remove: ")
            remove_member(member_id)
        elif choice == '8':
            view_members()
        elif choice == '9':
            member_id = input("Enter member_id: ")
            book_id = input("Enter book_id: ")
            borrow_book(member_id, book_id)
        elif choice == '10':
            member_id = input("Enter member_id: ")
            book_id = input("Enter book_id: ")
            return_book(member_id, book_id)
        elif choice == '11':
            print("1. Search with book ID \n2. Search with book details")
            search_choice = input("Choose an option: ")
            if search_choice == '1':
              search_id = input("Enter book ID: ")
              search_book_id(search_id)
            elif search_choice == '2':
              search_info = input("Enter related book detail: ")
              search_book_info(search_info)
            else:
              print("Invalid option.")
        elif choice == '12':
            view_records()
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")

AddbookBTN = Button(root,text="Add book" ,command=add_book)
UpdatebookBTN = Button(root,text="Update book",command=update_book)
DeletebookBTN = Button(root,text="Delete book",command=remove_book)
ViewbooksBTN =Button(root,text="View books",command= view_books)
AddmemberBTN =Button(root,text="Add member",command=add_member)
UpdatememberBTN =Button(root,text="Update member",command=update_member)
DeletememberBTN = Button(root,text="Delete member",command=remove_member)
ViewmembersBTN =Button(root,text="View members",command=view_members)
BorrowBookBTN =Button(root,text="Borrow Book",command=borrow_book)
ReturnBookBTN =Button(root,text="Return Book",command=return_book)
#####STA
search_book_idBTN =Button(root,text="Search Book With ID",command=search_book_id)
search_book_infoBTN =Button(root,text="Search Book With INFO",command=search_book_info)
########END
ViewrecordBTN =Button(root,text="View record",command=view_records)
download_personal_recordBTN =Button(root,text="download_personal_record",command=download_personal_record)
download_booksBTN =Button(root,text="download_booksBTN",command=download_books)
download_membersBTN =Button(root,text="download_members",command=download_members)

test_BTN = Button(root,text="test_BTN",command=test)

test_BTN.grid(row=10, column=2)
def clear_output():
    output.delete(1.0,END)  
Clear =  Button(root, text="Clear Output", command=clear_output)

output = scrolledtext.ScrolledText(root, width=80, height=15)
search_member_idBTN =Button(root,text="Search member With ID",command=search_member_id)
search_member_infoBTN =Button(root,text="Search member With INFO",command=search_member_info)

# AddbookBTN.pack()
# UpdatebookBTN.pack()
# DeletebookBTN.pack()
# ViewbooksBTN.pack()
# AddmemberBTN.pack()
# UpdatememberBTN.pack()
# DeletememberBTN.pack()
# ViewmembersBTN.pack()
# BorrowBookBTN.pack()
# ReturnBookBTN.pack()
# search_book_idBTN.pack()
# search_book_infoBTN.pack()
# ViewrecordBTN.pack()
# Clear.pack()
# output.pack()

# Define buttons and their grid positions

AddbookBTN.grid(row=0, column=0)
UpdatebookBTN.grid(row=1, column=0)
DeletebookBTN.grid(row=2, column=0)
ViewbooksBTN.grid(row=3, column=0)

AddmemberBTN.grid(row=0, column=1)
UpdatememberBTN.grid(row=1, column=1)
DeletememberBTN.grid(row=2, column=1)
ViewmembersBTN.grid(row=3, column=1)
search_member_idBTN.grid(row=4, column=1)
search_member_infoBTN.grid(row=5, column=1)

BorrowBookBTN.grid(row=1, column=2)
ReturnBookBTN.grid(row=2, column=2)
ViewrecordBTN.grid(row=3, column=2)

search_book_idBTN.grid(row=5, column=0)
search_book_infoBTN.grid(row=6, column=0)


Clear.grid(row=7, column=0)
output.grid(row=10, column=1)

download_personal_recordBTN.grid(row=4, column=2)
download_booksBTN.grid(row=5, column=2)
download_membersBTN.grid(row=6, column=2)



if __name__ == "__main__":
    #root.configure(bg='black')
    create_table()
    root.mainloop()