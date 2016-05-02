import sys
import math
import random
import subprocess
import time


def main():
    
    
    # How many points are in our dataset?
    num_points =  12500
    
    # For each of those points how many dimensions do they have?
    dimensions = 4
    
    # Bounds for the values of those points in each dimension
    lower = 20
    upper = 72998
    
    # The K in k-means. How many clusters do we assume exist?
    num_clusters = 7
    
    # When do we say the optimization has 'converged' and stop updating clusters
    opt_cutoff = 0.1
    
    # Generate some points
    points = [makeRandomPoint(ii, lower, upper) for ii in xrange(num_points)]



    while num_points >= 12500:
        # Cluster those data!
        f = open('shiftFile1.txt','a')
        f.write("\n\n\nData size : %s\n"%num_points)
        f.close()
        f = open('timeFile1.txt','a')
        f.write("\n\n\nData size : %s\n"%num_points)
        f.close()
        f = open('euclidFile1.txt','a')
        f.write("\n\n\nData size : %s\n"%num_points)
        f.close()
        f = open('iterationFile1.txt','a')
        f.write("\n\n\nData size : %s\n"%num_points)
        f.close()
        print num_points
        clusters = kmeans(points, num_clusters, opt_cutoff)
        num_points = num_points/2

    # Print our clusters
    clust1 =[]
    clust2 =[]
    clust3 =[]
    clust4 =[]
    for i,c in enumerate(clusters):
        for p in c.points:
            if i==0:
                clust1.append(p)
            if i==1:
                clust2.append(p)
            if i==2:
                clust3.append(p)
            if i==3:
                clust4.append(p)
    print "Length of cluster 1", len(clust1)
    print "Length of cluster 2", len(clust2)
    print "Length of cluster 3", len(clust3)
    print "Length of cluster 4", len(clust4)

            #print " Cluster: ", i, "\t Point :", p


class Point:
    
    def __init__(self, coords):
        
        self.coords = coords
        self.n = len(coords)
        # print "coords ", self.coords 
        # print "n ", self.n 
        
    def __repr__(self):
        return str(self.coords)

class Cluster:

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

        return str(self.points)
    
    def update(self, points):
       
        old_centroid = self.centroid
        self.points = points
        self.centroid = self.calculateCentroid()
        shift = getDistance(old_centroid, self.centroid) 
        return shift
    
    def calculateCentroid(self):

        numPoints = len(self.points)
        # Get a list of all coordinates in this cluster
        coords = [p.coords for p in self.points]
        # Reformat that so all x's are together, all y'z etc.
        unzipped = zip(*coords)
        # Calculate the mean for each dimension
        centroid_coords = [math.fsum(dList)/numPoints for dList in unzipped]
        
        
        # newCentroid = []
        # for nList in unzipped:
        #     total = 0.0
        #     for xx in nList:
        #         total = total + 1/(xx+.01)
        #     newCentroid.append(1/(total/numPoints))

        #print "Centroid ", centroid_coords
        #print newCentroid
        
        return Point(centroid_coords)

def kmeans(points, k, cutoff):
    start_time = time.time()
    
    # Pick out k random points to use as our initial centroids
    #initial = random.sample(points, k)
    # print initial

    #50k - 36 iter
    # initial1 = Point([59.0, 575.0, 60767.0, 25.0, 3.0, 56730.0, 217.0])
    # initial2 = Point([79.0, 443.0, 13498.0, 11.0, 1.0, 15572.0, 316.0])
    # initial3 = Point([64.0, 569.0, 55464.0, 24.0, 4.0, 55298.0, 247.0])
    # initial4 = Point([54.0, 596.0, 68805.0, 22.0, 4.0, 59967.0, 269.0])

    initial1 = Point([35.0, 629.0, 3749.0, 31.0, 3.0, 46585.0, 16.0])
    initial2 = Point([39.0, 753.0, 46517.0, 47.0, 3.0, 56181.0, 151.0])
    initial3 = Point([74.0, 463.0, 49089.0, 11.0, 3.0, 52885.0, 301.0])
    initial4 = Point([49.0, 773.0, 45883.0, 47.0, 3.0, 52778.0, 114.0])


    initial = []
    initial.append(initial1)
    initial.append(initial2)
    initial.append(initial3)
    initial.append(initial4)

    p1=[]
    p2=[]
    p3=[]
    p4=[]
    
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
        totalEuclidDistance =0.0
        
        # Start counting loops
        loopCounter += 1
        # For every point in the dataset ...
        for p in points:
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
            totalEuclidDistance = totalEuclidDistance + smallest_distance        
            lists[clusterIndex].append(p)            
            
        # Set our biggest_shift to zero for this iteration
        biggest_shift = 0.0
        
        # As many times as there are clusters ...
        for i in range(clusterCount):
            # Calculate how far the centroid moved in this iteration
            shift = clusters[i].update(lists[i])
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
            f = open('iterationFile1.txt','a')
            f.write("%s,"%loopCounter)
            f.close()
            print "%s iterations" % loopCounter
            break
        totalEuclid.append(totalEuclidDistance)
        f = open('euclidFile1.txt','a')
        f.write("%s,"%loopCounter)
        f.write("%s\n"%totalEuclidDistance)
        f.close()
        # print "loop", loopCounter, " euclid_distance", totalEuclidDistance   

    # print "p1", p1
    # print "p2 ", p2
    # print "p3 ", p3
    # print "p4", p4
    f = open('shiftFile1.txt','a')
    f.write("Iteration : %s\n"%loopCounter)
    f.write("%s\n"%p1)
    f.write("%s\n"%p2)
    f.write("%s\n"%p3)
    f.write("%s\n"%p4)
    f.close()

    execTime =time.time() - start_time
    f = open('timeFile1.txt','a')
    f.write("%s,"%execTime)
    f.close()
    print "Exec time = ", time.time() - start_time
    return clusters

def getDistance(a, b):

    if a.n != b.n:
        raise Exception("ILLEGAL: non comparable points")

    euclid_distance_squared=0
    for aa in xrange (a.n):
        euclid_distance_squared= euclid_distance_squared + (a.coords[aa]- b.coords[aa])**2
        
    euclid_distance = euclid_distance_squared**0.5


    return euclid_distance

def makeRandomPoint(ii, lower, upper):


    fp = open("notNormalizedDataset4.csv")
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