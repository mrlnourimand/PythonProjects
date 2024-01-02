"""
COMP.CS.100 Ohjelmointi 1 / Programming 1
Week 09, the 3rd project of the course. title: Road Trip Optimizer.

(In this project we implement a program which can be used to examine distances
and routes between cities. The program will process distance information from a file
 and saves the data. When the program starts it ask the user to enter the name of
 the input file, then it reads the file, and stores it in a suitable data structure.
  Then the program prints a prompt and waits the user to enter an action:
  display/add/remove/route/neighbours. Depending on the action the user enters
  it prints out different info.)

Creator: Maral Nourimand
Student id number: 151749113
Email: maral_n70@yahoo.com
"""

# what separates the departure city, destination city and the distance in the input file, each line
PART_SEPARATOR = ";"


def find_route(data, departure, destination):
    """
    This function tries to find a route between <departure>
    and <destination> cities. It assumes the existence of
    the two functions fetch_neighbours and distance_to_neighbour
    (see the assignment and the function templates below).
    They are used to get the relevant information from the data
    structure <data> for find_route to be able to do the search.

    The return value is a list of cities one must travel through
    to get from <departure> to <destination>. If for any
    reason the route does not exist, the return value is
    an empty list [].

    :param data: nested dictionary, A data structure of dictionary of dictionaries
           which contains the distance information between the cities.
    :param departure: str, the name of the departure city.
    :param destination: str, the name of the destination city.
    :return: list[str], a list of cities the route travels through, or
           an empty list if the route can not be found. If the departure
           and the destination cities are the same, the function returns
           a two element list where the departure city is stored twice.
    """

    # +--------------------------------------+
    # |                                      |
    # |     DO NOT MODIFY THIS FUNCTION!     |
    # |                                      |
    # +--------------------------------------+

    if departure not in data:
        return []

    elif departure == destination:
        return [departure, destination]

    greens = {departure}
    deltas = {departure: 0}
    came_from = {departure: None}

    while True:
        if destination in greens:
            break

        red_neighbours = []
        for city in greens:
            for neighbour in fetch_neighbours(data, city):
                if neighbour not in greens:
                    delta = deltas[city] + distance_to_neighbour(data, city, neighbour)
                    red_neighbours.append((city, neighbour, delta))

        if not red_neighbours:
            return []

        current_city, next_city, delta = min(red_neighbours, key=lambda x: x[2])

        greens.add(next_city)
        deltas[next_city] = delta
        came_from[next_city] = current_city

    route = []
    while True:
        route.append(destination)
        if destination == departure:
            break
        destination = came_from.get(destination)

    return list(reversed(route))


def read_distance_file(file_name):
    """
    Reads the distance information from <file_name> and stores it
    in a suitable data structure (you decide what kind of data
    structure to use). This data structure is also the return value,
    unless an error happens during the file reading operation.

    :param file_name: str, The name of the file to be read.
    :return: a dictionary of dictionaries | None: this data structure contains the information
             read from the <file_name> or None if any kind of error happens.
             data = {key=departure city: {key=destination city : value = distance}}
    """
    try:
        # Try to open the file for reading
        data_file = open(file_name, mode="r", encoding="utf-8")

        # Initialize a dictionary for the data.
        data = {}

        # Populate the dictionary, until the file has been processed.
        for line in data_file:
            # Split the line into departure city, destination city and the distance.
            departure_city, destination_city, distance = line.rstrip().split(PART_SEPARATOR)
            distance = int(distance)

            # Create a new nested dictionary if it does not already exist.
            if departure_city not in data:
                data[departure_city] = {}

            # Add the destination and its distance in a nested dictionary into the dictionary.
            data[departure_city][destination_city] = distance

        # Close the file.
        data_file.close()
    except OSError:
        data = None

    # Return the data or None.
    return data


def fetch_neighbours(data, city):
    """
    Returns a list of all the cities that are directly
    connected to parameter <city>. In other words, a list
    of cities where there exist an arrow from <city> to
    each element of the returned list. Return value is
    an empty list [], if <city> is unknown or if there are no
    arrows leaving from <city>.

    :param data: nested dictionary, A data structure containing the distance
           information between the known cities.
    :param city: str, the name of the city whose neighbours we
           are interested in.
    :return: list[str], the neighbouring city names in a list.
             Returns [], if <city> is unknown (i.e. not stored as
             a departure city in <data>) or if there are no
             arrows leaving from the <city>.
    """

    neighbor_list = []
    if city in data:
        neighbor_list = list(data[city].keys())  # to save the neighbor cities in a list
        sorted(neighbor_list)   # to have an alphabetically sorted list

    return neighbor_list


def distance_to_neighbour(data, departure, destination):
    """
    Returns the distance between two neighbouring cities.
    Returns None if there is no direct connection from
    <departure> city to <destination> city. In other words
    if there is no arrow leading from <departure> city to
    <destination> city.

    :param data: nested dictionary, A data structure containing the distance
           information between the known cities.
    :param departure: str, the name of the departure city.
    :param destination: str, the name of the destination city.
    :return: int | None, The distance between <departure> and
           <destination>. None if there is no direct connection
           between the two cities.
    """
    neigh_list = fetch_neighbours(data, departure)
    if destination in neigh_list:
        return data[departure][destination]
    else:
        return None


def add_city(data):
    """ This function asks from the user which city and routes they like to add, checks the inputs
        and then add the new data to the dictionary of dictionaries.

    :param data: nested dict, it contains the data of the cities.
    :return: nested dic, the updated version of the nested dic will be returned
    """
    dep_city = input("Enter departure city: ")
    des_city = input("Enter destination city: ")
    dist_input = input("Distance: ")
    try:
        distance = int(dist_input)
    except ValueError:
        print(f"Error: '{dist_input}' is not an integer.")
        return

    if dep_city not in data:
        data[dep_city] = {}

    # Add the destination and its distance in a nested dictionary into the dictionary.
    data[dep_city][des_city] = distance
    data[dep_city][des_city] = distance
    return data


def display(data):
    """ this function prints out the all available routes between cities in
        the alphabetical order.

    :param data: nested dict, it contains the data of the cities.
    :return: it returns nothing
    """
    for city1 in sorted(data.keys()):  # to sort it in alphabetical order
        for city2 in sorted(data[city1].keys()):
            print(f"{city1:<14}", end="")
            print(f"{city2:<14}", end="")
            print(f"{data[city1][city2]:>5}")


def remove_city(data):
    """ this function asks for a route (city1-city2) that the user likes to remove, checks
        whether the route already exists, if yes then it removes them from the dictionary.
        And returns the updated version of the nested dictionary.

    :param data: nested dict, it contains the data of the cities.
    :return: nested dict, the updated version of the nested dic will be returned
    """
    departure_city = input("Enter departure city: ")
    if departure_city in data:
        destination_city = input("Enter destination city: ")
        if destination_city in data[departure_city]:
            del data[departure_city][destination_city]
        else:
            print(f"Error: missing road segment between '{departure_city}' and '{destination_city}'.")
    else:
        print(f"Error: '{departure_city}' is unknown.")

    return data


def print_neighbors(data,city):
    """ This function receives the name of a city and prints out all its neighbor cities with
        their distances in km.

    :param data: nested dict, it has all cities' data
    :param city: str, the name of the city whose neighbors we want to find
    :return: it returns nothing
    """
    if city in data:  # the city exists as a departure city
        # first we find its neighbour cities
        neighbor_cities = fetch_neighbours(data, city)
        sorted(neighbor_cities)
        for neighbor in sorted(neighbor_cities):
            print(f"{city:<14}", end="")
            print(f"{neighbor:<14}", end="")
            print(f"{data[city][neighbor]:>5}")

    # This is for the case when the city exists in the data structure but not as departure city.
    # It means no route comes out of that city.
    elif search_city_in_data(city,data) is True:
        return

    else:
        print(f"Error: '{city}' is unknown.")


def print_route_distance(data, trip_cities, city1, city2):
    """ this function receives the list of the cities we pass to reach the destination,
        checks if the route exists, if exists calculates the total distance between the
        departure-destination cities and prints the result in the desired format.

    :param data: nested dict, it has all cities' data
    :param trip_cities: list of str, the list of the cities we go through to reach the destination.
    :param city1: str, the departure city
    :param city2: str, the destination city
    :return: it returns nothing unless no route found between two cities
    """
    total_distance = 0
    if len(trip_cities) == 0:
        print(f"No route found between '{city1}' and '{city2}'.")
        return

    for i in range(0, len(trip_cities) - 1):
        if len(trip_cities) > 2:
            total_distance += distance_to_neighbour(data, trip_cities[i], trip_cities[i + 1])

        # there is a direct route between two cities
        elif len(trip_cities) == 2 and city1 != city2:
            total_distance = distance_to_neighbour(data,city1,city2)
        print(f"{trip_cities[i]}-", end="")

    # to print the destination and the total distance
    print(f"{trip_cities[-1]} ({total_distance} km)")


def search_city_in_data(city, data):
    """  this function takes two parameters: city (the name of the city to search)
        and data (the nested dictionary representing the distance data).
         It iterates over the outer dictionary using items(), checks if
         the city matches the departure city, or if it exists in the destination cities
          of any departure city. If a match is found, it returns True.
          If no match is found after iterating through the entire dictionary, it returns False.

    :param city: str, the name of the city to search
    :param data: the nested dictionary representing the distance data
    :return: True/False
    """
    for departure_city, destination_cities in data.items():
        if city == departure_city or city in destination_cities:
            return True
    return False


def main():
    input_file = input("Enter input file name: ")

    distance_data = read_distance_file(input_file)

    if distance_data is None:
        print(f"Error: '{input_file}' can not be read.")
        return

    while True:
        action = input("Enter action> ")

        if action == "":
            print("Done and done!")
            return

        elif "display".startswith(action):
            # to call display function
            display(distance_data)

        elif "add".startswith(action):
            # to call add function
            add_city(distance_data)

        elif "remove".startswith(action):
            # to call remove function
            remove_city(distance_data)

        elif "neighbours".startswith(action):
            first_city = input("Enter departure city: ")
            print_neighbors(distance_data,first_city)  # to call the function

        elif "route".startswith(action):
            route_from = input("Enter departure city: ")
            # to check whether the city exists in the data as departure/destination city
            if search_city_in_data(route_from,distance_data) is False:
                print(f"Error: '{route_from}' is unknown.")
                continue
            route_to = input("Enter destination city: ")
            # to find the list of cities we pass via the route
            route_cities = find_route(distance_data,route_from,route_to)
            # to call the function for printing the route info
            print_route_distance(distance_data,route_cities,route_from,route_to)

        else:
            print(f"Error: unknown action '{action}'.")


if __name__ == "__main__":
    main()
