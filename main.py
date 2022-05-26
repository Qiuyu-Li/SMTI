from util import *
import numpy as np
import time

# -------------------------------------
# Simple test case
# -------------------------------------
n = 6
p1 = 0.7
p2 = 0.5
m_pr = generate_smti_table(n,p1,p2)
w_pr = generate_smti_table(n,p1,p2)

print("The preference table of men:")
print(m_pr)
print("The preference table of women:")
print(w_pr)

repair = True
non_repeating = True
iter = 0

# record unmatched pairs to avoid being trapped in swapping within a subgroup
match_m_record = []
while repair and non_repeating and iter < 100:
    iter = iter + 1
    match_m, match_w = Gale_Shapley(n,m_pr,w_pr)
    w_pr, repair = swap(m_pr,w_pr,match_m,match_w,n)
    if len(match_m_record) != 0:
        for record in match_m_record:
            if np.array_equiv(record,match_m):
                non_repeating = False
                break
    match_m_record.append(match_m)

print("Iteration times: ",iter)

'''
# -------------------------------------
# More users for testing
# -------------------------------------
def run(n,p1,p2):
    m_pr = generate_smti_table(n,p1,p2)    # Generate a random reference table for men
    w_pr = generate_smti_table(n,p1,p2)    # Generate a random reference table for women

    repair = True
    non_repeating = True
    iter = 0
    match_m_record = []
    while repair and non_repeating:
        iter = iter + 1
        match_m, match_w = Gale_Shapley(n,m_pr,w_pr)
        w_pr, repair = swap(m_pr,w_pr,match_m,match_w,n)
        if len(match_m_record) != 0:
            for record in match_m_record:
                if np.array_equiv(record,match_m):
                    non_repeating = False
                    break
        match_m_record.append(match_m)
        if iter == 1:
            matched_1 = 0
            for m in match_m:
                if m != -1:
                    matched_1 = matched_1 + 1

    matched_2 = 0
    for m in match_m:
        if m != -1:
            matched_2 = matched_2 + 1

    improve = matched_2 - matched_1

    return (iter,improve)
'''

'''
iter_list = []
improve_list = []
time_list = []
total_iter = 10
for n in np.linspace(30, 300, num=11, dtype=int):
    iter = 0
    improve = 0
    time_cost = 0
    for t in range(total_iter):
        time0 = time.perf_counter()
        iter_this,improve_this = run(n,0.5,0.5)
        time1 = time.perf_counter()
        iter = iter + iter_this
        improve = improve + improve_this
        time_cost = time_cost + time1 - time0

    print("finished n=",n,iter/total_iter,improve/total_iter,time_cost/total_iter)
    iter_list.append(iter/total_iter)
    improve_list.append(improve/total_iter)
    time_list.append(time_cost/total_iter)

print(iter_list)
print(improve_list)
print(time_list)
'''
'''
iter_list = []
improve_list = []
time_list = []
total_iter = 100
for p1 in np.linspace(0, 1, num=11):
    iter = 0
    improve = 0
    time_cost = 0
    for t in range(total_iter):
        time0 = time.perf_counter()
        iter_this,improve_this = run(100,p1,0.5)
        time1 = time.perf_counter()
        iter = iter + iter_this
        improve = improve + improve_this
        time_cost = time_cost + time1 - time0

    iter_list.append(iter/total_iter)
    improve_list.append(improve/total_iter)
    time_list.append(time_cost/total_iter)

print(iter_list)
print(improve_list)
print(time_list)
'''

'''
iter_list = []
improve_list = []
time_list = []
total_iter = 100
for p2 in np.linspace(0, 1, num=11):
    iter = 0
    improve = 0
    time_cost = 0
    for t in range(total_iter):
        time0 = time.perf_counter()
        iter_this,improve_this = run(100,0.5,p2)
        time1 = time.perf_counter()
        iter = iter + iter_this
        improve = improve + improve_this
        time_cost = time_cost + time1 - time0

    iter_list.append(iter/total_iter)
    improve_list.append(improve/total_iter)
    time_list.append(time_cost/total_iter)

print(iter_list)
print(improve_list)
print(time_list)
'''