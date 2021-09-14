import math
import random
import matplotlib.pyplot as plt


class City:
    ###
    # class city is in charge for the each node
    def __init__(self, c_x=None, c_y=None, name=None):
        self.x = None
        self.y = None
        self.name = None
        if c_x is not None:
            self.x = c_x
        else:
            self.x = int(random.random() * 200)
        if c_y is not None:
            self.y = c_y
        else:
            self.y = int(random.random() * 200)
        if name is not None:
            self.name = name
        else:
            self.name = "(city " + str(self.x) + ":" + str(self.y) + ")"

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_name(self):
        return self.name

    def manhattan_distance(self, m_city):
        x_distance = abs(self.get_x() - m_city.get_x())
        y_distance = abs(self.get_y() - m_city.get_y())
        distance = math.sqrt((x_distance * x_distance) + (y_distance * y_distance))
        return distance

    def __repr__(self):
        return "x = " + str(self.get_x()) + ", y = " + str(self.get_y()) + ", city: " + self.get_name()


class Map:

    destination_cities = []

    def add_city(self, new_city):
        self.destination_cities.append(new_city)

    def get_city(self, index):
        return self.destination_cities[index]

    def number_of_cities(self):
        return len(self.destination_cities)


#candidate solutions class
class Population:
    def __init__(self, cities, population_size, initialise):
        self.paths = [] # we find all pathes for the selection
        for i in range(0, population_size):
            self.paths.append(None)
        #initialising
        if initialise:
            for i in range(0, population_size):
                new_path = Path(cities)
                new_path.generate_individual()
                self.save_path(i, new_path)

    def save_path(self, index, path):
        self.paths[index] = path

    def get_path(self, index):
        return self.paths[index]

    def get_fittest(self):
        fittest = self.paths[0]
        for i in range(0, self.population_size()):
            if fittest.get_fitness() <= self.get_path(i).get_fitness():
                fittest = self.get_path(i)
        return fittest

    def population_size(self):
        return len(self.paths)

#each solution class
class Path:
    def __init__(self, cities_set, path=None):
        self.cities_set = cities_set
        self.path = []
        self.fitness = 0.0
        self.distance = 0
        if path is not None:
            self.path = path
        else:
            for i in range(0, self.cities_set.number_of_cities()):
                self.path.append(None)

    def __repr__(self):
        genetic_string = ""
        for i in range(0, self.path_len()):
            genetic_string += str(self.get_city(i)) + "->" + "\n"
        return genetic_string

    def draw_path(self):
        x = []
        y = []
        names = []
        for j in range(0, self.path_len()):
            x.append(self.get_city(j).get_x)
            y.append(self.get_city(j).get_y)
            names.append(self.get_city(j).get_name)
        return x, y, names

    def get_cities(self):
        x = []
        y = []
        names = []
        for i in range(0, self.path_len()):
            x.append(self.get_city(i).get_x())
            y.append(self.get_city(i).get_y())
            names.append(self.get_city(i).get_name())
        return x, y, names

    #genotype of an individual, here its solutions
    def  generate_individual(self):
        for city_id in range(0, self.cities_set.number_of_cities()):
            self.set_city(city_id, self.cities_set.get_city(city_id))
        random.shuffle(self.path)

    def get_city(self, path_position):
        return self.path[path_position]

    def set_city(self, path_position, city):
        self.path[path_position] = city
        self.fitness = 0.0
        self.distance = 0

    def get_fitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.get_distance())
        return self.fitness

    def get_distance(self):
        if self.distance == 0:
            path_distance = 0
            for city_id in range(0, self.path_len()):
                from_city = self.get_city(city_id)
                destination_city = None
                if city_id + 1 < self.path_len():
                    destination_city = self.get_city(city_id + 1)
                else:
                    destination_city = self.get_city(0)
                path_distance += from_city.manhattan_distance(destination_city)
            self.distance = path_distance
        return self.distance

    def path_len(self):
        return len(self.path)

    def has_city(self, city):
        return city in self.path


class Genetic_algorithm:
    def __init__(self, cities_set):
        self.cities_set = cities_set
        self.mutation_rate = 0.015
        self.competition_size = 5
        self.elitism = True

    def evolve_population(self, pop):
        new_population = Population(self.cities_set, pop.population_size(), False)
        elitism_offset = 0
        if self.elitism:
            new_population.save_path(0, pop.get_fittest())
            elitism_offset = 1

        for i in range(elitism_offset, new_population.population_size()):
            parent1 = self.selection(pop)
            parent2 = self.selection(pop)
            child = self.intersection(parent1, parent2)
            new_population.save_path(i, child)

        for i in range(elitism_offset, new_population.population_size()):
            self.mutate(new_population.get_path(i))

        return new_population

    def intersection(self, parent1, parent2):
        child = Path(self.cities_set)

        start_pos = int(random.random() * parent1.path_len())
        end_pos = int(random.random() * parent1.path_len())

        for i in range(0, child.path_len()):
            if start_pos < end_pos and i > start_pos and i < end_pos:
                child.set_city(i, parent1.get_city(i))
            elif start_pos > end_pos:
                if not (i < start_pos and i > end_pos):
                    child.set_city(i, parent1.get_city(i))

        for i in range(0, parent2.path_len()):
            if not child.has_city(parent2.get_city(i)):
                for ii in range(0, child.path_len()):
                    if child.get_city(ii) == None:
                        child.set_city(ii, parent2.get_city(i))
                        break

        return child

    def mutate(self, path):
        for path_position_one in range(0, path.path_len()):
            if random.random() < self.mutation_rate:
                path_position_two = int(path.path_len() * random.random())

                city_one = path.get_city(path_position_one)
                city_two = path.get_city(path_position_two)

                path.set_city(path_position_two, city_one)
                path.set_city(path_position_one, city_two)

    def selection(self, pop):
        competition = Population(self.cities_set, self.competition_size, False)
        for i in range(0, self.competition_size):
            random_id = int(random.random() * pop.population_size())
            competition.save_path(i, pop.get_path(random_id))
        fittest = competition.get_fittest()
        return fittest


if __name__ == '__main__':

    cities_set = Map()

    f = open("test_files/test3.txt", 'r')
    lines = f.readlines()
    x = []  # for the graphics
    y = []  # for the graphics
    names = []  # for the graphics
    print("Given cities and their coordinates:\n")
    for l in lines:
        this_string = l.split()
        x.append(int(this_string[0]))
        y.append(int(this_string[1]))
        names.append(this_string[2])
        print(l.split())
    for i in range(0, len(x)):
        city = City(x[i], y[i], names[i])
        cities_set.add_city(city)

    p = Population(cities_set, 100, True)
    print("First run: " + str(p.get_fittest().get_distance()))

    ga = Genetic_algorithm(cities_set)
    p = ga.evolve_population(p)
    for i in range(0, 100):
        p = ga.evolve_population(p)

    print("Final path length: " + str(p.get_fittest().get_distance()))

    print("Path route:")
    print(p.get_fittest())
    x, y, names = p.get_fittest().get_cities()
    plt.plot(x, y, 'bo-')

    for i in range(0, len(x)):
        plt.text(x[i], y[i], names[i])
    # naming the x axis
    plt.xlabel('x - axis')
    # naming the y axis
    plt.ylabel('y - axis')

    # giving a title to my graph
    plt.title('Map for the travelling salesman problem via GeneticAlgorythm')

    # function to show the plot
    plt.show()
