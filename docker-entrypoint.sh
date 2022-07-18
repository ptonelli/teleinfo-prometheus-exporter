#! /bin/sh

uvicorn --host $HOST --port $PORT main:app --reload 
