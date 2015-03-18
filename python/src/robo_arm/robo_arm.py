import time, glob
import serial, numpy
from trial_utils import clean_trial
from matplotlib import pyplot as plt

FILENAME = "testpos.txt"
DEFAULT_BAUDRATE = 115200
#DEFAULT_BAUDRATE = 57600


class RoboArm(object):
    def __init__(self, port, **kwargs):
        self._ser = serial.Serial(port, **kwargs)
        self._ser.flush()
        self._last_trial = None
        self._last_start_timestamp = None
        self._last_end_timestamp   = None
        self._last_procdata = None

    def record_trial(self, duration = None):
        self._ser.flushInput()
        buff = []
        t0 = time.time()
        t  = time.time()
        try:
            self._last_start_timestamp = t
            is_active = True
            while is_active:
                t  = time.time()
                line = self._ser.readline().strip()
                print line
                buff.append(line)
                if not duration is None:
                    is_active = (t-t0 < duration)
                #print is_active, t-t0
        except KeyboardInterrupt:
            pass
        self._last_start_timestamp = t
        buff.append("") #final line termination
        self._last_trial = "\n".join(buff)

    def save_raw_trial(self, filename):
        outfile = open(filename,'w')
        outfile.write(self._last_trial)
        outfile.close()

    def load_raw_trial(self, filename):
        infile = open(filename,'r')
        self._last_trial = infile.read()
        infile.close()

    def process_trial(self):
        data = clean_trial(self._last_trial)
        D = numpy.array(data)
        #D = D[START_INDEX:,]
        t  = D[:,0]
        P1 = D[:,1]
        P2 = D[:,2]
        #P1= sig.medfilt(P1,MEDIAN_FILTER_WIDTH)
        #D = numpy.vstack((t,P1,P2)).transpose()
        self._last_procdata = D
        return t, P1, P2
    
    def plot_trial(self):
        D = self._last_procdata
        t  = D[:,0]
        P1 = D[:,1]
        P2 = D[:,2]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(t,P1,'.-')
        ax.plot(t,P2,'.-')
        plt.show()

def get_interface():
    port = glob.glob("/dev/ttyU*")[0]
    return RoboArm(port, baudrate = DEFAULT_BAUDRATE)

################################################################################
# TEST CODE
################################################################################
if __name__ == "__main__":
    robo = get_interface()
    robo.load_raw_trial("test_trial.txt")
    robo.process_trial()
    robo.plot_trial()
