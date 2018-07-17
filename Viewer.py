from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, NumericProperty, ListProperty, StringProperty
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
import os
import json
import types

#All stories should be stored in this single directory with first character not a dot (".").

#This is the directory that contains the story. You may (and should) change it.
storyDir = "./ExampleStory/"
fullscreen = False


# representation of a gamestate object
# gamestate = {
#  choices = [{id: 1, text: ButtonText}, ...] (ids and texts of choices?)
#  storyText = String
#  
# }


# This class is supposed to store all the information about a story, including its current state and options
class Story:
	def __init__(self, folder):
		self.folder = folder
		self.options = json.load(open(folder+"options.json"))

	# Return path of a particular state with id i
	def stateLocation(self, i):
		return self.folder+"Story/"+str(i)+".json"

	# change state to one stored at newId
	def updateState(self, *args):
		# if no button is passed use the default starting position
		newId = args[0].fileId if args else self.options["startId"]

		# for debugging purposses
		print(newId)

		with open(self.stateLocation(newId)) as newState:
			self.state = json.load(newState)
	

# Main widget. Controls screens
class RootWidget(ScreenManager):
	# list of active stories
	active_stories = ListProperty([])

	# User definable options
	user_options = ObjectProperty({})

	# current story id in list
	cur_id = NumericProperty(-1) # by default no story is loaded

	# used to implement the functionality of a back button
	last_screen = ListProperty(["menu"])

# text of a particular section of the story
class StoryText(Label):
	pass

# describes action to be taken when pressed
class ChoiceButton(Button):
	pass


# Only GameScreen (and possibly OptionsScreen) should need a non-kivy implementation
# Also I might need to add a way to load new games, which would require an additional screen
class MenuScreen(Screen):
	pass


# Implement load and save functionalities
class LoadScreen(Screen):
	pass

class PauseScreen(Screen):
	pass

class BackButton(Button):
	pass

class GameScreen(Screen):
	currentStory = ObjectProperty()
	def __init__(self, **kwargs):
		super(GameScreen, self).__init__(**kwargs)
		self.currentStory = Story(storyDir)
		# add all the necessary widgets
		tmp = BoxLayout(orientation="vertical")
		self.storyText = StoryText()
		tmp.add_widget(self.storyText)

		self.buttons = BoxLayout(orientation="vertical")
		tmp.add_widget(self.buttons)
		self.add_widget(tmp)
		# update screen according to gamestate
		self.update()
	
	# Update screen according to gameState
	# Post: all visual elements of gameState appear in screen
	def update(self, *args):
		# update story state if needed
		self.currentStory.updateState(*args)

		# Clear old buttons
		self.buttons.clear_widgets()

		state = self.currentStory.state

		# Iterate over new state
		for i in state["choices"]:
			# Creation of new button
			btn = ChoiceButton(text=i["text"])
			btn.fileId = i["id"]
			btn.bind(on_press=self.update)
			self.buttons.add_widget(btn)
		# Add text label
		self.storyText.text = state["storyText"]

class OptionsScreen(Screen):
	pass

# application class
class ViewerApp(App):
	def build(self):
		# pass the directory of story to main Widget
		pass


if __name__ == '__main__':
	# set window to full screen and full resolution
	if fullscreen:
		import tkinter
		root = tkinter.Tk()
		root.withdraw()
		width, height = root.winfo_screenwidth(), root.winfo_screenheight()
		Window.fullscreen = fullscreen
		Window.size = (width, height)

	# run application
	ViewerApp().run()


# Ideas
# Add the ability to list all characters for convenience
# Keep a list of participating characters in a block for easier reference
# Add different interaction ways: keyboard input, images instead of text, puzzles and so on, timer, scares.
# Choices affect: game state, audio / visuals, time, availability of other choices
# Ability for character swapping mid story

# TODO
# Fix button size
# Experiment with different button formats
# Make button sizes "smart" (depending on number of buttons)
# Change colors to be more esthetically pleasing

# Things to store in main object (or maybe just some sccreen?):

# User options
# List of loadable games
# (List of) GameState(s). Should probably contain the path to game.
# Certain options for each game (specific for each) (non-urgent)