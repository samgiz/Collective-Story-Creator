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
from kivy.clock import Clock
import json
import types
from time import gmtime, strftime
import os.path
import pickle

#All stories should be stored in this single directory with first character not a dot (".").

#This is the directory that contains the story. You may (and should) change it.
storyDir = "./ExampleStory"
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
	def updateState(self, stateId = None):
		# if no button is passed use the default starting position
		self.stateId = stateId if stateId else self.options["startId"]

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
		self.title = story.options["title"] if "title" in story.options else self.folder.split('/')[-2]


# Main widget. Controls screens
class RootWidget(ScreenManager):
	# User definable options
	# Currently no options available as I'm focusing on the basic functionalities
	# userOptions = ObjectProperty({})

	# current story id in list.
	currentStory = ObjectProperty(None, allownone = True) # by default no story is loaded

	# used to implement the functionality of the back button
	lastScreen = ListProperty(["menu"])

	def __init__(self, **kwargs):
		super(RootWidget, self).__init__(**kwargs)
		# load the example story initially
		self.currentStory = Story(storyDir)
		if os.path.isfile("./.storystateinfo"):
			with open("./.storystateinfo", "rb") as f:
				tmp = pickle.load(f)["currentStoryMemento"]
			self.currentStory = Story(tmp.folder, tmp.stateId) if tmp else None
		

# describes action to be taken when pressed
class ChoiceButton(Button):
	pass

# Implement load and save functionalities
class NewGameScreen(Screen):
	# contains the loaded stories that can be selected in the RecycleView
	storyList = ListProperty([])
	def __init__(self, **kwargs):
		super(NewGameScreen, self).__init__(**kwargs)

		self.loadedStoryFolders = []

		if os.path.isfile("./.storystateinfo"):
			with open("./.storystateinfo", "rb") as f:
				tmp = pickle.load(f)
			for i in tmp["loadedStoryFolders"]:
				self.addNewStory(i)

		

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

class LoadSaveScreen(Screen):
	savedStories = ObjectProperty(None)
	labelText = StringProperty("")

class LoadScreen(LoadSaveScreen):
	def __init__(self, **kwargs):
		super(LoadScreen, self).__init__(**kwargs)
		def tmp(*args):
			if os.path.isfile("./.storystateinfo"):
				with open("./.storystateinfo", "rb") as f:
					tmp = pickle.load(f)["savedStoriesMementos"]
				for i in range(self.savedStories.cols*self.savedStories.rows):
					self.savedStories.add_widget(SavedStoryButton(index = i, memento = tmp[i]))
			else:
				for i in range(self.savedStories.cols*self.savedStories.rows):
					self.savedStories.add_widget(SavedStoryButton(index = i, memento = None))
		Clock.schedule_once(tmp)

class SaveScreen(LoadSaveScreen):
	def __init__(self, **kwargs):
		super(SaveScreen, self).__init__(**kwargs)
		def tmp(*args):
			children = App.get_running_app().root.get_screen("load").savedStories.children
			print(len(children))
			for i in range(self.savedStories.cols*self.savedStories.rows):
				loadButton = children[self.savedStories.cols*self.savedStories.rows-1-i]
				btn = SavedStoryButton(index = i, memento = loadButton.memento)
				btn.bind(memento = loadButton.setter("memento"))
				self.savedStories.add_widget(btn)
		Clock.schedule_once(tmp)

class ChangeScreenButton(Button):
	pass

class EndGameButton(ChangeScreenButton):
	pass

class StoryListViewButton(RecycleDataViewBehavior, ChangeScreenButton):
	def __init__(self, **kwargs):
		self.folder = kwargs.pop("folder", None)
		super(StoryListViewButton, self).__init__(**kwargs)

class LoadPopup(Popup):
	def __init__(self, **kwargs):
		self.caller = kwargs.pop("caller", None)
		super(LoadPopup, self).__init__(**kwargs)

class GameScreen(Screen):
	currentStory = ObjectProperty(allownone = True)
	storyText = ObjectProperty(None)
	buttons = ObjectProperty(None)
	def __init__(self, **kwargs):
		super(GameScreen, self).__init__(**kwargs)
	
	# Update screen according to gameState
	# Post: all visual elements of gameState appear in screen
	def update(self, pressedButton = None, updateState = True):
		# update story state if needed
		if updateState:
			self.currentStory.updateState(pressedButton.fileId) 

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
			self.buttons.add_widget(EndGameButton())
		# Add text label
		self.storyText.text = state["storyText"]

class SavedStoryButton(Button):
	memento = ObjectProperty(None)
	def __init__(self, **kwargs):
		self.index = kwargs.pop("index", None)
		self.memento = kwargs.pop("memento", None)
		super(SavedStoryButton, self).__init__(**kwargs)

	def loadOrSave(self):
		app = App.get_running_app().root
		print(app.current)
		if app.current == "load":
			if self.memento:
				app.currentStory = Story(self.memento.folder, self.memento.stateId)
				app.current = "game"
		else: # save current game
			self.memento = StoryMemento(story = app.currentStory)

# application class
class ViewerApp(App):
	def build(self):
		pass
	def on_stop(self):
		# store loaded games both in load screen and in newgame screen, as well as current story info
		tmp = {"currentStoryMemento": StoryMemento(story = self.root.currentStory) if self.root.currentStory else None, 
			"savedStoriesMementos": list(map(lambda x: x.memento, self.root.get_screen("load").savedStories.children)),
			"loadedStoryFolders": self.root.get_screen("new").loadedStoryFolders}
		with open("./.storystateinfo", "wb+") as f:
			pickle.dump(tmp, f, pickle.HIGHEST_PROTOCOL)
		
	def on_pause(self):
		self.on_stop()


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
# Certain options for each game (specific for each) (non-urgent)