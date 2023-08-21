from rest_framework.views import APIView
from rest_framework.response import Response
from bson import ObjectId
from pymongo import MongoClient
from .serializers import AttendanceStatusSerializer

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
        client_id = ObjectId(request.data.get("client_id"))
        phase_id = ObjectId(request.data.get("phase_id"))
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
                    'phase': phase_id,
                }
            },
            { "$addFields": { "dateStr": { "$dateToString": { "format": "%Y-%m-%d", "date": "$date" } } } },
            { "$match": { "dateStr": specified_date } },
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
        ]

        result = list(db.attendances.aggregate(pipeline))
        print(result)
        if result:
            response = result[0]["result"]
            return Response({"attendance": response})
        else:
            return Response({"message": "No attendance data found for the specified criteria."})








