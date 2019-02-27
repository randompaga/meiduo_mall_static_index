from rest_framework import serializers

from areas.models import Area

# area
# 省的信息
class AreaSerializer(serializers.ModelSerializer):

    # area_set = serializers.PrimaryKeyRelatedField(many=True,read_only=True)

    class Meta:
        model = Area
        fields = ['id','name']
# 市的序列化器
class SubsAreaSerializer(serializers.ModelSerializer):

    # 想 通过id 来获取这个id所对应的所有的值 area
    # 同时 转换为 字典
    # area_set = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    # [1,2,3,4,5]

    area_set = AreaSerializer(many=True,read_only=True)
    # subs = AreaSerializer(many=True,read_only=True)


    class Meta:
        model = Area
        # fields = ['subs','id','name']
        fields = ['area_set','id','name']