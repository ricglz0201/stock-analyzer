#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py
Module in charge of the main process
"""

from thread import run_threads
from analyse_ticker import print_datas

if __name__ == "__main__":
    stocks = [line.rstrip() for line in open('stocks.txt', 'r')]
    threads = run_threads(stocks)

    for thread in threads:
        thread.join()

    print_datas()
