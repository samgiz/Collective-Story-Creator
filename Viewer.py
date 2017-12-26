from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, StringProperty, ObjectProperty
from kivy.uix.label import Label
import os
import json
import types

#All stories should be stored in this single directory with first character not a dot (".").

#This is the directory that contains the story. You may change it.
storyDir = "./ExampleStory/"

#For simplicity the starting screen has been removed. You have to manually add the required 

# gamestate = {
#  choices = [a, b, c, d] (ids and texts of choices?)
#  storyText = String
#  
# }


# choice 


class RootWidget(BoxLayout):
	storyLocation = StringProperty("./")
	gameState = ObjectProperty({})
	options = ObjectProperty({})

	def __init__(self, **kwargs):
		self.storyLocation=kwargs.pop("storyDir", "./")
		if self.storyLocation[-1]!="/":
			self.storyLocation+="/"

		super(RootWidget, self).__init__(orientation="vertical",**kwargs)

		self.storyText = Label(text="Choose a story from the list below", font_size=50)
		self.add_widget(self.storyText)

		self.options = json.load(open(self.storyLocation+"options.json"))
		
		self.gameState = json.load(open(self.storyLocation+"Story/"+str(self.options["startId"])+".json"))
		self.bind(gameState=self.update)

		self.buttons = BoxLayout(orientation="vertical")
		self.add_widget(self.buttons)

		self.update()
	

	def update(self, *ignore):
		self.buttons.clear_widgets()
		for i in self.gameState["choices"]:
			btn = Button(text=i["text"])
			btn.fileId = i["id"]
			btn.bind(on_press=self.btn_pressed)
			self.buttons.add_widget(btn)

		self.storyText.text=self.gameState["storyText"]
		self.storyText.font_size=30


	def btn_pressed(self, instance):
		self.gameState=json.load(open(self.storyLocation+"Story/"+str(instance.fileId)+".json"))



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
# Fix button size
# Experiment with different button formats