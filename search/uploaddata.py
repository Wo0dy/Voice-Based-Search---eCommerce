import json
from elasticsearch import Elasticsearch as es;
from elasticsearch import helpers;
import datetime;
import itertools;

index_file_name = "indexfinal1"
host_to_connect = "192.168.43.227:9200"
data_file_name = "finalDataset.json"


def updateDataFormat():
    with open('data.json') as f:
        data = json.load(f)

    f.close()

    lineToAdd = {"index": {"_index": "productIndex", "_type": "_doc"}}

    with open('dataToFeed.json', 'w') as f2:
        for d in data:
            lineToAdd["index"]["_id"] = d["id"]
            json.dump(lineToAdd, f2)
            f2.write('\n')
            json.dump(d, f2)
            f2.write('\n')
    f2.close()


def createIndex():
    with open(data_file_name) as f:
        data = json.load(f)
    j = 0
    actions = []
    for d in data:
        action = {
            "_index": index_file_name,
            "_type": "productMetadata",
            "_id": d["id"],
            "_source": d
        }
        actions.append(action)
    es_client = es(host_to_connect)

    size = len(actions)
    startTime = datetime.datetime.now()
    print("index creation start time" + str(startTime))
    i = 0
    for i in range(16):
        if (i * 100 + 100 > size):
            helpers.bulk(es_client, actions[i * 100:size + 1])
            break
        else:
            helpers.bulk(es_client, actions[i * 100:i * 100 + 100])

    endTime = datetime.datetime.now()
    print("index creation stop time " + str(endTime))
    print("\n total time taken to create the index for ", len(actions), " records")
    print(endTime - startTime)


# Builds query for voice to text search
def buildQuery(args):
    shouldQuery = []
    for arg in args:
        shouldQuery.append({"match": {"productDescr": arg}})
    return shouldQuery


def search(args):
    es_client = es(host_to_connect)
    queryCondition = buildQuery(args)
    i = 0
    totalNoOfWords = len(args)
    weight = totalNoOfWords * 30
    filterWeightedAndConditions = []
    for i in range(totalNoOfWords - 1):
        listOfTuples = itertools.combinations(args, totalNoOfWords - i)
        # print(listOfTuples)
        for eachTuple in listOfTuples:
            filterWeightedAndConditions.append(buildFilterCondition(eachTuple, weight))
        weight -= 10
    if(totalNoOfWords==2):
            filterWeightedAndConditions.append(buildFilterCondition([args[1]],50))
    else:
            filterWeightedAndConditions.append(buildFilterCondition([args[0]], 50))
    query = {"query": {
        "function_score": {"query": {"bool": {"should": queryCondition}}, "functions": filterWeightedAndConditions}}}
    print("final query: ")
    print(json.dumps(query) + "\n")
    es_response = es_client.search(index=index_file_name, body=query)
    # print(json.dumps(es_response))
    return es_response["hits"]


# Returns filter condition for functions object in personalized search
def buildFilterCondition(listOfTokens, weight):
    functionFilter = {"filter": {"bool": {"must": []}}, "weight": weight}
    mustQuery = []
    for token in listOfTokens:
        mustQuery.append({"match": {"productDescr": token}})
    functionFilter['filter']['bool']['must'] = mustQuery
    return functionFilter


# Returns similar products in the index for given tokens
def getSimilarProducts(listOfTokens):
    queryCondition = buildQuery(listOfTokens)
    filterCondition = []
    if (len(listOfTokens) == 2 or len(listOfTokens) == 1):
        filterCondition = buildFilterCondition(listOfTokens, 70)
    if (len(listOfTokens) == 3):
        filterCondition.append(buildFilterCondition(listOfTokens[0:2], 50))
        filterCondition.append(buildFilterCondition(listOfTokens[1:3], 30))
        filterCondition.append(buildFilterCondition([listOfTokens[0], listOfTokens[2]], 30))

    query = {"query": {"function_score": {"query": {"bool": {"should": queryCondition}}, "functions": filterCondition}}}
    print("final query "+ json.dumps(query))
    # print(json.dumps(query))
    startTime = datetime.datetime.now()
    print("\nstart exceution " + str(startTime))
    es_client = es(host_to_connect)
    es_response = es_client.search(index=index_file_name, body=query)
    endTime = datetime.datetime.now()
    print("stop exceution " + str(endTime))
    print("\n total query exceution Time")
    print(endTime - startTime)
    return es_response['hits']


def buildQuery(args):
    shouldQuery = []
    for arg in args:
        # print("arg : " + arg + "\n")
        shouldQuery.append({"match": {"productDescr": arg}})
    return shouldQuery


if __name__ == "__main__":
    #createIndex()
    search(['shirt', 'white', 'circle'])
    # search("nikon","camera")
    # print(json.dumps(getSimilarProducts(['gold','rose','ring'])))
