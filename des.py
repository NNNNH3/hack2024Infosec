import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.uix.spinner import Spinner
from kivy.lang import Builder
import sqlite3
from kivy.core.window import Window
import uuid
conn = sqlite3.connect('DBCVE.db')
cursor = conn.cursor()

log_people = [""]
cursor.execute("SELECT Компонент FROM CVE")
components = [row[0] for row in cursor.fetchall()]
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
Window.fullscreen = 'auto'
class First_Page(Screen):
    def __init__(self,**kwargs):
        super(First_Page,self).__init__(**kwargs)
        self.reg_button = Button(text="Регистрация",size_hint=(None, None), size=(200, 100),pos_hint={"center_x": 0.9, "center_y": 0.95},on_press=self.swap_on_reg)
        self.sign_in = Button(text="войти",size_hint=(None, None), size=(200, 100),pos_hint={"center_x": 0.78, "center_y": 0.95},on_press=self.swap_on_sign_in)
        self.add_widget(self.reg_button)
        self.add_widget(self.sign_in)
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

        self.second_button_press = Button(text='Перейти на второй экран',size_hint=(None, None), size=(200, 100), on_press=self.swap_on_main_screen)
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

    def proverka(self,*args):
        self.text_email = self.email.text
        self.password = self.password.text
        print(self.text_email)
        print(self.password)
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT username, password FROM users WHERE username = ? AND password = ?", (self.text_email, self.password))
        user = cursor.fetchone()
        print(user)
        print(type(user))
        if user ==None:
            self.error_pass_or_email = Label(text="Что-то введено неверно", pos_hint={"center_x": 0.5, "center_y": 0.4})
            self.add_widget(self.error_pass_or_email)
            self.gig()
        else:
            if self.text_email == user[0] and self.password == user[1]:
                conn.close()
                log_people.append(self.text_email)
                self.manager.current = 'main'
            else:
                self.error_pass_or_email = Label(text="Что-то введено неверно",
                                                 pos_hint={"center_x": 0.5, "center_y": 0.4})
                self.add_widget(self.error_pass_or_email)
                self.gig()




class Main_Project(Screen):
    components = []
    def __init__(self, **kwargs):
        super(Main_Project, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.layout = BoxLayout(orientation='vertical')
        self.create_component_spinner()
        self.create_add_component_button()
        self.create_project_button()
        self.add_widget(self.layout)

    def create_component_spinner(self):
        self.component_spinners_layout = BoxLayout(orientation='vertical')
        self.layout.add_widget(self.component_spinners_layout)
        self.project_name = TextInput(text='введите название проекта', multiline=False,size_hint=(None, None), size=(200, 100),
                                      pos_hint={"center_x": 0.4, "center_y": 0.5})
        self.add_widget(self.project_name)
        self.add_component_spinner()
    def add_component_spinner(self, *args):
        component_spinner = Spinner(text='Выберите компонент', values=(components),size_hint=(None, None), size=(200, 100),pos_hint={"center_x": 0.1, "center_y": 0.9})
        self.component_spinners_layout.add_widget(component_spinner)

    def create_add_component_button(self):
        add_component_button = Button(text='Добавить компонент', size_hint=(None, None), size=(200, 100),
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
                        (id TEXT, variable TEXT, login TEXT, my_array TEXT)''')
        unique_id = str(uuid.uuid4())
        my_variable = self.name_prod
        my_login = str(log_people)
        my_array = str(self.components)
        cursor.execute("INSERT INTO my_table (id, variable, login, my_array) VALUES (?, ?, ?, ?)",
                       (unique_id, my_variable, my_login, str(my_array)))
        conn.commit()
        conn.close()




class MainPage(Screen):
    def __init__(self,**kwargs):
        super(MainPage, self).__init__(**kwargs)
        self.text_main= Label(text='Мэин')
        self.add_widget(self.text_main)
        self.cont_page = Button(text='создрать проект',on_press=self.swap_on_project)
        self.add_widget(self.cont_page)

    def swap_on_project(self,*args):
        self.manager.current = "project"

class RegisterApp(App):
    def build(self):
        self.sm = ScreenManager()
        screen1 = First_Page(name='first')
        screen2 =RegisterScreen(name='register')
        screen3 = MainPage(name="main")
        screen4 = Main_Project(name = "project")
        screen5 = Sign_In(name="sign_in")
        self.sm.add_widget(screen1)
        self.sm.add_widget(screen2)
        self.sm.add_widget(screen3)
        self.sm.add_widget(screen4)
        self.sm.add_widget(screen5)
        return self.sm

if __name__ == '__main__':
    RegisterApp().run()
