from django.contrib import admin
from .models import *


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    list_filter = ()
    search_fields = ()


class DataFieldAdmin(admin.TabularInline):
    suit_classes = 'suit-tab suit-tab-data'
    model = DataField


class HeaderFieldAdmin(admin.TabularInline):
    suit_classes = 'suit-tab suit-tab-header'
    model = HeaderField


class ValidateAdmin(admin.TabularInline):
    suit_classes = 'suit-tab suit-tab-validate'
    model = Validate


@admin.register(RestApiTestCase)
class RestApiTestCaseAdmin(admin.ModelAdmin):
    list_display = ('project', 'url', 'headers_disp',
                    'data_disp', 'validate_disp', 'successed', 'last_run_result')
    list_filter = ()
    search_fields = ()
    inlines = [DataFieldAdmin, HeaderFieldAdmin, ValidateAdmin]

    suit_form_tabs = (('general', '主数据'), ('data', '数据'),
                      ('header', '头部'), ('validate', '校验'))

    actions = ['run']

    def get_fieldsets(self, request, obj=None):
        return [(None, {'classes': ('suit-tab suit-tab-general',), 'fields': self.get_fields(request, obj)})]

    def run(self, request, queryset):
        for obj in queryset:
            obj.run_test()
