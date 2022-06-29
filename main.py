from cProfile import label
import datetime
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as mb
from tkinter import ttk
from matplotlib.pyplot import text
from tkcalendar import DateEntry  # pip install tkcalendar
import sqlite3

headlabelfont = ("Noto Sans CJK TC", 15, 'bold')
labelfont = ('Garamond', 14)
entryfont = ('Garamond', 12)

connector = sqlite3.connect('diş_kontrol.db')
cursor = connector.cursor()

connector.execute(
"CREATE TABLE IF NOT EXISTS DİS_KONTROL (STUDENT_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, NAM0 EMAIL TEXT, PHONE_NO INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, GENDER TEXT, DOB TEXT, STREAM TEXT)"
)

def reset_fields():
    global isim_strvar, mail_strvar, kontakno_strvar, cinsiyet_strvar, dob, stream_strvar

    for i in ['isim_strvar', 'mail_strvar', 'kontakno_strvar', 'cinsiyet_strvar', 'stream_strvar']:
        exec(f"{i}.set('')")
    dob.set_date(datetime.datetime.now().date())

def reset_form():
    global tree
    tree.delete(*tree.get_children())

    reset_fields()

def display_records():
    tree.delete(*tree.get_children())

    curr = connector.execute('SELECT * FROM DİS_KONTROL')
    data = curr.fetchall()

    for records in data:
        tree.insert('', END, values=records)

def add_record():
    global isim_strvar, mail_strvar, kontakno_strvar, cinsiyet_strvar, dob, stream_strvar

    name = isim_strvar.get()
    email = mail_strvar.get()
    contact = kontakno_strvar.get()
    gender = cinsiyet_strvar.get()
    DOB = dob.get_date()
    stream = stream_strvar.get()

    if not name or not email or not contact or not gender or not DOB or not stream:
        mb.showerror('HATA!', "Lütfen tüm eksik alanları doldurun!!")
    else:
        try:
            connector.execute(
            'INSERT INTO DİS_KONTROL (NAME, EMAIL, PHONE_NO, GENDER, DOB, STREAM) VALUES (?,?,?,?,?,?)', (name, email, contact, gender, DOB, stream)
            )
            connector.commit()
            mb.showinfo('Kayıt eklendi', f"! {name} ! İsimli kayıt başarıyla eklendi!")
            reset_fields()
            display_records()
        except:
            mb.showerror('Yanlış biçim', 'Girilen değerlerin türü doğru değil. Lütfen iletişim alanının yalnızca numara içerebileceğini unutmayın.')

def remove_record():
    if not tree.selection():
        mb.showerror('HATA!', 'Lütfen veritabanından bir öğe seçin!!!')
    else:
        current_item = tree.focus()
        values = tree.item(current_item)
        selection = values["values"]

        tree.delete(current_item)

        connector.execute('DELETE FROM DİS_KONTROL WHERE STUDENT_ID=%d' % selection[0])
        connector.commit()

        mb.showinfo('BAŞARILI!!', 'KAYIT BAŞARIYLA SİLİNDİ!!')

        display_records()

def view_record():
    global isim_strvar, mail_strvar, kontakno_strvar, cinsiyet_strvar, dob, stream_strvar

    current_item = tree.focus()
    values = tree.item(current_item)
    selection = values["values"]

    date = datetime.date(int(selection[5][:4]), int(selection[5][5:7]), int(selection[5][8:]))

    isim_strvar.set(selection[1]); mail_strvar.set(selection[2])
    kontakno_strvar.set(selection[3]); cinsiyet_strvar.set(selection[4])
    dob.set_date(date); stream_strvar.set(selection[6])




main = Tk()
main.title('Jolanka DİŞ KONTROL SİSTEMİ')
main.geometry('1000x600')
main.resizable(0, 0)

Label(main, text="DİŞ RANDEVU SİSTEMİ", font=headlabelfont, bg='#D1DBBD').pack(side=TOP, fill=X)



lf_bg = '#3E606F' 
cf_bg = '#91AA9D'


isim_strvar = StringVar()
mail_strvar = StringVar()
kontakno_strvar = StringVar()
cinsiyet_strvar = StringVar()
stream_strvar = StringVar()

left_frame = Frame(main, bg=lf_bg)
left_frame.place(x=0, y=30, relheight=1, relwidth=0.2)

center_frame = Frame(main, bg=cf_bg)
center_frame.place(relx=0.2, y=30, relheight=1, relwidth=0.2)

right_frame = Frame(main, bg="Gray35")
right_frame.place(relx=0.4, y=30, relheight=1, relwidth=0.6)

Label(left_frame, text="İsim", font=labelfont, bg=lf_bg).place(relx=0.375, rely=0.05)
Label(left_frame, text="Kontak numarası", font=labelfont, bg=lf_bg).place(relx=0.175, rely=0.18)
Label(left_frame, text="Email Adresi", font=labelfont, bg=lf_bg).place(relx=0.2, rely=0.31)
Label(left_frame, text="Cinsiyet", font=labelfont, bg=lf_bg).place(relx=0.3, rely=0.44)
Label(left_frame, text="Doğum Tarihi", font=labelfont, bg=lf_bg).place(relx=0.1, rely=0.57)
Label(left_frame, text="Veri Aktarımı", font=labelfont, bg=lf_bg).place(relx=0.3, rely=0.7)

Entry(left_frame, width=19, textvariable=isim_strvar, font=entryfont).place(x=20, rely=0.1)
Entry(left_frame, width=19, textvariable=kontakno_strvar, font=entryfont).place(x=20, rely=0.23)
Entry(left_frame, width=19, textvariable=mail_strvar, font=entryfont).place(x=20, rely=0.36)
Entry(left_frame, width=19, textvariable=stream_strvar, font=entryfont).place(x=20, rely=0.75)

OptionMenu(left_frame, cinsiyet_strvar, 'Male', "Female").place(x=45, rely=0.49, relwidth=0.5)

dob = DateEntry(left_frame, font=("Arial", 12), width=15)
dob.place(x=20, rely=0.62)

Button(left_frame, text='Gönder ve Kayıt Ekle', font=labelfont, command=add_record, width=18).place(relx=0.025, rely=0.85)
Button(center_frame, text='Kaydı Sil', font=labelfont, command=remove_record, width=15).place(relx=0.1, rely=0.25)
Button(center_frame, text='Kayıtlara Bak', font=labelfont, command=view_record, width=15).place(relx=0.1, rely=0.35)
Button(center_frame, text='Bilgileri Sıfırla', font=labelfont, command=reset_fields, width=15).place(relx=0.1, rely=0.45)
Button(center_frame, text='Databaseyi Sil', font=labelfont, command=reset_form, width=15).place(relx=0.1, rely=0.55)

Label(right_frame, text='Diş kaytıları', font=headlabelfont, bg='#6C8190', fg='LightCyan').pack(side=TOP, fill=X)

tree = ttk.Treeview(right_frame,show='headings', height=100, selectmode=BROWSE,
                    columns=('Hasta İD', "İsim","Mail Adres", "Kontak Numarası", "Cinsiyet", "Doğum Tarihi", "Aktarım"))

X_scroller = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
Y_scroller = Scrollbar(tree, orient=VERTICAL, command=tree.yview)

X_scroller.pack(side=BOTTOM, fill=X)
Y_scroller.pack(side=RIGHT, fill=Y)

tree.config(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)

tree.heading('Hasta İD', text='ID', anchor=CENTER)
tree.heading('İsim', text='İsim', anchor=CENTER)
tree.heading('Mail Adres', text='Mail ID', anchor=CENTER)
tree.heading('Kontak Numarası', text='Telefon No', anchor=CENTER)
tree.heading('Cinsiyet', text='Cinsiyet', anchor=CENTER)
tree.heading('Doğum Tarihi', text='Doğum Tarihi', anchor=CENTER)
tree.heading('Aktarım', text='Aktarım', anchor=CENTER)

tree.column('#0', width=0, stretch=NO)
tree.column('#1', width=40, stretch=NO)
tree.column('#2', width=130, stretch=NO)
tree.column('#3', width=210, stretch=NO)
tree.column('#4', width=80, stretch=NO)
tree.column('#5', width=80, stretch=NO)
tree.column('#6', width=80, stretch=NO)
tree.column('#7', width=150, stretch=NO)

tree.place(y=30, relwidth=1, relheight=0.9, relx=0)

display_records()

main.update()
main.mainloop()