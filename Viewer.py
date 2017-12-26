from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, StringProperty
from kivy.uix.label import Label
import os
import json


#All stories should be stored in this single directory with first character not a dot (".").
#By default it is assumed that the script is stored in the story folder.
#This is the directory that contains the story, not the story directory itself!!! There can be multiple stories in the same directory
storyDir = "./"

class RootWidget(BoxLayout):
	storyLocation = StringProperty("./")
	def __init__(self, **kwargs):
		self.storyLocation=kwargs.pop("storyDir", "./")
		if self.storyLocation[-1]!="/":
			self.storyLocation+="/"

		super(RootWidget, self).__init__(orientation="vertical",**kwargs)

		self.storyText = Label(text="Choose a story from the list below", font_size=50)
		self.add_widget(self.storyText)

		self.buttons = BoxLayout(orientation="vertical")
		self.add_widget(self.buttons)

		self.bind(storyLocation=self.update)

		self.updateButtons()

	def update(self, *unused):
		self.updateText()
		self.updateButtons()

	def updateButtons(self):
		print(self.storyLocation)
		folders = [f for f in os.listdir(self.storyLocation) if (not os.path.isfile(self.storyLocation+f))]
		print(folders)
		elements = list(filter(lambda s: s[0]!='.', folders))
		print(elements)
		self.buttons.clear_widgets()
		for i in elements:
			print(i+" asdjadjka")
			btn = Button(text=i)
			btn.bind(on_press=self.btn_pressed)
			self.buttons.add_widget(btn)
		print(self.buttons)

	def updateText(self):
		gamestate=json.load(open(self.storyLocation+"gamestate.json"))
		print(gamestate)
		self.storyText.text=gamestate["text"]
		self.storyText.font_size=20

	def btn_pressed(self, instance):
		self.storyLocation+=instance.text+"/"
		self.update()



class StoryApp(App):

	def build(self):
		return RootWidget(storyDir=storyDir)


if __name__ == '__main__':
	StoryApp().run()

#Encapsules a choice and 
# class ChoiceButton(Button):
# 		print ('pressed at {pos}'.format(pos=pos))

# 	def __init__(self, choice, **kwargs):



# Ideas
# Add the ability to list all characters
# Keep a list of participating characters in a block for easier reference

# TODO
# Add custom storyLocation option
# Fix button size
# Experiment with different button formats