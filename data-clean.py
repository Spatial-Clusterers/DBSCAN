import csv
import sys
import numpy as np

def importDataSet():
	'Import the data set into a list of lists.'

	dataFile = open("noaa-hail-cleaned-100.csv", 'rt')
	outFile = open('noaa-hail-cleaned-100-index-coords.csv', 'wb')
	outFileNoIndex = open('noaa-hail-cleaned-100-coords-dbscan.csv', 'wb')


	# Read lines into list container
	try:
		#
		noaa_hail_data = []
		#
		coords = []
		#
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