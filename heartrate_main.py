from analyze import get_heartrate_score, get_10_score, example_scores
import random


# for i in range(10):
#     example_heartrate = []
#     for j in range(50):
#         example_heartrate.append(50+random.random()*50)
#     example_heartrate.sort()
#     print("pre fitting")
#     print(example_heartrate)
#     print(get_heartrate_score(example_heartrate))


for i in example_scores:
    print(get_10_score(i))