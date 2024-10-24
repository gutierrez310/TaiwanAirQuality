# import contextlib
import io
import os
import pathlib
import shutil
import kagglehub
import argparse

def import_dataset(data_id):
    kagglehub.login()
    DIR = pathlib.Path(".").resolve()

    # NOTE: The ``path`` argument does not specify the path downloaded to, but
    #       instead a subpath of the data.
    # DATA_DOWNLOAD_IO = io.StringIO()
    DATA_DIR = pathlib.Path(kagglehub.dataset_download(data_id))
    print(DATA_DIR)

    # Define destination paths
    # destination_dir = pathlib.Path(r".\data")
    destination_dir = pathlib.Path(__file__)
    destination_dir = destination_dir.parent.parent.joinpath("data")

    # Ensure the destination directory exists (create it if it doesn't)
    destination_dir.mkdir(parents=True, exist_ok=True)

    # Move the entire directory from cache to the destination
    # if destination_dir.is_dir():
    #     shutil.copy(str(DATA_DIR), str(destination_dir))
    # else:
    #     shutil.move(str(DATA_DIR), str(destination_dir))
    shutil.move(str(DATA_DIR), str(destination_dir))

    print(f"Data moved to {destination_dir}")

    # Path.home().joinpath("python"

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Will download the kaggle database to the data file")
    parser.add_argument("data_id")
    args = parser.parse_args()
    print(f'args.data_id: {args.data_id}')
    import_dataset(args.data_id)

# kagglehub.auth.login()
# 