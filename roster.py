import random
import csv
roles = ["MC", "TH", "AC1", "AC2", "CB"]
# Define who can do each role
NUM_WEEKS = 8 # number of weeks to generate a roster for

def read_candidates(candidate_file="servers.csv"):
    '''
    read the candidates from a CSV file defining who can do each role, in the format
    MC, name1, name2
    TH, name1, name3
    etc
    inputs:
        filepath of the CSV file
    '''
    with open(candidate_file, mode='r') as csv_file:
        reader = csv.reader(csv_file)
        candidates = {}
        for row in reader:
            # remove whitespace
            row = [x.strip() for x in row]
            # save the candidates in a dictionary
            candidates[row[0]] = frozenset(row[1:])
    return candidates

def choose_server(temp_candidates: set, week_servers: dict, all_candidates: frozenset, exclude_servers: list):
    '''
    Select a server from the candidates
    Parameters:
        temp_candidates - set of the people who can be the role, who haven't since it last reset
        week_servers - dict of the people who already have a role
        all_candidates - all the possible people who can be the role
        exclude_servers - anyone to exclude from this round of selection
    '''
    # check if temp_candidates is empty and reset if it is 
    debugTempreset = False
    if len(all_candidates) == 3:
        print(temp_candidates)
    if not temp_candidates:
        debugTempreset = True
        temp_candidates.update(all_candidates)

    # remove all servers in exclude_servers from temp_candidates and
    # all_candidates
    eligble_candidates = set(temp_candidates)
    if exclude_servers:
        eligble_candidates.difference_update(exclude_servers)
    # remove all servers in week_servers from temp_candidates and all_candidates
    eligble_candidates.difference_update(week_servers.values())
    # if there are no eligible candidates, update eligible candidates to be
    # all_candidates - exclude_servers
    debugReset = False
    if not eligble_candidates:
        debugReset = True
        eligble_candidates = set(all_candidates)
        if exclude_servers:
            eligble_candidates.difference_update(exclude_servers)
        eligble_candidates.difference_update(week_servers.values())
    # if there are stil none, return NA
    if not eligble_candidates:
        return "NA"
    # choose a random server
    week_server = random.choice(list(eligble_candidates))

    temp_candidates.discard(week_server)
    #if debugReset:
    #    week_server += "[RST]"
    #if debugTempreset:
    #    week_server += "[TMPRST]"
    # return the person
    return week_server
 


def generate_roster(exclude_servers={}, weeks=NUM_WEEKS):
    '''
    Generates roster for a number of weeks specified (default 4)
    Parameters:
        exclude_servers: dictionary of dictionaries contianing servers to exclude from each role for each week
            e.g {1:{"MC":["Person 1", "Person 2"]}}
    A dictionary can be passed to exclude a server from the roster
    for a given week, the dictionary should have a key of int equal to
    the week number (starting at 0), and the value should be a dictionary where
    the key is the role, and the value is a list of servers
    '''
    candidates = read_candidates()
    MC = candidates.get("MC")
    TH = candidates.get("TH")
    AC1 = candidates.get("AC1")
    AC2 = candidates.get("AC2")
    CB = candidates.get("CB")
    # if any of the roles are empty, raise an error
    if not MC or not TH or not AC1 or not AC2 or not CB:
        raise ValueError("One or more roles in candidates.csv has no available servers")
    temp_MC = set(MC)
    temp_TH = set(TH)
    temp_AC1 = set(AC1)
    temp_AC2 = set(AC2)
    temp_CB = set(CB)
    rosters = []
    for week in range(0, weeks):
        if not exclude_servers.get(week):
            excluded = {"MC":[], "TH":[], "AC1":[], "AC2":[], "CB":[]}
        else:
           excluded = exclude_servers.get(week)
        week_servers = dict()
        # select a MC
        week_MC = choose_server(temp_MC, week_servers, MC, excluded.get("MC"))       
        # add the person to the dictionary
        week_servers["MC"] = week_MC

        # select a TH
        week_TH = choose_server(temp_TH, week_servers, TH, excluded.get("TH"))
        # add the person to the dictionary
        week_servers["TH"] = week_TH
    
        # select an AC1
        week_AC1 = choose_server(temp_AC1, week_servers, AC1, excluded.get("AC1"))
        # add the person to the dictionary
        week_servers["AC1"] = week_AC1

        # select an AC2
        week_AC2 = choose_server(temp_AC2, week_servers, AC2, excluded.get("AC2"))
        # add the person to the dictionary
        week_servers["AC2"] = week_AC2

        # select a CB
        week_CB = choose_server(temp_CB, week_servers, CB, excluded.get("CB"))
        # add the person to the dictionary
        week_servers["CB"] = week_CB

        # check if there are any other roles
        # Check for additional roles and fill them if necessary
        other_roles = set(candidates.keys()) - set(["MC", "TH", "AC1", "AC2", "CB"])
        for role in other_roles:
            candidates_for_role = candidates.get(role, [])
            if any(candidate not in week_servers.values() for candidate in candidates_for_role):
                week_server = choose_server(
                    set(candidates_for_role),
                    week_servers,
                    candidates_for_role,
                    []
                )
                week_servers[role] = week_server
            else:
                print("Nobody available for " + role)
            # check if TB1 has been added but not TB2
        if "TB1" in week_servers and "TB2" not in week_servers:
            # remove TB1 from week_servers
            week_servers.pop("TB1")
        if "TB2" in week_servers and "TB1" not in week_servers:
            # remove TB2 from week_servers
            week_servers.pop("TB2")
        # add the roster to the list of rosters
        rosters.append(week_servers)
    return rosters

def print_rosters(rosters):
    '''
    Prints a list of rosters
    '''
    i = 0
    for week_servers in rosters:
        if len(week_servers.values()) != len(set(week_servers.values())):
            raise ValueError("Duplicate server in roster")
        i+=1
        print("Week " + str(i) + ":")
        for role in roles:
            print(role + ": " + week_servers[role])
        # check if there are any other roles
        other_roles = set(week_servers.keys()) - set(["MC", "TH", "AC1", "AC2", "CB"])
        for role in other_roles:
            print(role + ": " + week_servers[role])

        print("\n")

def save_rosters(rosters, output_file="roster.csv"):
    '''
    Save the rosters as a CSV
    Parameters:
        rosters (list): List of dictionaries where each dictionary represents a week's roster.
        output_file (str): File path for the output CSV file. Default is "combined_rosters.csv".
    '''
    # Ensure that the rosters list is not empty
    if not rosters:
        print("No rosters to write.")
        return

    # Extract field names from the first roster
    fieldnames = list(rosters[0].keys())
    # Add a column for week number
    fieldnames.insert(0, "Week")

    # Write the rosters to the CSV file
    with open(output_file, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write the header
        writer.writeheader()

        # Write each week's roster
        i = 0
        for week_servers in rosters:
            i +=1
            week_servers["Week"] = i
            writer.writerow(week_servers)

    print(f"Rosters written to {output_file}.")

def ask_excluded():
    '''
    Interactive prompt to exclude people from the roster
    '''
    excluded = {}
    for week in range(0,NUM_WEEKS):
        add_person = True
        while (add_person):
            # ask for a person to exclude
            next_exclusion = input(("Enter name of a person to exclude for week " + str(week + 1) + ", or press enter when nobody else to exclude week " + str(week + 1) +": "))
            if next_exclusion == "" or next_exclusion == " ":
                break
            add_role = True
            exclude_roles = []
            while(add_role):
                # ask what roles to exclude the person from
                role_exclusion = input(("Enter a role to exclude (MC, TH, AC1, AC2, CB or ALL), or press enter when no more roles to exclude: ")).upper()
                valid_inputs = ["MC", "TH", "AC1", "AC2", "CB", "ALL", ""]
                if role_exclusion not in valid_inputs:
                    print("Invalid input")
                else:
                    if role_exclusion == "ALL":
                        exclude_roles = ["MC", "TH", "AC1", "AC2", "CB"]
                        add_role = False
                    elif role_exclusion != "":
                        exclude_roles.append(role_exclusion)
                    else:
                        add_role = False
            # add the person to the excluded dictionary
            if next_exclusion != "":
                # format of exclusion is {week: {role: [person1, person2]}}
                if week not in excluded:
                    excluded[week] = {}
                for role in exclude_roles:
                    if role not in excluded[week]:
                        excluded[week][role] = []
                    excluded[week][role].append(next_exclusion)
            else:
                add_person = False
        print("\n")
    return excluded
            

if __name__ == "__main__":
    excluded_servers = ask_excluded()
    print("Excluded Servers:", excluded_servers)
    rosters = generate_roster(excluded_servers)
    print_rosters(rosters)
    file_name = input("Enter the name to save the roster as, or leave blank to skip: ")
    if file_name == "" or file_name == " ":
        exit()
    # check if the name ends with .csv, append it if not
    if file_name[-4:] != ".csv":
        file_name += ".csv"
    save_rosters(rosters, file_name)
