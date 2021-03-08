#!/bin/bash
dockerize -wait tcp://db:3306 -timeout 20s
alembic upgrade head && python3 main.py