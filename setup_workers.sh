#!/bin/sh

celery -A server.celery worker -l INFO -Q s3