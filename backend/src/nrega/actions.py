


def reset_in_progress(modeladmin, request, queryset):
    for obj in queryset:
        obj.inProgress=False
        obj.status = "inQueue"
        obj.priority = 100
        obj.save()
