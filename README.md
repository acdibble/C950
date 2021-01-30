A. Identify a named self-adjusting algorithm (e.g., “Nearest Neighbor
algorithm,” “Greedy algorithm”) that you used to create your program to deliver
the packages.

```
In order to load the packages onto the trucks I used a combination of a
nearest-neighbor algorithm and a greedy algorithm, i.e. after loading a package
onto one truck, the algorithm will load that truck until there are no more
available packages (greedy), and it will choose the next package according to
the distance between the next package and the previously-loaded package
(nearest-neighbor).
```

B. Write an overview of your program, in which you do the following:

1.  Explain the algorithm’s logic using pseudocode.

```
initialize Trucks
initialize Packages
initialize Graph

While priority packages remain
    For each Truck of Trucks
        Until Truck is full or no priority packages remain
            Load Truck with nearest priority

    For each Truck of Trucks
        Load package closest to the previously-loaded package's destination

    Deliver packages

While packages available for delivery
    For each Truck of Trucks
        Load package closest to the previously-loaded package's destination

    Deliver packages
```

2.  Describe the programming environment you used to create the Python
    application.

```
IDE: Visual Studio Code v1.52.1
Python: v3.9
Hardware:
Processor: 2.2 GHz Intel Core i7
Memory: 16 GB 2400 MHz DDR4
```

3.  Evaluate the space-time complexity of each major segment of the program, and
    the entire program, using big-O notation.

4.  Explain the capability of your solution to scale and adapt to a growing
    number of packages.

```
My solution doesn't assume a fixed number of packages, trucks, or destinations,
which means it can continue to grow with packages until the algorithms
themselves are no longer efficient enough to quickly enough determine how to
deliver the packages.
```

5.  Discuss why the software is efficient and easy to maintain.

```
The software is efficient because it is able quickly determine a short route for
both trucks to travel while still meeting all the requirements. It is easy to
maintain due to the presence of comments and static typing which helps reduce
type errors.
```

6.  Discuss the strengths and weaknesses of the self-adjusting data structures
    (e.g., the hash table).

```
The hashing method used to insert items into the the hash table is not perfect
and it causes a lot of collisions in buckets which causes the underlying linear
storage to grow much larger than it needs to be.

It however allows for an average insertion and lookup time-complexity of O(1).
The table also allows for easy O(n) iteration over all items
```

C. Write an original program to deliver all the packages, meeting all
requirements, using the attached supporting documents “Salt Lake City Downtown
Map,” “WGUPS Distance Table,” and the “WGUPS Package File.”

1.  Create an identifying comment within the first line of a file named
    “main.py” that includes your first name, last name, and student ID.

[X]

2.  Include comments in your code to explain the process and the flow of the
    program.

[X]

D. Identify a self-adjusting data structure, such as a hash table, that can be
used with the algorithm identified in part A to store the package data.

```
Hash table
```

1.  Explain how your data structure accounts for the relationship between the
    data points you are storing.

```
The hash table is used to store packages with matching destinations. When a
package is loaded on a truck, other packages with the same destination are
checked to see if they are available to be loaded on the truck.

It is also used to store all the packages so they can be looked up by their ID.
```

G. Provide an interface for the user to view the status and info (as listed in
part F) of any package at any time, and the total mileage traveled by all
trucks. (The delivery status should report the package as at the hub, en route,
or delivered. Delivery status must include the time.)

[X]

1.  Provide screenshots to show the status of all packages at a time between
    8:35 a.m. and 9:25 a.m.

9:00 AM screenshot:

![](assets/09-00-status.png)

2.  Provide screenshots to show the status of all packages at a time between
    9:35 a.m. and 10:25 a.m.

10:00 AM screenshot:

![](assets/10-00-status.png)

3.  Provide screenshots to show the status of all packages at a time between
    12:03 p.m. and 1:12 p.m.

12:03 PM screenshot:

![](assets/12-00-status.png)

H. Provide a screenshot or screenshots showing successful completion of the
code, free from runtime errors or warnings, that includes the total mileage
traveled by all trucks.

![](assets/miles-traveled.png)

I. Justify the core algorithm you identified in part A and used in the solution
by doing the following:

1.  Describe at least two strengths of the algorithm used in the solution.

```
The algorithm is scalable. It makes no assumptions about the number of trucks,
packages, or destinations, and it should therefore be able to accommodate an
increase in any of them.

The algorithm finds an efficient solution for the given requirements in that
both trucks must travel fewer than 80 miles to deliver all the packages.
```

2.  Verify that the algorithm used in the solution meets all requirements in the
    scenario.

```
The requirements have been met and this is verifiable by using option 3 in the
app. There you can find loading times, delivery times, which truck delivered the
package and with what other packages the package was delivered.

Additionally there are errors in place that will throw if a requirement isn't
met at runtime and there are unit tests validating the requirements as well.
```

3.  Identify two other named algorithms, different from the algorithm
    implemented in the solution, that would meet the requirements in the
    scenario.

```
Dijkstra algorithm, A* search algorithm
```

a. Describe how each algorithm identified in part I3 is different from the
algorithm used in the solution.

```
The Dijkstra and A* search algorithms both traverse the graph to find the
shortest distance between two vertices. The solution I used just uses the given
distances between all the vertices without any optimizations.
```

J. Describe what you would do differently, other than the two algorithms
identified in I3, if you did this project again.

```
If I were to do this project again, I would look for a more general solution to
the problem. The current solution works well for the limited input given and I'm
not sure what edge cases would arise as the packages to be delivered increase.
Also the solution might not scale well with a large number of packages. Lastly,
I used a very naive algorithm to determine the next package to deliver. The
routes could be shortened by finding shorter paths between two points.
```

K. Justify the data structure you identified in part D by doing the following:

1.  Verify that the data structure used in the solution meets all requirements
    in the scenario.

```
The hash table has an insert and lookup function that work correctly and without
any errors.
```

a. Explain how the time needed to complete the look-up function is affected by
changes in the number of packages to be delivered.

```
Anywhere I needed to directly address a package, it was part of a hashmap with a
O(1) lookup. Other than that, the packages are linearly iterated in O(n) when
determining which packages to deliver. Obviously as the number of packages
increase, so too will the runtime of the algorithm.
```

b. Explain how the data structure space usage is affected by changes in the
number of packages to be delivered.

```
The hash table will continue to grow was the number of packages grow. To
mitigate the effect of using large amounts of linear
```

c. Describe how changes to the number of trucks or the number of cities would
affect the look-up time and the space usage of the data structure.

```
The trucks are held in a simple list and are never directly addressed. The space
will grow linearly but the lookup time is moot.

The cities and distances between them are held in a graph. The lookup time there
will remain O(1) as the number of cities grows. The space grows at O(n^2) as
each city references the other.
```

1.  Identify two other data structures that could meet the same requirements in
    the scenario.

```
Linked list, priority queue
```

a. Describe how each data structure identified in part K2 is different from the
data structure used in the solution.

```
A linked list is a linear storage data structure. Its average lookup is O(n)
because its stored elements need to be iterated over in order to find the
desired value. If appending to the end of the list, insertion is O(n) unless
there is a tail pointer. If a new value is prepended, insertion is O(1).

A priority queue could help simplify the delivery of packages by assigning a
priority to the package before putting it in the queue. This could be done two
ways:

O(1) retrieval and O(n) insertion if elements are sorted at insertion time
O(n) retrieval and O(1) insertion if elements are not sorted at insertion time
```
