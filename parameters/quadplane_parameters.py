import sys
sys.path.append('..')
import numpy as np
from tools.rotations import Euler2Quaternion

######################################################################################
                #   Initial Conditions
######################################################################################
#   Initial conditions for MAV
north0 = 0.  # initial north position
east0 = 0.  # initial east position
down0 = 0.0  # initial down position
u0 = 0.0  # initial velocity along body x-axis
v0 = 0.  # initial velocity along body y-axis
w0 = -0.0001  # initial velocity along body z-axis
phi0 = 0.  # initial roll angle
theta0 = 0.  # initial pitch angle
psi0 = 0.0  # initial yaw angle
p0 = 0  # initial roll rate
q0 = 0  # initial pitch rate
r0 = 0  # initial yaw rate
Va0 = np.sqrt(u0**2+v0**2+w0**2)
#   Quaternion State
e = Euler2Quaternion(phi0, theta0, psi0)
e0 = e.item(0)
e1 = e.item(1)
e2 = e.item(2)
e3 = e.item(3)


######################################################################################
                #   Physical Parameters
######################################################################################
mass = 11. #kg
Jx = 0.8244 #kg m^2
Jy = 1.135
Jz = 1.759
Jxz = 0.1204
S_wing = 0.55
b = 2.8956
c = 0.18994
S_prop = 0.2027
rho = 1.2682
e = 0.9
AR = (b**2) / S_wing
gravity = 9.81

e_oswald = e
AR_wing = AR

######################################################################################
                #   Rotor Parameters
######################################################################################

#the positions of each rotor
rotor_q0 = np.array([[.5, .5, 0]]).T #Front Starboard Prop
rotor_q1 = np.array([[.5, -.5, 0]]).T #Front Port Prop
rotor_q2 = np.array([[-.5, .5, 0]]).T #Rear Starboard Prop
rotor_q3 = np.array([[-.5, -.5, 0]]).T #Rear Port Prop
rotor_q4 = np.array([[.5, 0, 0]]).T #forward prop
rotor_qs = [rotor_q0, rotor_q1, rotor_q2, rotor_q3, rotor_q4]


#the normal vector of each rotor
rotor_r0 = np.array([[0, 0, -1]]).T #Front Starboard Prop
rotor_r1 = np.array([[0, 0, -1]]).T #Front Port Prop
rotor_r2 = np.array([[0, 0, -1]]).T #Rear Starboard Prop
rotor_r3 = np.array([[0, 0, -1]]).T #Rear Port Prop
rotor_r4 = np.array([[1, 0, 0]]).T #forward prop
rotor_rs = [rotor_r0, rotor_r1, rotor_r2, rotor_r3, rotor_r4]

#sets the directions of the propellers
prop_dir0 = -1 #Front Starboard Prop
prop_dir1 = 1 #Front Port Prop
prop_dir2 = 1 #Rear Starboard Prop
prop_dir3 = -1 #Rear Port Prop
prop_dir4 = 1 #forward prop
prop_dirs = np.array([prop_dir0, prop_dir1, prop_dir2, prop_dir3, prop_dir4])

######################################################################################
                #   Longitudinal Coefficients
######################################################################################
C_L_0 = 0.23
C_D_0 = 0.043
C_m_0 = 0.0135
C_L_alpha = 5.61
C_D_alpha = 0.03
C_m_alpha = -2.74
C_L_q = 7.95
C_D_q = 0.0
C_m_q = -38.21
C_L_delta_e = 0.13
C_D_delta_e = 0.0135
C_m_delta_e = -0.99
M = 50.0
alpha0 = 0.47
epsilon = 0.16
C_D_p = 0.0


######################################################################################
                #   Lateral Coefficients
######################################################################################
C_Y_0 = 0.0
C_ell_0 = 0.0
C_n_0 = 0.0
C_Y_beta = -0.98
C_ell_beta = -0.13
C_n_beta = 0.073
C_Y_p = 0.0
C_ell_p = -0.51
C_n_p = 0.069
C_Y_r = 0.0
C_ell_r = 0.25
C_n_r = -0.095
C_Y_delta_a = 0.075
C_ell_delta_a = 0.17
C_n_delta_a = -0.011
C_Y_delta_r = 0.19
C_ell_delta_r = 0.0024
C_n_delta_r = -0.069

######################################################################################
                #   Propeller thrust / torque parameters (see addendum by McLain)
######################################################################################
# Prop parameters
D_prop = 20*(0.0254)     # prop diameter in m

# Motor parameters
KV = 145.                   # from datasheet RPM/V
KQ = (1. / KV) * 60. / (2. * np.pi)  # KQ in N-m/A, V-s/rad
R_motor = 0.042              # ohms
i0 = 1.5                     # no-load (zero-torque) current (A)


# Inputs
ncells = 12.
V_max = 3.7 * ncells  # max voltage for specified number of battery cells

# Coeffiecients from prop_data fit
C_Q2 = -0.01664
C_Q1 = 0.004970
C_Q0 = 0.005230
C_T2 = -0.1079
C_T1 = -0.06044
C_T0 = 0.09357

######################################################################################
                #   Calculation Variables
######################################################################################
#   gamma parameters pulled from page 36 (dynamics)
gamma = Jx * Jz - (Jxz**2)
gamma1 = (Jxz * (Jx - Jy + Jz)) / gamma
gamma2 = (Jz * (Jz - Jy) + (Jxz**2)) / gamma
gamma3 = Jz / gamma
gamma4 = Jxz / gamma
gamma5 = (Jz - Jx) / Jy
gamma6 = Jxz / Jy
gamma7 = ((Jx - Jy) * Jx + (Jxz**2)) / gamma
gamma8 = Jx / gamma

#   C values defines on pag 62
C_p_0         = gamma3 * C_ell_0      + gamma4 * C_n_0
C_p_beta      = gamma3 * C_ell_beta   + gamma4 * C_n_beta
C_p_p         = gamma3 * C_ell_p      + gamma4 * C_n_p
C_p_r         = gamma3 * C_ell_r      + gamma4 * C_n_r
C_p_delta_a    = gamma3 * C_ell_delta_a + gamma4 * C_n_delta_a
C_p_delta_r    = gamma3 * C_ell_delta_r + gamma4 * C_n_delta_r
C_r_0         = gamma4 * C_ell_0      + gamma8 * C_n_0
C_r_beta      = gamma4 * C_ell_beta   + gamma8 * C_n_beta
C_r_p         = gamma4 * C_ell_p      + gamma8 * C_n_p
C_r_r         = gamma4 * C_ell_r      + gamma8 * C_n_r
C_r_delta_a    = gamma4 * C_ell_delta_a + gamma8 * C_n_delta_a
C_r_delta_r    = gamma4 * C_ell_delta_r + gamma8 * C_n_delta_r

# Ordering of state variable

STATE_P_NORTH = 0
STATE_P_EAST = 1
STATE_P_DOWN = 2
STATE_V_U = 3
STATE_V_V = 4
STATE_V_W = 5
STATE_Q_E0 = 6
STATE_Q_E1 = 7
STATE_Q_E2 = 8
STATE_Q_E3 = 9
STATE_ANG_P = 10
STATE_ANG_Q = 11
STATE_ANG_R = 12