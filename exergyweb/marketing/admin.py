from django.contrib import admin

from .models import Stay_Tuned

class Stay_tuned_Admin(admin.ModelAdmin):
    list_display = ('email', 'name', 'timestamp')

admin.site.site_header = "EXERGY Administration"
admin.site.register(Stay_Tuned, Stay_tuned_Admin)

