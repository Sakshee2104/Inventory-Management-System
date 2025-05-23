from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import pymysql

def connect_database():
    try:
        connection = pymysql.connect(host='localhost', user='root',password='Sakshee@2104', port=3307)
        cursor = connection.cursor()
    except:
        messagebox.showerror('Error','Database connectivity issue try again, open mysql command line client')
        return None, None
    
    return cursor, connection

def create_db_table():
    cursor, connection = connect_database()
    cursor.execute('CREATE DATABASE IF NOT EXISTS dbmsProj')
    cursor.execute('USE dbmsProj')
    cursor.execute('CREATE TABLE IF NOT EXISTS emp_data (empid INT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100), gender VARCHAR(100), dob VARCHAR(50), contact VARCHAR(50), emp_type VARCHAR(100), education VARCHAR(100), work_shift VARCHAR(100), address VARCHAR(100), doj VARCHAR(50), salary VARCHAR(100), user_type VARCHAR(100), password VARCHAR(100))')
    
#connect_database()

def treeview_data():
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute('USE dbmsProj')
    try:
        cursor.execute('SELECT * FROM emp_data')
        emp_records = cursor.fetchall()
        employee_treeview.delete(*employee_treeview.get_children())
        for records in emp_records:
            employee_treeview.insert('',END, values=records)
    except Exception as e:
        messagebox.showerror('Error',f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()

def select_data(event, empid_entry, name_entry, email_entry, 
                gender_combobox, dob_date_entry, contact_entry,
                education_combobox, employement_type_combobox, 
                workshift_combobox, address_text, 
                doj_date_entry, salary_entry, usertype_combobox, 
                password_entry):
    index = employee_treeview.selection()
    content = employee_treeview.item(index)
    row = content['values']
    clear_fields(empid_entry, name_entry, email_entry, 
                gender_combobox, dob_date_entry, contact_entry,
                education_combobox, employement_type_combobox, 
                workshift_combobox, address_text, 
                doj_date_entry, salary_entry, usertype_combobox, 
                password_entry, False)
    empid_entry.insert(0, row[0])
    name_entry.insert(0, row[1])
    email_entry.insert(0, row[2])
    gender_combobox.set(row[3])
    dob_date_entry.set_date(row[4])
    contact_entry.insert(0, row[5])
    education_combobox.set(row[6])
    employement_type_combobox.set(row[7])
    workshift_combobox.set(row[8])
    address_text.insert(1.0, row[9])
    doj_date_entry.set_date(row[10])
    salary_entry.insert(0, row[11])
    usertype_combobox.set(row[12])
    password_entry.insert(0, row[13])
    
    
def add_employee(empid, name, email, gender,dob, contact,emp_type,education, work_shift, address, doj, salary, user_type, password):
    if (empid=='' or name=='' or email=='' or gender=='Select Gender' or contact=='' or emp_type=='Select Type' or education=='Select Education' or work_shift=='Select Shift' or address=='\n' or salary=='' or user_type=='Select User Type' or password==''):
        messagebox.showerror('Error', 'All fields are required.')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        cursor.execute('USE dbmsProj')
        try:
            cursor.execute('SELECT empid from emp_data WHERE empid=%s', (empid))
            if cursor.fetchone():
                messagebox.showerror('Error','Id already exists')
                return
            address=address.strip()
            cursor.execute('INSERT INTO emp_data VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (empid, name, email, gender,dob, contact,emp_type,education, work_shift, address, doj, salary, user_type, password))
            connection.commit()
            treeview_data()
            messagebox.showinfo('Success','Data is inserted successfully!')
        except Exception as e:
            messagebox.showerror('Error',f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()

def clear_fields(empid_entry, name_entry, email_entry, 
                gender_combobox, dob_date_entry, contact_entry,
                education_combobox, employement_type_combobox, 
                workshift_combobox, address_text, 
                doj_date_entry, salary_entry, usertype_combobox, 
                password_entry, check):
    empid_entry.delete(0,END)
    name_entry.delete(0,END)
    email_entry.delete(0,END)
    gender_combobox.set('Select Gender')
    from datetime import date
    dob_date_entry.set_date(date.today())
    contact_entry.delete(0,END)
    education_combobox.set('Select Education')
    employement_type_combobox.set('Select Type')
    workshift_combobox.set('Select Work Shift')
    address_text.delete(1.0,END)
    doj_date_entry.set_date(date.today())
    salary_entry.delete(0,END)
    usertype_combobox.set('Select User Type')
    password_entry.delete(0,END)
    if check:
        employee_treeview.selection_remove(employee_treeview.selection())

def update_emp(empid, name, email, gender, dob, contact, emp_type, education, work_shift, address, doj, salary, user_type, password):
    selected = employee_treeview.selection()
    if not selected:
        messagebox.showerror('Error', 'No row is selected')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('USE dbmsProj')
            cursor.execute('SELECT * FROM emp_data WHERE empid=%s',(empid,))
            current_data= cursor.fetchone()
            current_data=current_data[1:]
            
            address=address.strip()
            new_data=(name, email, gender, dob, contact, emp_type, education, work_shift, address, doj, salary, user_type, password)

            if current_data==new_data:
                messagebox.showinfo('Information', 'No changes detected.')
                return

            cursor.execute('''UPDATE emp_data SET name=%s, email=%s, gender=%s, dob=%s, contact=%s, emp_type=%s, 
                            education=%s, work_shift=%s, address=%s, doj=%s, salary=%s, user_type=%s, password=%s 
                            WHERE empid=%s''', 
                        (name, email, gender, dob, contact, emp_type, education, work_shift, address, doj, salary, user_type, password, empid))
            connection.commit()
            messagebox.showinfo('Success', 'Data is updated successfully!')
        except Exception as e:
            messagebox.showerror('Error',f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()

def delete_emp(empid,):
    selected = employee_treeview.selection()
    if not selected:
        messagebox.showerror('Error', 'No row is selected')
    else:
        result=messagebox.askyesno('Confirm','Do you really want to delete the record?')
        if result:
            cursor, connection = connect_database()
            if not cursor or not connection:
                return
            try:
                cursor.execute('USE dbmsProj')
                cursor.execute('DELETE FROM emp_data WHERE empid=%s',(empid,))
                connection.commit()
                treeview_data()
                messagebox.showinfo('Success','Record is deleted.')
            except Exception as e:
                messagebox.showerror('Error',f'Error due to {e}')
            finally:
                cursor.close()
                connection.close()

def search_emp(search_option, value):
    if search_option=='Search By':
        messagebox.showerror('Error','No option is selected.')
    elif value=='':
        messagebox.showerror('Error','Enter the value to search.')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('USE dbmsProj')
            cursor.execute(f'SELECT * FROM emp_data WHERE {search_option} LIKE %s',f'%{value}%' )
            records = cursor.fetchall()
            employee_treeview.delete(*employee_treeview.get_children())
            for record in records:
                employee_treeview.insert('', END, value=record)
        except Exception as e:
            messagebox.showerror('Error',f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()

def show_all(search_entry, search_combobox):
    treeview_data()
    search_entry.delete(0,END)
    search_combobox.set('Search By')

def employee_form(window):
    global back_image, employee_treeview
    employee_frame=Frame(window, width=1070, height=567, bg='white')
    employee_frame.place(x=200, y=110)
    heading_label=Label(employee_frame, text='Manage Employee Details', font=('times new roman', 16, 'bold'), bg='#0f4d7d',fg='white')
    heading_label.place(x=0,y=0, relwidth=1)

    top_frame=Frame(employee_frame, bg='white')
    top_frame.place(x=0,y=40,relwidth=1,height=235)
    back_image=PhotoImage(file='back.png')
    back_button=Button(top_frame, image=back_image, bd=0, cursor='hand2',bg='white', command=lambda: employee_frame.place_forget())
    back_button.place(x=10, y=0)
    search_frame=Frame(top_frame, bg='white')
    search_frame.pack()
    search_combobox=ttk.Combobox(search_frame,values=('EmpId', 'Name', 'Email'), font=('times new roman',12),state='readonly',justify='center')
    search_combobox.set('Search By')
    search_combobox.grid(row=0, column=0,padx=20)
    search_entry=Entry(search_frame, font=('times new roman',12), bg='lightyellow')
    search_entry.grid(row=0, column=1)
    search_button=Button(search_frame, text='Search',font=('times new roman',12),width=10, cursor='hand2',fg='white', bg='#0f4d7d', command=lambda : search_emp(search_combobox.get(), search_entry.get()))
    search_button.grid(row=0, column=2, padx=20)
    show_button=Button(search_frame, text='Show All',font=('times new roman',12),width=10, cursor='hand2', fg='white', bg='#0f4d7d', command=lambda : show_all(search_entry, search_combobox))
    show_button.grid(row=0, column=3)

    horizontal_scrollbar=Scrollbar(top_frame, orient=HORIZONTAL)
    vertical_scrollbar=Scrollbar(top_frame,orient=VERTICAL)

    employee_treeview=ttk.Treeview(top_frame, columns=('empid', 'name','email', 'gender', 'dob','contact','employement_type',
        'education','work_shift','address', 'doj','salary','usertype'), show='headings',
        yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
    horizontal_scrollbar.pack(side=BOTTOM, fill=X)
    vertical_scrollbar.pack(side=RIGHT, fill=Y, pady=(10,0))
    horizontal_scrollbar.config(command=employee_treeview.xview)
    vertical_scrollbar.config(command=employee_treeview.yview)
    employee_treeview.pack(pady=(10,0))

    employee_treeview.heading('empid', text='EmpID')
    employee_treeview.heading('name', text='Name')
    employee_treeview.heading('email', text='Email')
    employee_treeview.heading('gender', text='Gender')
    employee_treeview.heading('dob', text='Date Of Birth')
    employee_treeview.heading('contact', text='Contact')
    employee_treeview.heading('employement_type', text='Employement Type')
    employee_treeview.heading('education', text='Education')
    employee_treeview.heading('work_shift', text='Work Shift')
    employee_treeview.heading('address', text='Address')
    employee_treeview.heading('doj', text='Date Of Joining')
    employee_treeview.heading('salary', text='Salary')
    employee_treeview.heading('usertype', text='User Type')

    employee_treeview.column('empid', width=60)
    employee_treeview.column('name', width=140)
    employee_treeview.column('email', width=180)
    employee_treeview.column('gender', width=80)
    employee_treeview.column('contact', width=100)
    employee_treeview.column('dob', width=100)
    employee_treeview.column('employement_type', width=120)
    employee_treeview.column('education', width=120)
    employee_treeview.column('work_shift', width=100)
    employee_treeview.column('address', width=200)
    employee_treeview.column('doj', width=100)
    employee_treeview.column('salary', width=140)
    employee_treeview.column('usertype', width=120)

    treeview_data()

    detail_frame=Frame(employee_frame, bg='white')
    detail_frame.place(x=20, y=280)

    empid_label=Label(detail_frame, text='EmpID',font=('times new roman', 12))
    empid_label.grid(row=0, column=0,padx=20, pady=10, sticky='w')
    empid_entry=Entry(detail_frame,font=('times new roman', 12), bg='lightyellow')
    empid_entry.grid(row=0, column=1,padx=20, pady=10)

    name_label=Label(detail_frame, text='Name',font=('times new roman', 12))
    name_label.grid(row=0, column=2,padx=20, pady=10, sticky='w')
    name_entry=Entry(detail_frame,font=('times new roman', 12), bg='lightyellow')
    name_entry.grid(row=0, column=3,padx=20, pady=10)

    email_label=Label(detail_frame, text='Email',font=('times new roman', 12))
    email_label.grid(row=0, column=4,padx=20, pady=10, sticky='w')
    email_entry=Entry(detail_frame,font=('times new roman', 12), bg='lightyellow')
    email_entry.grid(row=0, column=5,padx=20, pady=10)

    gender_label=Label(detail_frame, text='Gender',font=('times new roman', 12))
    gender_label.grid(row=1, column=0,padx=20, pady=10, sticky='w')
    gender_combobox=ttk.Combobox(detail_frame, values=('Male','Female'),font=('times new roman', 12), width=18, state='readonly')
    gender_combobox.set('Select Gender')
    gender_combobox.grid(row=1, column=1)

    dob_label=Label(detail_frame, text='Date of Birth',font=('times new roman', 12))
    dob_label.grid(row=1, column=2,padx=20, pady=10, sticky='w')
    dob_date_entry=DateEntry(detail_frame,width=18, font=('times new roman', 12),state='readonly', date_pattern='dd/mm/yyyy')
    dob_date_entry.grid(row=1, column=3)

    contact_label=Label(detail_frame, text='Contact',font=('times new roman', 12))
    contact_label.grid(row=1, column=4,padx=20, pady=10, sticky='w')
    contact_entry=Entry(detail_frame,font=('times new roman', 12), bg='lightyellow')
    contact_entry.grid(row=1, column=5,padx=20, pady=10)

    employement_type_label=Label(detail_frame, text='Employement Type',font=('times new roman', 12))
    employement_type_label.grid(row=2, column=0,padx=20, pady=10, sticky='w')
    employement_type_combobox=ttk.Combobox(detail_frame, values=('Full time', 'Part time','Casual', 'Contract','Intern'),font=('times new roman', 12), width=18, state='readonly')
    employement_type_combobox.set('Select Type')
    employement_type_combobox.grid(row=2, column=1)

    education_label=Label(detail_frame, text='Education',font=('times new roman', 12))
    education_label.grid(row=2, column=2,padx=20, pady=10, sticky='w')
    education_options = ["B.Tech","B.Com","M.Tech","M.Com","B.Sc","M.Sc","MBA","LLB","B.Arch","M.Arch"]
    education_combobox=ttk.Combobox(detail_frame, values=education_options,font=('times new roman', 12), width=18, state='readonly')
    education_combobox.set('Select Education')
    education_combobox.grid(row=2, column=3)

    workshift_label=Label(detail_frame, text='Work Shift',font=('times new roman', 12))
    workshift_label.grid(row=2, column=4,padx=20, pady=10, sticky='w')
    workshift_combobox=ttk.Combobox(detail_frame, values=('Morning', 'Evening','Night'),font=('times new roman', 12), width=18, state='readonly')
    workshift_combobox.set('Select Work Shift')
    workshift_combobox.grid(row=2, column=5)

    address_label=Label(detail_frame, text='Address',font=('times new roman', 12))
    address_label.grid(row=3, column=0,padx=20, pady=10, sticky='w')
    address_text=Text(detail_frame, width=20, height=3,font=('times new roman', 12), bg='lightyellow')
    address_text.grid(row=3, column=1, rowspan=2)

    doj_label=Label(detail_frame, text='Date of Joining',font=('times new roman', 12))
    doj_label.grid(row=3, column=2,padx=20, pady=10, sticky='w')
    doj_date_entry=DateEntry(detail_frame,width=18, font=('times new roman', 12),state='readonly', date_pattern='dd/mm/yyyy')
    doj_date_entry.grid(row=3, column=3)

    usertype_label=Label(detail_frame, text='User Type',font=('times new roman', 12))
    usertype_label.grid(row=4, column=2,padx=20, pady=10, sticky='w')
    usertype_combobox=ttk.Combobox(detail_frame, values=('Admin', 'Employee'),font=('times new roman', 12), width=18, state='readonly')
    usertype_combobox.set('Select User Type')
    usertype_combobox.grid(row=4, column=3)

    salary_label=Label(detail_frame, text='Salary',font=('times new roman', 12))
    salary_label.grid(row=3, column=4,padx=20, pady=10, sticky='w')
    salary_entry=Entry(detail_frame,font=('times new roman', 12), bg='lightyellow')
    salary_entry.grid(row=3, column=5,padx=20, pady=10)

    password_label=Label(detail_frame, text='Password',font=('times new roman', 12))
    password_label.grid(row=4, column=4,padx=20, pady=10, sticky='w')
    password_entry=Entry(detail_frame,font=('times new roman', 12), bg='lightyellow')
    password_entry.grid(row=4, column=5,padx=20, pady=10)

    button_frame=Frame(employee_frame, bg='white')
    button_frame.place(x=220, y=520)

    add_button = Button(button_frame, text='Add', font=('times new roman', 12), width=10, cursor='hand2', fg='white', bg='#0f4d7d',
                        command=lambda: add_employee(empid_entry.get(), name_entry.get(), email_entry.get(), 
                                                     gender_combobox.get(), dob_date_entry.get(), contact_entry.get(),
                                                     education_combobox.get(), employement_type_combobox.get(), 
                                                     workshift_combobox.get(), address_text.get(1.0, END), 
                                                     doj_date_entry.get(), salary_entry.get(), usertype_combobox.get(), 
                                                     password_entry.get()))
    add_button.grid(row=0, column=0, padx=20)

    update_button=Button(button_frame, text='Update',font=('times new roman',12),width=10, cursor='hand2',fg='white', bg='#0f4d7d', 
                         command= lambda: update_emp(empid_entry.get(), name_entry.get(), email_entry.get(), 
                                                     gender_combobox.get(), dob_date_entry.get(), contact_entry.get(),
                                                     education_combobox.get(), employement_type_combobox.get(), 
                                                     workshift_combobox.get(), address_text.get(1.0, END), 
                                                     doj_date_entry.get(), salary_entry.get(), usertype_combobox.get(), 
                                                     password_entry.get()))
    update_button.grid(row=0, column=1, padx=20)

    delete_button=Button(button_frame, text='Delete',font=('times new roman',12),width=10, cursor='hand2',fg='white', 
                         bg='#0f4d7d', command=lambda: delete_emp(empid_entry.get(),))
    delete_button.grid(row=0, column=2, padx=20)

    clear_button=Button(button_frame, text='Clear',font=('times new roman',12),width=10, cursor='hand2',
                        fg='white', bg='#0f4d7d', command=lambda :clear_fields(empid_entry, name_entry, email_entry, 
                                                     gender_combobox, dob_date_entry, contact_entry,
                                                     education_combobox, employement_type_combobox, 
                                                     workshift_combobox, address_text, 
                                                     doj_date_entry, salary_entry, usertype_combobox, 
                                                     password_entry, True))
    clear_button.grid(row=0, column=3, padx=20)
    employee_treeview.bind('<ButtonRelease-1>',lambda event: select_data(event, empid_entry, name_entry, email_entry, 
                                                     gender_combobox, dob_date_entry, contact_entry,
                                                     education_combobox, employement_type_combobox, 
                                                     workshift_combobox, address_text, 
                                                     doj_date_entry, salary_entry, usertype_combobox, 
                                                     password_entry))
    create_db_table()
    return employee_frame
