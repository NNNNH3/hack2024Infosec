
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.lang import Builder
import json
from telethon.sync import TelegramClient
from kivymd.app import MDApp
import sqlite3
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.popup import Popup

import uuid

from kivy.lang import Builder
import json
Builder.load_file("hack.kv")
conn = sqlite3.connect('DBCVE.db')
cursor = conn.cursor()
counter = 1
log_people = []
conn2 = sqlite3.connect('users.db')
cursor2 = conn2.cursor()
cursor2.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        email TEXT,
        password TEXT
    );
''')
with open('channel_posts1.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    components = [entry['component'] for entry in data]

Window.fullscreen = 'auto'
class AdminUserDB(Screen):
    def __init__(self, **kwargs):
        super(AdminUserDB, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.add_user_button = Button(text="Создать пользователя", size_hint=(None, None), size=(200, 50),
                                      pos_hint={"center_x": 0.5, "center_y": 0.8})
        self.add_user_button.bind(on_press=self.create_user_popup)
        self.layout.add_widget(self.add_user_button)

        self.edit_user_button = Button(text="Редактировать пользователя", size_hint=(None, None), size=(200, 50),
                                       pos_hint={"center_x": 0.5, "center_y": 0.6})
        self.edit_user_button.bind(on_press=self.edit_user_popup)
        self.layout.add_widget(self.edit_user_button)

        self.delete_user_button = Button(text="Удалить пользователя", size_hint=(None, None), size=(200, 50),
                                         pos_hint={"center_x": 0.5, "center_y": 0.4})
        self.delete_user_button.bind(on_press=self.delete_user_popup)
        self.layout.add_widget(self.delete_user_button)

        self.add_widget(self.layout)

    def create_user_popup(self, instance):
        content = BoxLayout(orientation='vertical')
        self.username_input = TextInput(hint_text="Логин", multiline=False)
        self.password_input = TextInput(hint_text="Пароль", multiline=False, password=True)
        self.create_button = Button(text="Создать")
        self.create_button.bind(on_press=self.create_user)
        content.add_widget(self.username_input)
        content.add_widget(self.password_input)
        content.add_widget(self.create_button)
        self.popup = Popup(title='Создать пользователя', content=content, size_hint=(None, None), size=(300, 200))
        self.popup.open()

    def create_user(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        if username and password:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            self.popup.dismiss()
        else:
            pass

    def edit_user_popup(self, instance):
        content = BoxLayout(orientation='vertical')
        self.username_input = TextInput(hint_text="Логин", multiline=False)
        self.password_input = TextInput(hint_text="Новый пароль", multiline=False, password=True)
        self.edit_button = Button(text="Редактировать")
        self.edit_button.bind(on_press=self.edit_user)
        content.add_widget(self.username_input)
        content.add_widget(self.password_input)
        content.add_widget(self.edit_button)
        self.popup = Popup(title='Редактировать пользователя', content=content, size_hint=(None, None), size=(300, 200))
        self.popup.open()

    def edit_user(self, instance):
        username = self.username_input.text
        new_password = self.password_input.text
        if username and new_password:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET password=? WHERE username=?", (new_password, username))
            conn.commit()
            conn.close()
            self.popup.dismiss()
        else:
            pass

    def delete_user_popup(self, instance):
        content = BoxLayout(orientation='vertical')
        self.username_input = TextInput(hint_text="Логин", multiline=False)
        self.delete_button = Button(text="Удалить")
        self.delete_button.bind(on_press=self.delete_user)
        content.add_widget(self.username_input)
        content.add_widget(self.delete_button)
        self.popup = Popup(title='Удалить пользователя', content=content, size_hint=(None, None), size=(300, 200))
        self.popup.open()

    def delete_user(self, instance):
        username = self.username_input.text
        if username:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE username=?", (username,))
            conn.commit()
            conn.close()
            self.popup.dismiss()
        else:
            pass
class AdminVulnerabilitiesDB(Screen):
    def __init__(self, **kwargs):
        super(AdminVulnerabilitiesDB, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')

        self.create_vulnerability_button = Button(text="Создать уязвимость", size_hint=(None, None), size=(200, 50),
                                         pos_hint={"center_x": 0.5, "center_y": 0.8})
        self.create_vulnerability_button.bind(on_press=self.create_vulnerability_popup)
        self.layout.add_widget(self.create_vulnerability_button)

        self.edit_vulnerability_button = Button(text="Редактировать уязвимость", size_hint=(None, None), size=(200, 50),
                                       pos_hint={"center_x": 0.5, "center_y": 0.6})
        self.edit_vulnerability_button.bind(on_press=self.edit_vulnerability_popup)
        self.layout.add_widget(self.edit_vulnerability_button)

        self.delete_vulnerability_button = Button(text="Удалить уязвимость", size_hint=(None, None), size=(200, 50),
                                         pos_hint={"center_x": 0.5, "center_y": 0.4})
        self.delete_vulnerability_button.bind(on_press=self.delete_vulnerability_popup)
        self.layout.add_widget(self.delete_vulnerability_button)

        self.add_widget(self.layout)

    def create_vulnerability_popup(self, instance):
        content = BoxLayout(orientation='vertical')
        self.vulnerability_number_input = TextInput(hint_text="Номер уязвимости", multiline=False)
        self.component_input = TextInput(hint_text="Компонент", multiline=False)
        self.description_input = TextInput(hint_text="Описание", multiline=True)
        self.create_button = Button(text="Создать")
        self.create_button.bind(on_press=self.create_vulnerability)
        content.add_widget(self.vulnerability_number_input)
        content.add_widget(self.component_input)
        content.add_widget(self.description_input)
        content.add_widget(self.create_button)
        self.popup = Popup(title='Создать уязвимость', content=content, size_hint=(None, None), size=(300, 200))
        self.popup.open()

    def create_vulnerability(self, instance):
        number = self.vulnerability_number_input.text
        component = self.component_input.text
        description = self.description_input.text
        if number and component and description:
            conn = sqlite3.connect('DBCVE.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO CVE (Номер_уязвимости, Компонент, Описание) VALUES (?, ?, ?)", (number, component, description))
            conn.commit()
            conn.close()
            self.popup.dismiss()
        else:
            pass

    def edit_vulnerability_popup(self, instance):
        content = BoxLayout(orientation='vertical')
        self.vulnerability_number_input = TextInput(hint_text="Номер уязвимости", multiline=False)
        self.component_input = TextInput(hint_text="Компонент", multiline=False)
        self.description_input = TextInput(hint_text="Новое описание", multiline=True)
        self.edit_button = Button(text="Редактировать")
        self.edit_button.bind(on_press=self.edit_vulnerability)
        content.add_widget(self.vulnerability_number_input)
        content.add_widget(self.component_input)
        content.add_widget(self.description_input)
        content.add_widget(self.edit_button)
        self.popup = Popup(title='Редактировать уязвимость', content=content, size_hint=(None, None), size=(300, 200))
        self.popup.open()

    def edit_vulnerability(self, instance):
        number = self.vulnerability_number_input.text
        component = self.component_input.text
        description = self.description_input.text
        if number and component and description:  # Проверяем, что все поля заполнены
            conn = sqlite3.connect('DBCVE.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE CVE SET Компонент=?, Описание=? WHERE Номер_уязвимости=?", (component, description, number))
            conn.commit()
            conn.close()
            self.popup.dismiss()
        else:
            pass

    def delete_vulnerability_popup(self, instance):
        content = BoxLayout(orientation='vertical')
        self.vulnerability_number_input = TextInput(hint_text="Номер уязвимости", multiline=False)
        self.delete_button = Button(text="Удалить")
        self.delete_button.bind(on_press=self.delete_vulnerability)
        content.add_widget(self.vulnerability_number_input)
        content.add_widget(self.delete_button)
        self.popup = Popup(title='Удалить уязвимость', content=content, size_hint=(None, None), size=(300, 200))
        self.popup.open()

    def delete_vulnerability(self, instance):
        number = self.vulnerability_number_input.text
        if number:
            conn = sqlite3.connect('DBCVE.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM CVE WHERE Номер_уязвимости=?", (number,))
            conn.commit()
            conn.close()
            self.popup.dismiss()
        else:
            pass

class First_Page(Screen):
    def __init__(self,**kwargs):
        super(First_Page,self).__init__(**kwargs)
    def swap_on_reg(self,*args):
        self.manager.current = 'register'
    def swap_on_sign_in(self,*args):
        self.manager.current = 'sign_in'
class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)
        label = Label(text="Регистрация пользователя", size_hint=(1, 0.1))
        self.layout.add_widget(label)
        self.username_input = TextInput(hint_text="Введите имя пользователя", multiline=False)
        self.layout.add_widget(self.username_input)
        self.email_input = TextInput(hint_text="Введите адрес электронной почты", multiline=False)
        self.layout.add_widget(self.email_input)
        self.password_input = TextInput(hint_text="Введите пароль", multiline=False, password=True)
        self.layout.add_widget(self.password_input)
        register_button = Button(text="Зарегистрироваться")
        register_button.bind(on_press=self.register_user)
        self.layout.add_widget(register_button)
    def register_user(self, instance):
        self.remove_widget(self.layout)
        self.remove_widget(self.username_input)
        self.remove_widget(self.email_input)
        self.remove_widget(self.password_input)
        self.res_name = (self.username_input).text
        self.res_email = (self.email_input).text
        self.res_password = (self.password_input).text
        cursor2.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (self.res_name, self.res_email, self.res_password))
        conn2.commit()
        conn2.close()

        self.second_button_press = Button(text='Перейти в главное меню',size_hint=(None, None), size=(200, 100),pos_hint={"center_x": 0.5, "center_y": 0.55}, on_press=self.swap_on_main_screen)
        self.add_widget(self.second_button_press)
        self.res_name = (self.username_input).text
        self.res_email = (self.email_input).text
        self.res_password = (self.password_input).text
        self.login_mass = [self.res_name, self.res_email, self.res_password]
    def swap_on_main_screen(self,*args):
        self.manager.current = 'main'
class Sign_In(Screen):
    def __init__(self,**kwargs):
        super(Sign_In,self).__init__(**kwargs)
        self.gig()
    def gig(self):
        self.email = TextInput(text="введите почту", multiline=False, size_hint=(None, None), size=(300, 50),
                               pos_hint={"center_x": 0.5, "center_y": 0.75})
        self.password = TextInput(text="введите пароль", multiline=False, size_hint=(None, None), size=(300, 50),
                                  pos_hint={"center_x": 0.5, "center_y": 0.55})
        self.sign_button = Button(text="войти", size_hint=(None, None), size=(200, 100),
                                  pos_hint={"center_x": 0.5, "center_y": 0.45}, on_press=self.proverka)
        self.add_widget(self.email)
        self.add_widget(self.password)
        self.add_widget(self.sign_button)

    def proverka(self, *args):
        text_email = self.email.text
        password = self.password.text

        if text_email == "admin" and password == "admin":
            self.manager.current = 'notif'
        else:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute("SELECT username, password FROM users WHERE username = ? AND password = ?",
                           (text_email, password))
            user = cursor.fetchone()
            conn.close()

            if user is None:
                error_pass_or_email = Label(text="Что-то введено неверно", pos_hint={"center_x": 0.5, "center_y": 0.4})
                self.add_widget(error_pass_or_email)
                self.gig()
            else:
                if text_email == user[0] and password == user[1]:
                    log_people.append(text_email)
                    self.manager.current = 'main'
                else:
                    error_pass_or_email = Label(text="Что-то введено неверно",
                                                pos_hint={"center_x": 0.5, "center_y": 0.4})
                    self.add_widget(error_pass_or_email)
                    self.gig()



class Main_Project(Screen):
    components = []
    def __init__(self, **kwargs):
        super(Main_Project, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.layout = BoxLayout(orientation='vertical',size_hint=(None, None), size=(200, 100),pos_hint={"center_x": 0.1, "center_y": 0.1})
        self.create_component_spinner()
        self.create_add_component_button()
        self.create_project_button()
        self.add_widget(self.layout)
        self.back = Button(text="назад", size_hint=(None, None), size=(200, 100),
                           pos_hint={"center_x": 0.75, "center_y": 0.95}, on_press=self.swap_on_project)

        self.add_widget(self.back)


    def swap_on_project(self, *args):
        self.manager.current = 'main'

    def create_component_spinner(self):
        self.component_spinners_layout = BoxLayout(orientation='vertical')
        self.layout.add_widget(self.component_spinners_layout)
        self.project_name = TextInput(text='введите название проекта', multiline=False,size_hint=(None, None), size=(200, 100),
                                      pos_hint={"center_x": 0.4, "center_y": 0.5})
        self.add_widget(self.project_name)
        self.add_component_spinner()
    def add_component_spinner(self, *args):
        component_spinner = Spinner(text='Выберите компонент', values=(components),size_hint=(None, None), size=(200, 100))
        self.component_spinners_layout.add_widget(component_spinner)

    def create_add_component_button(self):
        add_component_button = Button(text='Добавить компонент', size_hint=(None, None), size=(200, 100),
                                  pos_hint={"center_x": 0.9, "center_y": 0.1})
        add_component_button.bind(on_press=self.add_component_spinner)
        self.add_widget(add_component_button)
    def create_add_people_button(self):
        add_colab = TextInput(text='введите название проекта', multiline=False,size_hint=(None, None), size=(200, 100),pos_hint={"center_x": 0.9, "center_y": 0.9})
        add_component_button = Button(text='Добавить колаборатора', size_hint=(None, None), size=(200, 100),
                                  pos_hint={"center_x": 0.9, "center_y": 0.1})
        add_component_button.bind(on_press=self.add_component_spinner)
        self.add_widget(add_component_button)

    def create_project_button(self):
        create_project_button = Button(text='Создать проект', size_hint=(None, None), size=(200, 100),
                                  pos_hint={"center_x": 0.9, "center_y": 0.95})
        create_project_button.bind(on_press=self.create_project)
        self.add_widget(create_project_button)

    def create_project(self, *args):
        conn = sqlite3.connect('mydatabase.db')
        cursor = conn.cursor()
        self.components = []
        self.name_prod = self.project_name.text
        for component_spinner in self.component_spinners_layout.children:
            self.components.append(component_spinner.text)
        cursor.execute('''CREATE TABLE IF NOT EXISTS my_table
                        (num TEXT,id TEXT, variable TEXT, login TEXT, my_array TEXT)''')
        unique_id = str(uuid.uuid4())
        my_variable = self.name_prod
        my_login = str(log_people)
        my_array = str(self.components)
        cursor.execute("INSERT INTO my_table (id, variable, login, my_array) VALUES (?, ?, ?, ?)",
                       (unique_id, my_variable, my_login, str(my_array)))
        conn.commit()
        conn.close()
        self.cve_create()
    def cve_create(self):
        components = self.components
        print(components)
        cve_threats = []
        with open('channel_posts1.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        for component in components:
            for record in data:
                if record['component'] == component:
                    for threat in record['угроза']:
                        if "CVE" in threat:
                            cve_threats.append(threat)
        cve_text = str(cve_threats)
        print(cve_threats)
        self.cve_mass = Label(pos_hint={"center_x": 0.5, "center_y": 0.65},size_hint_y=None)
        self.cve_mass.text = cve_text
        self.cve_mass.bind(size=self.adjust_text_size)
        self.add_widget(self.cve_mass)
    def adjust_text_size(self, instance, size):
        instance.text_size = size



class MainPage(Screen):
    def __init__(self,**kwargs):
        super(MainPage, self).__init__(**kwargs)
        global log_people
        self.kent = log_people
        self.res()
    def res(self,*args):
        self.counter = 1
        conn = sqlite3.connect('mydatabase.db')
        cursor = conn.cursor()
        query = "SELECT variable FROM my_table WHERE login LIKE ?"
        cursor.execute(query, (f'%{self.kent}%',))
        projects = [row[0] for row in cursor.fetchall()]
        print(projects)
        conn.close()
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        # Добавляем кнопки для каждого проекта
        for self.project in projects:
            self.btn_text = Button(text=str(self.project), size_hint_y=None, height=40, on_press=self.pointer_page)
            layout.add_widget(self.btn_text)
            self.counter = self.counter + 1
        self.root = ScrollView(size_hint=(0.3, 0.7))
        self.root.add_widget(layout)
        self.add_widget(self.root)
        self.projects()
    def projects(self):
        self.text_main = Label(text='Мэин')
        self.project_page = Button(text='создать проект', on_press=self.swap_on_project, size_hint=(None, None),
                                   size=(200, 100), pos_hint={"center_x": 0.1, "center_y": 0.95})
        self.notifications = Button(text='уведомления', on_press=self.swap_on_notifications, size_hint=(None, None),
                                    size=(200, 100), pos_hint={"center_x": 0.3, "center_y": 0.95})
        self.export = Button(text='парсинг(не жмякать)', on_press=self.swap_on_project, size_hint=(None, None), size=(200, 100),
                             pos_hint={"center_x": 0.5, "center_y": 0.95})
        self.proj = Button(text='окно проектов', on_press=self.res, size_hint=(None, None), size=(200, 100),
                             pos_hint={"center_x": 0.7, "center_y": 0.95})
        self.add_widget(self.text_main)
        self.add_widget(self.project_page)
        self.add_widget(self.notifications)
        self.add_widget(self.export)
        self.add_widget(self.proj)

    def pointer_page(self,*args):
        self.remove_widget(self.root)
        self.remove_widget(self.text_main)
        self.remove_widget(self.project_page)
        self.remove_widget(self.notifications)
        self.remove_widget(self.export)
        print(self.counter)

    def swap_on_project(self,*args):
        self.manager.current = "project"
    def swap_on_notifications(self,*args):
        self.manager.current = "notif"
    def swap_on_export(self,*args):
        #просьба не пользоваться это функцией,банит тг акк
        api_id = #ID 
        api_hash = '#HASH'
        phone_number = '#NUMBER'

        # Создаем клиента Telegram
        client = TelegramClient('session_name', api_id, api_hash)

        async def main():
            client.start(phone_number)

            channel_username = '#ссылка на тг канал'
            channel_entity = await client.get_entity(channel_username)
            posts = []
            async for message in client.iter_messages(channel_entity):
                post = {
                    'id': message.id,
                    'text': message.text,
                    'date': str(message.date),
                    'views': message.views,
                }
                posts.append(post)
            with open('channel_posts.json', 'w', encoding='utf-8') as json_file:
                json.dump(posts, json_file, ensure_ascii=False, indent=4)

class Notifications(Screen):
    def __init__(self,**kwargs):
        super(Notifications, self).__init__(**kwargs)
        mass_cve_name=[]
        mass_cve_kol = []
        with open('channel_posts (1).json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        trigger_words = components
        triggered_word_ids = {word: [] for word in trigger_words}
        trigger_words = components

        triggered_word_ids = {word: [] for word in trigger_words}

        for item in data:
            for words in trigger_words:
                if words in item['text']:
                    triggered_word_ids[words].append(item['id'])


        for word, ids in triggered_word_ids.items():
            print(f'Для триггер-слова "{word}" найдены ID: {ids}')
            length = len(triggered_word_ids[word])
            name = list(triggered_word_ids.keys())
            mass_cve_kol.append(length)
            mass_cve_name.append(name)
        print(mass_cve_kol)
        flat_list = mass_cve_name[0]
        print(flat_list)
        print(triggered_word_ids)
        self.trigger_words = triggered_word_ids
        conn = sqlite3.connect('info_new_old.db')
        cursor = conn.cursor()
        for i, value in enumerate(mass_cve_kol, start=1):
            cursor.execute("UPDATE mytable SET New_Year = ? WHERE RowID = ?", (value, i))
        conn.commit()
        conn.close()
        self.button_res = Button(text="новости",size_hint=(None, None), size=(200, 100),
                             pos_hint={"center_x": 0.5, "center_y": 0.95},on_press=self.cabinet)
        self.back = Button(text="назад",size_hint=(None, None), size=(200, 100),
                             pos_hint={"center_x": 0.9, "center_y": 0.95},on_press =self.swap_on_project)

        self.add_widget(self.back)
        self.add_widget(self.button_res)
        self.new_data()
    def swap_on_project(self,*args):
        self.manager.current = 'main'
    def new_data(self):
        mass_ib = []
        conn = sqlite3.connect('info_new_old.db')
        cursor = conn.cursor()
        cursor.execute('SELECT New_Year, Year FROM mytable')
        rows = cursor.fetchall()

        results = []
        for row in rows:
            result = row[0] - row[1]
            results.append(result)

        print(results)
        conn.close()


        print(results)
        conn.close()


        for key, value in self.trigger_words.items():
            length = min(len(value), results.pop(0))
            self.trigger_words[key] = value[:length]
        print("епта")
        print(self.trigger_words)
        self.values_array = [value for values in self.trigger_words.values() for value in values]
        with open('channel_posts (1).json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        results = []

        for item in data:
            if item['id'] in self.values_array:
                text = item['text']
                first_sentence = text.split('.')[0]
                cve_start = text.find('CVE-')
                cve = text[cve_start: text.find('`', cve_start)]
                result = {
                    'id': item['id'],
                    'first_sentence': first_sentence,
                    'CVE': cve
                }
                results.append(result)
        print(results)
        self.kris_label=results
    def cabinet(self,*args):
        layout = GridLayout(cols=1,spacing=100, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        for item in self.kris_label:
            self.nicname = Label(text=f"CVE: {item['CVE']}")
            self.bonjur = Label(text=f"first_sentence: {item['first_sentence']}")
            layout.add_widget(self.nicname)
            layout.add_widget(self.bonjur)
        self.root = ScrollView(size_hint=(1, 0.7))
        self.root.add_widget(layout)
        self.add_widget(self.root)
    def back(self,*args):
        self.manager.current = "main"
    def open_user_db(self, instance):
        self.manager.current = 'admin_user_db'

    def open_component_db(self, instance):
        self.manager.current = 'admin_vulnerabilities_db'
class RegisterApp(MDApp):
    def build(self):
        self.sm = ScreenManager()
        self.screen1 = First_Page(name='first')
        self.screen2 =RegisterScreen(name='register')
        self.screen3 = MainPage(name="main")
        self.screen4 = Main_Project(name = "project")
        self.screen5 = Sign_In(name="sign_in")
        self.screen6 =Notifications(name = "notif")
        self.sm.add_widget(self.screen1)
        self.sm.add_widget(self.screen2)
        self.sm.add_widget(self.screen3)
        self.sm.add_widget(self.screen4)
        self.sm.add_widget(self.screen5)
        self.sm.add_widget(self.screen6)
        self.sm.add_widget(AdminUserDB(name='admin_user_db'))
        self.sm.add_widget(AdminVulnerabilitiesDB(name='admin_vulnerabilities_db'))
        return self.sm

if __name__ == '__main__':
    RegisterApp().run()
