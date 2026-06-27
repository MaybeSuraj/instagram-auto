#!/usr/bin/env bash
set -e

pip install -r requirements.txt
pip install "instagrapi[video]"
pip install --no-deps "moviepy==2.2.1"