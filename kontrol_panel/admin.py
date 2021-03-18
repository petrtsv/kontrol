from django.contrib import admin

from kontrol_panel.models import Session, Plot, Point, ImageData


class SessionAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'token')


admin.site.register(Session, SessionAdmin)
admin.site.register(Plot)
admin.site.register(Point)
admin.site.register(ImageData)
