# Import libraries

# Using Xanadu Strawberry Fields quantum computing simulation library
import strawberryfields as sf
from strawberryfields.ops import *
import numpy as np
from matplotlib import pyplot as plt


# Variables

# Amplitude
r_c = 10

# Phase
phi_c = np.pi/4

# Number of variations
No_of_iterations = 1000

# Phase Variation

phi_input = phi_c
phi_output = phi_c + 4*np.pi
diff_phi = (phi_output - phi_input)/No_of_iterations
current_phi = phi_input
diff_phi_vector = np.arange(phi_input, phi_output, diff_phi)

homodyne_array = np.zeros((No_of_iterations))

homodyne_loop_counter = 1

# Homodyne measurement phase loop
while current_phi <= phi_output - diff_phi:

    # Set number of modes in quantum system
    prog = sf.Program(1)

    # Choosing the gaussian backend from the options provided in the SF library
    eng = sf.Engine("gaussian")

    with prog.context as q:

        # Squeezing to give state
        DisplacedSqueezed(r_c, phi_c, 2, phi_c * 2 + np.pi) | q[0] 

        # Measuring Homodyne
        MeasureHomodyne(current_phi) | q[0]

    result = eng.run(prog)

    homodyne_array[homodyne_loop_counter - 1] = result.samples[0][0]

    current_phi = current_phi + diff_phi
    homodyne_loop_counter = homodyne_loop_counter + 1

# Classical measurement
plt.plot(diff_phi_vector,  2*r_c*np.cos(diff_phi_vector - phi_c), 'b')

# Quantum measurement
plt.plot(diff_phi_vector,  homodyne_array, 'or' )


plt.xlabel('Homodyne measurement angle')
plt.ylabel('Homodyne measurement result')
plt.title('Squeezed Phase State')
plt.show()   




