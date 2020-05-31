import datetime

import click
import numpy as np

import covid_statistics as co_stat
import plot_utils


def fractal_analysis(country_data):
    month = _get_month_name_from_num(country_data.month_num)
    print(
        f'Country - {country_data.country.capitalize()}; '
        f'Month - {month}\n'
    )

    plot_utils.plot_points(country_data.data)
    plot_utils.plot_piecewise(country_data.data)

    result_points = rs_get_points(country_data.data)
    H = get_herst(result_points)
    print('H = ', H)

    D = 2 - H
    print('D = ', D)
    plot_utils.plot_points(
        result_points, title='Herst dimension', xlabel='T', ylabel='R/S'
    )
    plot_utils.linear_result_plot(result_points)


def rs_get_points(data: np.array):
    n = len(data)
    x = np.log(np.array(range(1, n + 1)))
    rs = np.log(np.array(
        [
            get_rs(data[:i])
            for i in range(3, n + 1)
        ]
    ))
    result = np.array([
        (x[i], rs[i])
        for i in range(len(rs))
    ])
    return result


def get_rs(points: np.array):
    data_x, data_y = plot_utils.get_points(points)

    n = len(points)
    h = np.array(data_y[0] + [
        np.log(data_y[i] / data_y[i-1])
        for i in range(1, n)
    ])
    h_average = np.average(h)

    delta_sum = [
        np.sum(h[:i] - h_average)
        for i in range(1, n + 1)
    ]
    R = np.max(delta_sum) - np.min(delta_sum)
    S = np.sum(np.square(h - h_average)) / n
    return R / S


def get_herst(points: np.array):
    data_x, data_y = plot_utils.get_points(points)
    c1 = np.sum(np.square(data_x))
    c2 = np.sum(data_x)
    g1 = np.sum(data_x * data_y)
    g2 = np.sum(data_y)
    N = len(points)
    return (N*g1 - c2*g2) / (N*c1 - np.square(c2))


def _get_month_name_from_num(month_num: int):
    return datetime.date(1900, month_num, 1).strftime('%B')


@click.command()
@click.option('--country', type=str, default='russia', help='Country')
@click.option('--month', type=int, default=4, help='Month')
def main(country, month):
    data = co_stat.get_country_month_data_for_analysis(country, month)
    fractal_analysis(data)


if __name__ == '__main__':
    main()
