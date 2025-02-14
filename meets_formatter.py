import os
import re

meets = {}
for fl in os.listdir('.'):
    if fl.endswith('_meets.txt'):
        with open(fl, 'r') as tf:
            content = [l[:-1] for l in tf.readlines()]
        # txt to dict
        data = []
        index_pointer = -1
        for i in range(len(content)):
            item = content[i]
            date_re = re.search(rf'\d+/\d+', item)
            if date_re:
                data.append([])
                index_pointer += 1
            data[index_pointer].append(item)

        # Clean up rows since they can be different
        for line in data:
            if len(line) == 5:
                line.pop(1)
            elif len(line) == 4:
                pass
            else:
                x=1
            x=1
        meets[fl[:9]] = data
for year, meets in meets.items():
    print('')
    print(year)
    for line in meets:
        print(','.join(line))
x=1
