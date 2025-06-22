from django.urls import path
from inventory.views import *
from inventory.views.categoryView import *
from django.conf.urls.static import static
from django.conf import settings 

urlpatterns = [
    path('get_all_items/', itemView.as_view(), name="get_all_items"),
    path('add_item/', itemView.as_view(), name="add_items"),
    path('edit_item/<int:id>/', itemView.as_view(), name="edit_item"),
    path('delete/<int:id>/', itemView.as_view(), name="delete"),
    path('get_categories/', get_categories.as_view(), name="get_categories"),
    path('add_categories/', add_categories.as_view(), name="add_categories"),
    path('get_subcategories/', get_subcategories.as_view(), name="get_subat_by_cat"),
    path('add_subcategories/', add_subcategories.as_view(), name="add_subcategories"),
    path('get_cat_subcat/', get_cat_subcat.as_view(), name="get_cat_subcat"),
    path('get_subcat_by_catid/<int:id>/', get_subcat_by_catid.as_view(), name="get_subcat_by_catid"),
    path('get_subcat_by_cat/<int:id>/', get_subcat_by_cat.as_view(), name="get_subcat_by_cat"),
    path('get_items_by_catid/<int:id>/', get_items_by_catid.as_view(), name="get_items_by_catid"),
    path('get_items_by_subcatid/<int:cid>/<int:sid>/', get_items_by_subid.as_view(), name="get_items_by_subcatid"),
    path('get_item_by_id/<int:id>/', get_item_by_id.as_view(), name="get_item_by_id"),

    # locations
    path('get_locations/', LocationView.as_view(), name="get_locations"),
    path('get_Items_locations/', ItemsLocationView.as_view(), name="get_locations"),
    path('get_items_by_location/<int:id>/', ItemsByLocationId.as_view(), name="get_items_by_location"),
    path('locations_by_item/', LocationByItems.as_view(), name="locations_by_item"),
    
    # order
    path('orders/', orderView.as_view(), name="all_order"),
    path('edit_order/<int:id>/', orderView.as_view(), name="edit_order"),
    path('cancelled_orders/', cancelledOrderView.as_view(), name="cancelled_orders"),
    path('dispatched_orders/', dispatchedOrderView.as_view(), name="dispatched_orders"),
    path('delivered_orders/', deliveredOrderView.as_view(), name="delivered_orders"),
    path('confirmed_orders/', confirmedOrderView.as_view(), name="confirmed_orders"),
    path('returned_orders/', returnedOrderView.as_view(), name="returned_orers"),
    path('order/<int:id>/', getOrderView.as_view(), name="get_orders"),

    path('add_order/', orderView.as_view(), name="add_order"),
    path('cancel_order/<int:id>/', cancelorder.as_view(), name="cancel_order"),
    # path('add_img/', addImage.as_view(), name="add_image")

] 