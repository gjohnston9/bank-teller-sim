class Event:
	def __init__(self, timestamp):
		self.timestamp = timestamp
		self.next_event = None

class Engine:
	def __init__(self):
		self.FEL = Event(-1)

	def schedule(self, event):
		if (self.FEL == None):
			self.FEL = event
			return
		cur = self.FEL
		while True:
			if (cur.next_event == None) or (cur.timestamp <= event.timestamp):
				break
			cur = cur.next_event
		event.next_event = cur.next_event
		cur.next_event = event

	def remove(self):
		if (self.FEL == None):
			return None
		event = self.FEL
		self.FEL = self.FEL.next_event
		return event

	def __iter__(self):
		cur = self.FEL
		while (cur != None):
			yield cur
			cur = cur.next_event

	def __str__(self):
		if (self.FEL == None):
			return "empty list"
		s = ""
		return "\n".join(map(str, (event.timestamp for event in self)))
