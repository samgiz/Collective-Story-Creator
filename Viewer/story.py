import json
from time import gmtime, strftime

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