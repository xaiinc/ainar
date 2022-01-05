from pathlib import Path
from typing import Dict, List, Optional

from playhouse.sqlite_ext import SqliteExtDatabase
import json
import click

from ainar.database import proxy
from ainar.database.coco import Annotation, Category, Image
from ainar.datasets.coco import load_dataset


@click.command()
@click.argument("data_dir", type=Path)
@click.option("--cache", type=Path, default=None, help="")
@click.option("--filter", default=None, help="")
@click.option("--output", default=None, help="")
@click.option("--export", default=None, help="")
def main(**args):
    args = validate_args(**args)

    # Check cache file existence
    has_cache = args["cache"].exists()

    # Create sqlite client
    db = SqliteExtDatabase(args["cache"])
    proxy.initialize(db)

    # TODO: Add force analize option
    # Analize dataset if cache does not exists
    if not has_cache:
        # Create tables
        db.create_tables([Annotation, Category, Image], safe=True)
        # Load dataset
        dataset = load_dataset(args["data_dir"])
        # Save data
        with db.atomic():
            Category.insert_many(dataset.categories).execute()
            Image.insert_many(dataset.images).execute()
            Annotation.insert_many(dataset.annotations).execute()

    # Aggregation
    data = aggregate(db, filter)

    # Display results
    display_data(data, args["output"])

    # Export to file
    if args["export"]:
        export(data)


def validate_args(
    data_dir: Path,
    cache: Optional[str],
    filter: Optional[str],
    output: Optional[str],
    export: Optional[str],
):
    if not data_dir.exists():
        raise FileNotFoundError(f'Dataset "{data_dir}" does not exists')

    return {
        "data_dir": data_dir,
        "cache": cache if cache else create_cache_path_from_data_dir(data_dir),
        "filter": json.loads(filter) if filter else {},
        "output": json.loads(output) if output else {},
        "export": export,
    }


def create_cache_path_from_data_dir(path: Path):
    return Path("./hogehoge.sqlite3")


def save_records(db: SqliteExtDatabase, records: List[Dict]):
    # TODO: Save records to SQLite
    return True


def aggregate(db: SqliteExtDatabase, filter: Dict):
    # TODO: Fetch data
    return []


def display_data(data: List[Dict], options: Dict):
    # TODO: Display data
    print(data)


def export(data: List[Dict]):
    # TODO: Export data
    pass


if __name__ == "__main__":
    main()
