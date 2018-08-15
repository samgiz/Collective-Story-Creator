from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty
import os.path
import pickle
from story import StoryMemento
from kivy.uix.popup import Popup
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from buttons import ChangeScreenButton

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

class LoadPopup(Popup):
	def __init__(self, **kwargs):
		self.caller = kwargs.pop("caller", None)
		super(LoadPopup, self).__init__(**kwargs)

class StoryListViewButton(RecycleDataViewBehavior, ChangeScreenButton):
	def __init__(self, **kwargs):
		self.folder = kwargs.pop("folder", None)
		super(StoryListViewButton, self).__init__(**kwargs)