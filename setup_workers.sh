#!/bin/sh

celery -A server.celery worker -l INFO