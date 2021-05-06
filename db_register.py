from tkinter import messagebox

def insert_db(name, num, desig):
    try:
        import pymysql
        connection = pymysql.connect(host="localhost", user="root", passwd="", database="person_identification")
        cursor = connection.cursor()
        sql = "insert into employee values('%s','%s','%s')"
        args = (name, num, desig)
        cursor.execute(sql % args)
        connection.commit()
        str1 = "select * from employee"
        cursor.execute(str1)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        connection.close()
    except(Exception):
        messagebox.showwarning("Error","Registration failed")


