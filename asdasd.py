import sqlite3

# Подключение к БД
conn = sqlite3.connect('DBCVE.db')
cursor = conn.cursor()

# Ваш массив с компонентами
components = ['Компонент 1', 'Компонент 2', 'Компонент 3']

# Цикл запросов для каждого компонента
for component in components:
    query = f"SELECT CVE FROM CVE WHERE Компонент = '{component}'"
    cursor.execute(query)
    result = cursor.fetchall()
    print(component)
    print(result)
    print(f"Для компонента {component} значения CVE:", result)

# Закрытие соединения с БД