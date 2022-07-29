from django.urls import include, path

from order.views import PlaceOrderView, GetOrdersListView, GetOrderDetailView

urlpatterns = [

    path('all', GetOrdersListView.as_view(), name='get_orders_list'),
    path('add', PlaceOrderView.as_view(), name='place_order'),
    path('<int:order_id>', GetOrderDetailView.as_view(), name='get_order_detail'),



    # path('admin/', admin.site.urls),
    # path('api-auth/', include('rest_framework.urls')),
    # path('dj-rest-auth/', include('dj_rest_auth.urls')),
    # path('dj-rest-auth/', include('dj_rest_auth.urls')),
    # path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls'))


]
