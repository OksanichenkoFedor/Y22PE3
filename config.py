delta_t = 0.001
full_time = 20
num_cont = 3
num_upd_progress_bar = 1000.0

x0 = 1
v0 = 0

glob_A_w0 = 1
glob_A_epsilon = -0.9

glob_B_epsilon = 360
glob_B_gamma = 0.85
glob_B_f = 1
glob_B_omega = 2
glob_B_w0 = 26.3

glob_C_w0 = 1
glob_C_epsilon = 1.1
glob_C_omega = 2
glob_C_mu = 0.1
glob_C_gamma = 0.2

glob_D_w0 = 1
glob_D_gamma = 0.1
glob_D_f = 0.7

glob_E_R1 = 1000.0
glob_E_R2 = 560.0
glob_E_L1 = 0.0052
glob_E_L2 = 0.12
glob_E_C1 = 0.00000001*9.3
glob_E_C2 = 0.00000001*4.5
glob_E_r = 14.0
start_w = 0.1
end_w = 100000
step_w = 100
type_of_print_E = 0


curr_drawing = "A"

data = {}
data["t"] = []
data["pure_x"] = []
data["v"] = []
data["a"] = []
data["furie_ampl"] = []
data["furie_freq"] = []
data["w_U"] = []
data["w_I"] = []
data["w"] = []

noize = 0.000


plot_fontsize = 10

full_number = 100
curr_number = 0

type_of_B = 0

label_width_E1 = 10
label_width_E2 = 15