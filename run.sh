#!/bin/bash

source venv/bin/active
uvicorn webapp.main.application:app --host 0.0.0.0 --port 80

