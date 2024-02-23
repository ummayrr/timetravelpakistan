#!/bin/bash
chmod +x scraper.py
chmod +x img.py
chmod +x imagemagick.sh
chmod +x app.js
python3 scraper.py
python3 img.py
./imagemagick.sh
node app.js
