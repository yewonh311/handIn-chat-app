from kivymd.app import MDApp
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import TwoLineAvatarIconListItem, ImageLeftWidget, MDList
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.clock import Clock
import requests

import firebase_admin
from firebase_admin import auth, credentials
import pyrebase

import client
import socket

firebaseConfig = {"apiKey": "AIzaSyB6RtVkvyJ8QB8oWCsQh5Xc39ad3z6hhto",
                  "authDomain": "chat-ffedf.firebaseapp.com",
                  "databaseURL": "https://chat-ffedf-default-rtdb.firebaseio.com",
                  "projectId": "chat-ffedf",
                  "storageBucket": "chat-ffedf.appspot.com",
                  "messagingSenderId": "606774165463",
                  "appId": "1:606774165463:web:1a220914726a8b31619592",
                  "measurementId": "G-E08ZC3KBZF"}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
au = firebase.auth()
cred = credentials.Certificate(
    '/Users/yewonhong/Downloads/chat-ffedf-firebase-adminsdk-uwhds-8c95ee14ea.json')
firebase_admin.initialize_app(cred)


class LoginScreen(BoxLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

    def connect(self, _):
        email = self.ids.em_field.text
        user_email = auth.get_user_by_email(email)
        uid = user_email.uid
        name = db.child('users').child(uid).get().val()['name']
        # IP = "172.20.10.2"
        # socket.gethostbyname(socket.gethostname())
        # PORT = 8080
        if not client.conn(name, show_error):
            return
        Clock.schedule_once(self.connect, 1)
        # print("connected")
        # app.Closed()

    def validate_user(self):

        if self.ids.em_field.text == '' or self.ids.pw_field.text == '':
            self.ids.info.text = '[color=#FF0000]Username and/or Password required[/color]'
        else:
            try:
                au.sign_in_with_email_and_password(
                    self.ids.em_field.text, self.ids.pw_field.text)
                Clock.schedule_once(self.connect, 1)
                self.ids.info.text = ''
                chat_app.goto_main(dire="left")
            except:
                self.ids.info.text = '[color=#FF0000]Invalid Username and/or Password[/color]'


class SignUpScreen(BoxLayout):

    def __init__(self, **kwargs):
        super(SignUpScreen, self).__init__(**kwargs)

    def signup(self):

        if self.ids.su_em_field.text == '':
            self.ids.info_signup.text = '[color=#FF0000]Please enter email[/color]'
        elif self.ids.su_n_field.text == '':
            self.ids.info_signup.text = '[color=#FF0000]Please enter name[/color]'
        elif self.ids.su_pw_field.text == '':
            self.ids.info_signup.text = '[color=#FF0000]Please enter password[/color]'
        else:
            try:
                user = auth.create_user(
                    email=self.ids.su_em_field.text, password=self.ids.su_pw_field.text)
                uid = user.uid
                data = {'name': self.ids.su_n_field.text,
                        'email': self.ids.su_em_field.text}
                db.child("users").child(uid).set(data)
                self.ids.info_signup.text = '[color=#0000FF]Account created[/color]'

            except:
                self.ids.info_signup.text = '[color=#FF0000]Invalid email address or Already exist[/color]'


class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.my_message("YEWON", "Hello! How's going?", "yewon2.png")
        self.my_profile("Yewon Hong",
                        "Hello My name is Yewon", "yewon.png", )

    def my_message(self, name, message, image_name):
        self.ids.chat_list.text = name
        self.ids.chat_list.secondary_text = message
        self.ids.chat_list.add_widget(ImageLeftWidget(source=image_name))

    def my_profile(self, name, bio, image_name):
        self.ids.contact_list.text = name
        self.ids.contact_list.secondary_text = bio
        self.ids.contact_list.add_widget(ImageLeftWidget(source=image_name))


class FriendsList(BoxLayout):
    def __init__(self, **kwargs):
        super(FriendsList, self).__init__(
            item_strings=[str(index) for index in range(100)])

    def new_friend(self):
        screen = MainScreen()
        list_view = MDList()
        scroll = ScrollView()

        for i in range(20):
            new_friend = TwoLineAvatarIconListItem(
                text='friend '+str(i) + name, secondary_text=bio, source=image_name)

        list_view.add_widget(new_friend)
        screen.add_widget(scroll)
        return screen

    def on_tab_switch(
        self, instance_tabs, instance_tab, instance_tab_label, tab_text
    ):
        # instance_tab.ids.label.text = tab_text
        pass


class Tab(FloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''


class ChatScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(ChatScreen, self).__init__(**kwargs)

    def send_msg(self):
        msg = self.ids.message.text
        # self.ids.chat_logs.text += ('\nsays: %s' %
        #                             (msg))
        self.ids.chat_logs.text += '\n' + msg
        self.ids.message.text = ''
        # client.send(msg)


class ContactScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(ContactScreen, self).__init__(**kwargs)

    def popup1(self):
        box = BoxLayout(orientation='vertical', padding=(10))
        box.add_widget(Label(text="Are you sure delete this friend?"))
        popup = Popup(title='Check if Correct', title_size=(30),
                      title_align='center', content=box,
                      size_hint=(None, None), size=(500, 500),
                      auto_dismiss=True)
        box.add_widget(Button(text="YES to delete", ))
        box.add_widget(Button(text="NO to go back", on_press=popup.dismiss))
        popup.open()

    # def delete_friend(self, instance):


class AddScreen(BoxLayout):

    def __init__(self, **kwargs):
        super(AddScreen, self).__init__(**kwargs)
        self.ids.f_em_field.text = ""
        self.ids.f_n_field.text = ""
        self.ids.info_friend.text = ""

    def find_by_name(self):
        pass

    def add_friend(self):
        if self.ids.f_em_field.text:
            try:
                if auth.get_user_by_email(self.ids.f_em_field.text):
                    self.ids.info_friend.text = ''
                    box = BoxLayout(orientation='horizontal', padding=(10))
                    popup = Popup(title="Is this your friend?", title_size=(20),
                                  title_color=(.3, .8, .8, 1), title_align='center',
                                  content=box, size_hint=(.4, .25),
                                  background_color=(255, 255, 255, 1), auto_dismiss=True)
                    box.add_widget(Button(text="YES", background_color=(.3, .8, .8, 1), on_release=root.new_freind,
                                          background_normal=''))

                    box.add_widget(Button(text="NO to go back", background_color=(.3, .8, .8, 1),
                                          on_release=popup.dismiss, background_normal=''))
                    popup.open()
            except:
                self.ids.info_friend.text = f'[color=#FF0000] The email address "{self.ids.f_em_field.text}" does not exist.[/color]'
        elif self.ids.f_n_field.text:
            user = db.child('users').get()
            for users in user.each():
                uid = users.key()
                name = db.child('users').child(uid).get().val()['name']
                email_by_name = db.child('users').child(
                    uid).get().val()['email']
                if name == self.ids.f_n_field.text:
                    self.ids.info_friend.text = ''
                    print(email_by_name)
                else:
                    self.ids.info_friend.text = f'[color=#FF0000]The name "{self.ids.f_n_field.text}" does not exist.[/color]'
        else:
            self.ids.info_friend.text = '[color=#FF0000]Please enter email or name to add.[/color]'


class ChatApp(MDApp):

    def build(self):
        self.sm = ScreenManager()

        self.login_screen = LoginScreen()
        screen = Screen(name='login')
        screen.add_widget(self.login_screen)
        self.sm.add_widget(screen)

        self.signup_screen = SignUpScreen()
        screen = Screen(name='signup')
        screen.add_widget(self.signup_screen)
        self.sm.add_widget(screen)

        self.main_screen = MainScreen()
        screen = Screen(name='main')
        screen.add_widget(self.main_screen)
        self.sm.add_widget(screen)

        self.contact_screen = ContactScreen()
        screen = Screen(name="contact")
        screen.add_widget(self.contact_screen)
        self.sm.add_widget(screen)

        self.add_screen = AddScreen()
        screen = Screen(name="addfriend")
        screen.add_widget(self.add_screen)
        self.sm.add_widget(screen)

        self.chat_screen = ChatScreen()
        screen = Screen(name="chatroom")
        screen.add_widget(self.chat_screen)
        self.sm.add_widget(screen)

        return self.sm

    def goto_signup(self, dire):
        chat_app.sm.transition.direction = dire
        chat_app.sm.current = 'signup'
        self.login_screen.ids.em_field.text = ''
        self.login_screen.ids.pw_field.text = ''
        self.login_screen.ids.info.text = ''

    def goto_login(self, dire):
        chat_app.sm.transition.direction = dire
        chat_app.sm.current = 'login'
        self.signup_screen.ids.su_em_field.text = ""
        self.signup_screen.ids.su_n_field.text = ""
        self.signup_screen.ids.su_pw_field.text = ""
        self.signup_screen.ids.info_signup.text = ""

    def goto_chatroom(self, dire):
        chat_app.sm.transition.direction = dire
        chat_app.sm.current = "chatroom"

    def goto_contact(self, dire):
        chat_app.sm.transition.direction = dire
        chat_app.sm.current = "contact"

    def goto_addfriend(self, dire):
        chat_app.sm.transition.direction = dire
        chat_app.sm.current = "addfriend"

    def goto_main(self, dire):
        chat_app.sm.transition.direction = dire
        chat_app.sm.current = "main"


def show_error(message):
    pass


if __name__ == '__main__':
    chat_app = ChatApp()
    chat_app.run()
