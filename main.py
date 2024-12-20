import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
from PIL import Image, ImageTk

bdhost = 'localhost'
bduser = 'Arseny'
bdpassword = 'bd'
bd = 'Market'

#postgres
#1909
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

    name = text_product.get()
    am = amount.get()
    print("select max(id) as max_id from purchase")
    cursor.execute("select max(id) as max_id from purchase")
    s = str(cursor.fetchall())
    nums = re.findall('(\d+)', s)
    print(nums[-1])
    purchace_id = nums[-1]
    sqpos = "select name from product where id=" + name.rstrip()
    cursor.execute(sqpos)
    pos = str(cursor.fetchall())[3:-4]
    print(sqpos)
    print(str(pos))
    CheckText['state'] = NORMAL
    CheckText.insert("end", str(pos))
    CheckText.insert("end", " ")
    CheckText.insert("end", (str(amount.get())))
    CheckText.insert("end", "\n")
    CheckText['state'] = tk.DISABLED

    sq = "select rec_pos_insert(" + str(purchace_id) + ", " + name + ", " + str(am) + ")"
    print(sq)
    cursor.execute(sq)
    connection.commit()
    print(sq)

    cursor.close()
    connection.close()
    return


def showProdIdFunc():
    connection = psycopg2.connect(host=bdhost, user=bduser, password=bdpassword, database=bd)
    cursor = connection.cursor()
    name = text_product.get()
    if name:
        print(name.rstrip())
        sq = "select id, name from product where name like '%%" + name.rstrip() + "%%' order by id"
    else:
        sq = "select id, name from product order by id"
    print(sq)
    cursor.execute(sq)
    [prodIdTable.delete(i) for i in prodIdTable.get_children()]
    [prodIdTable.insert('', 'end', values=row) for row in cursor.fetchall()]

    cursor.close()
    connection.close()
    return


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
    print("INSERT INTO employee (market_id, name, position) VALUES ( ( SELECT id FROM market WHERE street=" + str(streetname).rstrip() + " AND house=" + str(num).rstrip() + " )," + str(name).rstrip() + ", " + str(pos).rstrip() + " )")
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
    print(sq)
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
    print("delete from employee where market_id in (select id from market where street=" + str(nam1).rstrip() + " AND house=" + str(house).rstrip() + ")")
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

    print ('name', productname)
    print('type', typename)
    print('manuf', manufacturer)
    print('price', price)
    sq = "select product_insert('" + str(productname).rstrip() + "', " + str(price).rstrip() + ", '" + str(typename).rstrip() + "', '" + str(manufacturer).rstrip() + "')"
    print(sq)
    cursor.execute(sq)
    connection.commit()

    cursor.close()
    connection.close()


def editProductButton():
    connection = psycopg2.connect(host=bdhost, user=bduser, password=bdpassword, database=bd)
    cursor = connection.cursor()

    prodid = productIdEntry.get()
    name = prodname.get(1.0, END)
    typename = typecombo.get()
    manufacturer = manufCombo.get()
    price = costText.get(1.0, END)

    # product_update(prod_id int, new_type_name text, new_company_name text, new_name text, new_price numeric)

    sq = "select product_update(" + str(prodid).rstrip() + ", '" + str(typename).rstrip() + "', '" + str(manufacturer).rstrip() + "', '" + str(name).rstrip() + "', " + str(price).rstrip() + ")"
    print(sq)
    cursor.execute(sq)
    connection.commit()

    cursor.close()
    connection.close()



def showProductButton():
    connection = psycopg2.connect(host=bdhost, user=bduser, password=bdpassword, database=bd)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM product ORDER BY id")
    print("SELECT * FROM product ORDER BY id")
    [prodTable.delete(i) for i in prodTable.get_children()]
    [prodTable.insert('', 'end', values=row) for row in cursor.fetchall()]

    cursor.close()
    connection.close()

    return

def sortProductButton():
    connection = psycopg2.connect(host=bdhost, user=bduser, password=bdpassword, database=bd)
    cursor = connection.cursor()

    prodtype = typecombo.get()
    sq = "select * from product join product_type on product.type_id = product_type.id where product_type.type_name = '" + str(prodtype).rstrip() + "'"
    print(sq)
    cursor.execute(sq)
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
    print(sq)
    cursor.execute(sq)
    [tableCustomer.delete(i) for i in tableCustomer.get_children()]

    [tableCustomer.insert('', 'end', values=row) for row in cursor.fetchall()]
    cursor.close()
    connection.close()
    return

def showScoreButton():
    connection = psycopg2.connect(host=bdhost, user=bduser, password=bdpassword, database=bd)
    cursor = connection.cursor()
    sq = "select customer.id, customer.name, sum(amount) as sum from purchase join customer on purchase.customer_id = customer.id group by customer.id order by sum desc"
    print(sq)
    cursor.execute(sq)
    [tableScore.delete(i) for i in tableScore.get_children()]
    [tableScore.insert('', 'end', values=row) for row in cursor.fetchall()]
    cursor.close()
    connection.close()
    return


def changeUser():
    username = logtext.get()
    passw = passtext.get()
    global bduser
    global bdpassword
    bduser = str(username).rstrip()
    bdpassword = str(passw).rstrip()
    print(username, passw)
    return


window = Tk()
window.title("Бристоль")
window.geometry("800x600")

appTabs = ttk.Notebook(window)

tab1 = ttk.Frame(appTabs)
tab2 = ttk.Frame(appTabs)
tab3 = ttk.Frame(appTabs)
tab4 = ttk.Frame(appTabs)
tab5 = ttk.Frame(appTabs)

appTabs.add(tab1, text="Покупка")
appTabs.add(tab2, text="Сотрудники")
appTabs.add(tab4, text='Товар')
appTabs.add(tab5, text='Покупатели')
appTabs.add(tab3, text="Ввод")



label1 = Label(tab1, text="Введите id продукта")
label1.grid(column=0, row=0)
text_product = Entry(tab1, width=40)
text_product.grid(column=0, row=1)

label2 = Label(tab1, text="Выберете количество")
label2.grid(column=1, row=0)
amount = Spinbox(tab1, from_=1, to=100, width=5)
amount.grid(column=1, row=1)

label4 = Label(tab1, text="Введите имя продавца")
label4.grid(column=1, row=2)
empNameEntry = Entry(tab1, width=40)
empNameEntry.grid(column=1, row=3)

label5 = Label(tab1, text="Введите имя покупателя")
label5.grid(column=0, row=2)
custNameEntry = Entry(tab1, width=40)
custNameEntry.grid(column=0, row=3)

buttonCreatePurchase = Button(tab1, text="Создать покупку")
buttonCreatePurchase['command'] = createPurchaseFunc
buttonCreatePurchase.grid(column=2, row=1)

n = 1.0
# кнопка добавления товара
buttonAddToCheck = Button(tab1, text="добавить")
buttonAddToCheck['command'] = addButtonFunc
buttonAddToCheck.grid(column=2, row=0)

CheckText = Text(tab1, width=35, height=10, wrap=WORD, state=tk.DISABLED)
CheckText.grid(column=0, row=4)

prodIdTable = ttk.Treeview(tab1, columns=('id', 'name'), height=10, show='headings')
prodIdTable.heading('id', text="id", anchor=CENTER)
prodIdTable.heading('name', text="name", anchor=CENTER)
prodIdTable.column('id', anchor=CENTER, width=70)
prodIdTable.column('name', anchor=CENTER, width=250)
prodIdTable.grid(column=1, row=4)

showProdIdButton = Button(tab1, text="Показать товары")
showProdIdButton['command'] = showProdIdFunc
showProdIdButton.grid(column=2, row=2)

# tab2, добавление сотрудника
label_t2_1 = Label(tab2, text="Выберете магазин")
label_t2_1.grid(column=0, row=0)

# выбор магазина
combo_shop = Combobox(tab2)
combo_shop['values'] = ("Дьяконова 15", "Ватутина 34", "Красных Партизан 2", "Ильинская 7", "Максима Горького 154",
                        "Алексеевская 30", "Снежная 3", "Октябрьская 11", "Львовская 7", "Ошарская 80", "Коминтерна 123")
combo_shop.grid(column=0, row=1)

# ввод имени сотрудника
label_t2_2 = Label(tab2, text="Введите имя")
label_t2_2.grid(column=1, row=0)

textname = Text(tab2, width=30, height=1, wrap=WORD)
textname.grid(column=1, row=1)

# ввод должности
label_t2_3 = Label(tab2, text="Введите должность")
label_t2_3.grid(column=2, row=0)

positionname = Text(tab2, width=15, height=1, wrap=WORD)
positionname.grid(column=2, row=1)

# кнопка добавления сотрудника
employeebutton = Button(tab2, text="Добавить сотрудника")
employeebutton['command'] = addEmployeeFunc
employeebutton.grid(column=4, row=0)

# добавление таблицы
tableemp = ttk.Treeview(tab2, columns=('id', 'market_id', 'name', 'position'), show='headings')
tableemp.column("#0", width=0, stretch=NO)
tableemp.column('id', anchor=CENTER, width=60)
tableemp.column('market_id', anchor=CENTER, width=60)
tableemp.column('name', anchor=CENTER, width=230)
tableemp.column('position', anchor=CENTER, width=90)
tableemp.heading('#0', text="", anchor=CENTER)
tableemp.heading('id', text='ID', anchor=CENTER)
tableemp.heading('market_id', text='market_id', anchor=CENTER)
tableemp.heading('name', text='Name', anchor=CENTER)
tableemp.heading('position', text='Position', anchor=CENTER)
#tableemp.grid(column=3, row=2)
#tableemp.place(relx=0, rely=0.5)
tableemp.grid(column=0, row=4, sticky='N', columnspan=10, pady=15 )


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
txtexample = Text(tab3, width=40, height=5, wrap=WORD)
txtexample.pack(anchor=NW)

b1 = Button(tab3, text="отправить запрос", width=15, height=3, command=change)
b1.pack(anchor=NW)

labellog = Label(tab3, text="сменить пользователя\n Логин").pack(anchor=NW)
logtext = Entry(tab3, width=30)
logtext.pack(anchor=NW)
labelpass = Label(tab3, text="пароль").pack(anchor=NW)
passtext = Entry(tab3, width=30, show="*")
passtext.pack(anchor=NW)
changeUserButton = Button(tab3, text="Сменить пользователя", command=changeUser)
changeUserButton.pack(anchor=NW)
#tab4 ДОБАВЛЕНИЕ ТОВАРА

label_t4_1 = Label(tab4, text="Название товара")
label_t4_1.grid(column=0, row=0)
prodname = Text(tab4, width=20, height=1)
prodname.grid(column=0, row=1)

label_t4_2 = Label(tab4, text="Выберете тип")
label_t4_2.grid(column=1, row=0)
typecombo = Combobox(tab4, width=30)
typecombo['values'] = ('Пиво', 'Вино', 'Виски', 'Коньяк', 'Шампанское', 'Ликёр', 'Водка', 'Ром')
typecombo.grid(column=1, row=1)


label_t4_3 = Label(tab4, text="Выберете производителя")
label_t4_3.grid(column=2, row=0)
manufCombo = Combobox(tab4, width=30)
manufCombo['values'] = ('Балтика', 'Efes Russia', 'HEINEKEN Russia', 'Московская пивоваренная компания',
                        'SUN InBev Russia', 'Löwenbräu AG', 'Paulaner Brauerei GmbH & Co. KG', 'Bayreuther', 'Spaten',
                        'BrewDog', 'Eichbaum', 'Vinos & Bodegas', 'Мысхако', 'Corporation Georgian Wine', 'Femar Vini',
                        'Jack Daniels', 'Glenfarclas', 'Douglas Laing', 'Gordon and MacPhail', 'Кизлярский коньячный завод',
                        'Tessendier', 'David Sarajishvili and Eniseli', 'Ragnaud-Sabourin', 'Louis Roederer',
                        'Moet Chandon', 'Кубань-Вино', 'Cantine Quattro Valli', 'Bisol', 'Lucas Bols', 'Cooymans',
                        'Handelshof NF & MS', 'Rossi D''Asiago Distillery', 'Renaud Cointreau', 'Absolut', 'Waldemar Behn',
                        'Reyka', 'Синергия', 'Nolet Distillery', 'Destilerias Unidas (Dusa)', 'Rossi & Rossi',
                        'Demerara Distillers', 'Oliver and Oliver', 'Cognac Ferrand')
manufCombo.grid(column=2, row=1)

label_t4_4 = Label(tab4, text="Ведите цену")
label_t4_4.grid(column=3, row=0)
costText= Text(tab4, width=10, height=1)
costText.grid(column=3, row=1)


buttonAddProduct = Button(tab4, text="Добавить товар")
buttonAddProduct['command'] = addProductButton
buttonAddProduct.grid(column=4, row=0)

buttonShowProduct = Button(tab4, text="Показать товар")
buttonShowProduct['command'] = showProductButton
buttonShowProduct.grid(column=4, row=1)


prodTable = ttk.Treeview(tab4, columns=('id', 'type_id', 'manufacturer_id', 'name', 'price'), height=10, show='headings')
prodTable.heading('id', text="id", anchor=CENTER)
prodTable.heading('type_id', text="type_id", anchor=CENTER)
prodTable.heading('manufacturer_id', text="manufacturer_id", anchor=CENTER)
prodTable.heading('name', text="name", anchor=CENTER)
prodTable.heading('price', text="price", anchor=CENTER)
prodTable.column('id', anchor=CENTER, width=90)
prodTable.column('type_id', anchor=CENTER, width=90)
prodTable.column('manufacturer_id', anchor=CENTER, width=120)
prodTable.column('name', anchor=CENTER, width=230)
prodTable.column('price', anchor=CENTER, width=90)

prodTable.grid(column=0, row=3, sticky='N', columnspan=10, pady=15 )
#prodTable.place(relx=0, rely=0.5)

productIdEntry = Entry(tab4, width=10)
productIdEntry.grid(column=0, row=4, sticky='W')

editProductByIdButton = Button(tab4, text="Изменить по id")
editProductByIdButton['command'] = editProductButton
editProductByIdButton.grid(column=1, row=4, sticky='W')

buttonSortProduct = Button(tab4, text="Сортировать по типу")
buttonSortProduct['command'] = sortProductButton
buttonSortProduct.grid(column=4, row=2)


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

buttonShowCustomer = Button(tab5, text="Показать покупателей")
buttonShowCustomer['command'] = showCutomerButton
buttonShowCustomer.grid(column=3, row=0)

tableCustomer = ttk.Treeview(tab5, columns=('id', 'name', 'phone number'), height=10, show='headings')
tableCustomer.column('id', anchor=CENTER, width=90)
tableCustomer.column('name', anchor=CENTER, width=230)
tableCustomer.column('phone number', anchor=CENTER, width=150)
tableCustomer.heading('id', text="id", anchor=CENTER)
tableCustomer.heading('name', text="name", anchor=CENTER)
tableCustomer.heading('phone number', text="phone number", anchor=CENTER)
tableCustomer.place(relx=0, rely=0.15)

tableScore = ttk.Treeview(tab5, columns=('id', 'name', 'sum'), height=10, show='headings')
tableScore.heading('id', text="id", anchor=CENTER)
tableScore.heading('name', text="name", anchor=CENTER)
tableScore.heading('sum', text="sum", anchor=CENTER)
tableScore.column('id', anchor=CENTER, width=60)
tableScore.column('name', anchor=CENTER, width=230)
tableScore.column('sum', anchor=CENTER, width=100)
tableScore.place(relx=0, rely=0.55)

buttonShowScore = Button(tab5, text="Показать статистику")
buttonShowScore['command'] = showScoreButton
buttonShowScore.grid(column=3, row=1)

canvas = Canvas(tab5, height=300, width=320)
image = Image.open("C:\pics\pivo.jpg")
photo = ImageTk.PhotoImage(image)
image = canvas.create_image(0, 0, anchor='nw',image=photo)
canvas.place(relx=0.6, rely=0.5)



appTabs.pack(expand=1, fill='both')
window.mainloop()
