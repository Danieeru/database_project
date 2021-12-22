from sqlalchemy import create_engine
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import tkinter as tk
from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
from tkinter.ttk import Combobox
from PIL import Image, ImageTk

# Устанавливаем соединение с postgres
#connection = psycopg2.connect(user="postgres", password="1909")
#connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
# Создаем курсор для выполнения операций с базой данных
#cursor = connection.cursor()
##engine = create_engine('postgresql://{}:{}@localhost/demo'.format(auth['postgres'], auth['1909']), echo=True)
##engine = create_engine('postgresql://postgres:1909@localhost/Market')
#engine = create_engine('postgresql://Arseny:bd@localhost/Market')
#cursor = engine.connect()


## отправляет запрос на бд и выполняет его
## это функция кнопки


bdhost='localhost'
bduser='Arseny'
bdpassword='bd'
bd='Market'

def change():
    s = txtexample.get(1.0, END)
    print(s)
    runfunc(s)
    print("button pressed")


## функция которая отправляет запрос к БД
def runfunc(str):
    connection = psycopg2.connect(host=bdhost, user=bduser, password=bdpassword, database=bd)
    cursor = connection.cursor()
    try:
        cursor.execute(str)
        cursor.close()
        connection.close()
    except Exception as ex:
        mb.showerror('Ошибка запроса', 'Ошибка в запросе к БД!\n Попробуйте изменить запрос.')
        print(ex)
        cursor.close()
        connection.close()



def createPurchaseFunc():
    connection = psycopg2.connect(host=bdhost, user=bduser, password=bdpassword, database=bd)
    cursor = connection.cursor()
    empName = empNameEntry.get()
    custName = custNameEntry.get()
    print (empName, custName)
    sq = "select purchase_insert('" + empName.rstrip() + "', '" + custName.rstrip() + "')"
    print(sq)
    cursor.execute(sq)
    connection.commit()
    cursor.close()
    connection.close()
    return



def addButtonFunc():
    connection = psycopg2.connect(host=bdhost, user=bduser, password=bdpassword, database=bd)
    cursor = connection.cursor()

    # insert into purchase(market_id, employee_id, customer_id, amount, purchase_date)
    # values
    # (2, 6, 7, 0, '21.12.2021 14:56:10')
    # создание покупки



    purchace_id = 0
    #name = combo_product.get()
    name = text_product.get()
    am = amount.get()

    CheckText['state'] = NORMAL
    #CheckText.insert("end", " ")
    #CheckText.insert("end", str(combo_product.get()))
    CheckText.insert("end", name.rstrip())
    CheckText.insert("end", " ")
    CheckText.insert("end", (str(amount.get())))
    CheckText.insert("end", "\n")
    CheckText['state'] = tk.DISABLED
    sq = "select rec_pos_insert(" + str(purchace_id) + ", '" + name + "', " + str(am) + ")"
    connection.commit()
    print(sq)
       # combo_product['values'] += ("ыыыы",)

    cursor.close()
    connection.close()


def addEmployeeFunc():
    connection = psycopg2.connect(host=bdhost, user=bduser, password=bdpassword, database=bd)
    cursor = connection.cursor()

    name = textname.get(1.0, END)
    pos = positionname.get(1.0, END)
    shopname = combo_shop.get()
    spacepos = 0  # индекс последнего пробела в полученном тексте
    for i in range(len(shopname)):
        if shopname[i] == " ":
            spacepos = i
    streetname = shopname[:spacepos]
    num = shopname[spacepos + 1::]
    cursor.execute("INSERT INTO employee (market_id, name, position) VALUES ( ( SELECT id FROM market WHERE street=%s AND house=%s ),%s, %s )", (str(streetname).rstrip(), num, str(name).rstrip(), str(pos).rstrip()))
    print('сотрудник добавлен - ' + name)
    connection.commit()
    cursor.close()
    connection.close()
    return


def showemployee():
    connection = psycopg2.connect(host=bdhost, user=bduser, password=bdpassword, database=bd)
    cursor = connection.cursor()
    sq = "select * from employee"
    cursor.execute("select * from employee")

    [tableemp.delete(i) for i in tableemp.get_children()]
    [tableemp.insert('', 'end', values=row) for row in cursor.fetchall()]

    cursor.close()
    connection.close()
    return


def delEmployeeBuuton():
    connection = psycopg2.connect(host=bdhost, user=bduser, password=bdpassword, database=bd)
    cursor = connection.cursor()
    name = textname.get(1.0, END)
    name.rstrip()
    # очень важно писать %%
    s = "delete from employee where name like '" + str(name).rstrip() + "'"
    print(s)
    cursor.execute(s)
    connection.commit()
    cursor.close()
    connection.close()


def delbymarketid():
    connection = psycopg2.connect(host=bdhost, user=bduser, password=bdpassword, database=bd)
    cursor = connection.cursor()
    marketname = combo_shop.get()
    namelist = marketname.split(' ')
    name = namelist[:-1:]
    nam1=""
    for i in range(len(name)):
        nam1 += name[i]
        nam1.rstrip()
        if i != len(name) - 1: nam1 += " "

    house = namelist[-1]
    cursor.execute("delete from employee where market_id in (select id from market where street=%s AND house=%s)", (nam1, house))
    connection.commit()
    cursor.close()
    connection.close()
    return


def addProductButton():
    connection = psycopg2.connect(host=bdhost, user=bduser, password=bdpassword, database=bd)
    cursor = connection.cursor()

    productname = prodname.get(1.0, END)
    typename = typecombo.get()
    manufacturer = manufCombo.get()
    price = costText.get(1.0, END)
    discount = discountText.get(1.0, END)
    print ('name', productname)
    print('type', typename)
    print('manuf', manufacturer)
    print('price', price)
    print('dics', discount)
    sq = "select product_insert('" + str(productname).rstrip() + "', " + str(price).rstrip() + ", '" + str(typename).rstrip() + "', '" + str(manufacturer).rstrip() + "')"
    print(sq)
    cursor.execute(sq)
    connection.commit()
    #combo_product['values'] += (productname,)
    cursor.close()
    connection.close()


def delProductButton():
    connection = psycopg2.connect(host=bdhost, user=bduser, password=bdpassword, database=bd)
    cursor = connection.cursor()
    name = prodname.get(1.0, END)
    sq = "delete from product where name like '" + name.rstrip() + "'"
    print(sq)
    #print(combo_product['values'])
    #for i in range(len(combo_product['values'])):
     #   if (combo_product['values'][i] == name.rstrip()):
       #     combo_product['values'] -= combo_product['values'][i]
        #print(combo_product['values'][i])
       # if combo_product[i] == name.rstrip():
    cursor.execute(sq)
    connection.commit()
    
    cursor.close()
    connection.close()



def showProductButton():
    connection = psycopg2.connect(host=bdhost, user=bduser, password=bdpassword, database=bd)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM product")
    [prodTable.delete(i) for i in prodTable.get_children()]
    [prodTable.insert('', 'end', values=row) for row in cursor.fetchall()]
    cursor.close()
    connection.close()

    return


def addCustomerButton():
    connection = psycopg2.connect(host=bdhost, user=bduser, password=bdpassword, database=bd)
    cursor = connection.cursor()

    name = customerText.get(1.0, END)
    number = phoneNumberText.get(1.0, END)
    sq = "insert into customer (name, phone_number) Values ('" + name.rstrip()\
         + "', " + str(number).rstrip() + ")"
    print(sq)
    cursor.execute("insert into customer (name, phone_number) values ( %s, %s)", (name.rstrip(), str(number).rstrip()))
    connection.commit()
    cursor.close()
    connection.close()
    return

def delCustomerButton():
    connection = psycopg2.connect(host=bdhost, user=bduser, password=bdpassword, database=bd)
    cursor = connection.cursor()

    name = customerText.get(1.0, END)
    sq = "delete from customer where name like '" + name.rstrip() + "'"
    print(sq)
    cursor.execute(sq)
    connection.commit()

    cursor.close()
    connection.close()
    return

def showCutomerButton():
    connection = psycopg2.connect(host=bdhost, user=bduser, password=bdpassword, database=bd)
    cursor = connection.cursor()

    sq = "select * from customer"
    cursor.execute(sq)
    [tableCustomer.delete(i) for i in tableCustomer.get_children()]

    [tableCustomer.insert('', 'end', values=row) for row in cursor.fetchall()]
    cursor.close()
    connection.close()
    return


window = Tk()
window.title("database experience")
window.geometry("800x600")

appTabs = ttk.Notebook(window)

tab1 = ttk.Frame(appTabs)
tab2 = ttk.Frame(appTabs)
tab3 = ttk.Frame(appTabs)
tab4 = ttk.Frame(appTabs)
tab5 = ttk.Frame(appTabs)

appTabs.add(tab1, text="Окно1")
appTabs.add(tab2, text="Сотрудники")
appTabs.add(tab3, text="ввод")
appTabs.add(tab4, text='Товар')
appTabs.add(tab5, text='Покупатели')
##создание тексового поля
##Значение WORD опции wrap позволяет переносить слова на новую строку целиком, а не по буквам.


label1 = Label(tab1, text="выберете продукт")
label1.grid(column=0, row=0)

#combo_product = Combobox(tab1, width=40)
#combo_product['values'] = ("Kronebourg 1664 Blanc", "Балтика №4 Оригинальное", "Балтика №0 Безалкогольное", "Балтика №6 Портер",
                           #"Горьковское", "Балтика №7 Экспортное", "Zatecky Gus Svetly", "Балтика №8 Пшеничное", "Carlsberg",
                           #"Балтика №9 Крепкое", "387. Особая варка", "Amsterdam Navigator", "Золотая Бочка Классическое",
                           #"Efes Pilsener", "Velkopopovicky Kozel Тёмное", "Miller", "Белый Медведь Светлое", "Bavaria Premium Pilsner",
                           #"Жигулевское Бочковое")
                           #"Amstel", "Corona", "Heineken", "Carlsberg",
                           #"Lowenbreau", "Miller", "Толстяк", "Kozel", "Старый мельник", "Клинское", "Жигулевское",
                           #"387", "Spaten", "Asahi", "Paulaner")
#combo_product.grid(column=1, row=0)
text_product = Entry(tab1, width=40)
text_product.grid(column=0, row=1)

label2 = Label(tab1, text="Выберете количество")
label2.grid(column=1, row=0)

amount = Spinbox(tab1, from_=1, to=100, width=5)
amount.grid(column=1, row=1)

label3 = Label(tab1, text="Выберете магазин")
label3.grid(column=2, row=0)

combo_shop_purchase = Combobox(tab1)
combo_shop_purchase['values'] = ("Дьяконова 15", "Ватутина 34", "Красных Партизан 2", "Ильинская 7", "Максима Горького 154",
                        "Алексеевская 30", "Снежная 3", "Октябрьская 11", "Львовская 7", "Ошарская 80", "Коминтерна 123")
combo_shop_purchase.grid(column=2, row=1)

label4 = Label(tab1, text="Введите имя продавца")
label4.grid(column=3, row=0)
empNameEntry = Entry(tab1, width=20)
empNameEntry.grid(column=3, row=1)

label5 = Label(tab1, text="Введите имя покупателя")
label5.grid(column=0, row=2)
custNameEntry = Entry(tab1, width=40)
custNameEntry.grid(column=0, row=3)

label6 = Label(tab1, text="Введите дату и время")
label6.grid(column=1, row=2)
dateEntry = Entry(tab1, width=20)
dateEntry.grid(column=1, row=3)

buttonCreatePurchase = Button(tab1, text="Создать покупку")
buttonCreatePurchase['command'] = createPurchaseFunc
buttonCreatePurchase.grid(column=5, row=0)

n = 1.0
# кнопка добавления товара
buttonAddToCheck = Button(tab1, text="добавить")
buttonAddToCheck['command'] = addButtonFunc
buttonAddToCheck.grid(column=5, row=1)

CheckText = Text(tab1, width=30, height=10, wrap=WORD, state=tk.DISABLED)
CheckText.grid(column=0, row=4)

# tab2, добавление сотрудника
label_t2_1 = Label(tab2, text="Выберете магазин")
label_t2_1.grid(column=0, row=0)

# выбор магазина
combo_shop = Combobox(tab2)
combo_shop['values'] = ("Дьяконова 15", "Ватутина 34", "Красных Партизан 2", "Ильинская 7", "Максима Горького 154",
                        "Алексеевская 30", "Снежная 3", "Октябрьская 11", "Львовская 7", "Ошарская 80", "Коминтерна 123")
combo_shop.grid(column=1, row=0)

# ввод имени сотрудника
label_t2_2 = Label(tab2, text="Введите имя")
label_t2_2.grid(column=2, row=0)

textname = Text(tab2, width=15, height=1, wrap=WORD)
textname.grid(column=3, row=0)

# ввод должности
label_t2_3 = Label(tab2, text="Введите должность")
label_t2_3.grid(column=2, row=1)

positionname = Text(tab2, width=15, height=1, wrap=WORD)
positionname.grid(column=3, row=1)

# кнопка добавления сотрудника
employeebutton = Button(tab2, text="Добавить сотрудника")
employeebutton['command'] = addEmployeeFunc
employeebutton.grid(column=4, row=0)



# canvas = Canvas(tab2, height=400, width=700)
# image = Image.open("C:\pics\empl.jpg")
# photo = ImageTk.PhotoImage(image)
# image = canvas.create_image(0, 0, anchor='nw',image=photo)
# canvas.grid(column=3, row=2)

# добавление таблицы
tableemp = ttk.Treeview(tab2, columns=('id', 'market_id', 'name', 'position'), show='headings')
#tableemp['columns'] = ('id', 'market_id', 'name', 'position')
tableemp.column("#0", width=0, stretch=NO)
tableemp.column('id', anchor=CENTER, width=90)
tableemp.column('market_id', anchor=CENTER, width=90)
tableemp.column('name', anchor=CENTER, width=90)
tableemp.column('position', anchor=CENTER, width=90)
tableemp.heading('#0', text="", anchor=CENTER)
tableemp.heading('id', text='ID', anchor=CENTER)
tableemp.heading('market_id', text='market_id', anchor=CENTER)
tableemp.heading('name', text='Name', anchor=CENTER)
tableemp.heading('position', text='Position', anchor=CENTER)
#tableemp.grid(column=3, row=2)
#tableemp.place(relx=0, rely=0.5)
tableemp.grid(column=0, row=2, sticky='N', columnspan=10, pady=15 )


showbutton = Button(tab2, text="Показать сотрудников")
showbutton['command'] = showemployee
showbutton.grid(column=4, row=1)

delbutton = Button(tab2, text="Удалить сотрудника")
delbutton['command'] = delEmployeeBuuton
delbutton.grid(column=5, row=0)

buttonbelbymarketid = Button(tab2, text="Удалить всех из магазина")
buttonbelbymarketid['command'] = delbymarketid
buttonbelbymarketid.grid(column=5, row=1)



# tab3
txtexample = Text(tab3, width=25, height=5, wrap=WORD)
# txtexample.grid(column=0, row=1)
txtexample.pack(anchor=NW)

b1 = Button(tab3, text="отправить запрос", width=15, height=3, command=change)
# b1.grid(column=0, row=0)
b1.pack(anchor=NW)
#query = '''select * from aircrafts_data'''

##cursor.execute(create_table_pokupka)
# add_to_pokupka(1, 2, 4, 3, 150)
##result = cursor.execute(query)
##print(list(result))

#tab4 ДОБАВЛЕНИЕ ТОВАРА

label_t4_1 = Label(tab4, text="Название товара")
label_t4_1.grid(column=0, row=0)
prodname = Text(tab4, width=20, height=1)
prodname.grid(column=0, row=1)

label_t4_2 = Label(tab4, text="Выберете тип")
label_t4_2.grid(column=1, row=0)
typecombo = Combobox(tab4, width=30)
typecombo['values'] = ('Пиво', 'Вино', 'Виски', 'Коньяк', 'Шампанское', 'Ликер', 'Водка', 'Слабоалкогольный напиток')
typecombo.grid(column=1, row=1)


label_t4_3 = Label(tab4, text="Выберете производителя")
label_t4_3.grid(column=2, row=0)
manufCombo = Combobox(tab4)
manufCombo['values'] = ('Балтика', 'Efes Russia', 'HEINEKEN Russia', 'Московская пивоваренная компания',
                        'SUN InBev Russia', 'Löwenbräu AG', 'Paulaner Brauerei GmbH & Co. KG', 'Bayreuther', 'Spaten',
                        'BrewDog', 'Eichbaum', 'Vinos & Bodegas', 'Мысхако', 'Corporation Georgian Wine', 'Femar Vini',
                        'Jack Daniels', 'Glenfarclas', 'Douglas Laing', 'Gordon and MacPhail', 'Кизлярский коньячный завод',
                        'Tessendier', 'David Sarajishvili and Eniseli', 'Ragnaud-Sabourin')
manufCombo.grid(column=2, row=1)

label_t4_4 = Label(tab4, text="Ведите цену")
label_t4_4.grid(column=3, row=0)
costText= Text(tab4, width=10, height=1)
costText.grid(column=3, row=1)

label_t4_5 = Label(tab4, text="Введите скидку")
label_t4_5.grid(column=4, row=0)
discountText = Text(tab4, width=10, height=1)
discountText.grid(column=4, row=1)

buttonAddProduct = Button(tab4, text="Добавить товар")
buttonAddProduct['command'] = addProductButton
buttonAddProduct.grid(column=5, row=0)

buttonDelProduct = Button(tab4, text="Удалить товар")
buttonDelProduct['command'] = delProductButton
buttonDelProduct.grid(column=5, row=1)

buttonShowProduct = Button(tab4, text="Показать товар")
buttonShowProduct['command'] = showProductButton
buttonShowProduct.grid(column=5, row=2)


prodTable = ttk.Treeview(tab4, columns=('id', 'type_id', 'manufacturer_id', 'name', 'price'), height=10, show='headings')
#prodTable['columns'] = ('id', 'type_id', 'manufacturer_id', 'name', 'price', 'discount')
#prodTable.column('#0', width=0, stretch=NO)

#prodTable.heading('#0', text="", anchor=CENTER)
prodTable.heading('id', text="id", anchor=CENTER)
prodTable.heading('type_id', text="type_id", anchor=CENTER)
prodTable.heading('manufacturer_id', text="manufacturer_id", anchor=CENTER)
prodTable.heading('name', text="name", anchor=CENTER)
prodTable.heading('price', text="price", anchor=CENTER)


prodTable.column('id', anchor=CENTER, width=90)
prodTable.column('type_id', anchor=CENTER, width=90)
prodTable.column('manufacturer_id', anchor=CENTER, width=120)
prodTable.column('name', anchor=CENTER, width=180)
prodTable.column('price', anchor=CENTER, width=90)


prodTable.grid(column=0, row=3, sticky='N', columnspan=10, pady=15 )
#prodTable.place(relx=0, rely=0.5)

#tab5 Покупатели

label_t5_1 = Label(tab5, text="Введите ФИО покупателя")
label_t5_1.grid(column=0, row=0)
customerText = Text(tab5, width=30, height=1)
customerText.grid(column=0, row=1)

label_t5_2 = Label(tab5, text="Введите номер")
label_t5_2.grid(column=1, row=0)
phoneNumberText = Text(tab5, width=20, height=1)
phoneNumberText.grid(column=1, row=1)

buttonAddCustomer = Button(tab5, text="Добавить")
buttonAddCustomer['command'] = addCustomerButton
buttonAddCustomer.grid(column=2, row=0)

buttonDelCustomer = Button(tab5, text="Удалить")
buttonDelCustomer['command'] = delCustomerButton
buttonDelCustomer.grid(column=2, row=1)

buttonShowCustomer = Button(tab5, text="Показать")
buttonShowCustomer['command'] = showCutomerButton
buttonShowCustomer.grid(column=2, row=2)

tableCustomer = ttk.Treeview(tab5)
tableCustomer['columns'] = ('id', 'name', 'phone number')
tableCustomer.column('#0', width=0, stretch=NO)
tableCustomer.column('id', anchor=CENTER, width=90)
tableCustomer.column('name', anchor=CENTER, width=150)
tableCustomer.column('phone number', anchor=CENTER, width=90)
tableCustomer.heading('#0', text="", anchor=CENTER)
tableCustomer.heading('id', text="id", anchor=CENTER)
tableCustomer.heading('name', text="name", anchor=CENTER)
tableCustomer.heading('phone number', text="phone number", anchor=CENTER)
tableCustomer.place(relx=0, rely=0.2)


appTabs.pack(expand=1, fill='both')
window.mainloop()
