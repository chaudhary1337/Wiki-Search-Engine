clear
mkdir -p /tmp/indices && rm -rf /tmp/indices/*.txt
python3 src/indexer.py "$1" "$2"
