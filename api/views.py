from rest_framework.views import APIView
from rest_framework.response import Response
from bson import ObjectId
from pymongo import MongoClient
from .serializers import AttendanceStatusSerializer
from bson.objectid import ObjectId
import json
from datetime import datetime,timedelta
from django.http import HttpResponse
from django.shortcuts import render




client = MongoClient("mongodb://65.2.116.84:27017/") 
db = client["production"] 
class AttendanceStatusView(APIView):
    def post(self, request, *args, **kwargs):
        lecture = ObjectId(request.data.get('lecture_id'))
        print(type(lecture))
        print(lecture)
        client = MongoClient("mongodb://65.2.116.84:27017/") 
        print("success") 
        db = client["production"]  
        print("done")
        pipeline = [
    {
        "$match": {
            "_id": lecture
        }
    },
    {
        "$unwind": "$users"
    },
    {
        "$group": {
            "_id": "$users.status",
            "count": {"$sum": 1}
        }
    }
]


        result = list(db.attendances.aggregate(pipeline))
        print(result)
        return Response(result)



class AttendanceStats(APIView):
    def post(self, request, *args, **kwargs):
        specified_start_date = None
        specified_end_date = None
        phase_id = None
        client_id = ObjectId(request.data.get("client_id"))
        
        phase_id = request.data.get("phase_id")
        specified_start_date = request.data.get("start_date")
        specified_end_date = request.data.get("end_date")
        # print(specified_start_date)
        # print(specified_end_date)
        if phase_id == '' or phase_id == '___NONE___':
            phase_id = None
        
        if specified_start_date == '':
            specified_start_date = None
            
        if specified_end_date == '':
            specified_end_date = None
        
        client = MongoClient("mongodb://65.2.116.84:27017/") 
        db = client["production"]  
        
        pipeline = [
            {
                '$match': {
                    'client': client_id,
                }
            }
        ]
        
        if phase_id is not None:
            pipeline[0]['$match']['phase'] = ObjectId(phase_id)
        
        if specified_start_date is not None:
            pipeline.append({ "$addFields": { "dateStr": { "$dateToString": { "format": "%Y-%m-%d", "date": "$date" } } } })
            date_match = {
                "$gte": specified_start_date
            }
            
            if specified_end_date is not None:
                date_match["$lte"] = specified_end_date
            print(date_match)  
            pipeline.append({ "$match": { "dateStr": date_match } })
        
        pipeline.extend([
            {
                '$lookup': {
                    'from': 'attendancestats', 
                    'localField': 'stats', 
                    'foreignField': '_id', 
                    'as': 'result'
                }
            },
             {
                '$lookup': {
                    'from': 'phases', 
                    'localField': 'phase', 
                    'foreignField': '_id', 
                    'as': 'phasename'
                }
            },
                {
            '$addFields': {
                'phaseAsString': { '$toString': '$phase' }
            }
    },
            {
                '$project': {
                    'result.stats': 1,
                    'date':1,
                    'phaseAsString':1,
                    'phasename.name':1,

                }
            }
        ])
        
        result = list(db.attendances.aggregate(pipeline))
        # print(result)
        if result:
            response=[]
            print("enter")
            for res in result:
                res['_id']=str(res['_id'])
                response.append(res)
            # print(response)
            return Response({"attendance": response})
        else:
            return Response({"message": "No attendance data found for the specified criteria."})




def clientSelect(request):
    # client_id=request.GET.get('client_id')
    client_id=request.GET.get("client_id")
    print(client_id)
    
    pipeline = [
    {
        '$match': {
            '_id': ObjectId(client_id)
        }
    },
    {
        '$unwind': '$phases'
    },
    {
        '$lookup': {
            'from': 'phases',
            'localField': 'phases',
            'foreignField': '_id',
            'as': 'phase_info'
        }
    },
    {
        '$unwind': '$phase_info'
    },
    {
        '$project': {
            '_id': 0,
            'phase_id': '$phase_info._id',
            'phase_name': '$phase_info.name'
        }
    }
]

    result = list(db.clients.aggregate(pipeline))
    # print(result)


    return render(request, 'AttendanceStats.html', {'phases': result,'client_id':client_id})



