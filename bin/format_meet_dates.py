import os
import re
import json

etc_dir = 'etc'
directory = os.path.join(etc_dir, 'year_overview')
etc_tmp = os.path.join(etc_dir, 'tmp')

exit()  # Just so I dont overwrite data...

try:
    with open(os.path.join(etc_tmp  , 'meet_dates.json'), 'r') as jf:
        meets = json.load(jf)
except:
    meets = {}

x=1

for fl in os.listdir(directory):
    if not fl.endswith('.txt'):
        continue
    with open(os.path.join(directory, fl), 'r') as f:
        data = [l[:-1] for l in f.readlines()]
    meet_data = []
    row = []
    for line in data:
        newline_re = re.search(r'^\d+/\d+$', line.strip())
        if newline_re:
            if len(row) > 1:
                if len(row) == 5:
                    row.pop(1)
                meet_data.append({
                    'date': row[0],
                    'meet': row[1],
                    'location': row[2],
                })
                row = []
        row.append(line)

    year = fl[:4]
    for item in meet_data:
        date = item['date']
        if year not in meets:
            meets[year] = {}
        if date not in meets[year]:
            item['filename'] = ''
            meets[year][date] = item
        else:
            item['filename'] = meets[year][date].get('filename', '')
            meets[year][date] = item
    for date, item in meets[year].items():
        x=1
        for fl in os.listdir(os.path.join(etc_dir, f"{year}-{int(year)+1}_results")):
            x=1
            if not item['filename']:
                if item['meet'][:5] == fl[:5]:
                    item['filename'] = fl
                    x=1
    x=1
    # meets[fl[:4]] = {v['date']: v for v in meet_data}

meet_keys = list(meets.keys())
meet_keys.sort()
meets = {k: meets[k] for k in meet_keys}

with open(os.path.join(etc_tmp  , 'meet_dates.json'), 'w') as jf:
    jf.write(json.dumps(meets, indent=4))

x=1
