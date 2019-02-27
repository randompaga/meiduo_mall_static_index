from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from areas.models import Area
from areas.serializers import AreaSerializer

"""

一.
    关联模型中
    书籍 和 人物
1       n

# 我们根据书籍(1) 查询人物(n)

class BookInfo(models.Model):


    # peopleinfo_set

    pass


class PeopleInfo(models.Model):

    #外键
    book = xxxxx
    pass

二. 序列化中

class BookInfoSerializer(serialzier.ModelSerializer):

    peopleinfo_set = xxxx


三. 序列化器的嵌套(序列化器的父类 本质也是 Field 字段)
    class TrackSerializer(serializers.ModelSerializer):
        class Meta:
            model = Track
            fields = ('order', 'title', 'duration')

    class AlbumSerializer(serializers.ModelSerializer):
        tracks = TrackSerializer(many=True, read_only=True)

        class Meta:
            model = Album
            fields = ('album_name', 'artist', 'tracks')

四. 根据数据库查询数据的sql语句


GET     areas/infos/

获取省的信息
select * from tb_areas where parent_id is null;


GET     areas/infos/id/

获取市的信息
select * from tb_areas where parent_id=130000;
获取区县的信息
select * from tb_areas where parent_id=130600;


"""

class ProvienceAPIView(APIView):
    # 获取省的信息
    def get(self,request):

        areas = Area.objects.filter(parent=None)
        # [Area,Area,Area,Area]

        serializer = AreaSerializer(areas,many=True)

        return Response(serializer.data)



class DistrictAPIView(APIView):
    #获取市/区县信息
    def get(self,request,id):

        areas = Area.objects.filter(parent_id=id)

        serializer = AreaSerializer(areas,many=True)

        return Response(serializer.data)


