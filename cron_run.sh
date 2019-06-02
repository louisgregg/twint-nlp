 #!/bin/bash
cd /home/f/fi/fin/Projects/twint-nlp
. twint-nlp-venv/bin/activate
python3.7 scrape_cities.py &> log.txt
deactivate
cd ~
