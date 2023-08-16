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
