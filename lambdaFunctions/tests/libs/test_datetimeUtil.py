import datetime

from libs.datetimeUtil import checkDate


def testcheckDate():
    tests = [
        {
            "name": "valid date string value",
            "input": "20190401",
            "except": datetime.datetime(2019, 4, 1, 0, 0),
        },
        {"name": "invalid date string value", "input": "20190431", "except": None},
    ]

    for test in tests:
        result = checkDate(test["input"])

        assert result == test["except"]
