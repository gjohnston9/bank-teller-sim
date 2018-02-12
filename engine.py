class Event:
    def __init__(self, timestamp):
        self.timestamp = timestamp
        self.next_event = None

    def callback(self):
        pass

class Engine:
    def __init__(self):
        self.FEL = None

    def schedule(self, event):
        if (self.FEL == None):
            event.next_event = None
            self.FEL = event
            return

        if (self.FEL.timestamp >= event.timestamp):
            event.next_event = self.FEL
            self.FEL = event
        else:
            cur = self.FEL
            while (cur.next_event is not None) and (cur.next_event.timestamp < event.timestamp):
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
