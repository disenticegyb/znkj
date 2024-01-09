# # This is an auto-generated django_project model module.
# # You'll have to do the following manually to clean this up:
# #   * Rearrange models' order
# #   * Make sure each model has one field with primary_key=True
# #   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
# #   * Remove `managed = False` lines if you wish to allow django_project to create, modify, and delete the table
# # Feel free to rename the models, but don't rename db_table values or field names.
# from django.db import models
#
#
# class Dataset(models.Model):
#     name = models.CharField(max_length=255)
#     content = models.TextField()
#     type = models.CharField(max_length=255, db_comment='数据集类型type 课程实验所需类型默认为0')
#     flag = models.CharField(max_length=255, blank=True, null=True, db_comment='对于多数据集的标识，以方便更新')
#
#     class Meta:
#         managed = False
#         db_table = 'dataset'
