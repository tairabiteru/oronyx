from oronyx.tokens import AnnualDate


def test_annualdate():
    assert AnnualDate("7/4").day == 4
    assert AnnualDate("7/4").month == 7
    assert AnnualDate("7/4").month_name == "July"

    assert AnnualDate("03/17").day == 17
    assert AnnualDate("03/17").month == 3
    assert AnnualDate("03/17").month_name == "March"

    assert AnnualDate("02/02").day == 2
    assert AnnualDate("02/02").month == 2
    assert AnnualDate("02/02").month_name == "February"