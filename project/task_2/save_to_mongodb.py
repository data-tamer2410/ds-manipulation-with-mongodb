"""Task 2 (part 2): Save data to MongoDB. """

import json
import os
from pymongo import MongoClient
from project.task_1.main import parse_error


@parse_error
def load_to_mongodb(login: str, password: str) -> None:
    """Load data to MongoDB."""
    client = MongoClient(
        f"mongodb+srv://{login}:{password}@cluster0"
        ".brvba.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    )

    db = client.goit_qoutes_authors

    db.qoutes.drop()
    with open("./qoutes.json", encoding="utf-8") as file:
        qoutes_data = json.load(file)
        db.qoutes.insert_many(qoutes_data)

    db.authors.drop()
    with open("./authors.json", encoding="utf-8") as file:
        authors_data = json.load(file)
        db.authors.insert_many(authors_data)

    print("Data saved to MongoDB.")


if __name__ == "__main__":
    load_to_mongodb("data-tamer2410", os.getenv("MONGO_PASSWORD"))
