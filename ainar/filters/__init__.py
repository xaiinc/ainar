import json
from typing import Any, Dict

import peewee as pw

from ainar.database.coco import Annotation, Category, Image


def parse_filter_string(filter_string: str) -> Dict[str, Any]:
    return json.loads(filter_string)


def filter_dataset(conditions: Dict[str, Any]):
    categories = Category.select(Category)
    if "classes" in conditions:
        categories = categories.where(Category.name << conditions["classes"])

    annotations = Annotation.select(Annotation)
    annotations = annotations.join(categories, on=(categories.c.id == Annotation.category_id))
    if "box_size" in conditions:
        annotations = annotations.where(Annotation.area_ratio > conditions["box_size"])

    images = Image.select(Image)
    images = images.join(annotations, on=(Image.id == annotations.c.image_id))
    if "box_per_image" in conditions:
        images = images.group_by(Image.id)
        images = images.having(pw.fn.Count(annotations.c.id) > conditions["box_per_image"])

    category_list = []
    for category in categories:
        category.annotations = list(annotations.where(Annotation.category_id == category.id))
        category_list.append(category)

    return category_list
