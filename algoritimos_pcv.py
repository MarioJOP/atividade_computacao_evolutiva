import numpy as np
import time

def nearestNeighbor(distance_matrix):
    n = len(distance_matrix[0]) # n = length of distance matrix

    visited_list = [False for _ in range(n)] # create visited list of size n with all False values
    tour_list = [] # create empty tour list

    total_distance = 0 # set total_distance = 0

    # choose a random starting city
    #start = random.randint(0, n - 1)  # set start = random city
    start = 5
    print("start:", start)
    visited_list[start] = True # mark start city as visited
    tour_list.append(start) # add start city to tour

    # set current city as the start city
    current_city = start

    # loop through the cities until all are visited
    while len(tour_list) < n:
        next_city = None
        min_distance = np.inf

        # for each city, find the nearest unvisited city
        for j in range(n):
            if not visited_list[j] and distance_matrix[current_city][j] < min_distance:
                next_city = j
                #print('a')
                min_distance = distance_matrix[current_city][j]

        # add the nearest city to the tour
        tour_list.append(next_city) # add next city to the tour
        visited_list[next_city] = True # mark next_city as visited
        total_distance += min_distance # add min_distance to total_distance
        current_city = next_city # set current city = next_city

    # return to the start city to to complete the cycle
    total_distance += distance_matrix[current_city][start] # add distance_matrix[current_city][start] to distance_matrix
    tour_list.append(start) # add start city to the tour

    return tour_list, total_distance

def cheapestInsertion(distance_matrix):
    n = len(distance_matrix[0])  # n = length of distance matrix

    unvisited_list = [i for i in range(n)]  # create unvisited with all cities
    tour_list = []  # create empty tour list

    # start = random.randint(0, n - 1)  # set start = random city
    start = 2  # set start = random city
    unvisited_list.remove(start)  # remove start from unvisited list
    second_city = 4  #
    unvisited_list.remove(second_city)
    print("start:", start)
    print("second_city:", second_city)


    # initialize the tour with these two cities
    tour_list.append(start)
    tour_list.append(second_city)
    tour_list.append(start)

    # loop until all cities are visited
    while unvisited_list:
        best_increase = np.inf
        best_city = None
        best_position = None

        # for each unvisited city, find the cheapest insertion
        for city in unvisited_list:
            for i in range(len(tour_list)-1):
                a = tour_list[i]
                b = tour_list[i+1]

                # calculate the increase in total distance when inserting city between a and b
                increase = distance_matrix[a][city] + distance_matrix[city][b] - distance_matrix[a][b]

                # if this incresion is the cheapest, save the position and city
                if increase < best_increase:
                    best_increase = increase
                    best_city = city
                    best_position = i

        # insert the best city at the best position
        tour_list.insert(best_position, best_city)
        unvisited_list.remove(best_city)

    # calculate the total distance of the tour
    total_distance = 0
    for i in range(len(tour_list)-1):
        a = tour_list[i]
        b = tour_list[i+1]
        total_distance += distance_matrix[a][b]

    return tour_list, total_distance


# distance_matrix = [[0, 2, 1, 4, 9, 1],
#                    [2, 0, 5, 9, 7, 2],
#                    [1, 5, 0, 3, 8, 6],
#                    [4, 9, 3, 0, 2, 6],
#                    [9, 7, 8, 2, 0, 2],
#                    [1, 2, 6, 6, 2, 0]]

n_cities = int(input("Enter the number of cities: "))
distance_matrix = np.random.randint(1, 10, size=(n_cities, n_cities))

start_time = time.time()
print("Nearest Neighbour")
tour_list, total_distance = nearestNeighbor(distance_matrix)

duration = time.time() - start_time
print("Tour list:", tour_list)
print("Total_distance?", total_distance)
print("Duration of Nearest Neighbour (Seconds):", duration)
print("Duration of Nearest Neighbour (Miliseconds):", duration*1000)

print('='*50)

start_time = time.time()
print("Cheapest Insertion")
tour_list, total_distance = cheapestInsertion(distance_matrix)
duration = time.time() - start_time
print("Tour list:", tour_list)
print("Total_distance?", total_distance)
print("Duration of Cheapest Insertion:", duration)
print("Duration of Cheapest Insertion (Miliseconds):", duration*1000)