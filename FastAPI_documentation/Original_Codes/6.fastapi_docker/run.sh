#!/bin/bash

cd TodoApp ; uvicorn main:app --host 172.16.239.6 --port 80 --reload
