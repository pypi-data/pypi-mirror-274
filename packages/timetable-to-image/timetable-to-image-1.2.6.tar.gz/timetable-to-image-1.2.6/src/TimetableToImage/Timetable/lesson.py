import textwrap


class Lesson:
    def __init__(self):
        self.group = None
        self.name = None
        self.room = None
        self.teacher = None

    def __str__(self):
        data = [x for x in [self.name, self.teacher, self.room] if x != ""]
        return ', '.join(data)
