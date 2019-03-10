#!/bin/bash
set -e

HOST=timelapse@idlecode.pl
PORT=2212

SRC_FILE=$1
DST_DIR=$2

ssh -p $PORT $HOST "mkdir -p $DST_DIR"
scp -P $PORT "$SRC_FILE" "$HOST:$DST_DIR"

