import sys
import math
import random
import subprocess
import time


def main():
    
    
    # How many points are in our dataset?
    num_points = 100000
    
    # For each of those points how many dimensions do they have?
    dimensions = 7
    
    # Bounds for the values of those points in each dimension
    lower = 20
    upper = 80
    
    # The K in k-means. How many clusters do we assume exist?
    num_clusters = 4
    
    # When do we say the optimization has 'converged' and stop updating clusters
    opt_cutoff = 0.1
    
    # Generate some points
    points = [makeRandomPoint(ii, lower, upper) for ii in xrange(num_points)]


    while num_points >= 6250:
        # Cluster those data!
        f = open('trainedShift.txt','a')
        f.write("\n\n\nData size : %s\n"%num_points)
        f.close()
        f = open('trainedTime.txt','a')
        f.write("\n\n\nData size : %s\n"%num_points)
        f.close()
        f = open('trainEuclid.txt','a')
        f.write("\n\n\nData size : %s\n"%num_points)
        f.close()
        f = open('trainedIteration.txt','a')
        f.write("\n\n\nData size : %s\n"%num_points)
        f.close()
        f = open('testTrainIteration.txt','a')
        f.write("\n\n\nData size : %s\n"%num_points)
        f.close()
        print "Data size : ", num_points
        clusters = kmeans(points, num_clusters, opt_cutoff, num_points)
        num_points = num_points/2


class Point:
    '''
    A point in n dimensional space
    '''
    def __init__(self, coords):
        '''
        coords - A list of values, one per dimension
        '''

        
        self.coords = coords
        self.n = len(coords)
        # print "coords ", self.coords 
        # print "n ", self.n 
        
    def __repr__(self):
        return str(self.coords)

class Cluster:
    '''
    A set of points and their centroid
    '''
    
    def __init__(self, points):
        '''
        points - A list of point objects
        '''
        
        if len(points) == 0: raise Exception("ILLEGAL: empty cluster")
        # The points that belong to this cluster
        self.points = points
        
        # The dimensionality of the points in this cluster
        self.n = points[0].n
        
        # Assert that all points are of the same dimensionality
        for p in points:
            if p.n != self.n: raise Exception("ILLEGAL: wrong dimensions")
            
        # Set up the initial centroid (this is usually based off one point)
        self.centroid = self.calculateCentroid()
        
    def __repr__(self):
        '''
        String representation of this object
        '''
        return str(self.points)
    
    def update(self, points):
        '''
        Returns the distance between the previous centroid and the new after
        recalculating and storing the new centroid.
        '''
        old_centroid = self.centroid
        self.points = points
        self.centroid = self.calculateCentroid()
        shift = getDistance(old_centroid, self.centroid) 
        return shift
    
    def calculateCentroid(self):
        '''
        Finds a virtual center point for a group of n-dimensional points
        '''
        numPoints = len(self.points)
        # Get a list of all coordinates in this cluster
        coords = [p.coords for p in self.points]
        # Reformat that so all x's are together, all y'z etc.
        unzipped = zip(*coords)
        # Calculate the mean for each dimension
        centroid_coords = [math.fsum(dList)/numPoints for dList in unzipped]
        
        return Point(centroid_coords)

def kmeans(points, k, cutoff,num_points):
    
    # Pick out k random points to use as our initial centroids
    num_training = int(math.floor(num_points*0.2))
    #print num_training
    training = random.sample(points, num_training)
    #initial = random.sample(training,k)

    initial1 = Point([33.0, 59.15, 39.73731582, 61.53846154, 20.0, 24.71978663, 28.18181818])
    initial2 = Point([71.0, 32.0, 78.0814721, 20.0, 40.0, 35.32555426, 73.5828877])
    initial3 = Point([70.0, 25.7, 36.05547036, 21.53846154, 40.0, 34.94249042, 79.35828877])
    initial4 = Point([53.0, 35.15, 77.25581705, 35.38461538, 40.0, 37.74095683, 52.56684492])


    initial = []
    initial.append(initial1)
    initial.append(initial2)
    initial.append(initial3)
    initial.append(initial4)


    trainedCentroid =[]

    
    p1=[]
    p2=[]
    p3=[]
    p4=[]

    #print "kmeans taining centroid ", initial


    
    # Create k clusters using those centroids
    clusters = [Cluster([p]) for p in initial]
    totalEuclid =[]
    totalEuclidDistance =0.0
    # Loop through the dataset until the clusters stabilize
    loopCounter = 0
    while True:
        # Create a list of lists to hold the points in each cluster
        lists = [ [] for c in clusters]
        clusterCount = len(clusters)
        #totalEuclidDistance =0.0
        
        # Start counting loops
        loopCounter += 1
        # For every point in the dataset ...
        for p in training:
            # Get the distance between that point and the centroid of the first
            # cluster.
            smallest_distance = getDistance(p, clusters[0].centroid)
            
            # Set the cluster this point belongs to
            clusterIndex = 0
        
            # For the remainder of the clusters ...
            for i in range(clusterCount - 1):
                # calculate the distance of that point to each other cluster's
                # centroid.
                distance = getDistance(p, clusters[i+1].centroid)
                # If it's closer to that cluster's centroid update what we
                # think the smallest distance is, and set the point to belong
                # to that cluster
                if distance < smallest_distance:
                    smallest_distance = distance
                    clusterIndex = i+1
            #totalEuclidDistance = totalEuclidDistance + smallest_distance        
            lists[clusterIndex].append(p)            
            
        # Set our biggest_shift to zero for this iteration
        biggest_shift = 0.0
        
        # As many times as there are clusters ...
        for i in range(clusterCount):
            # Calculate how far the centroid moved in this iteration
            shift = clusters[i].update(lists[i])
            # Keep track of the largest move from all cluster centroid updates
            biggest_shift = max(biggest_shift, shift)
            
        # If the centroids have stopped moving much, say we're done!
        if biggest_shift < cutoff:
            f = open('trainedIteration.txt','a')
            f.write("%s,"%loopCounter)
            f.close()
            print "Converged after %s iterations" % loopCounter
            break

    trainedCentroid.append(clusters[0].centroid)
    trainedCentroid.append(clusters[1].centroid)
    trainedCentroid.append(clusters[2].centroid)
    trainedCentroid.append(clusters[3].centroid)

    start_time = time.time()
    newclusters = [Cluster([p]) for p in trainedCentroid]
    totalEuclid =[]
    totalEuclidDistance =0.0
    # Loop through the dataset until the clusters stabilize
    loopCounter = 0
    while True:
        # Create a list of lists to hold the points in each cluster
        lists = [ [] for c in newclusters]
        clusterCount = len(newclusters)
        totalEuclidDistance =0.0
        
        # Start counting loops
        loopCounter += 1
        # For every point in the dataset ...
        for p in points:
            # Get the distance between that point and the centroid of the first
            # cluster.
            smallest_distance = getDistance(p, newclusters[0].centroid)
            
            # Set the cluster this point belongs to
            clusterIndex = 0
        
            # For the remainder of the clusters ...
            for i in range(clusterCount - 1):
                # calculate the distance of that point to each other cluster's
                # centroid.
                distance = getDistance(p, newclusters[i+1].centroid)
                # If it's closer to that cluster's centroid update what we
                # think the smallest distance is, and set the point to belong
                # to that cluster
                if distance < smallest_distance:
                    smallest_distance = distance
                    clusterIndex = i+1
            totalEuclidDistance = totalEuclidDistance + smallest_distance        
            lists[clusterIndex].append(p)            
            
        # Set our biggest_shift to zero for this iteration
        biggest_shift = 0.0
        
        # As many times as there are clusters ...
        for i in range(clusterCount):
            # Calculate how far the centroid moved in this iteration
            shift = newclusters[i].update(lists[i])
            # Keep track of the largest move from all cluster centroid updates
            biggest_shift = max(biggest_shift, shift)
            if i==0:
                p1.append(shift)
            if i == 1:
                p2.append(shift)
            if i == 2:
                p3.append(shift)
            if i == 3:
                p4.append(shift)

            
        # If the centroids have stopped moving much, say we're done!
        if biggest_shift < cutoff:
            f = open('testTrainIteration.txt','a')
            f.write("%s,"%loopCounter)
            f.close()
            print "Converged after %s iterations" % loopCounter
            break
        totalEuclid.append(totalEuclidDistance)
        f = open('trainEuclid.txt','a')
        f.write("%s,"%loopCounter)
        f.write("%s\n"%totalEuclidDistance)
        f.close()    
 
    f = open('trainedShift.txt','a')
    f.write("Iteration : %s\n"%loopCounter)
    f.write("%s\n"%p1)
    f.write("%s\n"%p2)
    f.write("%s\n"%p3)
    f.write("%s\n"%p4)
    f.close()

    execTime =time.time() - start_time
    print "Exec time = ", time.time() - start_time
    f = open('trainedTime.txt','a')
    f.write("%s,"%execTime)
    f.close()


    return newclusters

def getDistance(a, b):
    '''
    Euclidean distance between two n-dimensional points.
    Note: This can be very slow and does not scale well
    '''
    if a.n != b.n:
        raise Exception("ILLEGAL: non comparable points")

    euclid_distance_squared=0
    for aa in xrange (a.n):
        euclid_distance_squared= euclid_distance_squared + (a.coords[aa]- b.coords[aa])**2
        
    euclid_distance = euclid_distance_squared**0.5


    return euclid_distance

def makeRandomPoint(ii, lower, upper):
    '''
    Returns a Point object with n dimensions and values between lower and
    upper in each of those dimensions
    '''
    # p = Point([random.uniform(lower, upper) for i in range(n)])
    # print p , " break "
    # p = []
    # for line in open("testBank.csv"):
    #     p = line.rstrip('\r\n').split(',')   # strip new-line characters and split on column delimiter
    #     p = [float(pin.strip()) for pin in p] 
    #     Point(p)
    #     # print p, " break "   # strip extra whitespace off data items
    #     p.append(p)
    #     p = Point([p])

    # return p
    fp = open("normalizedDataset4.csv")
    for i, line in enumerate(fp):
        if i == ii:
            p = line.rstrip('\r\n').split(',')   # strip new-line characters and split on column delimiter
            p = [(float(pin.strip())) for pin in p] 
            p = Point(p)
            break
    fp.close()
    return p




if __name__ == "__main__": 
    main()