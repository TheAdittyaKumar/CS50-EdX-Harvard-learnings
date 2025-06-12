import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target): #BFS
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    #step 1 creating the node to represent the starting actor (source) and add it to the QueueFrontier which give BFS
    #Also a set to keep track of explored actors
    start = Node(state=source,parent=None,action=None) 
    frontier= QueueFrontier()
    frontier.add(start) # [ Node("1", parent=None, action=None) ]
    explored = set() #tracks explored person_id's
    #step 2
    while not frontier.empty():
        node= frontier.remove() #we take person A off the frontier to explore who they are connected to.
        #person "A" started in Movie X with person "B" and movie W with Person D
        #neighbors_for_person("1") ➜ { ("m1", "2"), ("m4", "4") }
        if node.state==target: #Pull the next actor from the frontier, If this actor is the target, backtrack to build the path by following .parent pointers
            path=[]
            while node.parent is not None:
                path.append((node.action,node.state)) #(movie_id, person_id)
                node= node.parent 
            path.reverse()  #("m3", "5")  ← C → E
                            #("m2", "3")  ← B → C
                            #("m1", "2")  ← A → B

            return path #[("m1", "2"), ("m2", "3"), ("m3", "5")]
                # “Person A starred in m1 with 2, who starred in m2 with 3, who starred in m3 with 5.”
        explored.add(node.state) #mark this person as explored so we don't revisit

        #step 4 adding neighbors to frontier
        for movie_id, person_id in neighbors_for_person(node.state): 
            if person_id not in explored and not frontier.contains_state(person_id): #This avoids revisiting nodes. If Person B or D is already in the explored set or frontier, we skip them.
                child=Node(state=person_id, parent=node,action=movie_id)
                #We now create a new node for this neighbor:
                    #state = person_id → the actor we’re going to next
                    #parent = node → the actor we're coming from
                    #action = movie_id → the movie they shared
                #“Create a path from the current actor to the one they acted with, and record how we got there.”
            if person_id==target: 
                # Optional Optimization: Check for target before adding to frontier
                path=[(movie_id,person_id)]
                while node.parent is not None:
                    path.append((node.action,node.state))
                    node = node.parent
                path.reverse()
                return path
            frontier.add(child)

    return None

    # TODO
    raise NotImplementedError


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
