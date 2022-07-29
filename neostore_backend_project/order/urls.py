from django.urls import include, path

urlpatterns = [
    path('order', include("user.urls")),
    path('order/all', include("product.urls")),
    path('api/cart/', include("cart.urls"))


    # path('admin/', admin.site.urls),
    # path('api-auth/', include('rest_framework.urls')),
    # path('dj-rest-auth/', include('dj_rest_auth.urls')),
    # path('dj-rest-auth/', include('dj_rest_auth.urls')),
    # path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls'))


]