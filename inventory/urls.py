from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, BlockViewSet, UnitViewSet, ProjectFiltersView, ProjectLocationsView, UserRegisterView
from .views import PropertyViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'blocks', BlockViewSet, basename='block')
router.register(r'units', UnitViewSet, basename='unit')
router.register(r'properties', PropertyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("api/", include(router.urls)),
    path('projects/filters/', ProjectFiltersView.as_view(), name='project-filters'),
    path('projects/locations/', ProjectLocationsView.as_view(), name='project-locations'),
    path('auth/register/', UserRegisterView.as_view(), name='user-register'),
]