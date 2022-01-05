from pathlib import Path
from typing import Dict, List, Optional

from peewee import SqliteDatabase
import json
import click


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
    db = SqliteDatabase(args["cache"], pragmas={"journal_mode": "wal"})

    # TODO: Add force analize option
    # Analize dataset if cache does not exists
    if not has_cache:
        records = [analize(annotation, image) for annotation, image in load_dataset(args["data_dir"])]
        save_records(db, records)

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
    return Path("./hogehoge")


def load_dataset(path: Path):
    # TODO: Return data as generator
    return []


def analize(annotation: Dict, image: Path):
    # TODO: Analize annotation and image
    return {}


def save_records(db: SqliteDatabase, records: List[Dict]):
    # TODO: Save records to SQLite
    return True


def aggregate(db: SqliteDatabase, filter: Dict):
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
