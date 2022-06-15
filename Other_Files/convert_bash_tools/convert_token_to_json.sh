#!/bin/bash

token="$@"

echo `echo "$token" | base64 --decode`
