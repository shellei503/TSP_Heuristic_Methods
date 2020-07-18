# TSP_Heuristic_Methods
 Solving TSP problems using heuristic methods
 
## Problem Definition
The traveling salesman problem (TSP) consists of a salesman and a set of cities. The salesman has to
visit each one of the cities starting from a certain one (e.g. the hometown) and returning to the
same city. The challenge of the problem is that the traveling salesman wants to minimize the total
length of the trip. 

https://www.csd.uoc.gr/~hy583/papers/ch11.pdf
 
## Heuristic Methods
1. Add - With the `add heuristic` method, we start by build N tours, where N is the total number of cities in our 
dataset. Each tour will start with a different city. A tour is created by successively selecting the next city in the 
tour based on whichever unvisited city is nearest to the current one. The total distance is calculated for each of the N 
tours and the tour with the lowest total distance is returned as the final solution.

 
## Main Files
* `city_data.csv`: input file for model, distances between cities 
* `add_heuristic_enginge.py`: Python model for solving TSP problem using add heuristic method

## Instructions
1. `Open add_heuristic_engine.py`
2. Run the model
3. Model results will print to the console.

## Required Environment/Packages/Libraries
* Conda
* Python           : 3.7
* pandas           : 1.0.5


## Contact
Please feel free to reach out with any questions, suggestions or comments:
* S. Lei
* slei232@gmail.com