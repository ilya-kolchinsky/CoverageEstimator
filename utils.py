import csv
from collections import defaultdict

from SequenceTransformerEmbeddingModel import SequenceTransformerEmbeddingModel
from SimilarityPredictionModel import SimilarityThresholdPredictionModel
from consts import CODE_BASE_ROOT_DIR


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
        embedding_model = SequenceTransformerEmbeddingModel(CODE_BASE_ROOT_DIR)
        for row in rows[1:]:
            X, Y, Z = row
            W = SimilarityThresholdPredictionModel.similarity(embedding_model.embed_path(X),
                                                              embedding_model.embed_path(Y))
            csvwriter.writerow([X, Y, Z, W])
