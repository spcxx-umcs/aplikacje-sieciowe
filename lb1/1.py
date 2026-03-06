#!/usr/bin/env python

source = input("File in: ")
dist = "lab1zad1.txt"

try:
    with open(source, "r") as src, open (dist, "w") as dst:
        for line in src:
            dst.write(line)
except IOError:
    print("Wrong path specified")
