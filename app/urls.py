
from django.urls import path, include

from django.urls import path

from app.views import department_list, department_delete, department_create, post_create, post_list, post_delete, \
    post_update, dashboard, delete_post_image

urlpatterns = [
    path('department-list',department_list,name='department_list'),
    path('department-create',department_create,name='department_create'),
    path('department-delete/<int:department_id>',department_delete,name='department_delete'),

    path('post-create',post_create,name='post_create'),
    path('post-list',post_list,name='post_list'),
    path('post-delete/<int:post_id>',post_delete,name='post_delete'),
    path('post_update/<int:post_id>',post_update,name='post_update'),
    path('delete-post-image/<int:image_id>/', delete_post_image, name='delete_post_image'),

    # path('dashboard',dashboard,name='dashboard'),
]
