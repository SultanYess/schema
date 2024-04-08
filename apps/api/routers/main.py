from django.urls import path, include
from rest_framework import routers
from apps.api.viewsets import *
from apps.api.viewsets.application import ApplicationViewSet, ApplicationListViewSet


router = routers.DefaultRouter()

router.register(r"employee", EmployeeViewSet, basename="employee")
router.register(r"application", ApplicationListViewSet, basename="application")
router.register(r"profile_application", ApplicationViewSet, basename="profile_application")
router.register(r"profile", ProfileViewSet, basename="profile")
router.register(r"change_event", ChangeLastEventViewSet, basename="change_event")
router.register(r"face_id", FaceIdViewSet, basename="face_id")
router.register(r"positions", PositionViewSet, basename="positions")
router.register(r"services", ServiceViewSet, basename="services")
router.register(r"org_structure", OrgStructureViewSet, basename="org_structure")
router.register(r"work_shift", WorkShiftViewSet, basename="work_shift")
urlpatterns = [
    path("", include(router.urls)),
]
