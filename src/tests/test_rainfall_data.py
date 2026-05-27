from main import monthly_rain_data


def test_monthly_rain_data_returns_matching_readings():
    rain_data = [
        (123, "20200101:0900", 10.5),
        (123, "20200115:1200", 20.0),
        (123, "20200201:0900", 30.0),
        (999, "20200101:0900", 40.0)
    ]

    result = monthly_rain_data(
        123,
        1,
        rain_data,
        2020
    )

    assert result == [10.5, 20.0]


def test_monthly_rain_data_returns_empty_list_when_no_matches():
    rain_data = [
        (123, "20200101:0900", 10.5),
        (123, "20200201:0900", 20.0)
    ]

    result = monthly_rain_data(
        123,
        3,
        rain_data,
        2020
    )

    assert result == []


def test_monthly_rain_data_filters_by_year():
    rain_data = [
        (123, "20200101:0900", 10.0),
        (123, "20210101:0900", 99.0)
    ]

    result = monthly_rain_data(
        123,
        1,
        rain_data,
        2020
    )

    assert result == [10.0]


def test_monthly_rain_data_filters_by_station():
    rain_data = [
        (123, "20200101:0900", 10.0),
        (999, "20200101:0900", 50.0)
    ]

    result = monthly_rain_data(
        123,
        1,
        rain_data,
        2020
    )

    assert result == [10.0]