from rq import Queue
from nrega.worker import conn

from django.db import models
from django_mysql.models import JSONField
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from nrega.bundle import create_bundle
User = get_user_model()
# Create your models here.


class LibtechTag(models.Model):
    """This is class to tags
    Tags can be applied to locations or reports
    """
    name = models.CharField(max_length=256)
    class Meta:
        """To define meta data attributes"""
        db_table = 'libtechtag'
    def __str__(self):
        """Default str method for the class"""
        return f"{self.name}"

class Location(models.Model):
    """This class holds all the meta data related to location"""
    name = models.CharField(max_length=256)
    scheme = models.CharField(max_length=64, default="nrega")
    location_type = models.CharField(max_length=64)
    code = models.CharField(max_length=20, db_index=True)
    nic_url = models.URLField(max_length=2048, blank=True, null=True)
    display_name = models.CharField(max_length=2048, null=True, blank=True)
    name_not_english = models.BooleanField(default=False)
    english_name = models.CharField(max_length=256, null=True, blank=True)
    parent_location = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    slug = models.SlugField(blank=True)
    crawl_ip = models.CharField(max_length=256, null=True, blank=True)
    state_short_code = models.CharField(max_length=2, null=True, blank=True)
    state_code = models.CharField(max_length=2, null=True, blank=True)
    state_name = models.CharField(max_length=256, null=True, blank=True)
    district_code = models.CharField(max_length=4, null=True, blank=True)
    district_name = models.CharField(max_length=256, null=True, blank=True)
    block_code = models.CharField(max_length=7, null=True, blank=True)
    block_name = models.CharField(max_length=256, null=True, blank=True)
    panchayat_code = models.CharField(max_length=10, null=True, blank=True)
    panchayat_name = models.CharField(max_length=256, null=True, blank=True)
    s3_filepath = models.CharField(max_length=2048, null=True, blank=True)
    is_nic = models.BooleanField(default=True)
    libtech_tag = models.ManyToManyField(LibtechTag, blank=True)
    accuracy = models.DecimalField(null=True, blank=True,  max_digits=5, decimal_places=2)
    last_crawl_date = models.DateTimeField(null=True, blank=True)
    is_data_available = models.BooleanField(default=False)
    remarks = models.TextField(blank=True, null=True)
    class Meta:
        """To define meta data attributes"""
        db_table = 'location'
    def __str__(self):
        """Default str method for the class"""
        return f"{self.code}-{self.name}"


class Report(models.Model):
    """This is the class for report meta data"""
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    libtech_tag = models.ManyToManyField(LibtechTag, blank=True, db_index=True)
    location_type = models.CharField(max_length=64, db_index=True, null=True,
                                     blank=True)
    location_code = models.CharField(max_length=20, db_index=True, null=True,
                                     blank=True)
    location_name = models.CharField(max_length=256, db_index=True, blank=True,
                                    null=True)
    health = models.CharField(max_length=64, default="unknown", null=True,
                                     blank=True)
    report_type = models.CharField(max_length=256, db_index=True)
    archive_reports = JSONField(null=True, blank=True, default=list)  
    report_url = models.URLField(max_length=2048, blank=True, null=True)
    excel_url = models.URLField(max_length=2048, blank=True, null=True)
    code = models.CharField(max_length=256, db_index=True, blank=True, null=True)
    finyear = models.CharField(max_length=2, blank=True, null=True, default='NA')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    remarks = models.TextField(blank=True, null=True)
    class Meta:
        """class to hold meta data attributes"""
        unique_together = ('location', 'report_type', 'finyear')
        db_table = 'report'
    def __str__(self):
        """Default str method for the class"""
        return f"{self.location.code}_{self.location.name}_{self.report_type}"


class TaskQueue(models.Model):
    """This is the class for Task Queue model"""
    report_type = models.CharField(max_length=256)
    location_code = models.CharField(max_length=20)
    location_class = models.CharField(max_length=64, default='NREGAPanchayat')
    task_type = models.CharField(max_length=64, default='download')
    scheme = models.CharField(max_length=64, default="nrega")
    start_finyear = models.CharField(max_length=2, null=True, blank=True)
    end_finyear = models.CharField(max_length=2, null=True, blank=True)
    status = models.CharField(max_length=256, default='inQueue')
    priority = models.PositiveSmallIntegerField(default=100)
    report_url = models.URLField(max_length=2048, blank=True, null=True)
    force_download = models.BooleanField(default=False)
    is_error = models.BooleanField(default=False)
    in_progress = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)
    response = models.CharField(max_length=256, null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    process_name = models.CharField(max_length=256, null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        """This is Meta class"""
        db_table = 'taskQueue'
    def __str__(self):
        return self.location_code + "_" + self.report_type

class Bundle(models.Model):
    title = models.CharField(max_length=2048, default="zipped bundle")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report_types = models.CharField(max_length=2048)
    finyears = models.CharField(max_length=2048, null=True, blank=True)
    location_code = models.CharField(max_length=20, null=True, blank=True)
    location_type = models.CharField(max_length=20, null=True, blank=True)
    filename = models.CharField(max_length=1024, null=True, blank=True)
    report_format = models.CharField(max_length=20, null=True, blank=True, default="csv")
    libtech_tags = models.CharField(max_length=2048, null=True, blank=True)
    bundle_url = models.URLField(max_length=2048, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    is_bundle_created = models.BooleanField(default=False)
    is_error = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        """This is Meta class"""
        db_table = 'bundle'
    def __str__(self):
        return self.title

class CrawlSchedule(models.Model):
    title = models.CharField(max_length=2048, default="zipped bundle")
    user = models.ForeignKey(LibtechTag, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=2048)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        """This is Meta class"""
        db_table = 'crawlschedule'
    def __str__(self):
        return self.title


def bundle_post_save_receiver(sender, instance, *args, **kwargs):
    '''Bundle Post save receiver'''
    if (instance.is_bundle_created == False):
        report_type_array = instance.report_types.split(",")
        qs = Report.objects.filter(report_type__in=report_type_array)
        if instance.libtech_tags is not None:
            libtech_tag_array = instance.libtech_tags.split(",")
            libtech_tag_object_array = []
            for tag in libtech_tag_array:
                obj = LibtechTag.objects.filter(name = tag).first()
                if obj is not None:
                    libtech_tag_object_array.append(obj)
            qs = qs.filter(libtech_tag__in=libtech_tag_object_array)
        if instance.location_type is not None:
            qs = qs.filter(location_type = instance.location_type)
        if instance.location_code is not None:
            qs = qs.filter(location_code = instance.location_code)
        bundle_url = create_bundle(instance, qs)
        instance.bundle_url = bundle_url
        instance.is_bundle_created = True
        instance.save()

#post_save.connect(bundle_post_save_receiver, sender=Bundle)
