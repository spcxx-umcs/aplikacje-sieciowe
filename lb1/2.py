#!/usr/bin/env python

source = input("Image in: ")
dist = "lab1zad1.png"

try:
    with open(source, "rb") as src, open(dist, "wb") as dst:
        while True:
            chunk = src.read(4096)
            if not chunk:
                break
            dst.write(chunk)
except IOError:
    print("Wrong path specified")
