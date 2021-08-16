
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
import os

class NotValid(FloatLayout):
	pass

# validation popup contents comes from the .kv file just a label saying to enter valid info
def validation_popup():
	showNotValid = NotValid()
	pop_window = Popup(title = "popup", content = showNotValid, size_hint=(None,None), size=(300,300))
	pop_window.open()

class LoginScreen(Screen):
	# object properties for username and password so i can use the entered info from the .kv file
	username = ObjectProperty(None)
	password = ObjectProperty(None)
	def validation(self):
		user_data = pd.read_csv("Data_File.csv") #called in file that stores passwords and usernames
		
		if self.username.text not in user_data['Username'].unique(): #validating that username exists
			validation_popup()
		else:
			MDApp.get_running_app().root.current = "menu"
			#self.username.text = ""
			self.password.text = ""


class SignUpScreen(Screen):
	# object properties for username and password so i can use the entered info from the .kv file
	name2 = ObjectProperty(None)
	username = ObjectProperty(None)
	password = ObjectProperty(None)

	def Signing_up(self):
		user_data = pd.read_csv("Data_File.csv")#called in file that stores passwords and usernames

		#storing data in correct layout to the .csv file
		user_data_format = pd.DataFrame([[self.name2.text, self.username.text, self.password.text]],columns = ['Name', 'Username', 'Password'])

		if self.username.text != "" and self.username.text not in user_data["Username"].unique():
			user_data_format.to_csv("Data_FIle.csv", mode = "a", header = False, index = False)
			MDApp.get_running_app().root.current = "login"
			self.name2.text = ""
			self.username.text = ""
			self.password.text = ""

		else:
			validation_popup()

# screen that contains data for the user to read/learn
class FirstScreen(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.showtext

	def showtext(self):
		with open("Basics.txt","r") as f:
			return(f.read())

# screen that contains the test
class SecondScreen(Screen):
	this = ObjectProperty()
	answer = ObjectProperty()
	questions = []
	answers = []
	count = 0
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.question_get

	def show_question(self):
		self.this.text = str(self.questions[self.count]) + " " + (self.answers[self.count])

	def add(self):
		self.count = self.count + 1

	def question_get(self):
		with open("Words.txt", "r") as filestream:
			for line in filestream:
				currentline = line.split(",")
				self.questions.append(currentline[0])
				self.answers.append(currentline[1])
			self.show_question()

# main screen	
class Menu(Screen):
	textInput = ObjectProperty()
	fileName = ObjectProperty()
	File_Path = ""

	# initalising thr file manager
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		Window.bind(on_keyboard=self.events)
		self.manager_open = False
		self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
        )

		# builder for the .kv file
	def build(self):
		return Builder.load_string(KV)

	#open file manager
	def file_manager_open(self):
		self.file_manager.show('/') 
		self.manager_open = True

	# gets paths and opens it if it is a .txt file
	def select_path(self, path):
		self.exit_manager()
		self.File_Path = str(path)

		if self.File_Path[-4:] == ".txt":
			f = open(self.File_Path,"r")
			self.textInput.text =  f.read()
			Get_File_Name = os.path.basename(self.File_Path)
			self.fileName.text = Get_File_Name

		else:
			self.on_save_as()

	# saves file if it does not exist then roots to save as
	def on_save(self, *args):
		if self.File_Path == "":
			self.on_save_as()
		else:
			f = open(self.File_Path,'w')
			f.write(self.textInput.text)
			f.close()
	# creates and save the new file as a .txt file
	def on_save_as(self):
		Directory = str(self.File_Path)
		txt = str(self.fileName.text)
		if self.File_Path == "":
			self.file_manager_open()
		if self.fileName.text != "" and self.File_Path != "":

			if txt[-4:] != ".txt":
				addtxt = ".txt"
				addedtxt = txt + addtxt
				saveDirectory = Directory + "\\" + addedtxt

				f = open(saveDirectory,"w+")
				f.write(self.textInput.text)

			if txt[-4:] == ".txt":
				saveDirectory = Directory + "\\" + txt
				f = open(saveDirectory,"w+")
				f.write(self.textInput.text)

			else:
				validation_popup()
				self.exit_manager()

		elif self.fileName.text == "" and self.File_Path != "":
			validation_popup()



	def Clear(self):
		self.textInput.text = ""


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
