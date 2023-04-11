docker stats >> report_resources.txt
python3 ./parse_resources_results.py ./report_resources.txt