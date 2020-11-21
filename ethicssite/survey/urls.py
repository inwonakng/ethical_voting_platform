from django.urls import path
from . import views
app_name = 'survey'
urlpatterns = [
    # this path is for mturk, where the random survey would be
    path('',views.index_view,name='index'),
    path('rules/lookup/',views.lookup_view),
    path('rules/lookup/<int:id>',views.dynamic_lookup_view),
    path('rules/',views.rules_view),
    path('rules',views.rules_view),
    path('loadsurvey', views.load_survey, name='loadsurvey'),
    path('getscenario', views.get_scenario, name='getscenario'),
    path('rulessample',views.rules_explain,name='rulessample'),
    path('submitsurvey', views.submit_survey, name="submitsurvey"),
    path('surveyresult', views.survey_result, name="surveyresult"),
    path('<random>', views.unknown_path)
]
