from django.contrib import admin
from . import models
from django.contrib.admin.models import LogEntry
from mptt.admin import MPTTModelAdmin
from mptt.admin import DraggableMPTTAdmin
from mapbox_location_field.admin import MapAdmin
from .models import Profile, Tree, Ticket
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportMixin
from jalali_date import datetime2jalali, date2jalali
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin



admin.site.site_header= " توانکار "
admin.site.site_title= "Tavankar"
admin.site.register(LogEntry)









#------------------------------------------------------------------------------
class TicketAdmin(ImportExportModelAdmin):
    list_display = ('user','to','title','j_created_on')
    list_filter = ("user", "to")

admin.site.register(models.Ticket, TicketAdmin)



#------------------------------------------------------------------------------
class ProfileAdmin(ImportExportModelAdmin):
    list_display = ('user_name','phone','address')

admin.site.register(models.Profile, ProfileAdmin)



#------------------------------------------------------------------------------
class NoticeAdmin(ImportExportModelAdmin):
    list_display = ('title', 'content', 'get_created_jalali')

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_on).strftime('%y/%m/%d _ %H:%M:%S')
    get_created_jalali.short_description = " زمان "

admin.site.register(models.Notice, NoticeAdmin)







#-------------------------------------------------------- by Nima Dorostkar ---
