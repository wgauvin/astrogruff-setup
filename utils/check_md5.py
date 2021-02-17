#!/usr/bin/env python

def check_md5(f, expected):
    if f.exists():
        with open(f, 'rb') as fd:
            import hashlib

            file_hash = hashlib.md5(fd.read()).hexdigest()
            if expected != file_hash:
                print(f"{f}'s md5sum {file_hash} not equal to {expected}")


def main():
    from pathlib import Path
    import argparse

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--md5-file', '-m', required=True, type=str)
    arg_parser.add_argument('--input-dir', '-i', default='data', type=str)
    arg_parser.add_argument('--index-file', '-f', default=None, type=str)

    args = arg_parser.parse_args()

    import pathlib
    data_dir = pathlib.Path(args.input_dir)

    md5_file = pathlib.Path(args.md5_file)
    if not md5_file.exists():
        raise ValueError(f"{md5_file} does not exist")

    md5_dict = {}
    with open(md5_file, 'r') as f:
        for line in f:
            [md5, fits_file] = line.strip().split(' *')
            md5_dict[fits_file] = md5

    if args.index_file:
        if args.index_file in md5_dict:
            f = data_dir / args.index_file
            check_md5(f, md5_dict[args.index_file])
    else:
        # need to have multiple workers on this.
        import queue

        q = queue.Queue()
        done = False

        def add_jobs():
            for f, h in md5_dict.items():
                f = data_dir / f
                # check_md5(f, h)
                q.put_nowait((f, h))

            done = True

            q.join()

        def check_md5_thread():
            while not done:
                try:
                    (f, expected) = q.get_nowait()
                    check_md5(f, expected)
                except queue.Empty:
                    pass

        from concurrent.futures import ThreadPoolExecutor

        with ThreadPoolExecutor(max_workers=21) as tpe:
            for _ in range(20):
                tpe.submit(check_md5_thread)

            tpe.submit(add_jobs)

if __name__ == '__main__':
    main()
