#!/bin/bash

python3 -c "import JSON.HTMLfromJSON; \
                   JSON.HTMLfromJSON.saveHTMLasShell ( 'JSON/template.json' )"

uvicorn main:app --host 0.0.0.0 --port 80 --reload-include extended.py --reload
