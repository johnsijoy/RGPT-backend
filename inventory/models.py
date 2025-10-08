
from django.db import models
import uuid

from django.contrib.gis.db import models

from django.db import models
import uuid


class Property(models.Model):
        
    
    location = models.CharField(max_length=200, null=True, blank=True)
    area_sqft = models.FloatField(null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.location or "Unnamed Property"


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)

    # GIS fields
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    # store polygon or boundary as list of [lat,lng] pairs
    boundary_coords = models.JSONField(blank=True, null=True)

    rera_number = models.CharField(max_length=200, blank=True, null=True)
    project_type = models.CharField(max_length=50, default='Residential')
    launch_date = models.DateField(blank=True, null=True)
    possession_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50, default='Pre-Launch')
    total_area = models.FloatField(blank=True, null=True)
    total_units = models.IntegerField(default=0)
    base_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    amenities = models.JSONField(blank=True, null=True)
    tax_details = models.JSONField(blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Block(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.CharField(max_length=100, blank=True, null=True)
    project = models.ForeignKey(Project, related_name='blocks', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    block_type = models.CharField(max_length=50, default='Tower')

    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    footprint_coords = models.JSONField(blank=True, null=True)

    total_floors = models.IntegerField(blank=True, null=True)
    total_units = models.IntegerField(blank=True, null=True)
    launch_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.project.name} - {self.name}"


class Unit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.CharField(max_length=100, blank=True, null=True)
    project = models.ForeignKey(Project, related_name='units', on_delete=models.CASCADE)
    block = models.ForeignKey(Block, related_name='units', on_delete=models.SET_NULL, blank=True, null=True)

    unit_number = models.CharField(max_length=100)
    unit_type = models.CharField(max_length=100, blank=True, null=True)

    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    polygon_coords = models.JSONField(blank=True, null=True)

    floor_number = models.IntegerField(blank=True, null=True)
    carpet_area = models.FloatField(blank=True, null=True)
    super_built_area = models.FloatField(blank=True, null=True)
    plot_size = models.FloatField(blank=True, null=True)
    facing = models.CharField(max_length=50, blank=True, null=True)
    view_type = models.CharField(max_length=50, blank=True, null=True)
    vastu_compliant = models.BooleanField(default=False)
    parking_count = models.IntegerField(default=0)

    base_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    plc_charges = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    floor_rise_charges = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amenities = models.JSONField(blank=True, null=True)

    STATUS_CHOICES = [
        ("Available", "Available"),
        ("Blocked", "Blocked"),
        ("Booked", "Booked"),
        ("Sold", "Sold"),
        ("Cancelled", "Cancelled"),
        ("Under Agreement", "Under Agreement"),
        ("Handed Over", "Handed Over"),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Available")

    blocked_until = models.DateTimeField(blank=True, null=True)
    blocked_by = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.project.name} - {self.unit_number}"

