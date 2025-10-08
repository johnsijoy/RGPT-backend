
from rest_framework import viewsets, generics, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User

from .models import Project, Block, Unit
from .serializers import ProjectSerializer, BlockSerializer, UnitSerializer, UserRegisterSerializer
from .permissions import IsAdminOrReadOnly
from .models import Property
from .serializers import PropertySerializer


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    
# Project CRUD
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'project_type', 'location']
    search_fields = ['name', 'location', 'rera_number']
    ordering_fields = ['created_at', 'updated_at', 'name']

# Block CRUD
class BlockViewSet(viewsets.ModelViewSet):
    queryset = Block.objects.all().order_by('-created_at')
    serializer_class = BlockSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project']

# Unit CRUD
class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all().order_by('-created_at')
    serializer_class = UnitSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project', 'block', 'status']

# Filters endpoint
class ProjectFiltersView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        locations = Project.objects.values_list('location', flat=True).distinct()
        types = Project.objects.values_list('project_type', flat=True).distinct()
        status = Project.objects.values_list('status', flat=True).distinct()
        return Response({
            'locations': [x for x in locations if x],
            'types': [x for x in types if x],
            'status': [x for x in status if x],
        })

# Locations for map
class ProjectLocationsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        qs = Project.objects.all().values('id', 'name', 'latitude', 'longitude', 'status')
        return Response(list(qs))

# User registration
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = []  # allow anyone to register

