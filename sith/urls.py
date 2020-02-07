from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('recruit/', views.NewRecruitView.as_view(), name='new_recruit'),
    path('recruit/(<int:recruit_id>/order/<int:order_id>/',
        views.ChallengeView.as_view(), name="challenge"),
    path('recruit/passed/',
        TemplateView.as_view(template_name='passed_recruit.html'), name='passed'),
    path('sith/', views.SithSelectView.as_view(), name='select_sith'),
    path('sith/<int:sith_id>/recruit/list/', views.SithView.as_view(), name='sith'),
    path('sith/<int:sith_id>/recruit/<int:recruit_id>/',
        views.RecruitToHandView.as_view(), name='recruit'),
    path('sith/list/', views.SithListView.as_view(), name='sith_list'),
    path('sith/list/gt1/', views.SithListMoreThanOneView.as_view(), name='sith_list_gt1')
]