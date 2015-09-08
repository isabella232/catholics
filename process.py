#!/usr/bin/env python

import agate
import dataset
import proof

from collections import OrderedDict, defaultdict
from decimal import Decimal

text_type = agate.TextType()
number_type = agate.NumberType()

COLUMNS = (
    ('diocese', text_type),
    ('state', text_type),
    ('diocesan_priests', number_type),
    ('religious_priests', number_type),
    ('parishes', number_type),
    ('high_schools_diocesan', number_type),
    ('students_in_diocesan_high_schools', number_type),
    ('high_schools_private', number_type),
    ('students_in_high_schools_private', number_type),
    ('elementary_schools_parish', number_type),
    ('students_in_elementary_schools_parish', number_type),
    ('private_schools_parish', number_type),
    ('students_in_private_schools_parish', number_type),
    ('catholics', number_type),
)

NORTHEAST_STATES = ('CT', 'MA', 'ME', 'NH', 'NJ', 'NY', 'PA', 'RI', 'VT',)
MIDWEST_STATES = ('IN', 'IL', 'MI', 'OH', 'WI', 'IA', 'KS', 'MN', 'MS', 'NE', 'ND', 'SD',)
REGIONS = (('northeast', NORTHEAST_STATES), ('midwest', MIDWEST_STATES))

# 1965 pop: https://www.census.gov/prod/1/pop/p25-420.pdf
# 2014 pop: http://www.census.gov/popclock/
NORTHEAST_POP = {
    '1965': Decimal(47428000),
    '2014': Decimal(56152333),
}
MIDWEST_POP = {
    '1965': Decimal(54185000),
    '2014': Decimal(67745108),
}

def summarize():
    table_1965_raw = agate.Table.from_csv('processed-data/1965.csv', COLUMNS)
    table_2015_raw = agate.Table.from_csv('processed-data/2015.csv', COLUMNS)

    for region, states in REGIONS:
        if region == 'midwest':
            pop = MIDWEST_POP
        else:
            pop = NORTHEAST_POP

        table_1965 = table_1965_raw.where(lambda row: row['state'] in states)
        table_2015 = table_2015_raw.where(lambda row: row['state'] in states)

        output = []

        for col_name, col_type in COLUMNS[2:]:
            row = OrderedDict()
            row['var'] = col_name
            row['1965'] = table_1965.columns[col_name].aggregate(agate.Sum())
            row['1965_per_capita'] = row['1965'] / pop['1965']
            row['2015'] = table_2015.columns[col_name].aggregate(agate.Sum())
            row['2015_per_capita'] = row['2015'] / pop['2014']
            row['absolute_percent_change'] = (row['2015'] - row['1965']) / row['1965']
            row['per_capita_percent_change'] = (row['2015_per_capita'] - row['1965_per_capita']) / row['1965_per_capita']

            output.append(row)

        dataset.freeze(output, format='csv', filename='processed-data/{0}-sums.csv'.format(region))

if __name__ == '__main__':
    summarize()
