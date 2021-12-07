from sqlalchemy import create_engine
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import tkinter as tk
from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
from tkinter.ttk import Combobox

# Устанавливаем соединение с postgres
connection = psycopg2.connect(user="postgres", password="1909")
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
# Создаем курсор для выполнения операций с базой данных
cursor = connection.cursor()
##engine = create_engine('postgresql://{}:{}@localhost/demo'.format(auth['postgres'], auth['1909']), echo=True)
engine = create_engine('postgresql://postgres:1909@localhost/try')
cursor = engine.connect()


## отправляет запрос на бд и выполняет его
## это функция кнопки
def change():
    s = txtexample.get(1.0, END)
    print(s)
    runfunc(s)
    print("button pressed")


## функция которая отправляет запрос к БД
def runfunc(str):
    try:
        cursor.execute(str)
    except:
        mb.showerror('Ошибка запроса', 'Ошибка в запросе к БД!\n Попробуйте изменить запрос.')
        # print("error")


# функция которая может вызываться внутри кода, но не из gui (пока)
def add_to_pokupka(shop_id, product_id, employee_id, amount, total):
    qu = "INSERT INTO pokupka (shop_id, product_id, employee_id, amount, total)" \
         " VALUES ('" + str(shop_id) + "', '" + str(product_id) + "', '" + str(employee_id) + "', '" + str(
        amount) + "', '" + str(total) + "');"
    runfunc(qu)


def addButtonFunc():
    CheckText['state'] = NORMAL
    CheckText.insert("end", str(combo_product.get()))
    CheckText.insert("end", " ")
    CheckText.insert("end", (str(amount.get())))
    CheckText.insert("end", "\n")
    CheckText['state'] = tk.DISABLED



window = Tk()
window.title("database experience")
window.geometry("800x600")

appTabs = ttk.Notebook(window)

tab1 = ttk.Frame(appTabs)
tab2 = ttk.Frame(appTabs)

appTabs.add(tab1, text="Окно1")
appTabs.add(tab2, text="Окно2")

##создание тексового поля
##Значение WORD опции wrap позволяет переносить слова на новую строку целиком, а не по буквам.
txtexample = Text(tab2, width=25, height=5, wrap=WORD)
txtexample.grid(column=0, row=1)

b1 = Button(tab2, text="отправить запрос", width=15, height=3, command=change)
b1.grid(column=0, row=0)

label1 = Label(tab1, text="выберете продукт")
label1.grid(column=0, row=0)

combo_product = Combobox(tab1)
combo_product['values'] = ("Bud", "Балтика 7", "Балтика 9", "Amstel", "Corona", "Heineken", "Carlsberg",
                           "Lowenbreau", "Miller", "Толстяк", "Kozel", "Старый мельник", "Клинское", "Жигулевское",
                           "387", "Spaten", "Asahi", "Paulaner")
combo_product.grid(column=1, row=0)

label2 = Label(tab1, text="Выберете количество")
label2.grid(column=2, row=0)

amount = Spinbox(tab1, from_=1, to=100, width=5)
amount.grid(column=3, row=0)

n = 1.0
buttonAddToCheck = Button(tab1, text="добавить")
buttonAddToCheck['command'] = addButtonFunc
buttonAddToCheck.grid(column=4, row=0)

CheckText = Text(tab1, width=30, height=10, wrap=WORD, state=tk.DISABLED)
CheckText.grid(column=0, row=1)
##CheckText.insert(1.0, "hello")


query = '''select * from aircrafts_data'''
create_table_pokupka = '''CREATE TABLE pokupka 
(
  purchase_id SERIAL PRIMARY KEY  NOT NULL ,
  shop_id INT NOT NULL,
  product_id Int NOT NULL,
  employee_id INT NOT NULL,
  amount INT,
  total INT
)'''

##cursor.execute(create_table_pokupka)
# add_to_pokupka(1, 2, 4, 3, 150)
##result = cursor.execute(query)
##print(list(result))
appTabs.pack(expand=1, fill='both')
window.mainloop()
