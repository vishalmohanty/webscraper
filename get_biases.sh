$!/bin/zsh

for i in data/location_data/capitols_split/*; do
  echo "Processing: $i"
  python3 webscraper.py $i >> results_auto.txt
  sleep 5400
done
