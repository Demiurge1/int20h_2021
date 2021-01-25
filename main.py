from __future__ import division
import csv
import sys

DEFAULT_INPUT_FILENAME = 'data_analytics.csv'

APPLE_COMMISSION = 0.3
WEEK_COST = 9.99
DEV_PROCEEDS = WEEK_COST * (1 - APPLE_COMMISSION)


def read_data_from_file(filename):
    res = {}
    with open(filename) as f:
        r = csv.DictReader(f)
        for row in r:
            subscriber_id = row['Subscriber ID']
            if subscriber_id not in res:
                res[subscriber_id] = 0
            res[subscriber_id] += 1

    return res


def calculate_conversions_and_ltv(user_weeks):

    people_on_week = [0 for _ in range(6)]
    people_on_week[0] = len(user_weeks.keys())
    for user_id, number_of_weeks in user_weeks.items():
        for i in range(1, 6):
            people_on_week[i] += int(number_of_weeks > i)

    conversions = [people_on_week[i + 1] / people_on_week[i] for i in range(5)]

    results_arr = [conversions[0] * DEV_PROCEEDS]
    for i in range(1, 5):
        results_arr.append(results_arr[i - 1] * conversions[i])
    ltv = sum(results_arr)
    return ltv, conversions, people_on_week


def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = DEFAULT_INPUT_FILENAME

    user_weeks = read_data_from_file(filename)
    ltv, conversions, people_on_week = calculate_conversions_and_ltv(user_weeks)

    print('Trial week: {} people'.format(people_on_week[0]))
    for i in range(1, 6):
        print('{} week: {} people'.format(i, people_on_week[i]))
    print('-' * 50)

    print('Conversion from trial week to 1 week: {}%'.format(conversions[0] * 100))
    for i in range(1, 5):
        print('Conversion from {} week to {} week: {}%'.format(i, i + 1, conversions[i] * 100))
    print('-' * 50)
    print('LTV: {}'.format(ltv))


if __name__ == '__main__':
    main()
