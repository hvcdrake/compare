# import sys
from waitress import serve
from compareDniFace import prepareAllAndGetFlaskApp

# sys.path.insert(0, '../')

if __name__ == '__main__':
    app = prepareAllAndGetFlaskApp()
    # http://michal.karzynski.pl/blog/2013/06/09/django-nginx-gunicorn-virtualenv-supervisor/
    # As a rule-of-thumb set the --workers (NUM_WORKERS) according
    # to the following formula: 2 * CPUs + 1. The idea being, that
    # at any given time half of your workers will be busy doing I/O.
    # For a single CPU machine it would give you 3.
    from multiprocessing import cpu_count
    th = 2 * cpu_count() + 1
    print("starting with", th, "threads")
    Port = 8089
    serve(app, host='0.0.0.0', port=Port, threads=th)
