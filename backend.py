import matplotlib.pyplot as plt
from math import cos, sin
import random
import config
from scipy.fft import fft, fftfreq
import numpy as np
from complex_part import AC_contur


def default_eq(funk, progress):
    curr_x = config.x0
    curr_v = config.v0
    curr_t = 0
    curr_a = funk(curr_x, curr_v, curr_t)
    progress["value"] = 0
    N = int((1.0 * config.full_time) / (1.0 * config.delta_t))
    if int(N / config.num_upd_progress_bar) != 0:
        freq = int(N / config.num_upd_progress_bar)
    else:
        freq = 1
    progress["maximum"] = N
    config.data["t"] = [0]
    config.data["x"] = [curr_x]
    config.data["v"] = [curr_v]
    config.data["a"] = [curr_a]
    config.data["pure_x"] = [curr_x+config.noize*(2.0*random.random()-1.0)]

    for i in range(N):
        if i%freq == 0:
            progress["value"] = i
            progress.update()
        new_x = curr_x + config.delta_t * curr_v
        new_v = curr_v + config.delta_t * curr_a
        new_a = funk(new_x, new_v, curr_t)
        for j in range(config.num_cont):
            new_x = curr_x + 0.5 * (curr_v + new_v) * config.delta_t
            new_v = curr_v + 0.5 * (curr_a + new_a) * config.delta_t
            new_a = funk(new_x, new_v, curr_t)
        # добавляем новые
        curr_x = new_x
        curr_v = new_v
        curr_a = new_a
        curr_t += config.delta_t
        config.data["t"].append(curr_t)
        #data["x"].append(curr_x)
        config.data["pure_x"].append(curr_x)
        config.data["x"].append(curr_x*(1.0+config.noize*(2.0*random.random()-1.0)))
        config.data["v"].append(curr_v)
        config.data["a"].append(curr_a)

    progress["value"] = 0
    progress.update()


def punkt_A(x, v, t):
    # x'' + alpha*x + epsilon*x^3 = 0
    return (-1.0) * (config.glob_A_w0*config.glob_A_w0 * x + config.glob_A_epsilon * (x * x * x))


def punkt_B(x, v, t):
    # x'' + 2*gamma*x' + w_0^2*x + epsilon*x^3 = f*cos(omega*t)
    return config.glob_B_f*cos(1.0*config.glob_B_omega*t)+(-1.0)*(config.glob_B_w0*config.glob_B_w0 * x + config.glob_B_epsilon * (x * x * x) + 2*config.glob_B_gamma*v)


def punkt_C(x, v, t):
    # x'' + 2*gamma*x' + w_0^2(1+mu*cos(omega*t))*x + epsilon*x^3 = 0
    return (-1.0) * (config.glob_C_w0 * config.glob_C_w0 * (1 + config.glob_C_mu * cos(1.0*config.glob_C_omega * t)) * x + config.glob_C_epsilon * (x * x * x) + 2*config.glob_C_gamma*v)


def punkt_D(x, v, t):
    # x'' + 2*gamma*x' + (w_0^2)*x = f
    return config.glob_D_f+(-1.0)*(config.glob_D_w0 * config.glob_D_w0 * sin(x) + 2 * config.glob_D_gamma * v)


def epsilon(curr_t):
    return config.glob_D_f*(2.0*random.random()-1.0)


def plot_text():
    if config.curr_drawing in ["A", "B", "C", "D", "E"]:
        pass
    else:
        print("Incorrect current drawing")
    curr_str = "График численного решения пункта " + config.curr_drawing + "\n"
    if config.curr_drawing == "A":
        curr_str += "$\ddot{x} + \omega_0^2 x + \epsilon x^3 = 0$\n"
        curr_str += "$\omega_0$ = " + str(config.glob_A_w0)
        curr_str += ", $\epsilon$ = " + str(config.glob_A_epsilon)
    elif config.curr_drawing == "B":
        curr_str += "$\ddot{x} + 2\gamma \dot{x} + \omega_{0}^2 x + \epsilon x^3 = f \cdot cos(\Omega t)$\n"
        #curr_str += "$\omega_0$ = " + str(config.glob_B_w0)
        #curr_str += ", $\gamma$ = " + str(config.glob_B_gamma)
        #curr_str += ", $\epsilon$ = " + str(config.glob_B_epsilon) + ", "
        curr_str += "$\Omega$ = " + str(config.glob_B_omega)
        curr_str += ", f = " + str(config.glob_B_f)
    elif config.curr_drawing == "C":
        curr_str += "$\ddot{x} + 2 \gamma \ddot{x} + \omega_{0}^2(1+\mu*cos(\Omega t))*x + \epsilon*x^3 = 0$\n"
        curr_str += "$\omega_0$ = " + str(config.glob_C_w0)
        curr_str += ", $\epsilon$ = " + str(config.glob_C_epsilon)
        curr_str += ", $\Omega$ = " + str(config.glob_C_omega)
        curr_str += ", $\gamma$ = " + str(config.glob_C_gamma)
        curr_str += ", $\mu$ = " + str(config.glob_C_mu)
    elif config.curr_drawing == "D":
        curr_str += "$\ddot{x} + 2\gamma\dot{x} + \omega_0^2 x = f$\n"
        curr_str += "$\omega_0$ = " + str(config.glob_D_w0)
        curr_str += ", $\gamma$ = " + str(config.glob_D_gamma)
        curr_str += ", $f$ = " + str(config.glob_D_f)
    elif config.curr_drawing == "E":
        curr_str = ""
        if config.type_of_print_E == 0:
            curr_str += "Амплитудно-частотная характеристика $U$\n"
        else:
            curr_str += "Амплитудно-частотная характеристика $I$\n"
        curr_str += "$\omega_0=$"+str(config.start_w) + ", $\Delta \omega=$ "+str(config.step_w) +\
                    " $, \omega_{end}=$ "+str(config.end_w) + "\n"
        curr_str += "$R_1$ = " + str(config.glob_E_R1)
        #curr_str += ", $R_2$ = " + str(config.glob_E_R2)
        #curr_str += ", $C_1$ = " + str(config.glob_E_C1)
        #curr_str += ", $C_2$ = " + str(config.glob_E_C2)
        #curr_str += ", $L_1$ = " + str(config.glob_E_L1)
        #curr_str += ", $L_2$ = " + str(config.glob_E_L2)
        #curr_str += ", $r$ = " + str(config.glob_E_r)

    return curr_str


def count_furie():
    T = config.delta_t
    N = len(config.data["pure_x"])
    yf = fft(config.data["pure_x"])
    xf = fftfreq(N, d=T)[:N // 2]
    config.data["furie_ampl"] = (2.0 / N) * np.abs(yf[0:N // 2])
    config.data["furie_freq"] = xf


def count_AC_contur(progress):
    AC = AC_contur()
    curr_w = config.start_w
    config.data["w"] = []
    config.data["w_I"] = []
    config.data["w_U"] = []
    progress["value"] = 0
    N = int((1.0 * (config.end_w-config.start_w)) / (1.0 * config.step_w))
    #print(N)
    if int(N / config.num_upd_progress_bar)!=0:
        freq = int(N / config.num_upd_progress_bar)
    else:
        freq=1
    progress["maximum"] = N
    i=0
    while(i<N):
        curr_I = AC.i(curr_w)
        curr_U = AC.u(curr_w)
        config.data["w"].append(curr_w)
        config.data["w_I"].append(curr_I)
        config.data["w_U"].append(curr_U)
        curr_w+=config.step_w
        i+=1
        if i%freq == 0:
            progress["value"] = i
            progress.update()
    #print(config.data["w"])
    progress["value"] = 0
    progress.update()
