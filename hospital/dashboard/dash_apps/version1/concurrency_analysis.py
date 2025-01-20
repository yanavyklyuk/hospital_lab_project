import time
import requests
import pandas as pd
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor


def make_request(args):
    url, api_token = args
    try:
        headers = {
            'Authorization': f'Token {api_token}'
        }
        response = requests.get(url, headers=headers)
        return response.status_code
    except Exception:
        return None


def worker_threaded(url, api_token, num_threads, num_requests):
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        start_time = time.time()
        results = list(executor.map(make_request, [(url, api_token)] * num_requests))
        elapsed_time = time.time() - start_time
    return elapsed_time


def worker_process(url, api_token, num_threads, num_requests_per_process):
    return worker_threaded(url, api_token, num_threads, num_requests_per_process)


def analyze_concurrency(url, api_token, num_requests=250):
    process_counts = [1, 2, 3, 4, 5]
    thread_counts = [1, 2, 5, 10, 25, 50]

    results = []

    for num_processes in process_counts:
        for num_threads in thread_counts:
            requests_per_process = int(num_requests) // num_processes

            start_time = time.time()
            with Pool(processes=num_processes) as pool:
                pool_results = pool.starmap(
                    worker_process,
                    [(url, api_token, num_threads, requests_per_process) for _ in range(num_processes)]
                )
            total_time = time.time() - start_time

            results.append({
                "processes": num_processes,
                "threads": num_threads,
                "time": total_time
            })

            print(f"Processes: {num_processes}, Threads: {num_threads}, Time: {total_time:.2f} seconds")

    return pd.DataFrame(results)


if __name__ == "__main__":
    url = "http://127.0.0.1:8000/frontend/patients/124/diseases_journal/"
    api_token = "0e6b59d6b34a0f9a9119ced567d72cf7190e9e60"
    df = analyze_concurrency(url, api_token)
    print(df)

    df.to_csv("concurrency_analysis.csv", index=False)
