from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, ListProperty
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
import os.path
import pickle
from story import *
from newgamescreen import *
from loadsavescreens import *
from buttons import *
from gamescreen import *

fullscreen = False


# representation of a state object
# state = {
#  choices: [{id: 1, text: ButtonText}, ...] (ids and texts of choices)
#  storyText: String
#  
# }

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
		if os.path.isfile("./.storystateinfo"):
			with open("./.storystateinfo", "rb") as f:
				tmp = pickle.load(f)["currentStoryMemento"]
			self.currentStory = Story(tmp.folder, tmp.stateId) if tmp else None



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

# load and store initial data not in current path but in script path