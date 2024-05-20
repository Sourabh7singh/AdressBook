from tkinter import *
import sqlite3
import messagebox
main_window = Tk()
main_window.title("Address Book")
main_window.iconbitmap("Saurabh.ico")
main_window.geometry("750x380+100+200")
main_window.resizable(False,False)
main_window.configure(background='black')

def check():
    flag = 0
    global f_name,l_name,phone_num,address,state,city,zcode
    if f_name.get() !="" and f_name.get()!=" ":
        flag+=1
    if l_name.get() !="" and l_name.get()!=" ":
        flag+=1
    if phone_num.get() !="" and phone_num.get()!=" ":
        flag+=1
    if address.get() !="" and address.get()!=" ":
        flag+=1
    if state.get() !="" and state.get()!=" ":
        flag+=1
    if city.get() !="" and city.get()!=" ":
        flag+=1
    if zcode.get() !="" and zcode.get()!=" ":
        flag+=1

    if flag==7: 
        try: 
            int(phone_num.get())
            int(zcode.get())
            Add()
        except:
            messagebox.showerror("Error","Please enter valid phone number or zipcode")
    else:
        messagebox.showerror("Error","Please enter complete Details.")

def Add():
    #create a database or connect
    conn = sqlite3.connect('address_book.db')
    #create a cursor
    c = conn.cursor()
    c.execute("INSERT INTO addresses VALUES (:f_name, :l_name, :phone_num, :address, :state, :city, :zcode)",
              {
                  "f_name": f_name.get(),
                  "l_name": l_name.get(),
                  "phone_num":phone_num.get(),
                  "address": address.get(),
                  "state": state.get(),
                  "city": city.get(),
                  "zcode": zcode.get()
              })   
    #commit changes
    conn.commit()
    #close the connection
    conn.close()
    f_name.delete(0,END)
    l_name.delete(0,END)
    phone_num.delete(0,END)
    address.delete(0,END)
    state.delete(0,END)
    city.delete(0,END)
    zcode.delete(0,END)

def Querry():
    #for clearing the widgets in the frame
    for widget in frame_name.winfo_children():
        widget.destroy()
    #create a database or connect
    conn = sqlite3.connect('address_book.db')
    #create a cursor
    c = conn.cursor()
    #query the database
    c.execute("SELECT *,oid FROM addresses")
    records = c.fetchall()
    print_record=''
    if records == [ ]:
        error = Label(frame_name,text="Records Empty",font=('Times New Roman',17,'bold'),bg="#FFE5B4")
        error.grid(row=0,column=0,rowspan=2)
        return
    else:
        naming = Label(frame_name,text="OID \t\t\tName",font=('Times New Roman',17,'bold'),bg="#FFE5B4")
        naming.grid(row=0,column=0,padx=0,pady=0)
        for record in records:
            print_record+=(str(record[7])+"\t\t"+str(record[0])+" "+str(record[1])+"\n")
            show = Label(frame_name,text=print_record,width=30,bd=5,font=('Times New Roman',17,'bold'),bg="#FFE5B4",fg="Maroon")
            show.grid(row=1,column=0)
    #commit changes
    conn.commit()
    #close the connection
    conn.close()

def oid_check():
    conn = sqlite3.connect('address_book.db')
    #create a cursor
    c = conn.cursor()
    #query the database
    c.execute("SELECT oid FROM addresses")
    records = c.fetchall()
    flag=0
    if del_box.get()=="" or del_box.get()==" ":
        messagebox.showerror("Error","Please Enter a vaid OID")
    else:
        for record in records:
            if int(del_box.get()) in record:
                flag=1
        if flag==1:
            edit()
        else: 
            messagebox.showerror("Error","Please Enter a vaid OID")
    #commit changes
    conn.commit()
    #close the connection
    conn.close()

def Updation():
    global updation_window,frame_name,del_box,frame_update,empty_frame
    updation_window=Tk()
    updation_window.configure(background='black')
    updation_window.iconbitmap("Saurabh.ico")
    updation_window.title("Updating Record")
    updation_window.geometry("630x500")
    updation_window.resizable(False,False)

    frame_update = LabelFrame(updation_window,padx=5,pady=5,width=300,height=300,bg="#FFE5B4")
    frame_name = LabelFrame(updation_window,padx=5,pady=5,width=620,height=300,bg="#FFE5B4")
    frame_name.grid(row=1,column=0,padx=5,pady=5)

    Select_id = Label(frame_update,text="Enter OID",font=('Times New Roman',17,'bold'),bg="#FFE5B4",fg="maroon")
    del_box = Entry(frame_update,bd=5,width=30,font=('Times New Roman',17,'bold'))
    show_record = Button(frame_update,text="Show Records",command=Querry,font=('Times New Roman',17,'bold'),bg="#FFE5B4",bd=5,fg="maroon")
    update_record = Button(frame_update,text="Update Record",command=oid_check,font=('Times New Roman',17,'bold'),bg="#FFE5B4",bd=5,fg="maroon")
    remove_record = Button(frame_update,text="Remove Record",command=Remove,font=('Times New Roman',17,'bold'),bg="#FFE5B4",bd=5,fg="maroon")
    
    Select_id.grid(row=1,column=0,padx=5,pady=5)
    del_box.grid(row=1,column=1,padx=5,pady=5)
    show_record.grid(row=0,columnspan=2,ipadx=180,pady=5,padx=5)
    update_record.grid(row=2,column=0,ipadx=10,padx=10,pady=5)
    remove_record.grid(row=2,column=1,padx=5,pady=5)
    
    frame_update.grid(row=0,column=0,padx=5,pady=5)
    
    updation_window.mainloop()
    
def Remove():
    #create a database or connect
    conn = sqlite3.connect('address_book.db')
    #create a cursor
    c = conn.cursor()
    #query the database
    c.execute("SELECT * from addresses")
    if del_box.get()=="":
        Label(empty_frame,text="Please Enter an OID",font=('Times New Roman',17,'bold')).grid(row=3,columnspan=2,padx=5)
    else:
        c.execute("DELETE from addresses WHERE oid="+del_box.get())
    #commit changes
    conn.commit()
    #close the connection
    conn.close()

def update():
    #create a database or connect
    conn = sqlite3.connect('address_book.db')
    #create a cursor
    c = conn.cursor()
    #query the database
    record_id = del_box.get()
    c.execute("""UPDATE addresses SET
        first_name = :first,
        last_name = :last,
        address = :address,
        phone_num = :phone_num,
        city = :city,
        state = :state,
        zipcode = :zipcode

        WHERE oid = :oid""",
        {
            'first' : f_name_editor.get(),
            'last' : l_name_editor.get(),
            'phone_num' : phone_num_editor.get(),
            'address' : address_editor.get(),
            'city' : city_editor.get(),
            'state' : state_editor.get(),
            'zipcode' : zcode_editor.get(),
            'oid' : record_id,
        } 
    
    )
    
    
    #commit changes
    conn.commit()
    #close the connection
    conn.close()
    #create entry boxes
    edit_window.destroy()

def create():
    #create a database or connect
    conn = sqlite3.connect('address_book.db')
    #create a cursor
    c = conn.cursor()
    #query the database
    #create a table
    c.execute("""CREATE TABLE addresses (
       first_name text,
        last_name text,
        phone_num integer,
        address text,
        city text,
        state text,
        zipcode integer
    )""")    
    #commit changes
    conn.commit()
    #close the connection
    conn.close()


def edit():
    global edit_window,Record_Box,l_name_editor,f_name_editor,address_editor,state_editor,city_editor,zcode_editor,phone_num_editor
    #create a database or connect
    conn = sqlite3.connect('address_book.db')
    #create a cursor
    c = conn.cursor()
    record_id = del_box.get()
    #query the database
    if del_box.get()=="":
        Label(updation_window,text="Please Enter an OID",font=('Times New Roman',17,'bold')).grid(row=3,columnspan=2,pady=(20,0),ipadx=100)
    else:
        edit_window = Tk()
        edit_window.title("Edit the record")
        edit_window.configure(background='black')
        edit_window.resizable(False,False)
        c.execute("SELECT * FROM addresses WHERE oid = "+record_id)
        records = c.fetchall()
        
        frame_entry = LabelFrame(edit_window,padx=5,pady=5,bg="#FFE5B4",bd=4)
        f_name_editor = Entry(frame_entry,width=30,font=('Times New Roman',17,'bold'),bd=5)
        l_name_editor = Entry(frame_entry,width=30,font=('Times New Roman',17,'bold'),bd=5)
        phone_num_editor = Entry(frame_entry,width=30,font=('Times New Roman',17,'bold'),bd=5)
        address_editor = Entry(frame_entry,width=30,font=('Times New Roman',17,'bold'),bd=5)
        state_editor = Entry(frame_entry,width=30,font=('Times New Roman',17,'bold'),bd=5)
        city_editor = Entry(frame_entry,width=30,font=('Times New Roman',17,'bold'),bd=5)
        zcode_editor = Entry(frame_entry,width=30,font=('Times New Roman',17,'bold'),bd=5)
        
        f_name_editor.grid(row=0,column=1,padx=5,pady=5)
        l_name_editor.grid(row=1,column=1,padx=5,pady=5)
        address_editor.grid(row=2,column=1,padx=5,pady=5)
        phone_num_editor.grid(row=3,column=1,padx=5,pady=5)
        state_editor.grid(row=4,column=1,padx=5,pady=5)
        city_editor.grid(row=5,column=1,padx=5,pady=5)
        zcode_editor.grid(row=6,column=1,padx=5,pady=5)

        #loop through results
        for record in records:
            f_name_editor.insert(0, record[0])
            l_name_editor.insert(0, record[1])
            phone_num_editor.insert(0, record[2])
            address_editor.insert(0, record[3])
            city_editor.insert(0, record[4])
            state_editor.insert(0, record[5])
            zcode_editor.insert(0, record[6])
        frame_entry.grid(row=0,column=1,padx=5,pady=5)

        frame_label = LabelFrame(edit_window,padx=5,pady=5,bg="#FFE5B4",bd=4,fg="blue")
        f_name_l = Label(frame_label,text="First Name",font=('Times New Roman',17,'bold'),fg="maroon",bg="#FFE5B4")
        l_name_l = Label(frame_label,text="Last Name",font=('Times New Roman',17,'bold'),fg="maroon",bg="#FFE5B4")
        phone_num_l = Label(frame_label,text="Phone Number",font=('Times New Roman',17,'bold'),fg="maroon",bg="#FFE5B4")
        address_l = Label(frame_label,text="Address",font=('Times New Roman',17,'bold'),fg="maroon",bg="#FFE5B4")
        state_l = Label(frame_label,text="State",font=('Times New Roman',17,'bold'),fg="maroon",bg="#FFE5B4")
        city_l = Label(frame_label,text="City",font=('Times New Roman',17,'bold'),fg="maroon",bg="#FFE5B4")
        zcode_l = Label(frame_label,text="Zip Code",font=('Times New Roman',17,'bold'),fg="maroon",bg="#FFE5B4")
        
        f_name_l.grid(row=0,column=0,padx=5,pady=8)
        l_name_l.grid(row=1,column=0,padx=5,pady=8)
        phone_num_l.grid(row=2,column=0,padx=5,pady=8)
        address_l.grid(row=3,column=0,padx=5,pady=8)
        state_l.grid(row=4,column=0,padx=5,pady=8)
        city_l.grid(row=5,column=0,padx=5,pady=8)
        zcode_l.grid(row=6,column=0,padx=5,pady=8)
        frame_label.grid(row=0,column=0,padx=5,pady=5)

        frame_btn = LabelFrame(edit_window,padx=5,pady=5,bg="#FFE5B4",bd=5)
        save_btn = Button(frame_btn,text="Save edited Record",command=update,font=('Times New Roman',17,'bold'),fg="maroon",bg="#FFE5B4")
        save_btn.grid(row=0,column=0,padx=80,columnspan=2)
        frame_btn.grid(row=1,column=0,columnspan=2,ipadx=106)

        edit_window.mainloop()

frame_entry = LabelFrame(main_window,padx=5,pady=5,bg="#FFE5B4",bd=4)

f_name = Entry(frame_entry,width=30,font=('Times New Roman',17,'bold'),bd=5)
l_name = Entry(frame_entry,width=30,font=('Times New Roman',17,'bold'),bd=5)
phone_num = Entry(frame_entry,width=30,font=('Times New Roman',17,'bold'),bd=5)
address = Entry(frame_entry,width=30,font=('Times New Roman',17,'bold'),bd=5)
state = Entry(frame_entry,width=30,font=('Times New Roman',17,'bold'),bd=5)
city = Entry(frame_entry,width=30,font=('Times New Roman',17,'bold'),bd=5)
zcode = Entry(frame_entry,width=30,font=('Times New Roman',17,'bold'),bd=5)

f_name.grid(row=0,column=1,padx=10,pady=2)
l_name.grid(row=1,column=1,padx=10,pady=2)
address.grid(row=2,column=1,padx=10,pady=2)
phone_num.grid(row=3,column=1,padx=10,pady=2)
state.grid(row=4,column=1,padx=10,pady=2)
city.grid(row=5,column=1,padx=10,pady=2)
zcode.grid(row=6,column=1,padx=10,pady=2)

frame_entry.grid(row=0,column=1,padx=5,pady=5)

frame_label = LabelFrame(main_window,padx=5,pady=5,bg="#FFE5B4",bd=4,fg="blue")

#create Labels
f_name_l = Label(frame_label,text="First Name",font=('Times New Roman',17,'bold'),bg="#FFE5B4",fg="maroon")
l_name_l = Label(frame_label,text="Last Name",font=('Times New Roman',17,'bold'),bg="#FFE5B4",fg="maroon")
address_l = Label(frame_label,text="Address",font=('Times New Roman',17,'bold'),bg="#FFE5B4",fg="maroon")
phone_num_l = Label(frame_label,text="Phone Number",font=('Times New Roman',17,'bold'),bg="#FFE5B4",fg="maroon")
state_l = Label(frame_label,text="State",font=('Times New Roman',17,'bold'),bg="#FFE5B4",fg="maroon")
city_l = Label(frame_label,text="City",font=('Times New Roman',17,'bold'),bg="#FFE5B4",fg="maroon")
zcode_l = Label(frame_label,text="Zip Code",font=('Times New Roman',17,'bold'),bg="#FFE5B4",fg="maroon")

f_name_l.grid(row=0,column=0,padx=50,pady=5)
l_name_l.grid(row=1,column=0,padx=50,pady=5)
address_l.grid(row=2,column=0,padx=50,pady=5)
phone_num_l.grid(row=3,column=0,padx=50,pady=5)
state_l.grid(row=4,column=0,padx=50,pady=5)
city_l.grid(row=5,column=0,padx=50,pady=5)
zcode_l.grid(row=6,column=0,padx=50,pady=5)
frame_label.grid(row=0,column=0,padx=5,pady=5,ipadx=20)
frame_btn = LabelFrame(main_window,padx=5,pady=5,bg="#FFE5B4",bd=5)

#create Buttons
submit = Button(frame_btn,text="Add record to Database",command=check,font=('Times New Roman',17,'bold'),bg="#FFE5B4",fg="maroon",bd=5)
querry = Button(frame_btn,text="Update/Edit/Show",command=Updation,font=('Times New Roman',17,'bold'),bg="#FFE5B4",fg="maroon",bd=5)
submit.grid(row=7,column=0,ipadx=26,padx=5)
querry.grid(row=7,column=1,ipadx=96,padx=10)
frame_btn.grid(row=1,column=0,columnspan=2)
main_window.mainloop()