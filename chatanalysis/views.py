from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from bson import ObjectId
from pymongo import MongoClient
from bson.objectid import ObjectId
import json
from datetime import datetime,timedelta
from django.http import HttpResponse
from django.shortcuts import render

client = MongoClient("mongodb://65.2.116.84:27017/") 
db = client["production"] 

def chatHtml(request):
    return render(request,"chatanalysis.html")

class chatAnalysis(APIView):
    def post(self, request, *args, **kwargs):
        startDate = request.data.get('startDate')
        endDate=request.data.get('endDate')
        print(startDate)
        print(endDate)
        pipeline=[]
        if startDate is not None:
            pipeline.append({ "$addFields": { "dateStr": { "$dateToString": { "format": "%Y-%m-%d", "date": "$updatedAt" } } } })
            date_match = {
                "$gte": startDate
            }
            
            if endDate is not None:
                date_match["$lte"] = endDate
            print(date_match)  
            pipeline.append({ "$match": { "dateStr": date_match } })

        result = list(db.conversations.aggregate(pipeline))
        print(result)
        Activegroups={}
        for res in result:
            Activegroups[str(res["_id"])]=res["name"]
        return Response(Activegroups)

