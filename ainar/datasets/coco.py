from pathlib import Path
from typing import List, Tuple, TypedDict, Union


class Image(TypedDict):
    id: int
    width: int
    height: int
    file_name: str
    license: int
    flickr_url: str
    coco_url: str
    date_captured: str


class Category(TypedDict):
    id: int
    name: str
    supercategory: str


class Segmentation(TypedDict):
    counts: List[int]
    size: Tuple[int, int]


class Annotation(TypedDict):
    id: int
    image_id: int
    category_id: int
    bbox: Tuple[int, int, int, int]  # [x, y, width, height]
    segmentation: Union[List[List[float]], Segmentation]
    area: float
    iscrowd: int  # 0 or 1


class Coco:
    @property
    def categories(self) -> List[Category]:
        return []

    @property
    def images(self) -> List[Image]:
        return []

    @property
    def annotations(self) -> List[Annotation]:
        return []


def load_dataset(path: Path):
    return Coco()
