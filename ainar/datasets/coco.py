from typing import Any, Dict, List

from pycocotools.coco import COCO


class CocoDetection:
    def __init__(
        self,
        annotation_file: str,
    ) -> None:

        self.coco = COCO(annotation_file)
        self.ids = list(sorted(self.coco.imgs.keys()))

    def _load_annotation(self, id: int) -> List[Any]:
        return self.coco.loadAnns(self.coco.getAnnIds(id))

    def __getitem__(self, index: int) -> List[Dict]:
        id = self.ids[index]
        annotation = self._load_annotation(id)
        return annotation

    def __len__(self) -> int:
        return len(self.ids)
