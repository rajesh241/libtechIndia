"""This module will have model definations for nrega"""
from django.db import models

# Create your models here.
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
    filepath = models.CharField(max_length=2048, null=True, blank=True)
    is_nic = models.BooleanField(default=True)
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
