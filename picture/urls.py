from django.urls import path

from . import views

app_name = 'picture'

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('picture/info/', views.AlbumAddInfoView.as_view(), name='post_album_info'),
    path('reply/info/', views.ReplyAddInfoView.as_view(), name='post_reply_info'),
    path('picture/info/<int:album_id>/', views.AlbumInfoView.as_view(), name='album_info'),
    path('reply/info/<int:reply_id>/', views.ReplyInfoView.as_view(), name='reply_info'),
    path('picture/favorite_album/', views.FavoriteAlbumView.as_view(), name='get_favorite_album'),
    path('picture/like_album/', views.LikeAlbumView.as_view(), name='get_like_album'),
]
