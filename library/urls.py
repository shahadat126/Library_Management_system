from django.urls import path
from .views import Home,book_add,book_list,book_detail,dashboard,book_edit,book_delete,add_review
app_name = 'library'
urlpatterns = [
    path("",Home,name="home"),
    path("dashboard/",dashboard,name="dashboard"),
    path("add/",book_add,name="book_add"),
    path("edit/<int:id>/",book_edit,name="book_edit"),
    path("delete/<int:id>/",book_delete,name="book_delete"),
    path("list/",book_list,name="book_list"),
    path("detail/<int:id>/",book_detail,name="book_detail"),
    path("review/<int:id>/",add_review,name="add_review"),

]