from z3 import *

# Create a Z3 solver instance
solver = Solver()

# Define a Boolean variable x
x = Bool('x')

# Add a constraint that x must be true
solver.add(x == True)

# Check if the constraints are satisfiable
if solver.check() == sat:
    # If the constraints are satisfiable, print the model
    model = solver.model()
    print("Model: x = {}".format(model[x]))
else:
    # If the constraints are unsatisfiable, print an error message
    print("Error: constraints are unsatisfiable")