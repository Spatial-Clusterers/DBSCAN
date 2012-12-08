# -*- coding: utf-8 -*-

# A Density-Based Algorithm for Discovering Clusters in Large Spatial Databases with Noise
# Martin Ester, Hans-Peter Kriegel, Jörg Sander, Xiaowei Xu
# dbscan: density based spatial clustering of applications with noise

import numpy as np
from rtree import index
from math import sqrt
import math
import csv
import sys

UNCLASSIFIED = False
NOISE = None

cids = []
input_file_path = ""
rtree_out_file_path = ""
dbscan_file_path = ""
dataset_n_string = ""
dataset_n = 0
# The container for the records
noaa_hail_data = []
# The container for the coordinates
coords = []
dsum = 0

# Create a 2D index
p = index.Property()
p.dimension = 2
idx2d = index.Index(properties=p)

average_nn = 9999

def indexDataSet():
    'TODO: Add function description.'
    global dataset_n
    noaa = []

    for i in range(dataset_n):
        noaa.append(noaa_hail_data[i])

    # Index CSV data
    for record in noaa:
        # Cast index to integer
        index = int(record[0])
        # Add set of coordinate points
        # print(record[1] + "," + record[2])
        coord = (float(record[1]), float(record[2]))
        # Add to list of coordinates
        coords.append(coord)
        # Add to the R*-Tree
        idx2d.add(index, coord)

def calculateANN():
    'TODO: Add function description.'
    global average_nn, coords, dsum

    range_n = dataset_n
    # Find closest pair for the first 10 points
    for index_1 in xrange(range_n):
        #
        nearest = list(idx2d.nearest(coords[index_1], 4))
        print(coords[index_1])
        #
        assert index_1 == nearest[0]
        #
        index_2 = nearest[3]
        #
        c1 = coords[index_1]
        #
        c2 = coords[index_2]
        # Pythagorean theorem
        dist = sqrt(sum([(a - b)**2 for a, b in zip(c1, c2)]))
        # Add distance to sum
        dsum += dist

    print('dsum:' + str(dsum))
    # Calculate the ANN
    average_nn = dsum / range_n
    # Display the result
    print('Average nearest neighbor: ' + str(average_nn))
    print("dbscan-path: " + dbscan_file_path)

def _dist(p,q):
    'TODO: Add function description.'
    return math.sqrt(np.power(p-q,2).sum())

def _eps_neighborhood(p,q,eps):
    'TODO: Add function description.'
    return _dist(p,q) < eps

def _region_query(m, point_id, eps):
    'TODO: Add function description.'
    n_points = m.shape[1]
    seeds = []
    for i in range(0, n_points):
        if not i == point_id:
            if _eps_neighborhood(m[:,point_id], m[:,i], eps):
                seeds.append(i)
    return seeds

def _expand_cluster(m, classifications, point_id, cluster_id, eps, min_points):
    'TODO: Add function description.'
    seeds = _region_query(m, point_id, eps)
    if len(seeds) < min_points:
        classifications[point_id] = NOISE
        return False
    else:
        classifications[point_id] = cluster_id
        for seed_id in seeds:
            classifications[seed_id] = cluster_id
            
        while len(seeds) > 0:
            current_point = seeds[0]
            results = _region_query(m, current_point, eps)
            if len(results) >= min_points:
                for i in range(0, len(results)):
                    result_point = results[i]
                    if classifications[result_point] == UNCLASSIFIED or \
                       classifications[result_point] == NOISE:
                        if classifications[result_point] == UNCLASSIFIED:
                            seeds.append(result_point)
                        classifications[result_point] = cluster_id
            seeds = seeds[1:]
        return True
        
def dbscan(m, eps, min_points):
    """Implementation of Density Based Spatial Clustering of Applications with Noise
    See https://en.wikipedia.org/wiki/DBSCAN
    
    scikit-learn probably has a better implementation
    
    Uses Euclidean Distance as the measure
    
    Inputs:
    m - A matrix whose columns are feature vectors
    eps - Maximum distance two points can be to be regionally related
    min_points - The minimum number of points to make a cluster
    
    Outputs:
    An array with either a cluster id number or dbscan.NOISE (None) for each
    column vector in m.
    """
    cluster_id = 1
    n_points = m.shape[1]
    classifications = [UNCLASSIFIED] * n_points
    for point_id in range(0, n_points):
        point = m[:,point_id]
        if classifications[point_id] == UNCLASSIFIED:
            if _expand_cluster(m, classifications, point_id, cluster_id, eps, min_points):
                cluster_id = cluster_id + 1
    for classifcation in classifications:
        cids.append(classifcation)

    return classifications

def importDataSet():
    'Import the data set of size n.'
    global input_file_path, rtree_out_file_path, dbscan_file_path, dataset_n

    # Prompt for the size of the data set
    print("Enter the number of data points n in the dataset: ")
    # Assign size
    dataset_n_raw = raw_input()
    dataset_n_string = str(dataset_n_raw)
    dataset_n = int(dataset_n_string)
    # Construct file paths for the input and output files
    input_file_path = "noaa-hail-cleaned.csv"
    rtree_out_file_path = "noaa-hail-cleaned-" + dataset_n_string + "-rtree.csv"
    dbscan_file_path = "noaa-hail-cleaned-" + dataset_n_string + "-dbscan.csv"
    # Open the file input and output files
    dataFile = open(input_file_path, 'rt')
    outFile = open(rtree_out_file_path, 'wb')
    outFileNoIndex = open(dbscan_file_path, 'wb')

    # Read lines into list container
    try:
        # 
        reader = csv.reader(dataFile)
        # Add each record to 
        i = 0
        for row in reader:
            coord = (float(row[0]), float(row[1]))
            row.reverse()
            row.append(i)
            row.reverse()
            i += 1
            noaa_hail_data.append(row)
            coords.append(coord)

        writer = csv.writer(outFile, delimiter=",")
        writerNoIndex = csv.writer(outFileNoIndex, delimiter=",")

        for record in noaa_hail_data:
            writer.writerow(record)

        for record in coords:
            writerNoIndex.writerow(record)

        print("len(coords): " + str(len(coords)))
        print("dataset_n: " + dataset_n_string)

    finally:
        # Close the file
        dataFile.close()
        outFile.close()
        outFileNoIndex.close()

def dbscan_runner():
    'Add description'
    m = np.asmatrix(np.loadtxt(dbscan_file_path, delimiter=",", skiprows=149414))
    
    #eps = 0.99
    eps = float(average_nn)
    print(eps)
    min_points = 4
    # Transpose coordinate matrix
    q = np.transpose(m)
    print(dbscan(q, eps, min_points))

    coords = np.array(m).tolist()

    i = 0
    for coord in coords:
        coord.append(str(cids[i]))
        i += 1

    # Open results output file
    outFile = open("noaa-hail-" + str(dataset_n) + "-dbscan-classified.csv", 'wb')
    resultWriter = csv.writer(outFile, delimiter=",")
    
    for coord in coords:
        resultWriter.writerow(coord)

# Run the program
importDataSet()
# Index the data to the R*-Tree
indexDataSet()
# Calculate ANN
calculateANN()

dbscan_runner()