import numpy as np

# weighting matrix for minimization of difference between desired and achieved force/torque
K_Tau = np.eye(5)

# weighting matrix for minimization of difference between optimal and necessary actuator setpoint
def K_delta(airspeed):
    return np.eye(8) * 0#* np.array([[1, 1, 10, 3, 3, 0.0, 0.0]]).T * 1e-6 * airspeed**2

# initial actuator guess
init_actuators = np.array([0.6, 0.6, 0.6, .6, 0.2, 0.0, 0.0, 0.0])


#creates the initial actuator guess for the contorl suraces
#these are forward
init_actuators_surfaces = init_actuators[4:8]

# minimum-energy actuator setpoints
actuators_desired = np.zeros(8)

#minimum energy surfaces actuator setpoints
actuators_surfaces_desired = np.zeros(4)

# max iterations for nonlinear solver
max_iter = 50