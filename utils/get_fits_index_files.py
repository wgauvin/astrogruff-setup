#!/usr/bin/env python

import threading, queue

class Worker():

    work_done = False
    next_worker_id = 0;

    def __init__(self, work_queue, data_dir):
        self.work_queue = work_queue
        self.data_dir = data_dir
        self.worker_id = Worker.next_worker_id
        self.worker_prefix = "[Worker {:2d}]".format(self.worker_id)
        Worker.next_worker_id += 1

    def __call__(self, *arg, **kwargs):
        while not Worker.work_done:
            try:
                data = self.work_queue.get_nowait()
                self.__get_file(**data)
                self.work_queue.task_done()
            except queue.Empty:
                pass

    def __get_file(self, index_class, index, suffix=None):
        try:
            f = f"index-{index}"
            if suffix is not None:
                f += f"-{suffix:02}"

            f += ".fits"

            outfile = self.data_dir / f
            if outfile.exists():
                print(f"{self.worker_prefix} Index file {outfile} exists")
                return

            print(f"{self.worker_prefix} Getting index file: {f}")
            import requests

            response = requests.get(
                f"http://broiler.astrometry.net/~dstn/{index_class}/{f}",
                allow_redirects=True,
                stream=True,
            )

            if response.status_code == requests.codes.ok:
                with open(outfile, 'wb') as out:
                    for b in response.iter_content(chunk_size=8192):
                        out.write(b)
            elif response.status_code == 404:
                print(f"{self.worker_prefix} Index file {f} does not exist")
                return
            else:
                response.raise_for_status()
        except Exception as e:
            print(e)

def add_4100_to_queue(q):
    # for the 4100 index files
    for index in range(4119, 4100, -1):
        q.put({'index': index, 'index_class': 4100 })

def add_4200_to_queue(q):
    for index in range(4219, 4201, -1):
        if index <= 4207:
            for suffix in range(50):
                q.put({'index': index, 'index_class': 4200, 'suffix': suffix})
        else:
            q.put({'index': index, 'index_class': 4200 })

def wait_on_workers(q):
    print("Waiting on workers")
    q.join()

    print("Marking work as done")
    Worker.work_done = True

def main():
    from pathlib import Path
    import argparse
    from concurrent.futures import ThreadPoolExecutor

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--out-dir', '-o', default='data', type=str)
    arg_parser.add_argument('--num-workers', '-n', default=5, type=int)

    args = arg_parser.parse_args()

    import pathlib
    data_dir = pathlib.Path(args.out_dir)
    data_dir.mkdir(parents=True, exist_ok=True)

    q = queue.Queue(maxsize=2 * args.num_workers)

    with ThreadPoolExecutor(max_workers=args.num_workers + 3) as tpe:
        tpe.submit(add_4100_to_queue, q)
        tpe.submit(add_4200_to_queue, q)

        for i in range(args.num_workers):
            worker = Worker(work_queue=q, data_dir=data_dir)
            tpe.submit(worker)

        tpe.submit(wait_on_workers, q)

if __name__ == '__main__':
    main()
