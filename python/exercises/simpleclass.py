class Person:
	def __init__(self, name):
		self.name = name
	def say_hi(self):
		print 'Hello, how are you?', self.name
		self.say_bye()
	def say_bye(self):
		print "Que?"

p = Person("dude")
p.say_hi()
p.say_bye()