import psycopg2
import os
import math
import pandas as pd
import numpy as np

dbName = 'nBody'
dbHost = 'localhost'
dbUsername = 'username'
dbPassword = 'password'

planetData = pd.read_csv('data/simResults/simCopyPlanets.txt', usecols=[0,2,15], header=None)
neptuneLongitudes = planetData.loc[planetData[2] == 3, [0, 15]]

try:
    conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}' password='{3}'".format(dbName, dbUsername, dbHost, dbPassword))
except:
    print( "Unable to connect to the database")
	
db = conn.cursor()

simParticlesFolder = 'data/simResults/simCopyParticles' 
fileList = [file for (_, _, files) in os.walk(simParticlesFolder) for file in files]
fileList.sort(key=int, reverse=False)
#del fileList[0] # exclude the first step, no resonances in first sim setup

def resonance(row):
	angle = 5 * reduceAngle(math.degrees(row[8])) - (2 * neptuneLongitude) - (3 * reduceAngle(math.degrees(row[7])))
	return reduceAngle(angle)
	
def reduceAngle(a):
    return ((a % 360) + 360) % 360
	
for fileName in fileList:

	theFile = os.path.join(simParticlesFolder, fileName)

	data = pd.read_csv(theFile, header=None)

	neptuneLongitude = reduceAngle(math.degrees(float(neptuneLongitudes.loc[neptuneLongitudes[0] == int(data[0][0])][15])))

	data[10] = data.apply(resonance, axis = 1)

	data.to_csv(theFile, header = None, index = False)

	file = open(theFile, 'r')
	
	db.copy_from(file, table='particleSimEntry', sep=',', columns=('t', 'pid', 'a', 'e', 'i', 'ascendingNode', 'omega', 'pomega', 'l', 'f', 'resonantAngle'))

	conn.commit()

	file.close()
	
	print('{0} read'.format(fileName))
