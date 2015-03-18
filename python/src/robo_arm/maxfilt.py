# coding: utf-8
import numpy as np

def maxfilt(Y, X = None, window_size=3):
    w = window_size
    xl = w//2
    xr = w//2 + 1
    Y2 = []
    for i in range(xl, len(Y) - xr):
        y_win = Y[i - xl:i + xr]
        y2 = y_win.max()
        Y2.append(y2)
    if X is None:
        return np.array(Y2)
    else:
        X2 = X[w//2:-w//2]
        return X2, np.array(Y2)


################################################################################
# TEST CODE
if __name__ == "__main__":
    from matplotlib import pyplot as plt
    X = np.linspace(0,1,100)
    #Y = abs(sin(50*X))
    D = np.loadtxt("data/quick-flex-2X_WIT-ND_Tyler_Kendall850-Foam-Electrodes_han1_G24_30sec_250SPS_bt_10ft_ADS1299_n2.csv", delimiter=",")
    C1 = D[:,0]
    plt.plot(C1,".-")
