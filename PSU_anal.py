#!/bin/python3.8

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# read data in from csv file
# has to reformat it first!
# change all ',' --> '.'
df = pd.read_csv('./log_toRead.csv', sep=';')

plt.close('all')

class Channel:
    def __init__(self, voltage, current, power, vmax=0, pmax=0, currmax=0):
        self.V = voltage
        self.Curr = current
        self.P = power
        # This would create the time date in s values from 8ms steps
        self.t = np.arange(len(self.V))*8/1000.0
        self.fig = []
        self.Vmax = vmax
        self.Pmax = pmax
        self.Currmax = currmax

    def setplotlength(self, a=0, dur=0):
        """
            params:
            a - the beginning of the desiered plot [s]
            dur - length of the plot in [ms],
            8 [ms] due to the step size in the sampling of the PSU
        """
        # A bit ugly sollution, but it gives what we exactly need
        t0_loc = np.where([np.floor(self.t) == a][0])[0][0]
        # t0 = self.t[t0_loc]
        if 0 == dur:
            t1_loc = int(np.floor(len(self.t)))
        else:
            t1_loc = int(t0_loc + np.ceil(dur/8.0))

        return t0_loc, t1_loc

    def plot(self, t0=0, dur=0):

        t0, t1 = self.setplotlength(t0, dur)

        fig, (ax1, ax3) = plt.subplots(2, 1, constrained_layout=True)
        color = 'b'
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Voltage [V]', color=color)
        ax1.plot(self.t[t0:t1], self.V[t0:t1], color=color)
        # ax1.vlines(self.Vmax, t0, t1, color=color, linestyles='dashed', label='Vmax')
        ax1.tick_params(axis='y', labelcolor=color)

        ax2 = ax1.twinx()
        color = 'tab:red'
        ax2.tick_params(axis='y', labelcolor=color)
        ax2.set_ylabel('Current [A]', color=color)
        ax2.plot(self.t[t0:t1], self.Curr[t0:t1], color=color)
        # ax2.hlines(self.Currmax, t0, t1, color=color, linestyles='dashed', label='Currmax')

        color = 'k'
        ax3.set_xlabel('Time (s)')
        ax3.set_ylabel('Power [W]', color=color)
        ax3.plot(self.t[t0:t1], self.P[t0:t1], color)
        # ax3.hlines(self.Pmax, t0, t1, color=color, linestyles='dashed', label='Pmax')

        ax3.tick_params(axis='y', labelcolor=color)
        fig.suptitle("Power Consumption")
        fig.tight_layout()
        # fig.legend('show')
        fig.show()


Ch1 = Channel(df['U1[V]'], df['I1[A]'], df['P1[W]'], 25.2, 125, 5)
Ch2 = Channel(df['U2[V]'], df['I2[A]'], df['P2[W]'], 8.4, 155, 19)
Ch3 = Channel(df['U3[V]'], df['I3[A]'], df['P3[W]'], 12.5, 155, 8)
Ch4 = Channel(df['U4[V]'], df['I4[A]'], df['P4[W]'], 8.4, 155, 19)

T0, T1 = 0, 55000

Ch1.plot()
# Ch2.plot()
# Ch3.plot(T0, T1)
# Ch4.plot(T0, T1)


# t0, t1 = Ch3.setplotlength(55, 150)
# Testing for inside function --- Use unit test next time...
t0, dd = Ch3.setplotlength(44, 0)
print("start [loc]: " + str(t0) + "; " + "end: " + str(dd) + " [loc]")
print("Total length: " + str(len(Ch3.t)))
print("Lenght of new vector: " + str(dd))

print("===============")
t0, dd = Ch3.setplotlength()
print("start [loc]: " + str(t0) + "; " + "end: " + str(dd) + " [loc]")
print("Total length: " + str(len(Ch3.t)))
print("Lenght of new vector: " + str(dd))

# EOF
