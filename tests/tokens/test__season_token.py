from oronyx.tokens import Season, AnnualDate


def test_season():
    assert Season("spring").met_begin == AnnualDate("3/1")
    assert Season("spring").season == "spring"

    assert Season("summer").met_begin == AnnualDate("6/1")
    assert Season("summer").season == "summer"

    assert Season("autumn").met_begin == AnnualDate("9/1")
    assert Season("fall").season == "autumn"

    assert Season("winter").met_begin == AnnualDate("12/1")
    assert Season("winter").season == "winter"