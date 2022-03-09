from typing import Tuple, Dict, List
from ainar.database.coco import Annotation, Category, Image
from peewee import ModelSelect


def aggregate(categories: ModelSelect, filter: Dict) -> Dict[str, dict]:
    data_per_category = [_gather_category_data(category) for category in categories.prefetch(Annotation, Image)]

    # Extract images from categories -> flatten -> unique
    images = list(set(sum([images for _, _, images in data_per_category], [])))
    # Extract annotations from categories -> flatten
    annotations = sum([annos for _, annos, _ in data_per_category], [])

    return {
        "per_class": {
            name: {
                "images": len(images),
                "boxes": len(boxes),
                "boxes_per_size": _sort_boxes_per_size(boxes),
                "boxes_per_image": len(boxes) / len(images),
            }
            for name, boxes, images in data_per_category
        },
        "__total__": {
            "num_classes": len(categories),
            "images": len(images),
            "boxes_per_size": _sort_boxes_per_size(annotations),
            "boxes_per_image": len(annotations) / len(images),
        },
    }


def _gather_category_data(category: Category) -> Tuple[str, List[Annotation], List[Image]]:
    return (
        category.name,
        list(category.annotations),
        list(set([anno.image for anno in category.annotations])),
    )


def _sort_boxes_per_size(annotations: List[Annotation]) -> Dict[str, int]:
    sizes = {
        "0-10": 0,
        "10-20": 0,
        "20-30": 0,
        "30-40": 0,
        "40-50": 0,
        "50-60": 0,
        "60-70": 0,
        "70-80": 0,
        "80-90": 0,
        "90-100": 0,
    }
    for annotation in annotations:
        _, _, width, height = annotation.bbox
        box_area = width * height
        image_area = annotation.image.width * annotation.image.height
        area_ratio = box_area / image_area
        sizes[_convert_scale_order(area_ratio)] += 1
    return sizes


def _convert_scale_order(scale: float) -> str:
    if scale < 0.1:
        return "0-10"
    elif scale < 0.2:
        return "10-20"
    elif scale < 0.3:
        return "20-30"
    elif scale < 0.4:
        return "30-40"
    elif scale < 0.5:
        return "40-50"
    elif scale < 0.6:
        return "50-60"
    elif scale < 0.7:
        return "60-70"
    elif scale < 0.8:
        return "70-80"
    elif scale < 0.9:
        return "80-90"
    return "90-100"
