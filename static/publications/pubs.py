import os, re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from loguru import logger

logger.info('Import OK')

input_path = 'static/publications/publications.xlsx'
output_folder = 'content/research/publications'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Read in csv
pubs = pd.read_excel(input_path)

# Format table
pubs.sort_values('Publication Year', inplace=True)
pubs['weight'] = [x+1 for x in reversed(range(len(pubs)))]

for (title, authors, first, journal, year, doi, preprint, data, code, communication, weight) in pubs.values:
    title = title.replace('"', "'")
        
    # template to fill
    template = [
        '---',
        f'title: "{title.capitalize()}"',
        '',
        f'location: "{journal}"',
        '',
        f'authors: "{authors}"',
        '',
        f'year: "{year}"',
        '',
        f'doi: https://doi.org/{doi}',
        '',
        f'weight: {weight}',
        '',
        f'color: "#fff"',
        '',
        'draft: false',
        'buttons:',
    ]

    for btype, button in zip(['preprint', 'published', 'data', 'code', 'comms'], [preprint, doi, data, code, communication]):
        url = None
        if type(button) == str:
            url = button
            button_types = {
                'preprint': [
                    '  - btype: Preprint',
                    '    icon: preprint',
                    '    newTab: true',
                    f'    url: "{url}"',
                    ],
                'published': [
                    '  - btype: Full text',
                    '    icon: book # optional: use an icon from icons.yaml',
                    '    newTab: true',
                    f'    url: "https://doi.org/{url}"',
                    ],
                'data': [
                    '  - btype: Data',
                    '    icon: data',
                    '    newTab: true',
                    f'    url: "{url}"',
                    ],
                'code': [
                    '  - btype: Code',
                    '    icon: code',
                    '    newTab: true',
                    f'    url: "{url}"',
                    ],
                'comms': [
                    '  - btype: Communication',
                    '    icon: comms',
                    '    newTab: true',
                    f'    url: "{url}"',
                    ],
            }
            template.extend(button_types[btype])
            
    template.extend(['---'])
            
    with open(f'{output_folder}/{year}-{first.split(" ")[0]}.md', mode='wt', encoding='utf-8') as myfile:
        myfile.write('\n'.join(template))

# Generate markdown files

