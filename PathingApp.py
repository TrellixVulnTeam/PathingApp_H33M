
from kivy.config import Config
Config.set("graphics","width","340")
Config.set("graphics","hight","640")

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang.builder import Builder

class LoginScreen(Screen):
	pass

class FirstScreen(Screen):
	pass

class SecondScreen(Screen):
	pass
		
class ThirdScreen(Screen):
	pass

class FourthScreen(Screen):
	pass

class FithScreen(Screen):
	pass
		
class SixthScreen(Screen):
	pass
		
class Menu(Screen):
	pass

class Main(ScreenManager):
	pass

class MainApp(MDApp):

    def build(self):
        self.theme_cls.theme_style='Dark'
        return Builder.load_file('main.kv')


        
if __name__ == '__main__':
    MainApp().run()
