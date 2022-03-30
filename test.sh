#!/bin/bash

usage_string="usage: ./$(basename "$0") [file_or_dir] [pytest_options] [-e]

Wraps the pytest command by adding the --extended option (see below).

Options
  -e, --extended  If provided, tests run against all combinations of hash
                  algorithm, encoding type, raw-bytes mode and security mode
                  (3240 in total); otherwise, only against the encodings UTF-8,
                  UTF-16 and UTF-32 (108 combinations in total).
  -h, --help      Display help message and exit
"

set -e

usage() { echo -n "$usage_string" 1>&2; }

EXTENDED=false

while [[ $# -gt 0 ]]
do
    arg="$1"
    case $arg in
        --extended|-e)
            EXTENDED=true
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "[-] Invalid argument: $arg"
            usage
            exit 1
            ;;
    esac
done


CONFIG="tests/conftest.py"

ENCODINGS_EXT="ENCODINGS = EXTENDED"
ENCODINGS_LIM="ENCODINGS = LIMITED"

if [ $EXTENDED = true ]; then
    sed -ie "/$ENCODINGS_EXT/s/^#//#" $CONFIG     # comment
    sed -ie "/$ENCODINGS_LIM/s/^#*/#/#" $CONFIG   # uncomment
else
    sed -ie "/$ENCODINGS_EXT/s/^#*/#/" $CONFIG    # uncomment
    sed -ie "/$ENCODINGS_LIM/s/^#//#" $CONFIG     # comment
fi

python3 -m pytest tests/ \
  --cov-report term-missing \
  --cov=. $*
