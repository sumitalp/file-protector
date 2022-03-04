from django.urls import path
from .views import UploaderCreateView, UploaderListView, UploaderRetrieveView
from .api import UploaderCreateAPIView, UploaderListAPIView, UploaderRetrieveAPIView


api_urlpatterns = [
    path('', UploaderCreateAPIView.as_view(), name='api-file-add'),
    path('list/', UploaderListAPIView.as_view(), name='api-file-list'),
]


urlpatterns = [
    path('', UploaderListView.as_view(), name='file-list'),
    path('add/', UploaderCreateView.as_view(), name='file-add'),
    path('link/<str:hash>/', UploaderRetrieveView.as_view(), name='file-detail'),
    # path('author/<int:pk>/', AuthorUpdateView.as_view(), name='author-update'),
    # path('author/<int:pk>/delete/', AuthorDeleteView.as_view(), name='author-delete'),
    # path('<int:pk>/detail/', UploaderCreateView.as_view(), name='file-detail'),
    # path('<str:hash>/', UploaderRetrieveAPIView.as_view(), name='file-redirect'),
]