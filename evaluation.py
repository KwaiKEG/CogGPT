import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import argparse
import pandas as pd
from sklearn.metrics import cohen_kappa_score

from utils.file_utils import load_json


def calculate_average_score(data, start, end):
    return sum(k for i, k in data.items() if start <= i <= end) / (end - start + 1)


def calculate_average_authenticity(file_path, method):
    df = pd.json_normalize(load_json(file_path), record_path=['questionnaire'], meta=['iteration'], record_prefix='questionnaire_')
    authenticity_avg_per_iteration = {}
    
    for iteration, group in df.groupby('iteration'):
        human_ratings = group['questionnaire_answer.human_rating'].tolist()
        method_ratings = group[f'questionnaire_answer.{method}.rating'].tolist()
        authenticity_avg_per_iteration[iteration] = cohen_kappa_score(human_ratings, method_ratings)

    average_kappa = calculate_average_score(authenticity_avg_per_iteration, 1, 10)
    kappa_iteration_5 = authenticity_avg_per_iteration.get(5, "No data for 5th iteration")
    kappa_iteration_10 = authenticity_avg_per_iteration.get(10, "No data for 10th iteration")

    print(f'======= {method} Authenticity =======')
    # print(f'0th iteration kappa: {rationality_avg_per_iteration[0]}')
    print(f'Average kappa: {average_kappa}')
    print(f'5th iteration kappa: {kappa_iteration_5}')
    print(f'10th iteration kappa: {kappa_iteration_10}')

    return authenticity_avg_per_iteration


def calculate_average_rationality(file_path, method):
    df = pd.json_normalize(load_json(file_path), record_path=['questionnaire'], meta=['iteration'], record_prefix='questionnaire_')
    rationality_avg_per_iteration = {}

    for iteration, group in df.groupby('iteration'):
        method_rationality = group[f'questionnaire_answer.{method}.rationality'].tolist()
        rationality_avg_per_iteration[int(iteration)] = sum(method_rationality) / len(method_rationality)

    average_rationality = calculate_average_score(rationality_avg_per_iteration, 1, 10)
    rationality_iteration_5 = rationality_avg_per_iteration.get(5, "No data for 5th iteration")
    rationality_iteration_10 = rationality_avg_per_iteration.get(10, "No data for 10th iteration")

    print(f'======= {method} Rationality =======')
    # print(f'0th iteration kappa: {rationality_avg_per_iteration[0]}')
    print(f'Average rationality: {average_rationality}')
    print(f'5th iteration rationality: {rationality_iteration_5}')
    print(f'10th iteration rationality: {rationality_iteration_10}')

    return rationality_avg_per_iteration


def add_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_path", type=str, default=os.path.join('data', 'datasets', 'huggingface', 'english', 'eval_a.json'), help="Path of the file.")
    parser.add_argument("--method", type=str, default="CoT", help="Method to calculate metrics.")
    parser.add_argument("--authenticity", action='store_true', default=True, help="Whether to calculate the authenticity metric.")
    parser.add_argument("--rationality", action='store_true', default=True, help="Whether to calculate the rationality metric.")

    return parser.parse_args()


def main():
    args = add_args()

    if args.authenticity:
        calculate_average_authenticity(args.file_path, args.method)

    if args.rationality:
        calculate_average_rationality(args.file_path, args.method)


if __name__ == '__main__':
    sys.exit(main())