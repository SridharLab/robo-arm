import cStringIO
import numpy
import scipy.signal as sig

FILENAME = "testpos.txt"
MEDIAN_FILTER_WIDTH = 19
START_INDEX = 500
NUM_COLS = 3
TIME_DELTA_VAL_THRESH = 50000
POS_DELTA_VAL_THRESH = 20
THROW_AWAY_LINES = 10


def clean_trial(raw_trial_string):
    infile = cStringIO.StringIO(raw_trial_string)
    data = []
    vals_m1 = numpy.array((0,0,0))
    for i,line in enumerate(infile):
        #print line,"->"
        vals = None
        try:
            cols = map(int,line.split(','))
            if len(cols) != NUM_COLS:
                raise ValueError("Bad column format.")
            vals = map(int,cols)
            new_vals = []
            #iterate through values
            for j,val in enumerate(vals):
                if val < 0:
                    #print "LINE #%d: Fixing negative position value in COL #%d." % (i,j)
                    val = vals_m1[j]
                new_vals.append(val)
            vals = numpy.array(new_vals)
            #compute change
            d_vals = vals - vals_m1
            new_vals = []
            for j,elems in enumerate(zip(vals,d_vals)):
                val, d_val = elems
                if (i > 1 and j == 0) and (d_val > TIME_DELTA_VAL_THRESH):
                    pass
                    # print vals_m1,vals,d_vals
                    #print "LINE #%d: Fixing TIME value change spike in COL #%d." % (i,j)
                    #val = vals_m1[j]
                elif (i > 1 and j >= 1) and (d_val > POS_DELTA_VAL_THRESH):
                    #print "LINE #%d: Fixing POS value change spike in COL #%d." % (i,j)
                    val = vals_m1[j]
                new_vals.append(val)
            vals = numpy.array(new_vals)
            #print vals
            vals_m1 = vals
            data.append(vals)
            #if i > 50:
            #    sys.exit()
        except ValueError, exc:
            print "****** BAD LINE ******"
            print "line #: %d" % i
            print "proceeding line: %r" % line
            print "next line:       %r" % infile.next()
            print "exception:       %s" % exc
    return data


