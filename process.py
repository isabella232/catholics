#!/usr/bin/env python

import agate
import proof

text_type = agate.TextType()
number_type = agate.NumberType()

COLUMNS = (
    ('diocese', text_type),
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

def summarize():
    table_1965 = agate.Table.from_csv('processed-data/1965.csv', COLUMNS)
    table_2015 = agate.Table.from_csv('processed-data/2015.csv', COLUMNS)


if __name__ == '__main__':
    summarize()
