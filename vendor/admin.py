import csv

from django.contrib import admin
from django.http import HttpResponse

from vendor.models import VendorPlanner, VendorMeetingRegister
from import_export.admin import ImportExportModelAdmin
from import_export.resources import ModelResource


class VendorPlannerResource(ModelResource):
    class Meta:
        model = VendorPlanner
        fields = ('id', 'company_name', 'country', 'first_name', 'last_name', 'job_title', 'company_type',
                  'website', 'asia_pacific', 'middle_east_africa', 'europe', 'north_america', 'canada',
                  'south_central_america', 'caribbean', 'budget_for_events', 'weddings_per_year')


# Register your models here.
@admin.action(description='Mark selected Vendor Planners as active')
def mark_active(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description='Mark selected Vendor Planners as inactive')
def mark_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)


class VendorPlannerAdmin(ImportExportModelAdmin):
    resource_class = VendorPlannerResource
    list_display = ('company_name', 'country', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('company_name',)

    fieldsets = (
        ("Base Info", {
            'fields': ('company_name', 'country', 'first_name', 'last_name', 'job_title', 'company_type',
                       'website', 'budget_for_events', 'weddings_per_year'),
        }),
        ('Destinations of Interest', {
            'fields': ('asia_pacific', 'middle_east_africa', 'europe', 'north_america', 'canada',
                       'south_central_america', 'caribbean')
        }),
        ("Is active?", {
            'fields': ('is_active',)
        })

    )

    actions = [mark_active, mark_inactive]


class VendorMeetingRegisterAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'company_name', 'email', 'create_time')
    list_filter = ('create_time',)
    search_fields = ('first_name', 'last_name', 'company_name', 'email')
    filter_horizontal = ('vendors',)

    actions = ['export_as_csv']

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="vendor_meeting_register.csv"'

        writer = csv.writer(response)
        writer.writerow(['First Name', 'Last Name', 'Company Name', 'Email', 'Create Time', 'Vendors'])

        for obj in queryset:
            vendors = ', '.join([vendor.company_name for vendor in obj.vendors.all()])
            writer.writerow([obj.first_name, obj.last_name, obj.company_name, obj.email, obj.create_time, vendors])

        return response

    export_as_csv.short_description = "Export selected as CSV"


admin.site.register(VendorMeetingRegister, VendorMeetingRegisterAdmin)
admin.site.register(VendorPlanner, VendorPlannerAdmin)
