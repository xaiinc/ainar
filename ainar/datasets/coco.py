from pathlib import Path
from typing import List, Tuple, TypedDict, Union

from pycocotools.coco import COCO

CLASSES = [
    "person",
    "bicycle",
    "car",
    "motorcycle",
    "airplane",
    "bus",
    "train",
    "truck",
    "boat",
    "traffic light",
    "fire hydrant",
    "stop sign",
    "parking meter",
    "bench",
    "bird",
    "cat",
    "dog",
    "horse",
    "sheep",
    "cow",
    "elephant",
    "bear",
    "zebra",
    "giraffe",
    "backpack",
    "umbrella",
    "handbag",
    "tie",
    "suitcase",
    "frisbee",
    "skis",
    "snowboard",
    "sports ball",
    "kite",
    "baseball bat",
    "baseball glove",
    "skateboard",
    "surfboard",
    "tennis racket",
    "bottle",
    "wine glass",
    "cup",
    "fork",
    "knife",
    "spoon",
    "bowl",
    "banana",
    "apple",
    "sandwich",
    "orange",
    "broccoli",
    "carrot",
    "hot dog",
    "pizza",
    "donut",
    "cake",
    "chair",
    "couch",
    "potted plant",
    "bed",
    "dining table",
    "toilet",
    "tv",
    "laptop",
    "mouse",
    "remote",
    "keyboard",
    "cell phone",
    "microwave",
    "oven",
    "toaster",
    "sink",
    "refrigerator",
    "book",
    "clock",
    "vase",
    "scissors",
    "teddy bear",
    "hair drier",
    "toothbrush",
]


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
    def __init__(
        self,
        annotation_file: Path,
    ) -> None:

        self._coco = COCO(str(annotation_file))
        self._classes = CLASSES

    @property
    def classes(self):
        return self._classes

    @property
    def categories(self) -> List[Category]:
        return self._coco.cats.values()

    @property
    def images(self) -> List[Image]:
        return self._coco.imgs.values()

    @property
    def annotations(self) -> List[Annotation]:
        return self._coco.anns.values()


def load_dataset(path: Path):
    return Coco(path)
