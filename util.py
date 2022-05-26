import random
import numpy as np

def generate_smti_table(n,p1,p2):
    preference = []

    # Generate a randomly ordered list for each man
    for _ in range(n):
        list_ordered = list(range(n))
        random.shuffle(list_ordered)
        preference.append(list_ordered)

    # Add incompleteness
    for i in range(n):
        for j in range(n):
            p = random.uniform(0, 1)
            if p < p1:
                preference[i][j] = -1

    # Add ties
    for i in range(n):
        for j in range(1,n):
            p = random.uniform(0, 1)
            if p < p2:
                tie = []
                tie.append(preference[i][j])
                if (type(preference[i][j-1]) == list):
                    tie = tie + preference[i][j-1]
                    preference[i][j-1] = []
                else:
                    tie.append(preference[i][j-1])
                    preference[i][j-1] = -1
                preference[i][j] = tie

    # Clear up

    # (1) Delete -1's in ties
    for i in range(n):
        for j in range(n):
            if type(preference[i][j]) == list:
                clean_list = [k for k in preference[i][j] if k != -1]
                preference[i][j] = clean_list

    # (2) Delete -1's in list
    for i in range(n):
        clean_list = []
        for j in range(n):
            if type(preference[i][j]) != list and preference[i][j] != -1:
                clean_list.append(preference[i][j])
            elif type(preference[i][j]) == list:
                if len(preference[i][j]) == 1:
                    clean_list.append(preference[i][j][0])
                elif len(preference[i][j]) > 1:
                    clean_list.append(preference[i][j])
        preference[i] = clean_list

    return preference

def tie_breaking(table):
    broken_table = []
    for i in range(len(table)):
        broken_list = []
        for j in range(len(table[i])):
            if type(table[i][j]) == list:
                for el in table[i][j]:
                    broken_list.append(el)
            else:
                broken_list.append(table[i][j])
        broken_table.append(broken_list)
    return broken_table

def gen_ranking_w(table,n):
    ranking_w = np.full((n,n),n+1)
    for i in range(n):
        for j in range(len(table[i])):
            if type(table[i][j]) == list:
                for el in table[i][j]:
                    ranking_w[i][el] = j
            else:
                ranking_w[i][table[i][j]] = j
    return ranking_w

def swap(table_m,table_w,match_m,match_w,n):
    repair = False                         # This is to tell the main function that calls this function whether  a tie-reordering happened after this function is run
    broken_table_m = tie_breaking(table_m) # arbitrary tie-breaking: this is only to convenient 
    ranking_w = gen_ranking_w(table_w,n)   
    for i in range(n):
        if match_m[i] != -1:
            continue
        for w in broken_table_m[i]:
            k = match_w[w]
            if (k != -1) and (ranking_w[w][i] == ranking_w[w][k]):
                repair = True
                row_i = ranking_w[w][i]    # the row in ordering_w that contains i and k
                table_w[w][row_i].remove(i)
                for a in range(len(table_w[w][row_i])):
                    if table_w[w][row_i][a] == k:
                        table_w[w][row_i][a] = i
                        table_w[w][row_i].insert(a+1,k)
    return (table_w,repair)

def Gale_Shapley(n,m_pr,w_pr):

    # (1) Break the tie
    ordering_m = tie_breaking(m_pr)
    ordering_w = tie_breaking(w_pr)

    # (2) Initialization
    match_m = np.full(n, -1)      # the matching result of men
    match_w = np.full(n, -1)      # the matching result of women
    list_position = np.full(n,0)   # how many women this man has proposed to
    match_w_rank = np.full(n, n+1) # the current best offer for each woman
    offer = np.full(n, -1)        # the women each man makes offer to at a particular iteration
    ranking_w = gen_ranking_w(ordering_w,n)

    offer_made = True
    while offer_made == True:

    # (3) Men making the offers
        offer_made = False
        for i in range(n):
            if (match_m[i] == -1) and (list_position[i] < len(ordering_m[i])):
                offer[i] = ordering_m[i][list_position[i]]
                list_position[i] = list_position[i] + 1
                offer_made = True
            else:
                offer[i] = -1

    # (4) Women considering the offers

        for j in range(n):
            ranking = ranking_w[j]
            best_man = -1
            best_offer_rank = n+1

        # (4.1) Women choose the best offer they get in this iteration (the smaller the rank, the better)
            for i in range(n):
                if offer[i] == j:
                    if ranking[i] < best_offer_rank:
                        best_man = i
                        best_offer_rank = ranking[i]
	
        # (4.2) Women accept or reject offers
            if best_offer_rank < match_w_rank[j]:
                if match_w[j] != -1: 
                    match_m[match_w[j]] = -1    # reject current offer
                match_m[best_man] = j
                match_w[j] = best_man
                match_w_rank[j] = best_offer_rank

    return (match_m,match_w)