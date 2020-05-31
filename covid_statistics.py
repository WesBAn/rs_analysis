import datetime
import dataclasses
import json
import pprint
import typing

import requests


COVID_URL_API = 'https://api.covid19api.com'
TOTAL_COUNTRY_METHOD = 'total/country'


@dataclasses.dataclass(frozen=True)
class CountryData:
    country: str
    month_num: int
    data: typing.List[typing.Tuple[int, int]]


def statistics_by_country_request(country: str) -> typing.List[typing.Optional[typing.Dict]]:
    url = '/'.join([COVID_URL_API, TOTAL_COUNTRY_METHOD, country])
    r = requests.get(url)
    result = json.loads(r.text)
    return result


def get_country_month_data_for_analysis(
        country: str,
        month: int
) -> CountryData:
    response_data = statistics_by_country_request(country)
    month_data = filter(
        lambda elem: datetime.datetime.fromisoformat(
            elem['Date'][:-1]
        ).month == month,
        response_data
    )
    data = [
        (
            datetime.datetime.fromisoformat(data['Date'][:-1]).day,
            data['Confirmed']
        )
        for data in month_data
    ]
    return CountryData(country=country, month_num=month, data=data)


if __name__ == '__main__':
    pprint.pprint(get_country_month_data_for_analysis('russia', 4))
