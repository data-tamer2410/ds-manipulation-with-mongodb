"""Task 1: Work with MongoDB."""

import os
from json.decoder import JSONDecodeError
from pymongo import MongoClient
from pymongo.errors import ConfigurationError, OperationFailure, InvalidURI


def parse_error(func):
    """Parse error."""

    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            return res
        except (
            ConfigurationError,
            OperationFailure,
            InvalidURI,
            FileNotFoundError,
            JSONDecodeError,
        ) as e:
            print(e)
            return None

    return wrapper


@parse_error
def create_db(
    login_db: str, password_db: str, clear_db: bool = True
) -> MongoClient | None:
    """Create client."""
    client = MongoClient(
        f"mongodb+srv://{login_db}:{password_db}@cluster0"
        f".brvba.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    )
    db = client.goit_cats
    db.cats.find_one()  # Check connection.
    if clear_db and login_db == "data-tamer2410":
        db.cats.drop()
        db.cats.insert_many(
            [
                {
                    "name": "barsik",
                    "age": 3,
                    "features": ["ходить в капці", "дає себе гладити", "рудий"],
                },
                {
                    "name": "musya",
                    "age": 9,
                    "features": [
                        "ходить на підлогу",
                        "не дає себе гладити",
                        "різнобарвна",
                    ],
                },
                {
                    "name": "chips",
                    "age": 1,
                    "features": ["ходить в лоток", "дає себе гладити", "сірий"],
                },
                {
                    "name": "senya",
                    "age": 9,
                    "features": [
                        "ходить в лоток",
                        "дає себе гладити",
                        "чорно-білий",
                    ],
                },
            ]
        )
    return db


# Read.
def read_all_doc(db: MongoClient) -> None:
    """Read all documents."""
    for doc in db.cats.find():
        print(doc)


def read_info_cat(db: MongoClient, name: str) -> None:
    """Read info about cat."""
    doc = db.cats.find_one({"name": name})
    print(doc if doc else f"Not found {name}")


# Update.
@parse_error
def update_age_cat(db: MongoClient, name: str, age: int) -> None:
    """Update age cat."""
    update = db.cats.update_one({"name": name}, {"$set": {"age": age}}).modified_count
    print(
        f"Age {name} updated"
        if update > 0
        else f"Not found {name} or this age has already been established"
    )


@parse_error
def update_features_cat(db: MongoClient, name: str, features: str) -> None:
    """Update features cat."""
    update = db.cats.update_one(
        {"name": name}, {"$push": {"features": features}}
    ).modified_count
    print(f"Features {name} updated" if update > 0 else f"Not found {name}")


# Delete.
@parse_error
def delete_cat(db: MongoClient, name: str) -> None:
    """Delete cat."""
    delete = db.cats.delete_one({"name": name}).deleted_count
    print(f"Cat {name} deleted" if delete > 0 else f"Not found {name}")


@parse_error
def delete_all_cats(db: MongoClient) -> None:
    """Delete all cats."""
    delete = db.cats.delete_many({}).deleted_count
    print("All cats deleted" if delete > 0 else "Not found cats")


if __name__ == "__main__":
    create_db("data-tamer2410", os.getenv("MONGO_PASSWORD"))
