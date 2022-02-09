import peewee as pw
from playhouse.sqlite_ext import JSONField

from ainar.database.base import BaseModel


class Image(BaseModel):
    width = pw.FloatField()
    height = pw.FloatField()
    file_name = pw.CharField()
    license = pw.IntegerField()
    flickr_url = pw.CharField()
    coco_url = pw.CharField()
    date_captured = pw.DateTimeField()

    @property
    def area(self):
        return self.width * self.hight


class Category(BaseModel):
    name = pw.CharField()
    supercategory = pw.CharField()


class Annotation(BaseModel):
    image = pw.ForeignKeyField(Image, backref="annotations")
    category = pw.ForeignKeyField(Category, backref="annotations")
    bbox = JSONField()
    segmentation = JSONField()
    area = pw.FloatField()
    iscrowd = pw.BooleanField()

    # Extra annotatins
    area_ratio = pw.FloatField()
