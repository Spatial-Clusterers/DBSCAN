import csv
import sys
import numpy as np

def importDataSet():
	'Import the data set of size n.'

	# Prompt for the size of the data set
	print("Enter the number of data points n in the dataset: ")
	# Assign size
	dataset_n = raw_input()
	# Construct file paths for the input and output files
	input_file_path = "noaa-hail-cleaned-" + str(dataset_n) + ".csv"
	rtree_out_file_path = "noaa-hail-cleaned-" + str(dataset_n) + "rtree.csv"
	dbscan_file_path = "noaa-hail-cleaned-" + str(dataset_n) + "dbscan.csv"
	# Open the file input and output files
	dataFile = open(file_path, 'rt')
	outFile = open(rtree_out_file_path, 'wb')
	outFileNoIndex = open(dbscan_file_path, 'wb')

	# Read lines into list container
	try:
		# The container for the records
		noaa_hail_data = []
		# The container for the coordinates
		coords = []
		# 
		reader = csv.reader(dataFile)
		reader.next()
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

	finally:
		# Close the file
		dataFile.close()
		outFile.close()

importDataSet()