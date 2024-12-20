from sqlalchemy import create_engine                        # Импорт библиотеки для работы с SQLAlchemy
import re                                                   # Импорт библиотеки для работы с регулярными выражениями
import psycopg2                                             # Импорт библиотеки psycopg2 для работы с PostgreSQL
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT  # Импорт уровня изоляции для работы с транзакциями
import tkinter as tk                                        # Импорт библиотеки tkinter для создания GUI
from tkinter import *                                       # Импорт всех элементов из tkinter для использования в GUI
from tkinter import messagebox as mb                        # Импорт messagebox для отображения диалоговых окон
from tkinter import ttk                                     # Импорт ttk для создания стильных элементов GUI
from tkinter.ttk import Combobox                            # Импорт комбинированного списка (выпадающего списка) из ttk
from PIL import Image, ImageTk                              # Импорт библиотеки для работы с приложениями

# Параметры для подключения к базе данных
dbname, user, password, host, port = "shopdatabase", "postgres", "postgres", "localhost", "5433"
def get_db_connection():
    """ Создает и возвращает подключение к базе данных"""
    try:
        connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        return connection
    except Exception as e:
        raise Exception(f"Ошибка при подключении к базе данных {e}")
def safe_close_connection(cursor=None, connection=None):
    """ Закрывает курсор и соединением с базой данных, если они существуют"""
    try:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection:
            connection.close()
    except Exception as e:
        print(f"Ошибка при закрытии ресурсов {e}")


def change():
    """
    Функция вызывается при нажатии на кнопку. Она получает текст из текстового поля и передает его
    в функцию runfunc() для выполнения SQL запроса.
    """
    s = txtexample.get(1.0, END)    # Получение текста из текстового поля с помощью метода get()
    print(s)                        # Вывод полученный текст в консоль для отладки
    runfunc(s)                      # Выполнение SQL-запроса, передавая полученный текст
    print("button pressed")         # Вывод в консоль сообщение о нажатии кнопки
def runfunc(str):
    """
    Функция выполняет SQL запрос, переданный ей в виде строки.
    Если запрос выполнен успешно, соединение с базой данных закрывается.
    В случае ошибки появляется окно с сообщением об ошибке.
    :param str: SQL-запрос в виде строки
    """
    # Устанавливается соединение с базой данных PostgreSQL
    connection = get_db_connection()
    cursor = connection.cursor()    # Создания курсора для выполнения запросов
    try:
        cursor.execute(str)         # Выполнение SQL-запроса, переданный в функцию
        cursor.close()              # Закрытие курсора
        connection.close()          # Закрытие соединение с базой данных
    except Exception as ex:
        # Если возникла ошибка, показываем сообщение об ошибке
        mb.showerror('Ошибка запроса', 'Ошибка в запросе к БД!\n Попробуйте изменить запрос.')
        print(ex)                   # Вывод ошибки в консоль для отладки
        cursor.close()              # Закрытие курсора
        connection.close()          # Закрытие соединение с базой данных

def createPurchaseFunc():
    """
    Функция для создания покупки в базе данных.
    Она использует значения из полей ввода интерфейса (tkinter) для формирования
    SQL-запроса, который вызывает хранимую функцию 'purchase_insert' в PostgreSQL.
    """
    # Устанавливается соединение с базой данных PostgreSQL
    try:
        cust_name = cust_name_entry.get().rstrip()  # Получение имени клиента из поля ввода custNameEntry
        emp_name = emp_name_entry.get().rstrip()    # Получение имени сотрудника из поля ввода empNameEntry
        if not emp_name or not cust_name:
            raise  ValueError("Имя сотрудника и имя клиента не должны быть пустыми.")
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "select purchase_insert(%s, %s)"       # Формирование SQL-запроса для вызова хранимой функции purchase_insert
        cursor.execute(query, (emp_name, cust_name))   # Выполнение сформированного SQL-запроса
        connection.commit()                         # Фиксирование изменения в базе данных (commit)
    except ValueError as ve:
        print(f"Ошибка ввода: {ve}")
    except Exception as e:
        print(f"Ошибка при создании покупки: {e}")
    finally:
        safe_close_connection(cursor, connection)
def addButtonFunc():
    """
    Функция добавляет новую запись в чек, используя данные о продукте и его количестве.
    Обновляет текстовый виджет для отображения чека и добавляет запись в базу данных.
    """
    try:
        # Устанавливается соединение с базой данных PostgreSQL
        connection = get_db_connection()
        cursor = connection.cursor()
        name = text_product.get()                           # Получение ID продукта
        am = amount.get()                                   # Получение количества продукта
        if not name or not am:                              # Проверка, что поля не пустые
            raise ValueError("Поля ID продукта и количество не должны быть пустыми.")
        if not am.isdigit():                                # Проверка, что количество продукта является числом
            raise ValueError("Количество продукта должно быть числом.")

        # SQL-запрос для получения максимального ID из таблицы покупок
        cursor.execute("SELECT MAX(id) AS max_id FROM purchase")
        purchase_id = cursor.fetchone()[0]                  # Извлечение максимального ID
        if not purchase_id:
            raise ValueError("Не удалось определить ID покупки.")

        # SQL-запрос для получения имени продукта по его ID
        cursor.execute("SELECT name FROM product WHERE id = %s", (name,))
        product_result = cursor.fetchone()
        if not product_result:
            raise ValueError("Продукт с указанным ID не найден.")
        product_name = product_result[0]                    # Извлечение названия продукта

        # Обновление текстового виджета CheckText
        CheckText['state'] = NORMAL
        CheckText.insert("end", f"{product_name} {am}\n")   # Добавление строки в чек
        CheckText['state'] = tk.DISABLED

        # SQL-запрос для добавления записи в таблицу позиций покупки
        cursor.execute("SELECT res_pos_insert(%s, %s, %s)", (purchase_id, name, am))
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        # Обработка ошибок и вывод сообщения
        mb.showerror("Ошибка", f"Произошла ошибка {error}")
        print(f"Ошибка: {error}")
    finally:
        safe_close_connection(cursor, connection)


def showProdIdFunc():
    """
    Получает список продуктов из базы данных и отображает их в таблице интерфейса.
        - Если текстовое поле 'text_product' содержит текст, выполняется поиск продуктов,
        имя которых частично соответствует введенному значению.
        - Если текстовое поле пустое, загружаются все продукты.
    Записи отображаются в 'prodIdTable'
    :var: text_product: Поле ввода для имени продукта.
    :var: prodIdTable: Таблица для отображения результатов.
    База данных:
        - Подключение выполняется с использованием глобальных переменных:
        - dbname, user, password, host, port - конфигурационные параметры подключения к базе данных.
    Исключения:
        - Обрабатывает ошибки подключения или выполнения SQL-запросов.
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        name = text_product.get().strip()
        if name:
            print(f"Поиск продукта: {name}")
            query = "SELECT id, name FROM product WHERE name ILIKE %s ORDER BY id"
            params = (f"%{name}%",)
        else:
            print("Загрузка всех продуктов")
            query = "SELECT id, name FROM product ORDER BY id"
            params = None
        print(f"SQL-запрос: {query}")
        cursor.execute(query, params)
        [prodIdTable.delete(i) for i in prodIdTable.get_children()]
        for row in cursor.fetchall():
            prodIdTable.insert("", "end", values=row)
    except psycopg2.Error as e:
        print("Ошибка при работе с базой данных", e)
        mb.showerror("Ошибка бд", "Не удалось выполнить запрос к базе данных")
    finally:
        safe_close_connection(cursor, connection)

def addEmployeeFunc():
    """
    Добавляет нового сотрудника в базу данных.
    Данные:
    - Имя сотрудника из поля text_name.
    - Должность сотрудника из поля position_name.
    - Магазин из выпадающего списка combo_shop (формат: "улица номер").
    Сохраняет запись в таблицу employee, связывая сотрудника с market_id.
    """
    try:
        # Установка соединения с базой данных
        connection = get_db_connection()
        cursor = connection.cursor()
        # Получение данных из интерфейса
        name = text_name.get(1.0, END).strip()
        position = position_name.get(1.0, END).strip()
        shop_name = combo_shop.get().strip()
        if not name or not posotion or not shop_name:
            raise ValueError("Все поля должны быть заполнены!")
        # Разделение адреса на улицу и номер дома
        try:
            street_name, house_num = shop_name.rsplit(" ", 1)
        except ValueError:
            raise ValueError("Некорректный формат адреса магазина. Укажите в формате 'улица номер'.")
        # Формирование и выполнение безопасного SQL-запроса
        query = """INSERT INTO employee (market_id, name, position
                   VALUES ((SELECT if FROM market WHERE street = %s AND house = %s), %s, %s"""
        cursor.execute(query, (street_name, house_num, name, positiom))
        connection.commit()
        print(f"Сотрудник добавлен: {name}, должность {position}, магазин: {shop_name}")
    except psycopg2.Error as db_error:
        print(f"Ошибка базы данных: {db_error}")
    except ValueError as input_error:
        print(f"Ошибка ввода: {input_error}")
    finally:
        safe_close_connection(cursor, connection)


def showEmployeeButtonFunc():
    """Отображает список всех сотрудников из базы данных в таблице table_emp"""
    try:
        # Установка соединения с базой данных
        connection = get_db_connection()
        cursor = connection.cursor()
        # SQL-запрос для получения всех записей из таблицы employee
        sq = "SELECT * FROM employee"
        print(sq)   # Вывод запроса в консоль для отладки
        cursor.execute(sq) # Выполнение SQL-запроса
        [tableemp.delete(i) for i in tableemp.get_children()]   # Очистка текущей таблицы table_emp в интерфейсе
        [tableemp.insert('', 'end', values=row) for row in cursor.fetchall()]   # Заполнение таблицы table_emp новыми данными из результата SQL-запроса
    except psycopg2.Error as db_error:
        print(f"Ошибка базы данных: {db_error}")
    finally:
        safe_close_connection(cursor, connection)

def delEmployeeButtonFunc():
    """
    Удаляет сотрудника из базы данных по имени, введенному в текстовое поле text_name.
    """
    try:
        # Подключение к базе данных
        connection = get_db_connection()
        cursor = connection.cursor()
        # Получаем имя сотрудника из текстового поля
        name = textname.get(1.0, END).strip()
        if not name:
            raise ValueError("Имя сотрудника не может быть пустым!")
        # Формирование запроса и использованием параметров для защиты от SQL-инъекций
        query = "DELETE FROM employee WHERE name LIKE %s"
        cursor.execute(query, (name,))
        connection.commit()
        print(f"Сотрудники с именем '{name}' удален.")
    except Exception as e:
        # Обработка ошибок
        print(f"Ошибка при удалении сотрудника: {e}")
    finally:
        safe_close_connection(cursor, connection)


def delAllEmployeeButtonFunc():
    """
    Удаляет всех сотрудников, работающих в магазине, по данным из выпадающего списка combo_shop.
    """
    try:
        # Подключение к базе данных
        connection = get_db_connection()
        cursor = connection.cursor()
        # Получение данных из выпадающего списка
        shop_name = combo_shop_get()
        if not shop_name:
            raise ValueError("Магазин не выбран")
        # Разделение адрес на улицу и номер дома
        name_list = shop_name.split(' ')
        if len(name_list) < 2:
            raise ValueError("Некорректный формат адреса магазина. Укажите в формате 'улица номер'.")
        street_name, house_num = shop_name.rsplit(" ", 1)
        print(f"DELETE FROM employee WHERE market_id IN (SELECT id FROM market WHERE street='{street_name}' and house='{house_num}')")
        query = """DELETE FROM employee WHERE market_id IN (SELECT id FROM market WHERE street = %s AND house = %s )"""
        cursor.execute(query, (street_name, house_num))
        connection.commit()
        print(f"Сотрудники из магазина по адресу '{street_name} {house_number}' успешно удалены.")
    except Exception as e:
        # Обработка ошибок
        print(f"Ошибка при удалении сотрудников из магазина: {e}")
    finally:
        safe_close_connection(cursor, connection)



def addProductButtonFunc():
    """Добавляет новый продукт в базу данных, используя пользовательскую функцию product_insert."""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Получение данных из интерфейса
        product_name = prod_name.get(1.0, END).strip()
        type_name = type_combo.get().strip()
        manufacturer_name = manuf_combo.get().strip()
        price = cost_text.get(1.0, END).strip()

        # Проверка на пустые поля
        if not product_name or not type_name or not manufacturer_name or not price:
            raise ValueError("Ошибка: Не все поля заполнены!")
        try:    # Проверка на корректность ввода цены
            price = float(price)
            if price <= 0:
                raise ValueError
        except ValueError:
            raise ValueError("Неверный формат ввода цены!")

        # Логирование данные для отладки
        print(f"Добавление продукта: name='{product_name}', type='{type_name}', manufacturer='{manufacturer_name}', price={price}")

        # Безопасный вызов пользовательской функции
        query = "SELECT product_insert(%s, %s, %s, %s)"
        cursor.execute(query, (product_name, type_name, manufacturer_name, price))
        connection.commit()
        print(f"Продукт успешно добавлен.")
    except Exception as e:
        # Обработка ошибок
        print(f"Ошибка при добавлении продукта: {e}")
    finally:
        # Закрываем курсор и соединение
        safe_close_connection(cursor, connection)

def editProductButtonFunc():
    """Редактирует данные продукта в базе данных, вызывая пользовательскую функцию product_update."""
    try:
        # Подключение к базе данных
        connection = get_db_connection()
        cursor = connection.cursor()

        # Получение данных из интерфейса
        product_id = prod_id_entry.get().strip()
        product_name = prod_name.get(1.0, END).strip()
        type_name = type_combo.get().strip()
        manufacturer_name = manuf_combo.get().strip()
        price = cost_text.get(1.0, END).strip()

        # Проверка на пустые поля
        if not product_id or not product_name or not type_name or not manufacturer_name or not price:
            raise ValueError("Ошибка: Не все поля заполнены!")

        # Проверка на корректность ввода идентификатора и цены
        try:
            product_id = int(product_id)
            price = float(price)
            if price <= 0:
                raise ValueError
        except ValueError:
            raise ValueError("Неверный формат значения для ID и цены")

        # Логирование данных для отладки
        print(f"Редактирование продукта: id='{product_id}', name='{product_name}', type='{type_name}', manufacturer='{manufacturer_name}', price={price}")

        # Безопасный вызов пользовательской функции
        query = "SELECT product_update(%s, %s, %s, %s, %s)"
        cursor.execute(query, (product_id, type_name, manufacturer_name, product_name, price))
        connection.commit()
        print(f"Продукт успешно обновлен.")
    except Exception as e:
        # Обработка ошибок
        print(f"Ошибка при редактировании продукта: {e}")
    finally:
        safe_close_connection(cursor, connection)
def showProductButtonFunc():
    """
    Получает и отображает все продукты, полученные из базы данных в таблице продуктов
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "SELECT * FROM product ORDER BY id"
        cursor.execute(query)
        [prodTable.delete(i) for i in prodTable.get_children()]
        [prodTable.insert('', 'end', values=row) for row in cursor.fetchall()]
    except Exception as e:
        print(f"Ошибка при подключении к базе данных: {e}")
    finally:
        safe_close_connection()

def sortProductButtonFunc():
    """
    """
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
    except Exception as e:
        print(f"Ошибка при подключении к базе данных: {e}")
    finally:
        safe_close_connection()

#=================================================
# def addCustomerButtonFunc():
#     """
#
#     :return:
#     """
#     try:
#         connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
#         cursor = connection.cursor()
#     except:
#
#     finally:
#         # Закрываем курсор и соединение
#         if 'cursor' in locals() and cursor:
#             cursor.close()
#         if 'connection' in locals() and connection:
#             connection.close()


# def delCustomerButtonFunc():
#     """
#
#     :return:
#     """
#     try:
#         connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
#         cursor = connection.cursor()
#     except:
#
#     finally:
#         # Закрываем курсор и соединение
#         if 'cursor' in locals() and cursor:
#             cursor.close()
#         if 'connection' in locals() and connection:
#             connection.close()


# def showCustomerButtonFunc():
#     """
#
#     :return:
#     """
#     try:
#         connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
#         cursor = connection.cursor()
#     except:
#
#     finally:
#         # Закрываем курсор и соединение
#         if 'cursor' in locals() and cursor:
#             cursor.close()
#         if 'connection' in locals() and connection:
#             connection.close()


# def showScoreButtonFunc():
#     """
#
#     :return:
#     """
#     try:
#         connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
#         cursor = connection.cursor()
#     except:
#
#     finally:
#         # Закрываем курсор и соединение
#         if 'cursor' in locals() and cursor:
#             cursor.close()
#         if 'connection' in locals() and connection:
#             connection.close()
def changeUserFunc():
    """
    Обновляет глобальные переменные имени пользователя и пароля для подключения к базе данных.
    Получает имя пользователя и пароль из полей ввода (tkinter), валидирует их и обновляет
    глобальные переменные 'bsuser' и 'bdpassword'.
    """
    try:
        new_username = login_text.get().strip()
        new_password = password_text.get().strip()
        if not new_username:
            raise  ValueError("Имя пользователя не может быть пустым.")
        if not new_password:
            raise ValueError("Пароль не может быть пустым.")
        # Обновление глобальных переменных
        global bsuser, bdpassword
        bsuser, bdpassword = new_username, new_password
        print(f"Изменены данные пользователя: {bsuser}")
        print(f"Имя пользователя: {new_username}, Пароль: {new_password}")
    except ValueError as ve:
        print(f"Ошибка: {ve}")
    except Exception as e:
        print(f"Произошла ошибка при обновлении данных пользователя {e}")


# Создание главного окна
window = Tk()
window.title("Бристоль")
window.geometry("800x600")
appTabs = ttk.Notebook(window)  # Создание виджета вкладов
tab_names = ["Покупка", "Сотрудники", "Ввод", "Товар", "Покупатели"]
tabs = {}
for name in tab_names:
    tabs[name] = ttk.Frame(appTabs)
    appTabs.add(tabs[name], text=name)

def init_tab1(tab):
    """Инициализация содержимого вкладки 'Покупка'."""
    # Метка и поле ввода для ID продукта
    label1 = Label(tab, text="Введите id продукта")
    label1.grid(column=0, row=0)
    text_product = Entry(tab, width=40)
    text_product.grid(column=0, row=1)

    # Метка и спинбокс для выбора количества
    label2 = Label(tab, text="Выберете количество")
    label2.grid(column=1, row=0)
    amount = Spinbox(tab, from_=1, to=100, width=5)
    amount.grid(column=1, row=1)

    # Метка и поле ввода для имени продавца
    label3 = Label(tab, text="Введите имя продавца")
    label3.grid(column=1, row=2)
    emp_name_entry = Entry(tab, width=40)
    emp_name_entry.grid(column=0, row=3)

    # Метка и поле ввода имени покупателя
    label4 = Label(tab, text="Введите имя покупателя")
    label4.grid(column=0, row=2)
    cust_name_entry = Entry(tab, width=40)
    cust_name_entry.grid(column=0, row=5)

    # Кнопка для создания покупки
    button_create_purchase = Button(tab, text="Создать покупку")
    button_create_purchase['command'] = createPurchaseFunc
    button_create_purchase.grid(column=2, row=1)

    # Кнопка для добавления покупки
    button_add_to_check = Button(tab, text="Добавить")
    button_add_to_check['command'] = addButtonFunc
    button_add_to_check.grid(column=2, row=0)

    # Поля для вывода чека
    check_text = Text(tab, width=35, height=10, wrap=WORD, state=tk.DISABLED)
    check_text.grid(column=0, row=4)

    # Таблица для отображения ID и имени товара
    prod_id_table = ttk.Treeview(tab, columns=('id', 'name'), height=10, show='headings')
    prod_id_table.heading('id', text="ID", anchor=CENTER)
    prod_id_table.heading('name', text="Название", anchor=CENTER)
    prod_id_table.column('id', width=70, anchor=CENTER)
    prod_id_table.column('name', width=250, anchor=CENTER)
    prod_id_table.grid(column=1, row=4)

    # Кнопка для отображения списка товаров
    show_prod_id_button = Button(tab, text="Показать товары")
    show_prod_id_button['command'] = showProductButtonFunc
    show_prod_id_button.grid(column=2, row=2)


def init_tab2(tab):
    """ Инициализирует содержимое вкладки 'Сотрудники'."""
    # Метка и выпадающий список для выбора магазина
    label_t2_1 = Label(tab, text="Выберете магазин")
    label_t2_1.grid(column=0, row=0)
    combo_shop = Combobox(tab, width=30)
    combo_shop['values'] = ("Дьяконова 15", "Ватутина 34", "Красных партизан 2",
                            "Ильинская 7", "Максима Горького 154", "Алексеевская 30", "Снежная 3",
                            "Октябрьская 11", "Львовская 7", "Ошарская 80", "Коминтерна 123")

    combo_shop.grid(column=0, row=1)

    # Метка и для ввода имени сотрудника
    label_t2_2 = Label(tab, text="Введите имя")
    label_t2_2.grid(column=1, row=0)
    text_name = Entry(tab, width=30)
    text_name.grid(column=1, row=1)

    # Метка и для ввода должности сотрудника
    label_t2_3 = Label(tab, text="Введите должность")
    label_t2_3.grid(column=2, row=0)
    position_name = Entry(tab, width=15)
    position_name.grid(column=2, row=1)

    # Кнопка для добавления сотрудника
    employee_button = Button(tab, text="Добавить сотрудника")
    employee_button['command'] = addEmployeeFunc
    employee_button.grid(column=4, row=0)

    # Таблица для отображения сотрудников
    table_employee = ttk.Treeview(tab, columns=('id', 'market_id', 'name', 'position'), show='headings')
    table_employee.column("#0", width=0, stretch=NO)
    table_employee.column('id', anchor=CENTER, width=60)
    table_employee.column('market_id', anchor=CENTER, width=100)
    table_employee.column('name', anchor=CENTER, width=230)
    table_employee.column("position", anchor=CENTER, width=120)
    table_employee.heading("#0", text="", anchor=CENTER)
    table_employee.heading('id', text="ID", anchor=CENTER)
    table_employee.heading('market_id', text="Магазин", anchor=CENTER)
    table_employee.heading('name', text="Имя", anchor=CENTER)
    table_employee.heading("position", text="Должность", anchor=CENTER)
    table_employee.grid(column=0, rows=4, sticky='N', columnspan=6, pady=15)

    # Кнопка для отображения сотрудников
    show_employee_button = Button(tab, text="Показать сотрудников")
    show_employee_button['command'] = showEmployeeButtonFunc
    show_employee_button.grid(column=4, row=1)

    # Кнопка для удаления сотрудника
    delete_employee_button = Button(tab, text="Удалить сотрудника")
    delete_employee_button['command'] = delEmployeeButtonFunc
    delete_employee_button.grid(column=5, row=0)
    
    # Кнопка для удаления всех сотрудников из выбранного магазина
    delete_all_employee_button = Button(tab, text="Удалить всех сотрудников")
    delete_all_employee_button['command'] = delAllEmployeeButtonFunc
    delete_all_employee_button.grid(column=5, row=1)

def init_tab3(tab):
    """Инициализирует содержимое вкладки 'Ввод'."""
    # Пример текстового поля для ввода данных
    text_example = Text(tab, width=40, height=5, wrap=WORD)
    text_example.pack(anchor=NW, pady=5)

    # Кнопка для отправки запроса
    button_send_request = Button(tab, text="Отправить запрос", width=15, height=3, command=change)
    button_send_request.pack(anchor=NW, pady=5)

    # Метка и поле для смены пользователя (логин)
    label_t3_login = Label(tab, text="Сменить пользователя\nЛогин")
    label_t3_login.pack(anchor=NW)
    login_entry_text = Entry(tab, width=30)
    login_entry_text.pack(anchor=NW, pady=2)

    # Метка и поле для смены пользователя (пароль)
    label_t3_password = Label(tab, text="Пароль")
    label_t3_password.pack(anchor=NW)
    password_entry_text = Entry(tab, show="*", width=30)    # Поле ввода с маскировкой символов
    password_entry_text.pack(anchor=NW, pady=2)

    # Кнопка для подтверждения смены пользователя
    change_user_button = Button(tab, text="Сменить пользователя", command=changeUserFunc)
    change_user_button.pack(anchor=NW, pady=5)


def init_tab4(tab):
    """Инициализирует содержимое вкладки 'Товары'."""
    label_t4_1 = Label(tab, text="Название товара")
    label_t4_1.grid(column=0, row=0)
    product_name = Text(tab, width=20, height=1)
    product_name.grid(column=0, row=1)

    label_t4_2 = Label(tab, text="Выберете тип")
    label_t4_2.grid(column=1, row=0)
    type_combo = Combobox(tab, width=30)
    type_combo['values'] = ('Пиво', "Вино", "Виски", "Коньяк", "Шампанское", "Ликер", "Водка", "Ром")
    type_combo.grid(column=1, row=1)


def init_tab5(tab):
    # Здесь добавляем элементы для вкладки "Покупатели"
    pass

init_functions = {
    "Покупка": init_tab1,
    "Сотрудники": init_tab2,
    "Ввод": init_tab3,
    "Товар": init_tab4,
    "Покупатели": init_tab5
}
for name, init_functions in init_functions.items():
    init_functions(tabs[name])