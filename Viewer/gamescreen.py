from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from buttons import ChangeScreenButton
from kivy.uix.button import Button


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

class EndGameButton(ChangeScreenButton):
	pass

class ChoiceButton(Button):
	pass