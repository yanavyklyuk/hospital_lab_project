import pandas


def get_concurrency_dataframe():
    return pandas.read_csv('concurrency_analysis.csv')
