#!/bin/bash
echo "Sleeping until web container is up..."
sleep 10
pytest -q
