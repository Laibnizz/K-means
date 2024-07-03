#Description: learn clusters analysis

import csv
import random
import math

def readFileToGetDataDict(fileName):
    with open('coordinate.txt', 'r') as dataFile:
        dataDict = {}
        key = 0

        for aLine in dataFile:
            key += 1
            
            dataString = list(aLine.split())
            coordinate = list(map(float, dataString))

            dataDict[key] = coordinate
            
    return dataDict


def createCentroids(k, dataDict):
    centroids = []
    selectedKeys = []
    count = 0

    while count < k:
        rKey  = random.randint(1, len(dataDict))
        
        if rKey not in selectedKeys:
            selectedKeys.append(rKey)
            centroids.append(dataDict[rKey])
            count += 1
    
    return centroids


def distanceLength(p1, p2, p):
    normSquare = 0
    dimensions = len(p1)
    
    for i in range(dimensions):
        normSquare = (p1[i] - p2[i]) ** p

    norm = normSquare ** (1 / p)
    
    return norm


def createClusters(k, centroids, dataDict, iterations, p):
    check = [0 for _ in range(k)]
    for aPass in range(iterations):
        print()
        print('*****Pass', aPass + 1, '*****')
        clusters = [[] for _ in range(k)]

        for key in dataDict:
            distance = []
            for i in range(k):
                d = distanceLength(dataDict[key], centroids[i], p)
                distance.append(d)

            minDistance = min(distance)
            minIdx = distance.index(minDistance)
            clusters[minIdx].append(key)

        dimensions = len(dataDict[1])

        for i in range(k):
            sums = [0 for _ in range(dimensions)]
            clusterLen = len(clusters[i])

            for key in clusters[i]:
                dataPoint = dataDict[key]
                for j in range(dimensions):
                    sums[j] += dataPoint[j]
                    
            if clusterLen != 0:
                for j in range(dimensions):
                    sums[j] /= clusterLen

            if sums == centroids[i]:
                check[i] = 1

            if 0 not in check:
                for cluster in clusters:
                    print('CLUSTER', end = ' ')
                    for key in cluster:
                        print(dataDict[key], end = ' ')
                    print()
                    print()
                    
                print('clusters are stable')
                    
                return clusters
            
            centroids[i] = sums

        for cluster in clusters:
            print('CLUSTER', end = ' ')
            for key in cluster:
                print(dataDict[key], end = ' ')
            print()
            print()

    return clusters


def createTxt(fileName):
    with open(fileName, 'r', encoding = 'utf8') as inFile:
        with open('coordinate.txt', 'w') as outFile:
            theReader = csv.reader(inFile)
            theTitle = next(theReader)

            latitudeCol = theTitle.index('latitude')
            longitudeCol = theTitle.index('longitude')

            for aLine in theReader:
                outFile.write(aLine[latitudeCol] + ' ' + aLine[longitudeCol] + '\n')


print('The purpose of this program is to learn clusters analysis.')

csvList = ['quakes_2023_6dot5.csv']

k = int(input('The number of clusters: '))
iterations = int(input('The maximum number of iterations: '))
p = int(input('Define the distance between two points with norm:'))

createTxt(csvList[0])
dataDict = readFileToGetDataDict('coordinate.txt')

print()
print('Processing: ', csvList[0])
print()
print('The dictionary:')
print(dataDict)

centroids = createCentroids(k, dataDict)

print()
print('The', k, 'initial centroids:', centroids)
createClusters(k, centroids, dataDict, iterations, p)

for _ in range(60):
    print('=', end = '')
print()