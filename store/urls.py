from django.urls import path
from .views import store,single_page,search_page
urlpatterns = [
    path('',store,name='store'),
    path('category/<slug:category_slug>/',store,name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/',single_page,name='product_detail'),
    path('search/',search_page,name='product_search'),
]
