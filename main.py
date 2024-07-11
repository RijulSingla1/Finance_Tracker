import sqlite3
import csv

# Connect to SQLite database (create if not exists)
conn = sqlite3.connect('finance_tracker.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create transactions table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        amount REAL NOT NULL,
        description TEXT,
        category TEXT
        
        
    )
''')

#categories table 

cursor.execute('''CREATE TABLE IF NOT EXISTS categories
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL)
                ''')

# # Commit changes to the database
conn.commit()

# # Close the database connection
# FUNCTIONS 

def add_transaction(date, amount,description='None',category='other'):
    try:
        amount=float(amount)
        conn = sqlite3.connect('finance_tracker.db')
        cursor = conn.cursor()


        cursor.execute('SELECT id FROM categories WHERE name= ?',(category,))
        category_id= cursor.fetchone()

        if not category_id:
            cursor.execute('INSERT INTO categories(name) VALUES(?)',(category,) )
            category_id= cursor.lastrowid
        else:
            category_id=category_id[0]
        
        
        cursor.execute(''' INSERT INTO transactions (date, amount, description,category)
                            VALUES (?, ?, ?,?)''',
                       (date, amount, description,category_id))
        conn.commit()
        

    except ValueError:
        print("Invalid amount entered. Please enter a numerical value.")
        
    except sqlite3.Error as e:
        print(f"An error occured: {e}")
        
    finally:
        conn.close()

def get_transactions(start_date,end_date):
    try:
        
        conn=sqlite3.connect('finance_tracker.db')
        cursor=conn.cursor()
        
        if start_date  and end_date :
            cursor.execute('''SELECT * FROM transactions WHERE date BETWEEN  ? AND 
             ? ''',(start_date,end_date))
            
        
    
        else:
            cursor.execute('SELECT * FROM transactions')
        output=cursor.fetchall()
        conn.close()
    
        if output:
            for i in output:
                print(f"Id: {i[0]}, Date:{i[1]}, Amount: {i[2]}, Description: {i[3]}")
    
        else:
            print("No Transactions found")

    except sqlite3.Error as e:
        print(f"An error occured: {e}")

    finally:
        conn.close()


def delete_transaction(Date):
    try:
        conn=sqlite3.connect('finance_tracker.db')
        cursor=conn.cursor()
        
        cursor.execute("DELETE FROM transactions WHERE date= ?",(Date,) )
        conn.commit()
        if cursor.rowcount>0:
            print("Deleted Successfully")
        else:
            print("Transaction not found for given date ")
            
    except sqlite3.Error as e:
        print(f"An error occured: {e}")
    finally:
        conn.close()
    

def update_transaction(Date,Amount):
    try:
        Amount=float(Amount)
        conn=sqlite3.connect('finance_tracker.db')
        cursor=conn.cursor()
        cursor.execute('UPDATE transactions SET amount = ? WHERE date=?',(Amount,Date) )
        conn.commit()
        
        if cursor.rowcount>0:
            print("Updated Successfully")
        else:
            print("Transaction not found for given date ")

    except ValueError:
        print("Invalid amount entered. Please enter a numerical value.")

    except sqlite3.Error as e:
        print(f"An error occured: {e}")
    finally:
        conn.close()
        

def get_categories():
    try:
        conn=sqlite3.connect('finance_tracker.db')
        cursor=conn.cursor()
        cursor.execute('SELECT name FROM categories ')
        name=cursor.fetchall()

        if name :
            for row in name:
                print( f"{row[0] }\n")

        else:
            print("no categories found")
    
        
            
    except sqlite3.Error as e:
        print(f"An error occured: {e}")
        
    finally:
        conn.close()


# GENERATING REPORTS

def generate_monthly_spending_report():
    try:
        conn=sqlite3.connect('finance_tracker.db')
        cursor=conn.cursor()
        cursor.execute('''SELECT  strftime('%Y-%m', date) AS month, SUM(amount) AS total_amount
                FROM transactions
                GROUP BY month
                ORDER BY month
            ''') 
        report = cursor.fetchall()
        conn.close()
        
        if report:
            print("Monthly Spending Report:")
            for row in report:
                print(f"Month: {row[0]}, Total Amount: {row[1]}")
        else:
            print("No transactions found.")
        
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")



def export_transactions_to_csv(filename):
    try:
        conn = sqlite3.connect('finance_tracker.db')
        cursor = conn.cursor()

        # Fetch all transactions from the database
        cursor.execute('SELECT * FROM transactions')
        transactions = cursor.fetchall()

        # Specify CSV file headers
        headers = ['ID', 'Date', 'Amount', 'Description']

        # Write data to CSV file
        with open(filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(headers)
            csv_writer.writerows(transactions)

        print(f"Transactions exported to {filename} successfully.")

    except sqlite3.Error as e:
        print(f"Error exporting transactions: {e}")

    finally:
        if conn:
            conn.close()
    
            
    
        
    
        
    
# add_transaction('2024-07-06',2000,'Movie')
# get_transactions()
    
def main():
    
    print("""Welcome to Personal Finance Tracker CLI\n
                option 1 : Add Transaction\n
                option 2 : Display Transactions\n
                option 3 : Delete Transaction \n
                option 4 : Update Transaction\n
                option 5 : View Categories \n
                option 6 : View monthly generated reports \n
                option 7 : Export CSV file \n
                option 8 : Exit the Menu""")



    while True:
        option=input("Enter an option: ")
        
        if(option == '1'):
            date =     input("Enter Date : ")
            amount=     input("Enter Amount : ")
            description= input("Enter Description : ")
            category= input("Enter category name : ")
            
            add_transaction(date,amount,description,category)
            print("Added Successfully")
            
        elif (option == '2'):
            start_date=input('Enter Starting Date: ')
            end_date=input('Enter End Date: ')
            
            get_transactions(start_date,end_date)
            print("Got Successfully")

        elif (option == '3'):
            Date= input('Enter Date for transaction you want to delete: ')
            delete_transaction(Date)

        elif (option == '4'):
            Date=input('Enter Date for transaction you want to update: ')
            Amount=input('Enter Amount for transaction you want to update: ')
            update_transaction(Date,Amount)

        elif(option=='5'):
            get_categories()

        elif(option=='6'):
            generate_monthly_spending_report()

        elif(option=='7'):
            export_transactions_to_csv('transactions.csv')
            
        elif (option =='8'):
            print("Exited the Menu")
            break
            
        else:
                print("Invalid Option")
            

if __name__ == "__main__":
    main()
        
        

    
