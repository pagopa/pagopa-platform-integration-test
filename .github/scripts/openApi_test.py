
import sys
import os

import scripts.fetch_github_files as fetch_github_files
import scripts.schemathesis_runner as schemathesis_runner

OPENAPI_FOLDER = "tmp_fetched"

def main():
    # Fetch the OpenAPI files from GitHub
    fetch_github_files.main()
    print(f"Fetched OpenAPI files to {OPENAPI_FOLDER}")
    # Run the Schemathesis tests
    schemathesis_runner.main()

    # Remove the fetched OpenAPI files after testing
    for file in os.listdir(OPENAPI_FOLDER):
        file_path = os.path.join(OPENAPI_FOLDER, file)
        os.remove(file_path)
    os.rmdir(OPENAPI_FOLDER)
    print(f"Removed fetched OpenAPI folder")


if __name__ == "__main__":
    main()