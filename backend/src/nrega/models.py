"""This module will have model definations for nrega"""
#pylint: disable-msg = too-few-public-methods
from django.db import models
from django_mysql.models import JSONField

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
    display_name = models.CharField(max_length=2048)
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
    libtech_tag = models.ManyToManyField(LibtechTag)
    data_json = JSONField(null=True, blank=True)  # requires Django-Mysql package
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
    report_type = models.CharField(max_length=256)
    report_url = models.URLField(max_length=2048, blank=True, null=True)
    excel_url = models.URLField(max_length=2048, blank=True, null=True)
    code = models.CharField(max_length=256, db_index=True, blank=True, null=True)
    finyear = models.CharField(max_length=2, blank=True, null=True, default='NA')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
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
    scheme = models.CharField(max_length=64, default="nrega")
    start_finyear = models.CharField(max_length=2, null=True, blank=True)
    end_finyear = models.CharField(max_length=2, null=True, blank=True)
    status = models.CharField(max_length=256, default='inQueue')
    priority = models.PositiveSmallIntegerField(default=100)
    report_url = models.URLField(max_length=2048, blank=True, null=True)
    force_download = models.BooleanField(default=False)
    is_error = models.BooleanField(default=False)
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
