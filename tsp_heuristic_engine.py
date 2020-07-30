import pandas as pd

__author__ = 'slei'


class HeuristicTSP:
    """ Finds the shortest path using a heuristic method """

    def __init__(self, df_cities):
        self.df = df_cities
        self.distance = dict([((t.origin, t.destination), t.distance) for t in self.df.itertuples()])
        self.cities = list(set(self.df['destination']))

        self.tour_lst = []
        self.tour_leg_distances_lst = []
        self.total_distance_lst = []

        self.soln_df = None
        self.shortest_tour = None
        self.shortest_tour_leg_distances = None
        self.shortest_distance = None

    def generate_soln_df(self):
        soln_dict = {'tour_lst': self.tour_lst, 'tour_leg_distances_lst': self.tour_leg_distances_lst,
                     'total_distance_lst': self.total_distance_lst}
        self.soln_df = pd.DataFrame(soln_dict)


    def generate_add_heuristic_df(self):
        i = 0
        while i < len(self.cities):
            starting_city = self.cities[i]
            self.generate_nearest_neighbor_soln(starting_city)
            i = i + 1
        self.generate_soln_df()



    def generate_nearest_neighbor_soln(self, starting_city):
        # initalize
        _total_distance_lst = []
        _tour_leg_distances_lst = []
        cities_unvisited = self.cities.copy()
        current_city = starting_city
        i = 0

        # initalize tracker lists
        _tour_lst = [starting_city]
        cities_unvisited.remove(starting_city)

        while len(cities_unvisited) > 0:
            df_temp1 = self.df[self.df['destination'].isin(cities_unvisited)]
            df_temp2 = df_temp1[df_temp1['origin'] == current_city]
            min_row = df_temp2.loc[df_temp2['distance'].idxmin()]
            d = min_row.distance
            next_city = min_row.destination

            # update local tracker lists
            _tour_lst.append(next_city)
            _tour_leg_distances_lst.append(d)
            cities_unvisited.remove(next_city)

            # update for next iteration
            current_city = next_city
            i = i + 1

        # accounting for last mile back to origin
        last_city = _tour_lst[-1]
        last_mile = (starting_city, last_city)
        last_mile_distance = self.distance[last_mile]
        _tour_lst.append(starting_city)
        _tour_leg_distances_lst.append(last_mile_distance)

        # update global tracker lists
        self.tour_lst.append(_tour_lst)
        self.tour_leg_distances_lst.append(_tour_leg_distances_lst)
        self.total_distance_lst.append(sum(_tour_leg_distances_lst))

    def print_optimal_from_soln_df(self):
        index_min = self.soln_df['total_distance_lst'].idxmin()
        min_row = self.soln_df.loc[index_min]
        self.shortest_tour = min_row.tour_lst
        self.shortest_tour_leg_distances = min_row.tour_leg_distances_lst
        self.shortest_distance = min_row.total_distance_lst

        print("shortest_tour", self.shortest_tour)
        print("shortest_leg_distances", self.shortest_tour_leg_distances)
        print("shortest_distance", self.shortest_distance)

    def generate_swap_heuristic_df(self):
        N = len(self.cities)
        i = 0
        # starting solution
        self.generate_nearest_neighbor_soln(self.cities[0])

        while i < N - 2:
            # generate new tour
            new_tour = self.tour_lst[0].copy()
            city1 = new_tour[i]  # 1
            city2 = new_tour[i + 1]  # 9
            city3 = new_tour[i + 2]  # 14
            city4 = new_tour[i + 3]  # 15

            new_tour.remove(city3)
            new_tour.insert(i + 1, city3)

            #     print("swap city", city2, " with city", city3)
            #     print("starting_tour:", tour_lst[0])
            #     print("new_tour_add:", new_tour)
            #     print()

            # update leg_distances
            new_leg_distance = self.tour_leg_distances_lst[0].copy()

            d1 = self.distance[(city1, city3)]
            d2 = self.distance[(city3, city2)]
            d3 = self.distance[(city2, city4)]

            #     print("d1:", d1)
            #     print("d2:", d2)
            #     print("d3:", d3)
            #     print()

            temp_lst = [d1, d2, d3]
            #     print("temp_lst:", temp_lst)
            #     print("new_leg_distance:", new_leg_distance)
            #     print()

            new_leg_distance[i:i + 3] = temp_lst
            #     print("new_leg_distance:", new_leg_distance)
            #     print()

            self.tour_lst.append(new_tour)
            self.tour_leg_distances_lst.append(new_leg_distance)
            self.total_distance_lst.append(sum(new_leg_distance))

            i = i + 1

        self.generate_soln_df()


# ********************************************************************************
# ********************************************************************************


if __name__ == '__main__':
    df2 = pd.read_csv('city_data_v2b.csv')
    df3 = pd.read_csv('city_data_v3.csv')

    tsp2 = HeuristicTSP(df2)
    tsp3 = HeuristicTSP(df3)

    # ADD
    # tsp2.generate_add_heuristic_df()
    # tsp2.print_optimal_from_soln_df()
    # print(tsp2.soln_df)

    # SWAP
    tsp3.generate_swap_heuristic_df()
    tsp3.print_optimal_from_soln_df()
    print(tsp3.soln_df)

