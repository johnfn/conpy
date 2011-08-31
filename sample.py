# Constrain some_fn
# x in range(25)
def some_fn(x):
  while x==555:
    pass
  return "yay"

# Constrain some_fn2
# x in range(25)
def some_fn2(x):
  while x==22:
    pass
  return "yay"

# Constrain some_fn3
# x in range(25)
def some_fn3(x):
  while x==555:
    pass
  return "yay"


# Constrain some_fn4
# x in range(25)
def some_fn4(x):
  if x == 1:
    print 1/0
  return "yay"
