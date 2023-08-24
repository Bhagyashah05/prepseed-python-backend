from rest_framework.views import APIView
from rest_framework.response import Response
from bson import ObjectId
from pymongo import MongoClient
from .serializers import AttendanceStatusSerializer
from bson.objectid import ObjectId
import json
from datetime import datetime,timedelta

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
        specified_date = None
        phase_id = None
        client_id = ObjectId(request.data.get("client_id"))
        phase_id = request.data.get("phase_id")
        specified_date = request.data.get("date")
        client = MongoClient("mongodb://65.2.116.84:27017/") 
        print("success")
        print(client_id)
        print(phase_id)
        print(specified_date)
        db = client["production"]  
        print("done")
        pipeline = [
            {
                '$match': {
                    'client': client_id,
                }
            }
        ]
        if phase_id is not None:
            pipeline[0]['$match']['phase'] = ObjectId(phase_id)
        if specified_date is not None:
            pipeline.append({ "$addFields": { "dateStr": { "$dateToString": { "format": "%Y-%m-%d", "date": "$date" } } } })
            pipeline.append({ "$match": { "dateStr": specified_date } })

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
                '$project': {
                    'result.stats': 1
                }
            }
        ])
        

        result = list(db.attendances.aggregate(pipeline))
        print(result)
        if result:
            response=[]
            print("enter")
            for res in result:
                res['_id']=str(res['_id'])
                response.append(res)
            return Response({"attendance": response})
        else:
            return Response({"message": "No attendance data found for the specified criteria."})








