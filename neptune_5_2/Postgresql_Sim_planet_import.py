import psycopg2
import os

dbName = 'nBody'
dbHost = 'localhost'
dbUsername = 'username'
dbPassword = 'password'

try:
    conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}' password='{3}'".format(dbName, dbUsername, dbHost, dbPassword))
except:
    print( "Unable to connect to the database")
	
db = conn.cursor()

file = open('data/simResults/simCopyPlanets.txt', 'r')

db.copy_from(file, table='planetSimEntry', sep=',', columns=('t', 'pid', 'planet', 'x', 'y', 'z', 'vx', 'vy', 'vz', 'a', 'e', 'i', 'ascendingNode', 'omega', 'pomega', 'l'))

conn.commit()

file.close()

print('File read')