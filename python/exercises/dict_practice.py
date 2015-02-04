my_dict = {'Atlas' : [1, 2, 3], 'Balthasar': [1, 2], 'Cersei': [1,2]}

def most_classes(teacher_dict):
  max_count = 0
  for key in teacher_dict:
    current_count = len(teacher_dict[key])
    if current_count > max_count:
      max_count = current_count
      name = key
    else:
      continue
  return name

def num_teachers(teacher_dict):
  return len(teacher_dict.keys())

def stats(teacher_dict):
	my_list = []
	for name in teacher_dict.keys():
		inner_list = []
		print "1. my_list is ",my_list
		classes = len(teacher_dict[name])
		inner_list.insert(0,name)
		inner_list.insert(1,classes)
		print "2. Inner list is ",inner_list
		my_list.append(inner_list)
		print "3. my_list ",my_list
	print my_list

def courses(teacher_dict):
	course_list = []
	for key in teacher_dict:
		for course in teacher_dict[key]:
			course_list.append(course)
		
	print course_list

courses(my_dict)
