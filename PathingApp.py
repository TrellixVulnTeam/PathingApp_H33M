
from kivy.config import Config
Config.set("graphics","width","340")
Config.set("graphics","hight","640")

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivymd.uix.filemanager import MDFileManager
from kivy.lang.builder import Builder

from kivy.core.window import Window

import pandas as pd


class NotValid(FloatLayout):
	pass

def validation_popup():
	showNotValid = NotValid()
	pop_window = Popup(title = "popup", content = showNotValid, size_hint=(None,None), size=(300,300))
	pop_window.open()

class LoginScreen(Screen):
	username = ObjectProperty(None)
	password = ObjectProperty(None)
	def validation(self):
		user_data = pd.read_csv("Data_File.csv")
		
		if self.username.text not in user_data['Username'].unique():
			validation_popup()
		else:
			MDApp.get_running_app().root.current = "menu"
			#self.username.text = ""
			self.password.text = ""


class SignUpScreen(Screen):
	name2 = ObjectProperty(None)
	username = ObjectProperty(None)
	password = ObjectProperty(None)

	def Signing_up(self):
		user_data = pd.read_csv("Data_File.csv")

		user_data_format = pd.DataFrame([[self.name2.text, self.username.text, self.password.text]],columns = ['Name', 'Username', 'Password'])

		if self.username.text != "" and self.username.text not in user_data["Username"].unique():
			user_data_format.to_csv("Data_FIle.csv", mode = "a", header = False, index = False)
			MDApp.get_running_app().root.current = "login"
			self.name2.text = ""
			self.username.text = ""
			self.password.text = ""

		else:
			print("RAN")
			validation_popup()


class FirstScreen(Screen):
	pass

class SecondScreen(Screen):
	pass
		
class ThirdScreen(Screen):
	pass
		
class Menu(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		Window.bind(on_keyboard=self.events)
		self.manager_open = False
		self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
        )

	def build(self):
		return Builder.load_string(KV)

	def file_manager_open(self):
		self.file_manager.show('/') 
		self.manager_open = True

	def select_path(self, path):
		self.exit_manager()
		print(path)

	def exit_manager(self, *args):


		self.manager_open = False
		self.file_manager.close()

	def events(self, instance, keyboard, keycode, text, modifiers):


		if keyboard in (1001, 27):
			if self.manager_open:
				self.file_manager.back()
		return True


class Main(ScreenManager):
	pass


class MainApp(MDApp):

	def build(self):
		self.theme_cls.theme_style='Dark'
		Builder.load_file('main.kv')




if __name__ == '__main__':
    MainApp().run()
