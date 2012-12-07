# http://scikit-learn.org/dev/auto_examples/cluster/plot_dbscan.html
from random import randrange
from rtree import index
from math import sqrt
import csv
import sys

class dbscan:
	
	def importDataSet(self):
		'Import the data set into a list of lists.'

		# File to be opened
		f = open("/home/sean/academic/utc/f2012/cpsc_5210/research-project/dataset/noaa-hail-mini.csv", 'rt')

		# List used for storing dataset
		hail_data = []

		# Read lines into list container
		try:
			reader = csv.reader(f)
			reader.next()
			# Add each record to 
			for row in reader:
				hail_data.append(row)

		finally:
			# Close the file
			f.close()

	def indexDataSet(self):
		'TODO: Add function description.'

		# Create a 2D index
		p = index.Property()
		p.dimension = 2
		idx2d = index.Index(properties=p)

		# Index CSV data
		coords = []
		for record in hail_data:
			# Cast ID to integer
			id = int(record[0]) -1
			# Add set of coordinate points
			coord = (float(record[15]), float(record[16]))
			# Add to list of coordinates
			coords.append(coord)
			# Add to the R*-Tree
			idx2d.add(id, coord)

	def calculateANN(self):
		'TODO: Add function description.'

		dsum = 0
		# Find closest pair for the first 10 points
		for id1 in range(len(coords)):
			#
		    nearest = list(idx2d.nearest(coords[id1], 2))
		    #
		    assert id1 == nearest[0]
		    #
		    id2 = nearest[1]
		    #
		    c1 = coords[id1]
		    #
		    c2 = coords[id2]
		    # Pythagorean theorem
		    dist = sqrt(sum([(a - b)**2 for a, b in zip(c1, c2)]))
		    # Add distance to sum
		    dsum += dist
		    # Display the result
		    # print '%i <-> %i : %.1f'%(id1, id2, dist)

		# Calculate the ANN
		average = dsum / len(coords)
		# Display the result
		# print('Average nearest neighbor: ' + str(average))