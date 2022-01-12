import json
from typing import Any, Dict, List

import peewee as pw

from ainar.database.coco import Annotation, Category, Image


def parse_filter_string(filter_string: str) -> Dict[str, Any]:
    return json.loads(filter_string)


def filter_annotations(query: pw.ModelSelect, conditions: Dict[str, Any]):
    query = query.join(Image, on=(Annotation.image_id == Image.id))
    query = query.join(Category, on=(Annotation.category_id == Category.id))

    if "classes" in conditions:
        query = filter_classes(query, conditions["classes"])

    return query


def filter_classes(query: pw.ModelSelect, classes: List[str]):
    return query.where(Category.name << classes)
