import logging
import numpy as np
from spins2 import functions
from spins2.single import triangular_update

kB = 8.61733e-2 # 玻尔兹曼常数(meV/K)

def run(file, init, X, Y, J, A, arrays_temperatures, nequilibrium, nworks):
    logging.basicConfig(level=logging.INFO,format="%(message)s",filename=file,filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    N   = X *  Y
    X_s = X // 2
    Y_s = Y // 2
    num = N *  2
    logging.info("{} {:<12} {} {} × {:<8} {} {} + {:<8} {} {}".format(
        "configuration:", file.split('_')[0], "lattice dimensions:", X, Y, "iterations:", nequilibrium, nworks, "Atom number:", num))
    p = len(J)
    np.seterr(divide='ignore', invalid='ignore')
    arrays_values = np.where(arrays_temperatures < 0.01, 0, 1.0/(arrays_temperatures * kB))
    lav = arrays_values.shape[0]
    arrays_T2 = kB * arrays_values ** 2
    if p == 1:
        J = [J[0], 0.0, 0.0]
    elif p == 2:
        J = [J[0], J[1], 0.0]
    else:
        J = [J[0], J[1], J[2]]

    Ja, Jb, Jc = J[0], J[1], J[2]
    if len(A) == 1:
        Aa, Ab = A[0], A[0]
    else:
        Aa, Ab = A[0], A[1]
    logging.info("{} {:<8} {} {:<8} {:<8} {:<8} {} {:<8} {:<8}".format("init:", init, "parameters(meV):", Ja, Jb, Jc, "anisotropy(meV):", Aa, Ab))
    if init == "fm":
        logging.info("{:>16} {:>16}".format("Round", "magnetism(e)"))
        latt = functions.OnesZNN(2, 4, Y_s, X_s)
        m_ave = functions.Average(latt[:,:,:,:,2])
        logging.info("{:>16} {:>16.6}".format(0, m_ave))
        logging.info("{:>16} {:>16} {:>18} {:>16} {:>16}".format(
            "Temperature", "magnetism(e)", "susceptibility(e)", "specific heat", "time(s)"))
        for i in range(lav):
            t, Nw, Ew = triangular_update.iteration3(latt, X_s, Y_s, Ja, Jb, Jc, Aa, Ab, arrays_values[i], nequilibrium, nworks)
            m_ave = functions.Average(Nw)
            s_ave = functions.Average2(Nw)
            susceptibility = arrays_values[i] * num * (s_ave - m_ave ** 2)
            Cv = arrays_T2[i] * (functions.Average2(Ew) - functions.Average(Ew) ** 2) / num
            logging.info("{:>16.2f} {:>16.6f} {:>18.6f} {:>16.6f} {:>16.6f}".format(
                arrays_temperatures[i], m_ave, susceptibility, Cv, t))
    elif init == "afm1":
        logging.info("{:>16} {:>16} {:>16}".format("Round", "magnetism0(e)", "magnetism1(e)"))
        latt = functions.OnesZNN(2, 4, Y_s, X_s)
        latt[1,:,:,:,2] = -1
        m_ave0 = functions.Average(latt[0,:,:,:,2])
        m_ave1 = functions.Average(latt[1,:,:,:,2])
        logging.info("{:>16} {:>16.6} {:>16.6}".format(0, m_ave0, m_ave1))
        logging.info("{:>16} {:>16} {:>16} {:>18} {:>18} {:>16} {:>16}".format(
            "Temperature", "magnetism0(e)", "magnetism1(e)", "susceptibility0(e)", "susceptibility1(e)", "specific heat", "time(s)"))
        for i in range(lav):
            t, Nw, Ew = triangular_update.iteration3(latt, X_s, Y_s, Ja, Jb, Jc, Aa, Ab, arrays_values[i], nequilibrium, nworks)
            arr_a, arr_b = np.hsplit(Nw,2)
            m_ave0 = functions.Average(arr_a)
            m_ave1 = functions.Average(arr_b)
            s_ave0 = functions.Average2(arr_a)
            s_ave1 = functions.Average2(arr_b)
            susceptibility0 = arrays_values[i] * N * (s_ave0 - m_ave0 ** 2)
            susceptibility1 = arrays_values[i] * N * (s_ave1 - m_ave1 ** 2)
            Cv = arrays_T2[i] * (functions.Average2(Ew) - functions.Average(Ew) ** 2) / num
            logging.info("{:>16.2f} {:>16.6f} {:>16.6f} {:>18.6f} {:>18.6f} {:>16.6f} {:>16.6f}".format(
                arrays_temperatures[i], m_ave0, m_ave1, susceptibility0, susceptibility1, Cv, t))
    elif init == "afm2":
        logging.info("{:>16} {:>16} {:>16}".format("Round", "magnetism0(e)", "magnetism1(e)"))
        latt = functions.OnesZNN(2, 4, Y_s, X_s)
        latt[:,[2,3],:,:,2] = -1
        m_ave0 = functions.Average(latt[:,[0,1],:,:,2])
        m_ave1 = functions.Average(latt[:,[2,3],:,:,2])
        logging.info("{:>16} {:>16.6} {:>16.6}".format(0, m_ave0, m_ave1))
        logging.info("{:>16} {:>16} {:>16} {:>18} {:>18} {:>16} {:>16}".format(
            "Temperature", "magnetism0(e)", "magnetism1(e)", "susceptibility0(e)", "susceptibility1(e)", "specific heat", "time(s)"))
        for i in range(lav):
            t, Nw, Ew = triangular_update.iteration3(latt, X_s, Y_s, Ja, Jb, Jc, Aa, Ab, arrays_values[i], nequilibrium, nworks)
            arr_a, arr_b = Nw[:,[0,1,4,5]], Nw[:,[2,3,6,7]]
            m_ave0 = functions.Average(arr_a)
            m_ave1 = functions.Average(arr_b)
            s_ave0 = functions.Average2(arr_a)
            s_ave1 = functions.Average2(arr_b)
            susceptibility0 = arrays_values[i] * N * (s_ave0 - m_ave0 ** 2)
            susceptibility1 = arrays_values[i] * N * (s_ave1 - m_ave1 ** 2)
            Cv = arrays_T2[i] * (functions.Average2(Ew) - functions.Average(Ew) ** 2) / num
            logging.info("{:>16.2f} {:>16.6f} {:>16.6f} {:>18.6f} {:>18.6f} {:>16.6f} {:>16.6f}".format(
                arrays_temperatures[i], m_ave0, m_ave1, susceptibility0, susceptibility1, Cv, t))
    elif init == "afm3":
        logging.info("{:>16} {:>16} {:>16}".format("Round", "magnetism0(e)", "magnetism1(e)"))
        latt = functions.OnesZNN(2, 4, Y_s, X_s)
        latt[:,[1,2],:,:,2] = -1
        m_ave0 = functions.Average(latt[:,[0,3],:,:,2])
        m_ave1 = functions.Average(latt[:,[1,2],:,:,2])
        logging.info("{:>16} {:>16.6} {:>16.6}".format(0, m_ave0, m_ave1))
        logging.info("{:>16} {:>16} {:>16} {:>18} {:>18} {:>16} {:>16}".format(
            "Temperature", "magnetism0(e)", "magnetism1(e)", "susceptibility0(e)", "susceptibility1(e)", "specific heat", "time(s)"))
        for i in range(lav):
            t, Nw, Ew = triangular_update.iteration3(latt, X_s, Y_s, Ja, Jb, Jc, Aa, Ab, arrays_values[i], nequilibrium, nworks)
            arr_a, arr_b = Nw[:,[0,3,4,7]], Nw[:,[1,2,5,6]]
            m_ave0 = functions.Average(arr_a)
            m_ave1 = functions.Average(arr_b)
            s_ave0 = functions.Average2(arr_a)
            s_ave1 = functions.Average2(arr_b)
            susceptibility0 = arrays_values[i] * N * (s_ave0 - m_ave0 ** 2)
            susceptibility1 = arrays_values[i] * N * (s_ave1 - m_ave1 ** 2)
            Cv = arrays_T2[i] * (functions.Average2(Ew) - functions.Average(Ew) ** 2) / num
            logging.info("{:>16.2f} {:>16.6f} {:>16.6f} {:>18.6f} {:>18.6f} {:>16.6f} {:>16.6f}".format(
                arrays_temperatures[i], m_ave0, m_ave1, susceptibility0, susceptibility1, Cv, t))
    else:
        print("Inconsistent parameters...")
