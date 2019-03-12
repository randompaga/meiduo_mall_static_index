from django.db import models

#省
class Area(models.Model):
    #id 默认生成的
    name = models.CharField(max_length=20, verbose_name='名称')
    # related_name 修改 关联的模型的数据的属性值 默认是: 关联模型类名小写_set
    parent = models.ForeignKey('self', on_delete=models.SET_NULL,null=True,related_name='subs', blank=True, verbose_name='上级行政区划')
    # parent = models.ForeignKey('self', on_delete=models.SET_NULL,null=True, blank=True, verbose_name='上级行政区划')
    # area_set = [市id,市id]
    # subs = [市id,市id]
    class Meta:
        db_table = 'tb_areas'
        verbose_name = '行政区划'
        verbose_name_plural = '行政区划'
    def __str__(self):
        return self.name
# 市
# class Area(models.Model):
#     """
#     行政区划
#     """
#     #id 默认生成的
#     area_set = [市id,市id,市id]

#市
# class Area(models.Model):
#     """
#     行政区划
#     """
#     #id 默认生成的
#     area_set = [区县id,区县id,区县id]



#区县
# class Area(models.Model):
#     """
#     行政区划
#     """
#     #id 默认生成的
#     name = models.CharField(max_length=20, verbose_name='名称')
#     parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='上级行政区划')



"""

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



"""