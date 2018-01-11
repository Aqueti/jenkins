#!/bin/bash

find . -type f | perl -lne 'print if -B' | xargs rm