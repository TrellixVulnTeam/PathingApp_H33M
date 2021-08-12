
from kivy.config import Config
Config.set("graphics","width","340")
Config.set("graphics","hight","640")

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.lang.builder import Builder
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
		user_data = pd.read_csv("Data_FIle.csv")
		
		if self.username.text not in user_data['Username'].unique():
			validation_popup()
			print("RAN")
		else:
			MDApp.get_running_app().root.current = "menu"
			self.username.text = ""
			self.password.text = ""


class SignUpScreen(Screen):
	name2 = ObjectProperty(None)
	username = ObjectProperty(None)
	password = ObjectProperty(None)

	def Signing_up(self):
		user_data = pd.read_csv("Data_FIle.csv")

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
	pass

class Main(ScreenManager):
	pass

sm = Main()

class MainApp(MDApp):

    def build(self):
        self.theme_cls.theme_style='Dark'
        return Builder.load_file('main.kv')


        
if __name__ == '__main__':
    MainApp().run()
