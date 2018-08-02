from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, NumericProperty, ListProperty, StringProperty
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.recycleview.views import RecycleDataViewBehavior
import json
import types
from time import gmtime, strftime
from pathlib import Path
import os.path

#All stories should be stored in this single directory with first character not a dot (".").

#This is the directory that contains the story. You may (and should) change it.
storyDir = "./ExampleStory/"
fullscreen = False


# representation of a state object
# state = {
#  choices = [{id: 1, text: ButtonText}, ...] (ids and texts of choices?)
#  storyText = String
#  
# }


# This class is supposed to store all the information about a story, including its current state and options
class Story:
	def __init__(self, folder, *args):
		if folder[-1]!="/":
			folder+="/"
		self.folder = folder
		self.options = json.load(open(folder+"options.json"))
		if len(args)>0:
			self.updateState(args[0])
		else:
			self.updateState()

	# Return path of a particular state with id i
	def stateLocation(self, i):
		return self.folder+"Story/"+str(i)+".json"

	# change state to one stored at newId
	def updateState(self, btn = None):
		# if no button is passed use the default starting position
		self.stateId = btn.fileId if btn else self.options["startId"]

		# for debugging purposses
		print(self.stateId)

		with open(self.stateLocation(self.stateId)) as newState:
			self.state = json.load(newState)
	
# store folder, stateId, any stats (in the future) and save time
# used when saving progress
class StoryMemento:
	def __init__(self, **kwargs):
		self.timeStamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
		if "story" in kwargs:
			story = kwargs["story"]
		# this is a little stupid but it works
		elif "folder" in kwargs:
			if "stateId" in kwargs:
				story = Story(kwargs["folder"], kwargs["stateId"])
			else:
				story = Story(kwargs["folder"])
		else:
			raise KeyError("StoryMemento cannot be initialized from given arguments")
		self.folder = story.folder
		self.stateId = story.stateId
		self.title = story.options["title"] if "title" in story.options else "No Title"


# Main widget. Controls screens
class RootWidget(ScreenManager):
	# User definable options
	# Currently no options available as I'm focusing on the basic functionalities
	userOptions = ObjectProperty({})

	# current story id in list.
	currentStory = ObjectProperty(None, allownone = True) # by default no story is loaded

	# used to implement the functionality of the back button
	lastScreen = ListProperty(["menu"])

	def __init__(self, **kwargs):
		super(RootWidget, self).__init__(**kwargs)
		# load the example story initially
		self.currentStory = Story(storyDir)
		


# text of a particular section of the story
class StoryText(Label):
	pass

# describes action to be taken when pressed
class ChoiceButton(Button):
	pass

class MenuScreen(Screen):
	pass

# Implement load and save functionalities
class NewGameScreen(Screen):
	# use thing below in a similar fashion to insert button at the top
	# self.add_widget(your_widget, len(self.children))
	storyList = ListProperty([])
	def __init__(self, **kwargs):
		self.loadedStoryFolders = []
		super(NewGameScreen, self).__init__(**kwargs)
	def addNewStory(self, selection):
		if os.path.exists(selection+"/options.json"):
			if selection not in self.loadedStoryFolders:
				tmp = StoryMemento(folder = selection)
				self.loadedStoryFolders.insert(0, selection)
				print(tmp.folder, tmp.title)
				self.storyList.insert(0, {"folder": tmp.folder, "text": tmp.title})
			# otherwise bring selection to the top
			else:
				pass
		else:
			print("incorrect folder, no game present here")
		
class StoryListViewButton(RecycleDataViewBehavior, Button):
	def __init__(self, **kwargs):
		self.folder = kwargs.pop("folder", None)
		super(StoryListViewButton, self).__init__(**kwargs)

class PauseScreen(Screen):
	pass

class BackButton(Button):
	pass

class LoadPopup(Popup):
	def __init__(self, **kwargs):
		self.caller = kwargs.pop("caller", None)
		super(LoadPopup, self).__init__(**kwargs)

class LoadStoryChooser(FileChooserListView):
	pass

class GameScreen(Screen):
	currentStory = ObjectProperty(allownone = True)
	def __init__(self, **kwargs):
		super(GameScreen, self).__init__(**kwargs)

		# add all the necessary widgets
		tmp = BoxLayout(orientation="vertical")
		self.storyText = StoryText()
		tmp.add_widget(self.storyText)

		self.buttons = BoxLayout(orientation="vertical")
		tmp.add_widget(self.buttons)
		self.add_widget(tmp)
	
	# Update screen according to gameState
	# Post: all visual elements of gameState appear in screen
	def update(self, pressedButton = None, updateState = True):
		# update story state if needed
		if updateState:
			self.currentStory.updateState(pressedButton) 

		# Clear old buttons
		self.buttons.clear_widgets()

		state = self.currentStory.state

		# Iterate over new state
		for i in state["choices"]:
			# Creation of new button. Bind the click to 
			btn = ChoiceButton(text=i["text"])
			btn.fileId = i["id"]
			btn.bind(on_release=self.update)
			self.buttons.add_widget(btn)

		# game ended, give option to return to menu
		if not state["choices"]:
			self.buttons.add_widget(StoryEndButton())
		# Add text label
		self.storyText.text = state["storyText"]

class StoryEndButton(Button):
	pass

class OptionsScreen(Screen):
	pass

# application class
class ViewerApp(App):
	def build(self):
		pass


if __name__ == "__main__":
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