import random
from matplotlib import pyplot as plt
import json
import math

points = []

with open('data.json') as json_file:
    data = json.load(json_file)
    for p in data['data']:
        points.append([p[0], p[1], 0, 'r'])
        points.append([p[2], p[3], 0, 'b'])


def apriori(amount_of_red, amount_of_blue):
    red_apriori = amount_of_red / (amount_of_red + amount_of_blue)
    blue_apriori = amount_of_blue / (amount_of_red + amount_of_blue)
    return red_apriori, blue_apriori


def find_close(point, how_many):
    for i in range(len(points)):
        dx = points[i][0] - point[0]
        dy = points[i][1] - point[1]
        points[i][2] = math.sqrt((dx*dx)+(dy*dy))

    points.sort(key=lambda x: x[2])
    red_count = 0
    blue_count = 0

    for i in range(how_many):
        if points[i][3] == 'r':
            red_count += 1
        else:
            blue_count += 1
    return red_count, blue_count


def posteriori(red_am, blue_am, red_close, blue_close):
    red_posteriori = red_close/ red_am
    blue_posteriori = blue_close/ blue_am
    return red_posteriori, blue_posteriori


def NaiveBayes(new_x, new_y, amount_of_red, amount_of_blue):
    red_apriori, blue_apriori = apriori(amount_of_red, amount_of_blue)
    close_red, close_blue = find_close([new_x, new_y], 5)
    red_posteriori, blue_posteriori = posteriori(amount_of_red, amount_of_blue, close_red, close_blue)

    red_chance = red_apriori*red_posteriori
    blue_chance = blue_apriori*blue_posteriori

    if red_chance > blue_chance:
        points.append([x, y, 0, 'r'])
        amount_of_red += 1
    else:
        points.append([x, y, 0, 'b'])
        amount_of_blue += 1


red = len(points)/2 
blue = len(points)/2

for i in range(10):
    x = random.randint(10, 40)
    y = random.randint(10, 40)
    NaiveBayes(x, y, red, blue)
    for collection in points:
        plt.scatter(collection[0], collection[1], c=collection[3])
    plt.scatter(x, y, c='g')
    plt.draw()
    plt.pause(1)
    plt.clf

plt.show()
