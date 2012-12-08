'''
TODO: Remove duplicates from input dataset
'''

from random import randrange
from rtree import index
from math import sqrt
import numpy as np
import csv
import sys

class DBSCAN:
	
	def __init__(self, fileName):
		'TODO: Add function description.'

		self.file = open(fileName, 'rt')
		self.hail_data = []
		self.coords = []
		self.dbscan = []
		
		# Create a 2D index
		p = index.Property()
		p.dimension = 2
		self.idx2d = idx2d = index.Index(properties=p)

	def importDataSet(self):
		'Import the data set into a list of lists.'

		# Read lines into list container
		try:
			reader = csv.reader(self.file)
			# Add each record to 
			for row in reader:
				self.hail_data.append(row)

		finally:
			# Close the file
			self.file.close()

	def indexDataSet(self):
		'TODO: Add function description.'

		# Index CSV data
		for record in self.hail_data:
			# Cast ID to integer
			id = int(record[0])
			# Add set of coordinate points
			## print(record[16] + "," + record[17])
			coord = (float(record[1]), float(record[2]))
			# Add to list of coordinates
			self.coords.append(coord)
			# Add to the R*-Tree
			self.idx2d.add(id, coord)

	def calculateANN(self):
		'TODO: Add function description.'

		dsum = 0
		# Find closest pair for the first 10 points
		for id1 in range(len(self.coords)):
			#
		    nearest = list(self.idx2d.nearest(self.coords[id1], 2))
		   # print("nearest: " + str(nearest))
		   # print("coords[id1]: " + str(self.coords[id1]))
		   # print("id1: " + str(id1))
		   # print("nearest[0] = " + str(nearest[0]))
		    #
		    assert id1 == nearest[0]
		    #
		    id2 = nearest[1]
		    #
		    c1 = self.coords[id1]
		    #
		    c2 = self.coords[id2]
		    # Pythagorean theorem
		    dist = sqrt(sum([(a - b)**2 for a, b in zip(c1, c2)]))
		    # Add distance to sum
		    dsum += dist
		    # Display the result
		    # print '%i <-> %i : %.1f'%(id1, id2, dist)

		# Calculate the ANN
		average = dsum / len(self.coords)
		# Display the result
		print('Average nearest neighbor: ' + str(average))

#=====================================================================
# Run Test Program
#=====================================================================

# Instantiate a DBSCAN object
test = DBSCAN("noaa-hail-cleaned-100-index-coords.csv")
# Import the dataset
test.importDataSet()
# Index the dataset
test.indexDataSet()
# Calculate the ANN
test.calculateANN()