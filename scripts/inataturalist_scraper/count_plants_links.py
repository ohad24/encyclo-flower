import csv


# read plants_links.csv, only two columns: plant_name, link
# read each row, and add the link to the list

with open('plants_links.csv', 'r') as f:
    reader = csv.reader(f)
    plants_links = list(reader)
    # print(plants_links[0], plants_links[1])
    c = {}
    for row in plants_links:
        if row[0] in c:
            c[row[0]] += 1
        else:
            c[row[0]] = 1
    # sort the dictionary by value, descending
    sorted_c = sorted(c.items(), key=lambda x: x[1], reverse=True)
    # write the list of dictionaries to a csv file
    with open('plants_count2.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'count'])
        for plant in sorted_c:
            writer.writerow([plant[0], plant[1]])
    quit()


    # sort the list by the count of links
    # write the list of links to a csv file