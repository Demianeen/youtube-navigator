from django.urls import path
from summaryGen import views

# template urls
app_name = 'summaryGen'

urlpatterns=[
    path('user_logout/',views.user_logout, name = 'user_logout'),
    path('api/user/registration/', views.registerHtml, name='registerHtml'),
    path('api/user/login/', views.user_login, name='loginHtml'),
    path('api/summary/', views.summary, name='summary')
]
