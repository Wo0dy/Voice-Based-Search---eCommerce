import os
import json
from pprint import pprint
import sys
import operator
import uploaddata

sys.path.append('../tagger/')
sys.path.append('../')
import tagger

UserData = eval(open('temp.txt', 'r').read())


def kcore(Overview, k=3):
    return Overview[:k]


def userRecommendation(UserId):
    nouns = []
    for eachReviewByUser in UserData[UserId]:
        temp_nns = []
        for nns in eachReviewByUser[1]:
            temp_nns.append(nns)
        x = kcore(temp_nns)
        nns = [tup[0] for tup in x]
        nouns.append(nns)
        # print(nns)

    response = []
    for lst in nouns:
        print(len(lst))
        response.append(uploaddata.getSimilarProducts(lst))

    subres = []
    for res in response:
        temp_lst = res['hits']
        print(len(temp_lst), temp_lst)

        if len(temp_lst) == 0:
            continue
        else:
            subres.append(temp_lst)
            break
    # print(len(subres))
    #print(subres)
    return subres


if __name__ == '__main__':
    userRecommendation("A00338282E99B8OR2JYTZ")
    # UserData = eval(open('temp.txt', 'r').read())
    # pprint(UserData)
    #
    # for eachUser in UserData.keys():
    #     for eachReviewByUser in UserData[eachUser]:
    #         print(eachReviewByUser)
    #
