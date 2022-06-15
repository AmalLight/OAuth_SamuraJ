#!/bin/bash

json="$@"

echo `echo "$json" | base64`
