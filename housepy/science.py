""" Utility functions for working with data.
    NumPy and SciPy when possible.

    break out signal processing algorithms from machine learning? ie, any function that takes a time series?

"""
import time, math
import numpy as np
from collections import defaultdict
from log import log


def distance(a, b):
    """Euclidean distance between two sequences"""
    assert len(a) == len(b)    
    t = sum((a[i] - b[i])**2 for i in xrange(len(a)))
    return math.sqrt(t)


def hamming_distance(a, b):
    """Hamming distance between two sequences (edit distance that only allows substitutions)"""
    assert len(a) == len(b)
    return sum(ch_a != ch_b for ch_a, ch_b in zip(a, b))


def weighted_hamming_distance(a, b):
    """Hamming distance between two sequences (edit distance that only allows substitutions) preserving the degree of substitution"""
    assert len(a) == len(b)
    return sum(abs(ch_a - ch_b) for ch_a, ch_b in zip(a, b))
    
    
def lev_distance(a, b):
    """Levenshtein distance between two sequences (edit distance that allows substitutions, adds, and deletions)"""    
    if len(a) < len(b):
        return levenshtein(b, a)
    previous_row = xrange(len(b) + 1)
    for i, ch_a in enumerate(a):
        current_row = [i + 1]
        for j, ch_b in enumerate(b):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer than b
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (ch_a != ch_b)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]    
    
     
def scale(value, in_min, in_max, out_min=0.0, out_max=1.0, limit=False):
    """Scales a value between the given min/max to a new min/max, default 0.0-1.0. If limit is True, limit the value to the min/max."""
    value = (value - in_min) / (in_max - in_min)
    if out_min != 0.0 or out_max != 1.0:
        value *= out_max - out_min
        value += out_min
    if limit:    
        if value > out_max:
            value = out_max
        elif value < out_min:
            value = out_min        
    return value
    

def trendline(_l1, _l2=None):
    """Returns a  line (slope, intersect) that is the regression line given x,y values. x is assumed to be the index if only one list is provided."""   # np optimize?
    l1 = list(_l1)
    l2 = list(_l2) if _l2 else None
    n = len(l1) - 1
    sum_x = 0
    sum_y = 0
    sum_xx = 0
    sum_xy = 0
    for i in range(1, n + 1):
        if (l2):
            x = l1[i]
            y = l2[i]
        else:
            x = i
            y = l1[i]
        sum_x = sum_x + x
        sum_y = sum_y + y
        xx = math.pow(x, 2)
        sum_xx = sum_xx + xx
        xy = x*y
        sum_xy = sum_xy + xy
    try:    
        a = (-sum_x * sum_xy + sum_xx * sum_y) / (n * sum_xx - sum_x * sum_x)
        b = (-sum_x * sum_y + n * sum_xy) / (n * sum_xx - sum_x * sum_x)
    except ZeroDivisionError:
        a, b = 0, 0    
    return (b, a) # (slope, intersect)


def heading(pt0, pt1):
    """Returns the angle between two points, in degrees"""
    degrees = math.degrees(math.atan2(float(pt1[0] - pt0[0]), float(pt1[1] - pt0[1])))
    if degrees < 0:
        degrees += 360
    return degrees
    
    
def angular_difference(deg0, deg1):
    """Return the difference between two angles in positive degrees"""
    result = abs(deg0 - deg1)
    if result > 180:
        result = abs(360 - result)
    return result    
    
    
def geo_distance(pt0, pt1, miles=True):
    """Return the distance between two points, specified (lon, lat), in miles (or kilometers)"""
    LON, LAT = 0, 1
    pt0 = math.radians(pt0[LON]), math.radians(pt0[LAT])
    pt1 = math.radians(pt1[LON]), math.radians(pt1[LAT])
    lon_delta = pt1[LON] - pt0[LON]
    lat_delta = pt1[LAT] - pt0[LAT]
    a = math.sin(lat_delta / 2)**2 + math.cos(pt0[LAT]) * math.cos(pt1[LAT]) * math.sin(lon_delta / 2)**2    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = 6371 * c # radius of Earth in km
    if miles:
        d *= 0.621371192
    return d

def geo_project(pt):
    """ Project a (lon, lat) point to x,y space using the Mercator projection
        http://wiki.openstreetmap.org/wiki/Mercator#Python_Implementation        
    """    
    def merc_x(lon):
        r_major = 6378137.000
        return r_major * math.radians(lon)
    def merc_y(lat):
        if lat > 89.5:
            lat = 89.5
        if lat < -89.5:
            lat = -89.5
        r_major = 6378137.000
        r_minor = 6356752.3142
        temp = r_minor / r_major
        eccent = math.sqrt(1 - temp**2)
        phi = math.radians(lat)
        sinphi = math.sin(phi)
        con = eccent * sinphi
        com = eccent / 2
        con = ((1.0 - con) / (1.0 + con))**com
        ts = math.tan((math.pi / 2 - phi) / 2) / con
        y = 0-r_major * math.log(ts)
        return y 
    return merc_x(pt[0]), merc_y(pt[1])    

def smooth(signal, window_len=10, window='blackman'):
    """Smooth the data using a window with requested size"""
    signal = np.array(signal)
    if signal.ndim != 1:
        raise ValueError, "smooth only accepts 1 dimension arrays."
    if signal.size < window_len:
        raise ValueError, "input vector needs to be bigger than window size."
    if window_len < 3:
        return signal
    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError, "window is not 'flat', 'hanning', 'hamming', 'bartlett', or 'blackman'"
    s = np.r_[2 * signal[0] - signal[window_len:1:-1], signal, 2 * signal[-1] - signal[-1:-window_len:-1]]
    if window == 'flat': # moving average
        w = np.ones(window_len,'d')
    else:
        w = getattr(np, window)(window_len)
    y = np.convolve(w / w.sum(), s, mode='same')
    return y[window_len - 1:-window_len + 1]

def detect_peaks(y_axis, x_axis=None, lookahead=300, delta=0):
    # https://gist.github.com/1178136
    """
    Converted from/based on a MATLAB script at: 
    http://billauer.co.il/peakdet.html
    
    function for detecting local maximas and minmias in a signal.
    Discovers peaks by searching for values which are surrounded by lower
    or larger values for maximas and minimas respectively
    
    keyword arguments:
    y_axis -- A list containg the signal over which to find peaks
    x_axis -- (optional) A x-axis whose values correspond to the y_axis list
        and is used in the return to specify the postion of the peaks. If
        omitted an index of the y_axis is used. (default: None)
    lookahead -- (optional) distance to look ahead from a peak candidate to
        determine if it is the actual peak (default: 200) 
        '(sample / period) / f' where '4 >= f >= 1.25' might be a good value
    delta -- (optional) this specifies a minimum difference between a peak and
        the following points, before a peak may be considered a peak. Useful
        to hinder the function from picking up false peaks towards to end of
        the signal. To work well delta should be set to delta >= RMSnoise * 5.
        (default: 0)
            delta function causes a 20% decrease in speed, when omitted
            Correctly used it can double the speed of the function
    
    return -- two lists [max_peaks, min_peaks] containing the positive and
        negative peaks respectively. Each cell of the lists contains a tupple
        of: (position, peak_value) 
        to get the average peak value do: np.mean(max_peaks, 0)[1] on the
        results to unpack one of the lists into x, y coordinates do: 
        x, y = zip(*tab)
    """
    def _datacheck_peakdetect(x_axis, y_axis):
        if x_axis is None:
            x_axis = range(len(y_axis))        
        if len(y_axis) != len(x_axis):
            raise (ValueError, 'Input vectors y_axis and x_axis must have same length')        
        # needs to be a numpy array
        y_axis = np.array(y_axis)
        x_axis = np.array(x_axis)
        return x_axis, y_axis    
    max_peaks = []
    min_peaks = []
    dump = []   #Used to pop the first hit which almost always is false       
    # check input data
    x_axis, y_axis = _datacheck_peakdetect(x_axis, y_axis)
    # store data length for later use
    length = len(y_axis)
    if lookahead < 1:
        raise ValueError, "Lookahead must be '1' or above in value"
    if not (np.isscalar(delta) and delta >= 0):
        raise ValueError, "delta must be a positive number"    
    # maxima and minima candidates are temporarily stored in
    # mx and mn respectively
    mn, mx = np.Inf, -np.Inf    
    # Only detect peak if there is 'lookahead' amount of points after it
    for index, (x, y) in enumerate(zip(x_axis[:-lookahead], y_axis[:-lookahead])):
        if y > mx:
            mx = y
            mxpos = x
        if y < mn:
            mn = y
            mnpos = x        
        # look for max
        if y < mx-delta and mx != np.Inf:
            #Maxima peak candidate found
            #look ahead in signal to ensure that this is a peak and not jitter
            if y_axis[index:index+lookahead].max() < mx:
                max_peaks.append([mxpos, mx])
                dump.append(True)
                #set algorithm to only find minima now
                mx = np.Inf
                mn = np.Inf
                if index+lookahead >= length:
                    #end is within lookahead no more peaks can be found
                    break
                continue
            #else:  #slows shit down this does
            #    mx = ahead
            #    mxpos = x_axis[np.where(y_axis[index:index+lookahead]==mx)]        
        # look for min
        if y > mn+delta and mn != -np.Inf:
            #Minima peak candidate found 
            #look ahead in signal to ensure that this is a peak and not jitter
            if y_axis[index:index+lookahead].min() > mn:
                min_peaks.append([mnpos, mn])
                dump.append(False)
                #set algorithm to only find maxima now
                mn = -np.Inf
                mx = -np.Inf
                if index+lookahead >= length:
                    #end is within lookahead no more peaks can be found
                    break
            #else:  #slows shit down this does
            #    mn = ahead
            #    mnpos = x_axis[np.where(y_axis[index:index+lookahead]==mn)]
    # Remove the false hit on the first value of the y_axis
    try:
        if dump[0]:
            max_peaks.pop(0)
        else:
            min_peaks.pop(0)
        del dump
    except IndexError:
        # no peaks were found, should the function return empty lists?
        pass        
    return [max_peaks, min_peaks]    

def get_sampling_rate(ts, max_rate=10): # 10hz is quantized to 100ms
    """Find the slowest sampling rate using the gcd of the gap between datapoints, in hz, quantized to max_rate"""
    gaps = []
    min_gap = 1.0 / max_rate
    # log.debug("MIN GAP %s" % min_gap)
    for i in xrange(len(ts)):
        if i == 0:
            continue
        gap = float(ts[i]) - float(ts[i-1])
        gap = round(gap / min_gap) * min_gap
        if gap not in gaps:
            gaps.append(gap)
    # log.debug(gaps)
    min_gap = gcdm(*gaps)      
    # log.debug("MIN GAP %s" % min_gap)  
    sampling_rate = float(1.0 / min_gap)
    return sampling_rate

def upsample(signal, skip):
    log.info("Resampling x %s" % skip)    
    assert type(skip) == int and skip > 1
    result = [None] * ((len(signal) - 1) * skip)
    log.info("--> new length: %s" % (len(result)))    
    for i, v in enumerate(signal):
        if i == len(signal) - 1:
            result[-1] = v
            break
        v_ = signal[i+1]
        delta = v_ - v
        for j in xrange(skip):
            f = (i * skip) + j
            result[f] = v + ((delta / skip) * j)
    return result    

def downsample(signal, factor):
    try:
        from scipy.stats import nanmean as mean
    except ImportError:
        import np.mean as mean    
    signal = np.array(signal)
    xs = signal.shape[0]
    signal = signal[:xs-(xs % int(factor))]
    result = mean(np.concatenate([[signal[i::factor] for i in range(factor)]]), axis=0)
    return result

def filter_deviations(signal, num_devs=2, positive_only=False):
    average = np.average(signal)
    deviation = np.std(signal)
    for v, value in enumerate(signal):
        delta = value - average if positive_only else abs(value - average)
        if delta > deviation * num_devs:
            if v == 0:
                signal[v] = average
            else:
                signal[v] = signal[v-1]
    return signal

def gcd(a, b):
    """Return greatest common divisor using Euclid's Algorithm."""
    while b:      
        a, b = b, a % b
    return a

def gcdm(*args):
    """Return gcm of args."""   
    return reduce(gcd, args)

def lcm(a, b):
    """Return lowest common multiple."""
    return a * b / gcd(a, b)

def lcmm(*args):
    """Return lcm of args."""   
    return reduce(lcm, args)


####    


# improve with numpy?
def histogram(l):   # list of ints < 256
    d = defaultdict(int)
    for x in l:
        d[x] += 1    
    return [d[x] for x in xrange(256)]

# improve with numpy?
def autocontrast(l, cutoff=0, ignore=None): # list of ints < 256            # separate cutoff hi and lo
    "Maximize image contrast, based on histogram"
    hist = histogram(l)
    lut = []
    for layer in range(0, len(hist), 256):
        h = hist[layer:layer+256]
        if ignore is not None:
            # get rid of outliers
            try:
                h[ignore] = 0
            except TypeError:
                # assume sequence
                for ix in ignore:
                    h[ix] = 0
        if cutoff:
            # cut off pixels from both ends of the histogram
            # get number of pixels
            n = 0
            for ix in range(256):
                n = n + h[ix]
            # remove cutoff% pixels from the low end
            cut = n * cutoff / 100
            for lo in range(256):
                if cut > h[lo]:
                    cut = cut - h[lo]
                    h[lo] = 0
                else:
                    h[lo] = h[lo] - cut
                    cut = 0
                if cut <= 0:
                    break
            # remove cutoff% samples from the hi end
            # cut = n * cutoff / 100
            # for hi in range(255, -1, -1):
            #     if cut > h[hi]:
            #         cut = cut - h[hi]
            #         h[hi] = 0
            #     else:
            #         h[hi] = h[hi] - cut
            #         cut = 0
            #     if cut <= 0:
            #         break
        # find lowest/highest samples after preprocessing
        for lo in range(256):
            if h[lo]:
                break
        for hi in range(255, -1, -1):
            if h[hi]:
                break
        if hi <= lo:
            # don't bother
            lut.extend(range(256))
        else:
            scale = 255.0 / (hi - lo)
            offset = -lo * scale
            for ix in range(256):
                ix = int(ix * scale + offset)
                if ix < 0:
                    ix = 0
                elif ix > 255:
                    ix = 255
                lut.append(ix)
    return [lut[v] for i, v in enumerate(l)]

def autocorrelate(signal, fs=1, maxlags=None, normed=True, full=False): 
    """ 
    Get the auto-correlation function of a signal.

    Parameters
    ----------

    signal : a one dimensional array
    maxlags: the maximum number of time delay for which 
    to compute the auto-correlation.
    normed : a boolean option. If true the normalized 
    auto-correlation function is returned.
    fs : the sampling frequecy of the data
    full : if True also a time array is returned for 
    plotting purposes

    Returns
    -------
    rho : the auto-correlation function
    t : a time array. Only if full==True

    Example
    -------

    t = np.arange(2**20) / 1000.0
    signal = np.sin(2*np.pi*100*t)
    rho = acorr(signal, maxlags=1000)

    """ 

    if not maxlags: 
        maxlags = len(signal) / 2

    if maxlags > len(signal) / 2: 
        maxlags = len(signal) / 2

    fs = float(fs)

    # pad with zeros
    x = np.hstack( (signal, np.zeros(len(signal))) )

    # compute FFT trasform of signal
    sp = np.fft.rfft( x ) 
    tmp = np.empty_like(sp)
    tmp = np.conj(sp, tmp)
    tmp = np.multiply(tmp, sp, tmp)
    rho = np.fft.irfft( tmp )

    # divide by array length
    rho = np.divide(rho, len(signal), rho)[:maxlags] 

    # obtain the unbiased estimate
    tmp = len(signal) / ( len(signal) - np.arange(maxlags, dtype=np.float64) ) 
    rho = np.multiply(rho, tmp, rho)


    if normed:
        rho = rho / rho[0]

    if full:
        t = np.arange(maxlags, dtype=np.float32) / fs
        return t, rho
    else:
        return rho
        

# threshold

# compress

def normalize(signal):
    """Normalize an array of values"""
    signal = np.array(signal).astype('float')
    signal -= np.min(signal)
    signal /= np.max(signal)
    return signal


def derivative(signal):
    """Return a signal that is the derivative function of a given signal"""
    def f(x):
        x = int(x)
        return signal[x]
    def df(x, h=0.1e-5):
        return (f(x + h * 0.5) - f(x - h * 0.5)) / h
    return [df(x) for x in xrange(len(signal))]


def integral(signal):
    """Return a signal that is the integral function of a given signal"""
    result = []
    v = 0.0    
    for i in xrange(len(signal)):
        v += signal[i]
        result.append(v)
    return result

# hierarchical clustering

# svm


class KMeans(object):
    """KMeans clustering"""

    def __init__(self, clusters=3):
        from scipy.cluster.vq import vq, kmeans, whiten
        self.clusters = int(clusters)
        
    def learn(self, raw_vectors):  
        """Cluster a set of vectors and return an array of cluster indexes"""  
        vectors = whiten(np.array(raw_vectors))                         # normalize data
        self.centroids, variance = kmeans(vectors, self.clusters)       # generate clusters
        codes, distortion = vq(vectors, self.centroids)                 # assign code indexes            
        return codes
        
    def find(self, vector):
        """Classify a vector according to learned clusters"""
        code, distortion = vq([np.array(vector)], self.centroids)
        return code

        
class ClusterTree(object):
    """Hierarchical agglomerative clustering"""

    @staticmethod
    def build(vectors, distance_f=distance):  # use geo_distance for geography
        """Build a ClusterTree on the set of input vectors and a given distance function"""
        distance_f = distance_f
        vectors = vectors
        root = None        
        log.info("ClusterTree learning %d vectors..." % len(vectors))

        distances = {}
        current_cluster_id = -1

        # start with every feature in its own cluster
        cluster = [ClusterTree(vectors[i], id=i) for i in xrange(len(vectors))]

        while len(cluster) > 1:

            # find the smallest distance between pairs            
            closest_pair = (0, 1)
            min_distance = distance_f(cluster[0].vector, cluster[1].vector)
            for i in xrange(len(cluster)):
                for j in xrange(i + 1, len(cluster)):
                    if (cluster[i].id, cluster[j].id) not in distances:     # cache calcs
                        distances[(cluster[i].id, cluster[j].id)] = distance_f(cluster[i].vector, cluster[j].vector)        
                    d = distances[(cluster[i].id, cluster[j].id)]        
                    if d < min_distance:
                        min_distance = d
                        closest_pair = (i, j)

            # create new cluster with a merged vector that is the average between clusters
            average_vector = [(cluster[closest_pair[0]].vector[i] + cluster[closest_pair[1]].vector[i]) / 2.0 for i in xrange(len(cluster[0].vector))]
            new_cluster = ClusterTree(average_vector, id=current_cluster_id, left=cluster[closest_pair[0]], right=cluster[closest_pair[1]])
            current_cluster_id = current_cluster_id - 1

            # remove the clusters that have been agglomerated and add the new one to the cluster list
            del cluster[closest_pair[1]]
            del cluster[closest_pair[0]]
            cluster.append(new_cluster)

        # just one cluster remaining
        log.info("--> done. Calculating radii...")

        # radius is the furthest leaf node from a cluster's centroid
        ## this is really expensive (too expensive)        
        def calc_radii(master, cluster=None):               
            if cluster is None:
                master.radius_calculated = True        
                calc_radii(master, master)                
            elif cluster.id >= 0:
                # leaf
                d = distance_f(master.vector, cluster.vector)
                if d > master.radius:
                    master.radius = d                
            else:    
                # branches
                if cluster.left is not None: 
                    calc_radii(master, cluster.left)
                    if not cluster.left.radius_calculated:
                        calc_radii(cluster.left)
                if cluster.right is not None: 
                    calc_radii(master, cluster.right)
                    if not cluster.right.radius_calculated:                        
                        calc_radii(cluster.right)
        calc_radii(cluster[0], cluster[0])
        log.info("--> done")
        
        return cluster[0]

    def __init__(self, vector, id=None, left=None, right=None):
        self.left = left
        self.right = right
        self.vector = vector
        self.id = id
        self.radius = 0.0
        self.radius_calculated = False

    def get_order(self):
        """Return a list of indexes for how the input vectors are ordered in a depth first enumeration of the cluster, for ordering by likeness"""
        ids = self.get_leaf_ids()
        inverse = zip(range(len(ids)), ids)
        inverse.sort(key=lambda t: t[1])
        inverse, nop = zip(*inverse)    
        return inverse        

    def get_leaf_ids(self):
        """Perform a depth first listing of ids for elements"""
        if self.id >= 0:
            # leaf
            return [self.id]
        else:
            # branches
            left_branch = []
            right_branch = []
            if self.left is not None: 
                left_branch = self.left.get_leaf_ids()
            if self.right is not None: 
                right_branch = self.right.get_leaf_ids()
            return left_branch + right_branch  

    def get_pruned(self, max_radius):
        """Prune cluster until we have a set of sub-clusters with a maximum radius, return as a list of primary branches"""
        if self.radius <= max_radius:
            return [self]
        else:
            left_branch = []
            right_branch = []
            if self.left is not None:
                left_branch = self.left.get_pruned(max_radius)
            if self.right is not None:
                right_branch = self.right.get_pruned(max_radius)
            return left_branch + right_branch   
            
    def draw(self, n=0):
        """Indent to make a hierarchy layout"""
        ## I really want this to draw the complete lines
        output = []
        for i in xrange(n-1):
            # output.append("| ")
            output.append("  ")
        if n:   
            output.append("|\n") 
            for i in xrange(n-1):
                # output.append("| ")
                output.append("  ")
            output.append("|_")
        if self.id < 0:
            # negative id means that this is branch
            output.append("%f %s\n" % (self.radius, self.vector))
        else:
            # positive id means that this is an endpoint
            output.append("<%d> %s\n" % (self.id, self.vector))
        # now print the right and left branches
        if self.left != None:
            output.append(self.left.draw(n+1))
        if self.right != None:
            output.append(self.right.draw(n+1))
        output = "".join(output)    
        return output                             

    def __repr__(self):
        return "<Cluster %d %f %s>" % (self.id, self.radius, str(self.vector))        



class SOM(object):
    """
        Self-organizing map
        
        print("One-dimensional SOM over two-dimensional uniform square")
        som = SOM(100)
        samples = np.random.random((10000, 2))
        som.learn(samples)
        som.display()

        print("Two-dimensional SOM over two-dimensional uniform square")
        som = SOM(10, 10)
        samples = np.random.random((10000, 2))
        som.learn(samples)
        som.display()

        print("Two-dimensional SOM over two-dimensional non-uniform disc")
        som = SOM(10, 10)
        samples = np.random.normal(loc=.5, scale=.2, size=(10000, 2))
        som.learn(samples)
        som.display()

        print("Two-dimensional SOM over two-dimensional non-uniform ring")
        som = SOM(10, 10)
        angles = np.random.random(10000) * 2 * np.pi
        radius = 0.25 + np.random.random(10000) * .25
        samples = np.zeros((10000, 2))
        samples[:,0] = 0.5 + radius * np.cos(angles)
        samples[:,1] = 0.5 + radius * np.sin(angles)
        som.learn(samples)
        som.display()
                
    """

    def __init__(self, *args):
        """Initialize som"""
        log.info("SOM()")
        args = list(args)
        args.append(2)
        self.nodes = np.zeros(args)
        self.reset()

    def reset(self):
        """Reset weights"""
        log.info("SOM.reset")        
        self.nodes = np.random.random(self.nodes.shape)

    def learn(self, samples, epochs=10000, sigma=(10, 0.001), lrate=(0.5, 0.005)):
        """Learn samples"""
        log.info("SOM.learn")                
        learn_start = time.clock()
        
        sigma_i, sigma_f = sigma
        lrate_i, lrate_f = lrate

        for i in range(epochs):
            # adjust learning rate and neighborhood
            t = i / float(epochs)
            lrate = lrate_i * (lrate_f / float(lrate_i))**t
            sigma = sigma_i * (sigma_f / float(sigma_i))**t

            # get random sample
            index = np.random.randint(0, samples.shape[0])
            data = samples[index]

            # get index of nearest node (minimum distance)
            D = ((self.nodes - data)**2).sum(axis=-1)
            winner = np.unravel_index(np.argmin(D), D.shape)

            # generate a Gaussian centered on winner
            G = self._gaussian(D.shape, winner, sigma)
            G = np.nan_to_num(G)

            # move nodes towards sample according to Gaussian 
            delta = self.nodes - data
            for i in range(self.nodes.shape[-1]):
                self.nodes[...,i] -= lrate * G * delta[...,i]
                
        learn_end = time.clock() - learn_start
        log.info("--> completed in %fs" % learn_end)        

    def find(self, data):
        """Get index of nearest node (minimum distance)"""
        D = ((self.nodes - data)**2).sum(axis=-1)
        winner = np.unravel_index(np.argmin(D), D.shape)[0]
        return winner
        
    def _gaussian(self, shape, center, sigma=0.5):
        def g(x):
            return np.exp(-x**2 / sigma**2)
        return self._fromdistance(g, shape, center)

    def _fromdistance(self, fn, shape, center=None, dtype=float):
        def distance(*args):
            d = 0
            for i in range(len(shape)):
                d += ((args[i] - center[i]) / float(max(1, shape[i] - 1)))**2
            return np.sqrt(d) / np.sqrt(len(shape))
        if center == None:
            center = np.array(list(shape))//2
        return fn(np.fromfunction(distance, shape, dtype=dtype))
        
    def display(network):
        """Display with matplotlib"""
        import matplotlib
        import matplotlib.pyplot as plt
        try:
            from voronoi import voronoi
        except:
            voronoi = None        
        fig = plt.figure(figsize=(10,10))
        axes = fig.add_subplot(1,1,1)
        # Draw samples
        x, y = samples[:,0], samples[:,1]
        plt.scatter(x, y, s=1.0, color='b', alpha=0.1, zorder=1)
        # Draw network
        x, y = network.nodes[...,0], network.nodes[...,1]
        if len(network.nodes.shape) > 2:
            for i in range(network.nodes.shape[0]):
                plt.plot (x[i,:], y[i,:], 'k', alpha=0.85, lw=1.5, zorder=2)
            for i in range(network.nodes.shape[1]):
                plt.plot (x[:,i], y[:,i], 'k', alpha=0.85, lw=1.5, zorder=2)
        else:
            plt.plot (x, y, 'k', alpha=0.85, lw=1.5, zorder=2)
        plt.scatter (x, y, s=50, c='w', edgecolors='k', zorder=3)
        if voronoi is not None:
            segments = voronoi(x.ravel(), y.ravel())
            lines = matplotlib.collections.LineCollection(segments, color='0.65')
            axes.add_collection(lines)
        plt.axis([0,1,0,1])
        plt.xticks([]), plt.yticks([])
        plt.show()
      
