import argparse

def evaluate(curr_cities,costs):
    """Takes the current selection of cities which will be put together and calculates score

    Args: 

        curr_cities(list): List of cities as tuples 
        costs(dict): dictionary of costs 
    """
    cost = 0
    
    for x in curr_cities:
        
        cost += costs[x]

    return cost


def extend_admin(curr_cities, costs,cost_lim):
    """Extends the current selection of cities with another city pair and evalutes the score. If the score is below the threshold it will be returned for further investigation
    
        Args: 
        curr_cities(List) : List of current city tuples
        costs(dict) : dictionary of the costs. Key = City tuple; Value = cost
        cost_lim (int) : Value of the cost limit 
    """
    
    new_admins = []
    used_cities = [ x for tuple in curr_cities for x in tuple]
    
    for tuple in costs.keys():
        ext = []
        ext.append(curr_cities)


        flat_ext = []
        for sublist in ext:
            if isinstance(sublist,list):
                for item in sublist:
                    flat_ext.append(item)
            else:
                flat_ext.append(sublist)
        
        ext = flat_ext
        
        if tuple[0] not in used_cities and tuple[1] not in used_cities:
            ext.append(tuple)
           
            if evaluate(ext,costs) <= int(cost_lim):
                new_admins.append(ext)

   
    return new_admins




def admin(costs,cost_lim):
    """Takes the costs dictionary and searches for city combinations which fullfill the cost limit. 

        Args:

            costs(dict):  dictionary of the costs. Key = City tuple; Value = cost
            cost_lim(int): Value of the cost threshold

        Returns: 
            admin_cities(list): list where each sublist corresponds to one administration
    """ 

    admin_cities = []
    new_admins = []
    for city in costs.keys():
        admin_cities.append(city)
    
    while len(admin_cities[0]) < len(cities)/2:
        
        new_admins = []
        for x in admin_cities:
            new_admins.extend(extend_admin(x,costs,cost_lim))
        
        admin_cities = new_admins

    return admin_cities



def filter_results(results):
    """ Filters the results and only includes unique administrations
    """
    final_results = []
    for sub_lst in results:
        sub_set = set(sub_lst)
        if sub_set not in [set(x) for x in final_results]:
            final_results.append(sub_lst)
    
    return(final_results)


if __name__ == __name__:

    
    parser = argparse.ArgumentParser(
                        prog='Administration',
                        description='',
                        )

    parser.add_argument("input",help="Input File")
    parser.add_argument("-o","--optimize", help= "If this flag is activated only the lowest score will be displayed",default=False,action="store_true")

    args = parser.parse_args()

    #input parsing
    input = []
    with open(args.input) as f: 
        for line in f:
            input.append(line.strip().split())

    num_cap = input[0][0]
    cost_lim = input[0][1]
    input.remove(input[0])

    #creates a dictionary with the costs of each city tuple 
    costs = {}
    cities = list(input[0])
    for row in range(1,len(input)):
        for column in range(len(input[0])):
          
            if input[row][column] != "-" and str(input[0][column] + input[0][row - 1]) not in costs.keys(): # do not include city tuples with the same city and allready existing city pairs 
                costs[str(input[0][row - 1] + input[0][column])] = int(input[row][column])

    #Applying algorithm         
    final = admin(costs,cost_lim)
    filtered_results = filter_results(final)
    
    if args.optimize:
        score_dict = {}

        for admin in filtered_results:
            
            score_dict[str(admin)] = evaluate(admin,costs)
        print("Best scoring Solution:",min(score_dict.values()))
            
    else:
        with open("lmiksch-Adminstration.out","w") as out:
            for admin in filtered_results:
                print(" ".join(admin))
                for city_tuple in admin:
                    out.write(city_tuple)
                    out.write(" ")
                out.write("\n")


    



