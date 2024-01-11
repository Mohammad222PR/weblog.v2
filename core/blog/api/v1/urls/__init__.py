from django.urls import path, include


app_name = 'api-v1'


urlpatterns = [
    path('blog/', include('blog.api.v1.urls.blog'))
]
