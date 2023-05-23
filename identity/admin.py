from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from identity.models import Account

# Register your models here.


class AccountAdmin(UserAdmin):
    list_display = ('username', 'email', 'organization_name', 'type_of_organization', 'location_id', 'is_staff', 'is_admin', 'is_superuser')
    search_fields = ('username', 'email')
    # showing the group name from the options in the user auth (account) in the admin dashboard
    actions = ['add_selected_to_group']
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    # For adding the customer user to a group in the admin dashboard
                    
    def add_selected_to_group(self, request, queryset):
        group = Group.objects.get(name='Manager-admins')  # Replace 'Your Group Name' with the actual group name
        for user in queryset:
            user.groups.add(group)

    add_selected_to_group.short_description = "Add selected users to group"


admin.site.register(Account, AccountAdmin)
