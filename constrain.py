file_name = "sample.py"

lines = [line[:-1] for line in file(file_name)]

is_in_constraint = False
constraints = {}
function_being_constrained = ""

for line in lines:
	if line.startswith("#"):
		line_pieces = line.split(" ")
		if line_pieces[1] == "Constrain":
			is_in_constraint = True
			constraints[line_pieces[2]] = []
			function_being_constrained = line_pieces[2]
			continue
		if line_pieces[2] == "in":
			constraints[function_being_constrained].append(line_pieces[3])

	else:
		is_in_constraint = False

result = ""

for fn in constraints:
	result += "def %s_test():\n" % fn
	result += "\tfor testcase in range(500):\n"
	result += "\t\t%s(%s)\n" % (fn, constraints[fn][0])

print result
