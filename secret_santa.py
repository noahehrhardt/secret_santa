import random

'''
This program randomly assigns secret santa partners given a dictionary of names as keys and a set 
of people they don't want to match with (not including themself) as values.

It creates a dictionary that acts as a directed graph. The graph is used to create a Hamilton cycle
that finds a set of pairings that does not match people with themselves or somebody they do not want 
(perhaps the person they matched with last year). If no solution can be found, it prints and exits.

The program then starts a REPL that can print the matches to separate files, a single file, stdout,
or one at a time.

The algorithm is efficient, but it is not guaranteed to find a solution. It tries a certain number
times, shuffling the array each time, and then quits. It will not be able to find a solution if 
somebody lists every other person on their "do not match" list.
'''
if __name__ == '__main__' :
    # list of names and people they do not want to match with:
    graph = {"Noah": {"Oliver"}, "Oliver": {"Wyatt"}, "Wyatt": {"Eli"}, "Eli": {"Emery"}, "Emery": {"Noah"}}

    # get a shuffled list of names:
    shuffled = list(graph.keys())
    random.shuffle(shuffled)
    
    givers = set(shuffled)

    # get valid matches:
    for key in graph:
        graph[key] = givers - graph[key] - {key}

    fails = 0
    max_fails = 20
    placeholder = shuffled

    unfound = True
    while(unfound):
        # make matches with Hamilton cycle:
        path = [shuffled.pop(0)]
        for i in range(1, len(graph)):
            for j in range(len(shuffled)):
                if shuffled[j] not in path and shuffled[j] in graph[path[i-1]]:
                    path.append(shuffled.pop(j))
                    break
        
        # if a full path was found:
        if len(path) == len(graph) and path[0] in graph[path[len(path)-1]]:
            path.append(path[0])
            unfound = False
        else: #reshuffle and try again:
            fails += 1
            shuffled = placeholder
            random.shuffle(shuffled)
        
        # if a full path hasn't been found after max_fails attempts:
        if fails > max_fails:
            print("Failed to make matches :(")
            exit(1)

    # set up dictionary of matches and print to files:
    matches = {}
    for i in range(len(graph)):
        matches[path[i]] = path[i+1]
    
    # REPL:
    while(True):
        # input only works properly on python3
        name = input("Name or command: ")
        if name == "exit" or name == "quit" or name == "done":
            break
        
        #prints each match to a separate file:
        if name == "file":
            for key in matches:
                f = open("out/" + key + ".txt", "w+")
                f.write(key + " will give a gift to " + matches[key] + "\n")
                f.close()
            print("Matches printed to files.\n")
        
        # prints all matches to a master file:
        elif name == "master":
            f = open("out/master.txt", "w+")
            for key in matches:
                f.write(key + " will give a gift to " + matches[key] + "\n\n")
            f.close()
            print("All matches printed to master file.\n")

        # prints all matches to stdout:
        elif name == "all":
            for key in matches:
                print(key + " will give a gift to " + matches[key]  + "\n")
        
        # prints the reqested name:
        elif name in matches:
            print(name + " will give a gift to " + matches[name])
            # prints lines to hide previous input from others:
            for i in range(10):
                print("\n")
        else:
            print("Name not in list\n")
