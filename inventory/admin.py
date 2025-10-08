from django.contrib import admin
from .models import Project, Block, Unit

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'status', 'created_at')
    search_fields = ('name', 'location', 'rera_number')

@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'project', 'block_type', 'status')
    search_fields = ('name', )

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('id', 'unit_number', 'project', 'block', 'status')
    search_fields = ('unit_number', )