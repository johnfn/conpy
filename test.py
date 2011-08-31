#! Constrain some_fn
#! x is int
#! x in range(25)
def some_fn(x):
  return "yay"

#! Constrain tester
#! x is int
#! x in range(100)
def tester(x):
  if x == 5:
    return some_fn(2.1)
  else:
    return some_fn(x)
