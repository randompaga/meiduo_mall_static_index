from django.db import models

class Area(models.Model):
    """
    行政区划
    """
    #id 默认生成的
    name = models.CharField(max_length=20, verbose_name='名称')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='上级行政区划')

    class Meta:
        db_table = 'tb_areas'
        verbose_name = '行政区划'
        verbose_name_plural = '行政区划'

    def __str__(self):
        return self.name



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