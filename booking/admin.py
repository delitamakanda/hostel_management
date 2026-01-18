from django.contrib import admin
from django.contrib.admin.models import DELETION

from booking.models import Book, Room, Property
from django.utils.html import escape
from django.urls import reverse
from django.utils.safestring import mark_safe


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'is_active', 'object_link',)
    list_filter = ('is_active',)
    search_fields = ('name', 'location')
    actions = ('make_active', 'make_inactive')
    
    def image_tag(self, obj):
        return mark_safe(f'<img src="{obj.photo.url}" width="100" />')
    
    image_tag.short_description = 'Photo'
    image_tag.allow_tags = True
    image_tag.admin_order_field = 'photo'
    
    def make_active(self, request, queryset):
        queryset.update(is_active=True)
    
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
    
    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = '<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr)
            )
        return mark_safe(link)
    
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = 'object'

admin.site.register(Book)
admin.site.register(Room)
