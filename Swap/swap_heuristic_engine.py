import pandas as pd

__author__ = 'slei'

from Swap.helper_functions import swap


class SwapHeuristicTSP:
    """ Finds the shortest path using a heuristic method """

    def __init__(self, cities_df):

        self.df = cities_df
        # self.edges = list((t.origin, t.destination) for t in df.itertuples())
        self.distance = dict([((t.origin, t.destination), t.distance) for t in df.itertuples()])
        self.cities = list(set(df['destination']))
        self.cities_lst = []
        self.swap_index_lst = []
        self.tour_lst = []
        self.distance_lst = []
        self.tour_leg_distances_lst = []
        self._final_df = None
        self._shortest_distance = None
        self._shortest_tour = None
        self._shortest_tour_leg_distances = None

    @property
    def final_df(self):
        """ Add description here"""
        if self._final_df is None:
            self._final_df = self._generate_final_df()
        return self._final_df

    def _generate_final_df(self):
        swap_index = 0
        starting_tour = []

        # while swap_index < len(tsp.cities):
        while swap_index < 2:

            if swap_index == 0:
                print("*****")
                print("swap_index", swap_index)
                print("*****")
                # starting solution
                starting_city = self.cities[0]
                print("city: ", starting_city)  # generate a tour for each
                print("--------------------------------------------------------------------------------")
                self.find_subtour(starting_city)
                starting_tour = self.tour_lst[-1]
                print()
                print("current_tour:", starting_tour)
                print()
                self.swap_index_lst.append(swap_index)
                swap_index = swap_index + 1  # increment i

            else:
                print("*****")
                print("swap_index", swap_index)
                print("*****")

                starting_tour_lst = self.tour_lst[0]
                starting_tour_distance_lst = self.tour_leg_distances_lst[0]

                tour_lst_new = starting_tour_lst
                tour_leg_distances_lst_new = starting_tour_distance_lst

                # get the new distance for swapped cities
                swap_city_1 = starting_tour_lst[swap_index]
                swap_city_2 = starting_tour_lst[swap_index + 1]
                od = (swap_city_1, swap_city_2)
                new_d = [df['od'] == od].distance

                # drop the old distance
                del tour_lst_new[swap_index-1]
                tour_lst_new.insert(swap_index-1,new_d)

                # find new distance
                total = 0
                for d in range(0,len(tour_leg_distances_lst_new)):
                    total_distance = total + tour_leg_distances_lst_new[d]


            print("swap_index_lst", self.swap_index_lst)
            print("tour_lst", self.tour_lst)
            print("tour_leg_distances_lst", self.tour_leg_distances_lst)

            swap_index = swap_index + 1  # increment i

    def find_subtour(self, starting_city):
        """ Given a starting city, finds a tour by selecting next shortest distance from list of unvisited cities """
        tour = []
        tour_distance_lst = [0]
        cities_unvisited = list(set(self.df['destination']))
        initial_city = starting_city
        current_city = initial_city
        tour.append(current_city)
        cities_unvisited.pop(0)
        total_distance = 0
        count = 0

        self.update_list(tour, total_distance, tour_distance_lst)
        # check

        print("tour: ", tour)
        print("total_distance: ", total_distance)
        print("tour_leg_distances_lst: ", tour_distance_lst)
        print("********************************************************************************")
        print()

        # TODO move this to a utility function so it can be used in both heuristic methods
        while len(cities_unvisited) > 0:
            # remove any city that has already been visited from consideration
            df_unvisited = self.df[self.df['destination'].isin(cities_unvisited)]

            # filter for rows based on first criterion
            is_current = df_unvisited['origin'] == current_city
            df2 = df_unvisited[is_current]

            # find the nearest city
            index_min = df2['distance'].idxmin()
            min_row = df2.loc[index_min]
            d = min_row.distance
            print("distance: ", d)
            destination = min_row.destination
            print("next destination: ", destination)

            # update next city and tour and total distance
            current_city = destination
            total_distance = total_distance + d
            print("total_distance: ", total_distance)
            tour_distance_lst.append(d)
            print("tour_distance_lst: ", tour_distance_lst)

            # update city tracker lists
            tour.append(current_city)
            print("tour: ", tour)
            index_i = cities_unvisited.index(current_city)
            cities_unvisited.pop(index_i)
            print("cities_unvisited: ", cities_unvisited)
            count = count + 1

            # check
            print("next destination: ", destination)
            print("distance: ", d)
            print("total_distance: ", total_distance)
            print("tour: ", tour)
            print("tour_distance_lst: ", tour_distance_lst)
            print("cities_unvisited: ", cities_unvisited)
            print()

        # adding the distance from last city back to initial city
        last_city = tour[-1]
        last_mile = (initial_city, last_city)
        last_mile_distance = self.distance[last_mile]
        tour.append(initial_city)
        total_distance = total_distance + last_mile_distance
        tour_distance_lst.append(last_mile_distance)


        self.update_list(tour, total_distance, tour_distance_lst)
        # check
        print("last_mile: ", last_mile)
        print("last_mile_distance: ", last_mile_distance)
        print("tour: ", tour)
        print("total_distance: ", total_distance)
        print("tour_leg_distances_lst: ", tour_distance_lst)
        print()

    # update lists
    def update_list(self, tour, total_distance, tour_distance_lst):
        self.tour_lst.append(tour)
        self.distance_lst.append(total_distance)
        self.tour_leg_distances_lst.append(tour_distance_lst)

        print("tour_lst", self.tour_lst)
        print("tour_leg_distances_lst", self.tour_leg_distances_lst)
        print("********************************************************************************")
        print()
        # ********************************************************************************


# ********************************************************************************

if __name__ == '__main__':
    df = pd.read_csv('city_data_v3.csv')
    tsp = SwapHeuristicTSP(df)
    tsp.final_df

    # print("final_df")
    # print(tsp.final_df)
    # print()
