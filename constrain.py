import random
import thread, time, sys
from threading import Timer

file_name = "sample.py"

lines = [line[:-1] for line in file(file_name)]

is_in_constraint = False
constraints = {}
function_being_constrained = ""
fn_ordering = []

for line in lines:
  if line.startswith("#"):
    line_pieces = line.split(" ")
    if line_pieces[1] == "Constrain":
      is_in_constraint = True
      constraints[line_pieces[2]] = []
      fn_ordering.append(line_pieces[2])
      function_being_constrained = line_pieces[2]
      continue

    # constraint types

    if line_pieces[2] == "in":
      constraints[function_being_constrained].append(line_pieces[3])

  else:
    is_in_constraint = False

module_name = file_name.split(".")[0]

module = __import__(module_name)
done = False

def timeout():
  thread.interrupt_main()

for function in fn_ordering:
  last_args = []
  passed = True

  # Tricky behavior here since it is very difficult to stop a function once it
  # has been started. If the timer has made an interrupt then time is up, and 
  # we will receive an exception.

  t = Timer(.1, timeout)
  t.start()

  try:
    for x in range(500):
      arg_list = [random.choice(eval(constraint)) for constraint in constraints[function]]
      last_args = "(" + ",".join([str(x) for x in arg_list]) + ")"
      getattr(module, function)(*arg_list)
  except KeyboardInterrupt:
    passed = False
    print "%s%s has gone into apparent infinite loop." % (function, last_args)
  except:
    passed = False

    e = str(sys.exc_info()[0]) # get exception
    print "%s%s has raised exception %s." % (function, last_args, e)

  if passed:
    print "%s() PASS." % function

  # Don't cause the exception any more.
  t.cancel()
