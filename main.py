from kivy.app import App
from os.path import dirname, join
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ListProperty, ObjectProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout
from kivy.config import Config
Config.set('graphics', 'resizable', True)

import requests
import json
import pandas as pd

class PopupWindow(Widget):
  def btn(self):
    popFun()

class P(FloatLayout):
  pass

def popFun():
  show = P()
  window = Popup(title = "popup", content = show, size_hint = (None, None), size = (300, 300))
  window.open()

class HomeScreen(Screen):
  pass

class SignupScreen(Screen):
	name2 = ObjectProperty(None)
	email = ObjectProperty(None)
	pwd = ObjectProperty(None)
	def signupbtn(self):
		# creating a DataFrame of the info
		user = pd.DataFrame([[self.name2.text, self.email.text, self.pwd.text]], columns = ['Name', 'Email', 'Password'])
		if self.email.text != "":
			if self.email.text not in users['Email'].unique():
				# if email does not exist already then append to the csv file
				# change current screen to log in the user now 
				user.to_csv('login.csv', mode = 'a', header = False, index = False)
				sm.current = 'login'
				self.name2.text = ""
				self.email.text = ""
				self.pwd.text = ""
		else:
      # if values are empty or invalid show pop up
			popFun()

class LoginScreen(Screen):
	email = ObjectProperty(None)
	pwd = ObjectProperty(None)
	def validate(self):
	
		# validating if the email already exists 
		if self.email.text not in users['Email'].unique():
			popFun()
		else: 
			# switching the current screen to display validation result
			sm.current = 'logdata'

			# reset TextInput widget
			self.email.text = ""
			self.pwd.text = ""

class LogDataWindow(Screen):
  pass

class windowManager(ScreenManager):
  pass

class CardScreen(Screen):
	pass

class CoinScreen(Screen):
  pass

class StackLayoutApp(App):
		 
	def build(self):
	
		SL = StackLayout(orientation ='lr-bt')

		# Creating Multiple Buttons
		btn1 = Button(text ="Home", font_size = 20, background_normal = 'home.png', size_hint =(.2, .1))
		btn2 = Button(text ="Funding", font_size = 20, size_hint =(.2, .1))
		btn3 = Button(text ="Add", font_size = 20, size_hint =(.2, .1))
		btn4 = Button(text ="Interests", font_size = 20, size_hint =(.2, .1))
		btn5 = Button(text ="More", font_size = 20, size_hint =(.2, .1))

		# adding widgets
		SL.add_widget(btn1)
		SL.add_widget(btn2)
		SL.add_widget(btn3)
		SL.add_widget(btn4)
		SL.add_widget(btn5)

		# returning widgets
		return SL


#GUI = Builder.load_file("main.kv") #interface file
class MainApp(App): #inheriting kivy's app

	user_id = 1
	
	def build(self):
		return GUI
	
	def on_start(self):
		res = requests.get("https://carecoin-59e57-default-rtdb.firebaseio.com/" + str(self.user_id) + '.json')
		data = json.loads(res.content.decode())
		#print(data)
		coins = data['Change']
		#print('$' + str(coins))
	
	def change_screen(self, screen_name):
		screen_manager = self.root.ids["screen_manager"]
		screen_manager.current = screen_name

# kv file
kv = Builder.load_file('main.kv')
sm = windowManager()
  
# reading all the data stored
users=pd.read_csv('login.csv')
  
# adding screens
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(SignupScreen(name='signup'))
sm.add_widget(LogDataWindow(name='logdata'))
  
# class that builds gui
class loginMain(App):
  def build(self):
    return sm

if __name__ == '__main__':
	#MainApp().run()
	loginMain().run()
  #StackLayoutApp().run()