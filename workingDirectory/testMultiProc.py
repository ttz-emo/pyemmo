#
# Copyright (c) 2018-2024 M. Schuler, TTZ-EMO, Technical University of Applied Sciences Wuerzburg-Schweinfurt.
#
# This file is part of PyEMMO
# (see https://gitlab.ttz-emo.thws.de/ag-em/pyemmo).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
"""Script for tutorial by Corey Schafer: https://www.youtube.com/watch?v=fKl2JW_qrso"""
import concurrent.futures
import multiprocessing

# %%
import time


def do_something(sec):
    print(f"Sleeping for {sec} seconds ...")
    time.sleep(sec)
    return f"Done sleeping for {sec} seconds..."


def testMultiProc():
    start = time.perf_counter()

    # proc1 = multiprocessing.Process(target=do_something)
    # proc2 = multiprocessing.Process(target=do_something)

    # proc1.start()
    # proc2.start()

    # proc1.join()
    # proc2.join()

    processes = []
    for _ in range(10):
        p = multiprocessing.Process(target=do_something, args=[1.5])
        p.start()
        processes.append(p)

    for process in processes:
        process.join()

    finish = time.perf_counter()

    print(f"Finished in {round(finish-start, 2)} seconds.")


def testConcurrent():
    start = time.perf_counter()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        ## 1. Version
        # f1 = executor.submit(do_something, 1)
        # f2 = executor.submit(do_something, 1)

        # print(f1.result())
        # print(f2.result())

        ## 2. Version with loop
        # results = [executor.submit(do_something, duration/4) for duration in range(1,10)]

        # for f in concurrent.futures.as_completed(results):
        #     print(f.result())

        ## 3. Version
        duration = [5, 4, 3, 2, 1]
        # map will return the results of the function in the order that they started!
        results = executor.map(do_something, duration)
        # for result in results:
        #     print(result)

    finish = time.perf_counter()

    print(f"Finished in {round(finish-start, 2)} seconds.")


if __name__ == "__main__":
    # testMultiProc()
    testConcurrent()
