class SchoolMember:
    '''Represents any school member.'''
    def __init__(self, name, age):
        self.name = name
        self.age = age
        print '(Initialized SchoolMember: {})'.format(self.name)
        self.tellall()

    def tell(self):
        '''Tell my details.'''
        print 'MAIN Name:"{}" Age:"{}"'.format(self.name, self.age), #tricksy comma gets rid of tricksy newline
        self.tellall()

    @classmethod
    def tellall(self):
    	print "HERE I AM {}".format(self.__name__)

class Teacher(SchoolMember):
    '''Represents a teacher.'''
    def __init__(self, name, age, salary):
        SchoolMember.__init__(self, name, age)
        self.salary = salary
        print '(Initialized Teacher: {})'.format(self.name)
        #print "From",self.__name__

    def tell(self):
        SchoolMember.tell(self)
        print 'SUB Salary: "{:d}"'.format(self.salary)

class Student(SchoolMember):
    '''Represents a student.'''
    def __init__(self, name, age, marks):
        SchoolMember.__init__(self, name, age)
        self.marks = marks
        print '(Initialized Student: {})'.format(self.name)

    def tell(self):
        SchoolMember.tell(self)
        print 'SUB Marks: "{:d}"'.format(self.marks)

t = Teacher('Mrs. Shrividya', 40, 30000)
s = Student('Swaroop', 25, 75)

# prints a blank line
print

members = [t, s]
print "MEMBER ELEMENT",members
for member in members:
    # Works for both Teachers and Students
    #print member
    member.tell()