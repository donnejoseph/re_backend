from django.contrib import admin
from .models import Property, Image, City, Area


class PropertyImageAdmin(admin.ModelAdmin):
    pass


class PropertyImageInline(admin.StackedInline):
    model = Image
    max_num = 10
    extra = 0


class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline, ]
    search_fields = ('title', 'price', 'object_id')
    list_per_page = 25
    list_filter = ('area', 'bedrooms')
    list_display_links = ('object_id', 'title')
    list_display = ('object_id', 'title', 'is_published', 'price', 'list_date')


class CityAdmin(admin.ModelAdmin):
    list_per_page = 25


class AreaAdmin(admin.ModelAdmin):
    list_per_page = 25


# admin.site.register(Image, PropertyImageAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Area, AreaAdmin)
