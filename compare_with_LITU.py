from util import *
from LTIU import *
import numpy as np
import time

def run_compare(n,p1,p2):
    m_pr = generate_smti_table(n,p1,p2)    # Generate a random reference table for men
    w_pr = generate_smti_table(n,p1,p2)    # Generate a random reference table for women

    # My algorithm
    time0 = time.perf_counter()
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
    time1 = time.perf_counter()

    write_instance(m_pr,w_pr,n)
    LTIU()

    time2 = time.perf_counter()

    return (time1-time0, time2-time1)

total_iter = 10
time_list1 = []
time_list2 = []
for p2 in np.linspace(0, 1, num=11):
    total_time_elapsed1 = 0
    total_time_elapsed2 = 0
    for t in range(total_iter):
        time_elapsed1, time_elapsed2 = run_compare(100,0.5,p2)
        total_time_elapsed1 += time_elapsed1
        total_time_elapsed2 += time_elapsed2

    time_list1.append(total_time_elapsed1/total_iter)
    time_list2.append(total_time_elapsed2/total_iter)

    print("p2 = ",p2," finished.")

print(time_list1)
print(time_list2)