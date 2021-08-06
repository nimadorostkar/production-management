from django.contrib import admin
from . import models
from django.contrib.admin.models import LogEntry
from .models import Profile, Tree, Mother_Station, Ticket, Material, Station, Notice, Bom_material, Stations_inputs, Bom_product,Inventory_history,Station_exit_history, Order, Order_confirmation, Tag
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportMixin
from jalali_date import datetime2jalali, date2jalali
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin
from mptt.admin import MPTTModelAdmin
from mptt.admin import DraggableMPTTAdmin



admin.site.site_header= " توانکار "
admin.site.site_title= "Tavankar"
admin.site.register(LogEntry)





#------------------------------------------------------------------------------
class ProfileAdmin(ImportExportModelAdmin):
    list_display = ('user_name','phone','address')
    search_fields = ['user_name', 'phone', 'address']

admin.site.register(models.Profile, ProfileAdmin)




#------------------------------------------------------------------------------
class TagAdmin(ImportExportModelAdmin):
    list_display = ('name','name')

admin.site.register(models.Tag, TagAdmin)



#------------------------------------------------------------------------------
class ProductAdmin(ImportExportModelAdmin):
    list_display = ('name','code','short_description','image_tag')
    search_fields = ['name', 'code']
    raw_id_fields = ('synch_to',)
    #autocomplete_fields = ('synch_to',)

admin.site.register(models.Product, ProductAdmin)



#------------------------------------------------------------------------------
class Mother_StationAdmin(ImportExportModelAdmin):
    list_display = ('name', 'manager')
    search_fields = ['name', 'manager']
    raw_id_fields = ('manager',)

admin.site.register(models.Mother_Station, Mother_StationAdmin)



#------------------------------------------------------------------------------
class MaterialAdmin(ImportExportModelAdmin):
    list_display = ('name','code','short_description','inventory', 'image_tag', 'position')
    list_filter = ("position", "inventory")
    search_fields = ['name', 'code']

admin.site.register(models.Material, MaterialAdmin)




#------------------------------------------------------------------------------
class Bom_productAdmin(ImportExportModelAdmin):
    list_display = ('material','inventory', 'relatedProduct')
    list_filter = ("relatedProduct", "material", "inventory")
    search_fields = ['material', 'inventory', 'relatedProduct']
    raw_id_fields = ('relatedProduct', 'material')

admin.site.register(models.Bom_product, Bom_productAdmin)





#------------------------------------------------------------------------------
 #https://django-mptt.readthedocs.io/en/latest/admin.html#mptt-admin-draggablempttadmin
class Bom_materialMPTTModelAdmin(ImportExportMixin, MPTTModelAdmin):
    mptt_level_indent = 15   # specify pixel amount for this ModelAdmin only
    #mptt_indent_field = "some_node_field"

admin.site.register(Bom_material, DraggableMPTTAdmin,
    list_display=('tree_actions', 'indented_title'),
    #list_editable = ('relatedProduct','relatedProduct'),
    list_display_links=('indented_title',),)






#------------------------------------------------------------------------------
class Stations_inputsAdmin(ImportExportModelAdmin):
    list_display = ('id', 'material', 'inventory')
    search_fields = ['material', 'id']
    raw_id_fields = ('material',)

admin.site.register(models.Stations_inputs, Stations_inputsAdmin)



#------------------------------------------------------------------------------
class StationAdmin(ImportExportModelAdmin):
    list_display = ('name', 'code', 'manager', 'inventory', 'output_material', 'position')
    list_filter = ("position", "manager", "inventory")
    search_fields = ['name', 'code', 'manager', 'output_material']
    raw_id_fields = ('manager', 'mother_station', 'input_material', 'output_material')

admin.site.register(models.Station, StationAdmin)



#------------------------------------------------------------------------------
class TreeAdmin(ImportExportModelAdmin):
    list_display = ('station','parent_station','relatedProduct')
    list_filter = ("relatedProduct", "parent_station")
    search_fields = ['station', 'parent_station', 'relatedProduct']
    raw_id_fields = ('station', 'parent_station', 'relatedProduct')

admin.site.register(models.Tree, TreeAdmin)




#------------------------------------------------------------------------------
class TicketAdmin(ImportExportModelAdmin):
    list_display = ('user','to','title','j_created_on')
    list_filter = ("user", "to")
    search_fields = ['user', 'to', 'title']

admin.site.register(models.Ticket, TicketAdmin)




#------------------------------------------------------------------------------
class NoticeAdmin(ImportExportModelAdmin):
    list_display = ('title', 'content', 'get_created_jalali')

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.created_on).strftime('%y/%m/%d _ %H:%M:%S')
    get_created_jalali.short_description = " زمان "

admin.site.register(models.Notice, NoticeAdmin)




#------------------------------------------------------------------------------
class Inventory_historyAdmin(ImportExportModelAdmin):
    list_display = ('station', 'material', 'quantity', 'manager', 'j_time')
    list_filter = ("station", "material", "manager", "time")
    search_fields = ['material','station',]

admin.site.register(models.Inventory_history, Inventory_historyAdmin)




#------------------------------------------------------------------------------
class Station_exit_historyAdmin(ImportExportModelAdmin):
    list_display = ('station', 'material', 'quantity', 'manager', 'order_code', 'j_time')
    list_filter = ("station", "material", "manager", "time")
    search_fields = ['material','station',]

admin.site.register(models.Station_exit_history, Station_exit_historyAdmin)



#------------------------------------------------------------------------------
class OrderAdmin(ImportExportModelAdmin):
    list_display = ('product', 'code', 'image', 'confirmed', 'completed', 'j_time')
    list_filter = ("product", "confirmed", "completed")
    search_fields = ['product', 'code']
    raw_id_fields = ('product',)

    def get_created_jalali(self, obj):
        return datetime2jalali(obj.start_time).strftime('%y/%m/%d _ %H:%M:%S')
    get_created_jalali.short_description = " زمان شروع "

admin.site.register(models.Order, OrderAdmin)



#------------------------------------------------------------------------------
class Order_confirmationAdmin(ImportExportModelAdmin):
    list_display = ('order', 'station', 'confirmed')
    list_filter = ("order", "station", "confirmed")
    search_fields = ['order', 'station']

admin.site.register(models.Order_confirmation, Order_confirmationAdmin)










#-------------------------------------------------------- by Nima Dorostkar ---
