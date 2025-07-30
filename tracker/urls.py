from django.urls import path
from . import views
from tracker.apps import TrackerConfig
from rest_framework.routers import DefaultRouter, SimpleRouter

from .views import LocationViewSet, ActionViewSet

app_name = TrackerConfig.name

loc_router = DefaultRouter()
loc_router.register('locations', LocationViewSet, 'locations')
act_router = SimpleRouter()
act_router.register('actions', ActionViewSet, 'actions')


urlpatterns = ([
                   path("add_habit/", views.CreateHabit.as_view(), name="add_habit"),
                   path("edit_habit/<int:pk>/", views.HabitPartialUpdateAPIView.as_view(), name="edit_habit"),
                   path("delete_habit/<int:pk>/", views.HabitDestroyAPIView.as_view(), name="delete_habit"),
                   path("habits/", views.HabitListAPIView.as_view(), name="habits"),
                   path("habit/<int:pk>/", views.HabitRetrieveAPIView.as_view(), name="habit"),
                   path("habits/<int:pk>/", views.HabitRetrieveAPIView.as_view(), name="retrieve_habit"),
                   path("my_habits/", views.MyHabitListAPIView.as_view(), name="my_habits"),
                   path("my_habits_full/", views.MyHabitListAPIView.as_view(), name="my_habits_full",
                        kwargs={"full": True}),
               ] + loc_router.urls + act_router.urls)
