import os
import sys

sys.path.append('./')
from flask import Flask, render_template, request
import FinalPersonalisedSearch as ps
import FinalSearch as vs
import json
# import json
# import numpy as np
# #from feat import imgToSearch
# from featAlex import imgToSearchAlex
# from insert import getData

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/voiceSearch', methods=['GET'])
def voiceSearch():
    finalProductList = []
    results = []
    results = vs.voiceSearch()
    print("results of search "+json.dumps(results))
    for eachHit in results:
        for singleQueryHit in eachHit:
            finalProductList.append(singleQueryHit['_source'])

    return render_template('result.html', values=finalProductList)


@app.route("/productRecommendation/<userId>", methods=['GET'])
def productRecommendation(userId):
    finalProductList = []
    results = []
    # print(userId)
    results = ps.userRecommendation(userId)
    for eachHit in results:
        for singleQueryHit in eachHit:
            finalProductList.append(singleQueryHit['_source'])


    # proddes = [item['productDescr'] for item in values]
    # prodname = [ item['productname'] for item in values]
    print ("printing list : "+str(finalProductList))
    return render_template('result.html', values=finalProductList)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='6000', debug=True)
