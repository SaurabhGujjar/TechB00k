from django.urls import path
from blog.views import user_login, success, user_logout, user_add, delpost, delcmt, cmt_detail, blog_index, blog_detail, blog_category, editpost, editcmt, myprofile, myposts
from blog.views import updateprofile, deluser, search, forgot_password

urlpatterns = [
    path("", blog_index, name="blog_index"),
    path("profile/<str:uname>/", myprofile, name="myprofile"),
    path("myposts/<str:u>/", myposts, name="myposts"),
    # path("recover/<str:usrname>/", forgot_password, name="recover"),
    path("updateprofile/<str:usr>/", updateprofile, name="updateprofile"),
    path("<int:pk>/", blog_detail, name="blog_detail"),
    path("cmt_detail/<int:pk>/", cmt_detail, name="cmt_detail"),
    path('add/', user_add, name="user_add"),
    path('search/', search, name="search"),
    path('login/', user_login, name="user_login"),
    path('delpost/<int:pk>/', delpost, name="delpost"),
    path('deluser/<str:u>/', deluser, name="deluser"),
    path('editpost/<int:pk>/', editpost, name="editpost"),
    path('delcmt/<int:pk>/', delcmt, name="delcmt"),
    path('editcmt/<int:pk>/', editcmt, name="editcmt"),
    path('success/', success, name="user_success"),
    path('logout/', user_logout, name="user_logout"),
    path("<category>/", blog_category, name="blog_category"),
]
















