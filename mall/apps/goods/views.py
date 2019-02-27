from django.shortcuts import render

# Create your views here.

class Person(object):

    name = ''
    sex = ''


p = Person()
p.name='aaa'


"""
设置表的思想是:
不要上来就定义模型,要先分析
1. 尽量多的分析字段,而且将比较明显的表分析出来(不要分析表和表之间的关系)
2. 找一个安静的没有人打扰的时候,分析表和表之间的关系 (分析的时候,就分析2个表之间的分析)

"""