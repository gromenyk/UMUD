from pathlib import Path
import pandas as pd
import toml
from pymongo import MongoClient

secrets_path = (
    Path(__file__).parent.parent
    / ".streamlit"
    / "secrets.toml"
)

with open(secrets_path, "r") as f:
    secrets = toml.load(f)

mongo_uri = secrets["mongo"]["CONNECTION_STRING"]

client = MongoClient(mongo_uri)

benchmark_db = client.benchmarks

benchmarks_collection = (
    benchmark_db.benchmarks
)

pending_submissions_collection = (
    benchmark_db.review_pending_submissions
)

approved_submissions_collection = (
    benchmark_db.approved_submissions
)

rejected_submissions_collection = (
    benchmark_db.rejected_submissions
)

def list_pending_submissions():

    pending_submissions = []

    for document in pending_submissions_collection.find():

        pending_submissions.append(
            document["metadata"]
        )

    return pending_submissions

def load_submission(model_name):

    document = pending_submissions_collection.find_one(
        {
            "metadata.model_name": model_name
        }
    )

    if document is None:
        raise ValueError(
            f"Submission '{model_name}' not found."
        )

    submission = {
        "metadata": document["metadata"],
        "predictions": pd.DataFrame(
            document["predictions"]
        ),
        "model_name": model_name
    }

    return submission

def approve_submission(model_name):

    document = pending_submissions_collection.find_one(
        {
            "metadata.model_name": model_name
        }
    )

    if document is None:
        raise ValueError(
            f"Submission '{model_name}' not found."
        )

    document["metadata"]["status"] = "approved"

    approved_submissions_collection.insert_one(
        document
    )

    pending_submissions_collection.delete_one(
        {
            "_id": document["_id"]
        }
    )

def reject_submission(model_name):

    document = pending_submissions_collection.find_one(
        {
            "metadata.model_name": model_name
        }
    )

    if document is None:
        raise ValueError(
            f"Submission '{model_name}' not found."
        )

    document["metadata"]["status"] = "rejected"

    rejected_submissions_collection.insert_one(
        document
    )

    pending_submissions_collection.delete_one(
        {
            "_id": document["_id"]
        }
    )

def upload_benchmark(
    benchmark_name,
    csv_path
):

    csv_path = csv_path.strip('"')

    if not csv_path.lower().endswith(".csv"):
        csv_path += ".csv"

    benchmark_df = pd.read_csv(
        csv_path,
        sep=","
    )

    if len(benchmark_df.columns) == 1:
        raise ValueError(
            "Invalid CSV format. Benchmarks must use ',' as separator."
        )

    document = {

        "benchmark_name": benchmark_name,

        "data": benchmark_df.to_dict(
            "records"
        )

    }

    benchmarks_collection.delete_many(
        {
            "benchmark_name": benchmark_name
        }
    )

    benchmarks_collection.insert_one(
        document
    )