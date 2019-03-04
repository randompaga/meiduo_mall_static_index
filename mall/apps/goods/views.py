from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
class CategoryView(ListAPIView):
    pass

from rest_framework_extensions.cache.mixins import ListCacheResponseMixin
from goods.models import SKU
from .serializers import SKUSerializer
# Create your views here.
class HotSKUListView(ListCacheResponseMixin,ListAPIView):
    """
    获取热销商品
    GET /goods/categories/(?P<category_id>\d+)/hotskus/
    """
    serializer_class = SKUSerializer
    pagination_class = None

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return SKU.objects.filter(category_id=category_id,is_launched=True).order_by('-sales')[:2]

from rest_framework.generics import ListAPIView
from goods.models import SKU
from .serializers import SKUSerializer
from rest_framework.filters import OrderingFilter
# Create your views here.
class SKUListView(ListAPIView):
    serializer_class = SKUSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ('create_time', 'price', 'sales')

    def get_queryset(self):
        categroy_id = self.kwargs.get("category_id")
        return SKU.objects.filter(category_id=categroy_id, is_launched=True)



from .serializers import SKUIndexSerializer
from drf_haystack.viewsets import HaystackViewSet

class SKUSearchViewSet(HaystackViewSet):
    """
    SKU搜索
    """
    index_models = [SKU]

    serializer_class = SKUIndexSerializer