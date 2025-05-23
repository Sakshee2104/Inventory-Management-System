from tkinter import *
from Employees import employee_form
from suppliers import supplier_form
from category import category_form
from products import product_form
from Employees import connect_database
from tkinter import messagebox
import time

def update():
    cursor,connection=connect_database()
    if not cursor or not connection:
            return
    cursor.execute('USE dbmsProj')
    cursor.execute('SELECT * FROM emp_data')
    emp_records=cursor.fetchall()
    total_emp_count_label.config(text=(len(emp_records)))

    cursor.execute('SELECT * FROM sup_data')
    sup_records=cursor.fetchall()
    total_sup_count_label.config(text=(len(sup_records)))

    cursor.execute('SELECT * FROM cat_data')
    cat_records=cursor.fetchall()
    total_cat_count_label.config(text=(len(cat_records)))

    cursor.execute('SELECT * FROM prod_data')
    prod_records=cursor.fetchall()
    total_prod_count_label.config(text=(len(prod_records)))

    date_time = time.strftime('%I:%M:%S %p on %A, %B %d, %Y')
    subtitleLabel.config(text=f'Welcome Admin\t\t\t\t\t\t {date_time}')
    subtitleLabel.after(1000,update)

def tax_window():
    def save_tax():
        value1=tax_count.get()
        cursor,connection=connect_database()
        if not cursor or not connection:
            return
        cursor.execute('USE dbmsProj')
        cursor.execute('CREATE TABLE IF NOT EXISTS tax_table (id INT primary key, tax DECIMAL(5,2))')
        cursor.execute('SELECT id from tax_table WHERE id=1')
        if cursor.fetchone():
            cursor.execute('UPDATE tax_table SET tax=%s WHERE id=1', value1)
        else:
            cursor.execute('INSERT INTO tax_table (id,tax) VALUES (1,%s)', value1)
        connection.commit()
        messagebox.showinfo('Success',f'Tax is set to {value1}% and saved successfully.', parent=tax_root)

    tax_root=Toplevel()
    tax_root.title('Tax window')
    tax_root.geometry('300x200')
    tax_root.grab_set()
    tax_percentage=Label(tax_root, text='Enter Tax Percentage(%)', font=('arial',12))
    tax_percentage.pack(pady=10)
    tax_count=Spinbox(tax_root, from_=0, to=100, font=('arial',12))
    tax_count.pack(pady=10)
    save_button=Button(tax_root, text='  Save', font=('arial',12, 'bold'), bg='#4d636d', fg='white', width=10, command=save_tax)
    save_button.pack(pady=20)

current_frame=None
def show_form(form_function):
    global current_frame
    if current_frame:
        current_frame.place_forget()
    current_frame=form_function(window)

#GUI Part
window=Tk()

window.title('Dashboard')
window.geometry('1270x690+0+0')
#window.resizable(0,0)         //to disable maximize button
window.config(bg='white')

bg_image=PhotoImage(file='shopping.png')
titleLabel=Label(window, image=bg_image, compound=LEFT, text=" Inventory Management System", font=('times new roman',48, 'bold'), bg='#010c48', fg='white', anchor='w', padx=20)
titleLabel.place(x=0, y=0, relwidth=1)

logoutButton=Button(window, text='Logout', font=('times new roman',20, 'bold'),fg='#010c48')
logoutButton.place(x=1100, y=10)

subtitleLabel=Label(window, text='Welcome Admin\t\t Date: 02-10-2024\t\t Time:12.36.17 pm', font=('times new roman',15), bg='#4d636d',fg='white')
subtitleLabel.place(x=0, y=80, relwidth=1)

leftFrame=Frame(window)
leftFrame.place(x=0, y=108, width=200, height=600)

logoImage=PhotoImage(file='logo.png')
imageLabel=Label(leftFrame, image=logoImage)
imageLabel.grid(row=0,column=0)
imageLabel.pack()

employee_icon=PhotoImage(file='employee.png')
employee_button=Button(leftFrame, image=employee_icon, compound=LEFT, text='  Employees', font=('times new roman',20, 'bold'), anchor='w', padx=10, command=lambda :show_form(employee_form))
employee_button.pack(fill=X)

supplier_icon=PhotoImage(file='supplier.png')
supplier_button=Button(leftFrame, image=supplier_icon, compound=LEFT, text='  Supplier', font=('times new roman',20, 'bold'), anchor='w', padx=10, command=lambda:show_form(supplier_form))
supplier_button.pack(fill=X)

category_icon=PhotoImage(file='category.png')
category_button=Button(leftFrame, image=category_icon, compound=LEFT, text='  Category', font=('times new roman',20, 'bold'), anchor='w', padx=10, command=lambda:show_form(category_form))
category_button.pack(fill=X)

products_icon=PhotoImage(file='product.png')
products_button=Button(leftFrame, image=products_icon, compound=LEFT, text='  Products', font=('times new roman',20, 'bold'), anchor='w', padx=10, command=lambda: show_form(product_form))
products_button.pack(fill=X)

sales_icon=PhotoImage(file='sales.png')
sales_button=Button(leftFrame, image=sales_icon, compound=LEFT, text='  Sales', font=('times new roman',20, 'bold'), anchor='w', padx=10)
sales_button.pack(fill=X)

tax_icon=PhotoImage(file='tax.png')
tax_button=Button(leftFrame, image=tax_icon, compound=LEFT, text='  Tax', font=('times new roman',20, 'bold'), anchor='w', padx=10, command=tax_window )
tax_button.pack(fill=X)

exit_icon=PhotoImage(file='exit.png')
exit_button=Button(leftFrame, image=exit_icon, compound=LEFT, text='  Exit', font=('times new roman',20, 'bold'), anchor='w', padx=10)
exit_button.pack(fill=X)

emp_frame=Frame(window, bg='#2C3E50', bd=3, relief=RIDGE)
emp_frame.place(x=400,y=125,height=170, width=280)
total_emp_icon=PhotoImage(file='total_emp.png')
total_emp_icon_label=Label(emp_frame, image=total_emp_icon, bg='#2C3E50')
total_emp_icon_label.pack()

total_emp_label=Label(emp_frame, text='Total Employees', bg='#2C3E50', fg='white', font=('times new roman',20,'bold'))
total_emp_label.pack(pady=10)

total_emp_count_label=Label(emp_frame, text='0', bg='#2C3E50', fg='white', font=('times new roman',20,'bold'))
total_emp_count_label.pack()

sup_frame=Frame(window, bg='#8E44AD', bd=3, relief=RIDGE)
sup_frame.place(x=800,y=125,height=170, width=280)
total_sup_icon=PhotoImage(file='total_sup.png')
total_sup_icon_label=Label(sup_frame, image=total_sup_icon, bg='#8E44AD')
total_sup_icon_label.pack()

total_sup_label=Label(sup_frame, text='Total Suppliers', bg='#8E44AD', fg='white', font=('times new roman',20,'bold'))
total_sup_label.pack()

total_sup_count_label=Label(sup_frame, text='0', bg='#8E44AD', fg='white', font=('times new roman',20,'bold'))
total_sup_count_label.pack(pady=10)

cat_frame=Frame(window, bg='#27AE60', bd=3, relief=RIDGE)
cat_frame.place(x=400,y=310,height=170, width=280)
total_cat_icon=PhotoImage(file='total_cat.png')
total_cat_icon_label=Label(cat_frame, image=total_cat_icon, bg='#27AE60')
total_cat_icon_label.pack()

total_cat_label=Label(cat_frame, text='Total Categories', bg='#27AE60', fg='white', font=('times new roman',20,'bold'))
total_cat_label.pack()
 
total_cat_count_label=Label(cat_frame, text='0', bg='#27AE60', fg='white', font=('times new roman',20,'bold'))
total_cat_count_label.pack(pady=10)

prod_frame=Frame(window, bg='#2980B9', bd=3, relief=RIDGE)
prod_frame.place(x=800,y=310,height=170, width=280)
total_prod_icon=PhotoImage(file='total_prod.png')
total_prod_icon_label=Label(prod_frame, image=total_prod_icon, bg='#2980B9')
total_prod_icon_label.pack()

total_prod_label=Label(prod_frame, text='Total Products', bg='#2980B9', fg='white', font=('times new roman',20,'bold'))
total_prod_label.pack()

total_prod_count_label=Label(prod_frame, text='0', bg='#2980B9', fg='white', font=('times new roman',20,'bold'))
total_prod_count_label.pack(pady=10)

sales_frame=Frame(window, bg='#E74C3C', bd=3, relief=RIDGE)
sales_frame.place(x=600,y=495,height=170, width=280)
total_sales_icon=PhotoImage(file='total_sales.png')
total_sales_icon_label=Label(sales_frame, image=total_sales_icon, bg='#E74C3C')
total_sales_icon_label.pack()

total_sales_label=Label(sales_frame, text='Total Sales', bg='#E74C3C', fg='white', font=('times new roman',20,'bold'))
total_sales_label.pack()

total_sales_count_label=Label(sales_frame, text='0', bg='#E74C3C', fg='white', font=('times new roman',20,'bold'))
total_sales_count_label.pack(pady=10)

update()

window.mainloop()
