import concurrent.futures
import secrets
import traceback

def print_progress(cnt, lmt, err):
    percentage = 0
    if lmt>0:
        percentage = 100*cnt/lmt
    percentage = round(percentage, 1)

    if cnt > 0:
        percentage_error = 100*err/cnt
        percentage_error = round(percentage_error, 1)
    else:
        percentage_error = 0.0
    print(f'\33[2K{percentage}% - {cnt}/{lmt} ({err} errors {percentage_error}%)\r', end="")

def make_future(job_function, input_data, num_processes=None):
    i = 0
    err = 0
    lmt =len(input_data)
    print_progress(i, lmt, err)

    executor = concurrent.futures.ProcessPoolExecutor(num_processes)

    futures = []
    mapping = {}

    for c, v in enumerate(input_data):
        future = executor.submit(job_function, v)
        futures.append(future)
        mapping[future] = v

    for future in concurrent.futures.as_completed(futures):
        i += 1 
        try:
            result = future.result()
        except Exception as e:
            err += 1

            uniq = secrets.token_hex(15)
            file_name = f'/tmp/{uniq}.log'

            with open(file_name, 'w') as fp:
                fp.write(traceback.format_exc())

            print(f'{str(mapping[future])} -> {type(future.exception()).__name__} -> {file_name}')

        print_progress(i, lmt, err)

    print()