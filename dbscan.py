'''
Function: DBSCAN
Description: 

param D
	The input dataset.
param epsilon
	The neighborhood value.
param minimumPoints
	The minimum number of points required to form a cluster. 
''' 
def DBSCAN(D, epsilon, minimumPoints):
	# Set the cluster ID to zero
	clusterID = 0
	# For each unvisitied point P in dataset D
	for point in D: