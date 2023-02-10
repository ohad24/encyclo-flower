import json, csv

data = json.load(open('plants_count.json'))

# write the list of dictionaries to a csv file
with open('plants_count.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['name', 'count'])
    for plant in data:
        writer.writerow([plant['plant'], plant['count']])