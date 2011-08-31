import random
import thread, time, sys
from threading import Timer

# TODO: "Constrain" line not necessary.

file_name = "test.py"

lines = [line[:-1] for line in file(file_name)]

is_in_constraint = False
constraints = {}
types = {}
function_being_constrained = ""
fn_ordering = []

for line in lines:
  if line.startswith("#!"):
    line_pieces = line.split(" ")
    if line_pieces[1] == "Constrain":
      is_in_constraint = True
      function_being_constrained = line_pieces[2]

      constraints[function_being_constrained] = []
      types[function_being_constrained] = []
      fn_ordering.append(line_pieces[2])
      continue

    # constraint types

    if line_pieces[2] == "in":
      constraints[function_being_constrained].append(line_pieces[3])

    if line_pieces[2] == "is":
      types[function_being_constrained].append(line_pieces[3])

  else:
    is_in_constraint = False

module_name = file_name.split(".")[0]

module = __import__(module_name)
done = False

INVALID_TYPE = "INVALID_TYPE"

def timeout():
  thread.interrupt_main()

def decorated(func):
  function_name = func.__name__

  def dec(*args):
    if function_name in types:
      for x in range(len(args)):
        if not isinstance(args[x], eval(types[function_name][x])): #TODO: Better way?
          print "Bad argument passed to %s: %s. Expected: int" % (function_name, repr(args[0]))
          return INVALID_TYPE

    func(*args)
  return dec

# Instrument all functions with type-checking decorators.
for function in fn_ordering:
  setattr(module, function, decorated(getattr(module, function)))

module.tester(5)

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
      result = getattr(module, function)(*arg_list)

      if result == INVALID_TYPE: #special flag from decorator
        break
  except KeyboardInterrupt:
    # timer exception
    passed = False
    print "%s%s has gone into apparent infinite loop." % (function, last_args)
  except:
    # any other exception
    passed = False

    e = str(sys.exc_info()[0]) # get exception
    print "%s%s has raised exception %s." % (function, last_args, e)

  if passed:
    print "%s() PASS." % function

  # Don't cause the exception any more.
  t.cancel()
