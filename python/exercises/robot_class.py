class Robot:

    """Represents a robot, with a name."""

    # A class variable, counting the number of robots
    population = 0

    def callable(func):
        print "It's happening"
        return func

    @callable
    def __init__(self, name):
        """Initializes the data."""
        self.name = name
        print "(Initializing {})".format(self.name)

        # When this person is created, the robot
        # adds to the population
        Robot.population += 1

    def _die(self):
        """I am dying."""
        print "{} is being destroyed!".format(self.name)

        Robot.population -= 1

        if Robot.population == 0:
            print "{} was the last one.".format(self.name)
        else:
            print "There are still {:d} robots working.".format(
                Robot.population)

    def _say_hi(self):
        """Greeting by the robot. Yeah, they can do that."""
        print "Greetings, my masters call me {}.".format(self.name)
        # self.__privatetest()

    # def __privatetest(self):
    #    print "PRIVATE!"

    @classmethod
    def _how_many(self):
        """Prints the current population."""
        print "We have {:d} robots.".format(self.population)
        # print "I'm in the {} class".format(self.__name__)

droid1 = Robot("R2-D2")
droid1._say_hi()
Robot._how_many()

droid2 = Robot("C-3PO")
droid2._say_hi()
Robot._how_many()

print "\nRobots can do some work here.\n"

print "Robots have finished their work. So let's destroy them."
droid1._die()
droid2._die()

# Robot._how_many()

# print Robot._say_hi.__doc__
# print dir(Robot)
