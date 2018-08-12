from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
import os.path
import pickle
from kivy.clock import Clock
from kivy.app import App
from buttons import ChangeScreenButton
from story import Story, StoryMemento

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

class SavedStoryButton(ChangeScreenButton):
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