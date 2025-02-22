"""
URL configuration for peanut project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views  as auth_view 
from mainApp.views import get_question
from mainApp import views
from mainApp.views import compile_code
from django.conf.urls.static import static
from django.conf import settings
from mainApp.views import quick_play, save_custom_timer
from mainApp.views import apply_to_project, search_field, field_info


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.user_login, name='login'),
    path('accounts/post_job/', views.post_job, name='post_job'),
    path('accounts/post_achievement/', views.post_achievement, name='post_achievement'),
    path('logout/', views.logout_view, name='logout'),
    path('social-auth', include('social_django.urls', namespace='social')),
    path("", views.home, name='home'),
    path('apply-to-project/<int:project_id>/', views.apply_to_project, name='apply_to_project'),
    path('freelancing/', views.freelancing_project_list, name='freelancing_project_list'),
    path('freelancing/post-project/', views.post_project, name='post_project'),
    path('test-face/', views.test_face_detection, name='test_face'),

    path('question-page/', views.question_page, name='question_page'),
    path('start-match/', views.start_match, name='start_match'),
    path('check-room-status/', views.check_room_status, name='check_room_status'),
    path('accounts/profile/', views.profile,name='profile'),
    path('accounts/edit_profile/', views.edit_profile, name='edit_profile'),
    path('register/', views.register, name='register'),
    path('accounts/community_page/', views.community_page, name='community_page'),
    path('thank_you/', views.thank_you, name='thank_you'),
    path('accounts/store/', views.store, name='store'),
    path('accounts/aboutus/', views.aboutus, name='aboutus'),
    path('submit-answer/', views.submit_answer, name='submit_answer'),
    path('get_question/<int:question_id>/', get_question, name='get_question'),
    path('compile/', compile_code, name='compile_code'),
    path('accounts/community/feed/', views.community_feed, name='community_feed'),
    path('accounts/community/jobs/', views.jobs, name='jobs'),
    path('accounts/community/mentor/', views.mentor, name='mentor'),
    path('accounts/community/groups/', views.groups, name='groups'),
    path('accounts/community/frandz/', views.frandz, name='frandz'),
    path('accounts/community/roadmap/', views.roadmap, name='roadmap'),
    path('accounts/community/hackathons/', views.hackathons, name='hackathons'),
    path('quick_play/', views.quick_play, name='quick_play'),
    path('save-custom-timer/', save_custom_timer, name='save_custom_timer'),
    path('handle-violation/', views.handle_violation, name='handle_violation'),

    path('promoted/', views.promoted, name='promoted'),
    path('demoted/', views.demoted, name='demoted'),
    path('submit/', views.submit_view, name='submit'),
    path('quick-play-question-page/', views.quick_play_question_page, name='quick_play_question_page'),
    path('quick-play/', views.quick_play, name='quick_play'),
    path('leetcode/', views.leetcode, name='leetcode'),
    path('webdev/', views.webdev, name='webdev'),

     # VIDEO CONFERENCING
    # path('register/',views.register, name='register'),
    # path('login/',views.login_view, name='login'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('meeting/',views.videocall, name='meeting'),
    # path('logout/',views.logout_view, name='logout'),
    path('join/',views.join_room, name='join_room'),
    path('',views.index, name='index'),
    path('dsa-topics/', views.dsa_topics, name='dsa_topics'),
    path('questions/<str:topic>/', views.dsa_questions_page, name='dsa_questions_page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# PROJECT
    path('projects/', views.project_list, name='project_list'),
    path('apply-to-project/<int:project_id>/', apply_to_project, name='apply_to_project'),

# Recommendations
    path('search/', search_field, name='search_field'),
    path('field/<str:field_name>/', field_info, name='field_info'),
