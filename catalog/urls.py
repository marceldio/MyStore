from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView, contact

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    # path('<int:pk>/', cache_page(60)(ProductDetailView.as_view())),  # , name='product_view'
    path('<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product_view'),
    path('<int:pk>/edit', ProductUpdateView.as_view(), name='product_edit'),
    path('<int:pk>/delete', ProductDeleteView.as_view(), name='product_delete'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('contact/', contact, name='contact')
]
