import csv
from collections import defaultdict

import requests

from CodeBertEmbeddingModel import CodeBertEmbeddingModel
from SimilarityPredictionModel import SimilarityThresholdPredictionModel
from consts import CODE_BASE_ROOT_DIR, SOURCE_FILE_EXTENSION, GITHUB_TOKEN


def rearrange_and_group_csv(input_file, output_file):
    grouped_data = defaultdict(list)

    # Read the CSV file
    with open(input_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            X, Y, Z = row
            # Rearrange the order to Y,X,Z
            rearranged_row = [Y, X, Z]
            # Group by Y
            grouped_data[Y].append(rearranged_row)

    # Write the rearranged and grouped data to a new CSV file
    with open(output_file, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        for Y, rows in grouped_data.items():
            sorted_rows = sorted(rows, key=lambda x: x[2], reverse=True)
            for row in sorted_rows:
                csvwriter.writerow(row)


def add_similarity_to_data(input_file, output_file):
    with open(input_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        rows = [row for row in csvreader]

    with open(output_file, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        embedding_model = CodeBertEmbeddingModel(CODE_BASE_ROOT_DIR)
        for row in rows[1:]:
            X, Y, Z = row
            W = SimilarityThresholdPredictionModel.similarity(embedding_model.embed_path(X),
                                                              embedding_model.embed_path(Y))
            csvwriter.writerow([X, Y, Z, W])


def list_files_in_github_directory(github_url):

    def get_files(url, headers):
        urls = []
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            contents = response.json()
            for item in contents:
                if item['type'] == 'file' and item['name'].endswith(SOURCE_FILE_EXTENSION):
                    urls.append(item['download_url'])
                elif item['type'] == 'dir':
                    urls.extend(get_files(item['url'], headers))
            return urls
        return None

    request_headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json',
    }

    # Extract the owner and repo from the URL
    path_parts = github_url.rstrip('/').split('/')
    owner = path_parts[3]
    repo = path_parts[4]

    dir_path_parts = path_parts[5:]

    while len(dir_path_parts) > 0:
        dir_path = "/".join(dir_path_parts)
        api_url = f'https://api.github.com/repos/{owner}/{repo}/contents/{dir_path}'

        file_urls = get_files(api_url, request_headers)
        if file_urls is not None:
            return file_urls

        dir_path_parts = dir_path_parts[1:]

    raise Exception(f'Github URL {github_url} couldn\'t be resolved.')


def convert_to_raw_url(url):
    if 'github.com' in url and '/blob/' in url:
        # Convert the GitHub URL to the raw content URL
        return url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
    return url


def fetch_file_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        response.raise_for_status()


def fetch_github_file_content(url):
    raw_url = convert_to_raw_url(url)
    try:
        file_content = fetch_file_content(raw_url)
        return file_content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching file: {e}")
