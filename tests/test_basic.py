
def test():
    assert 2+2 == 4
    assert 50-5*6 == 20
    assert (50-5*6) / 4 == 5.0
    assert 8 / 5 == 1.6

    assert 17 / 3 == 5.666666666666667
    assert 17 // 3 == 5
    assert 17 // (4-1) == 5

    assert 17 % 3 == 2

    assert 5 * 3 + 2 == 17
    assert 3 * 3.75 / 1.5 == 7.5
    assert 7.0 / 2 == 3.5

    assert 5 ** 2 == 25
    assert 2 ** 7 == 128

    width = 20
    height = 5 * 9
    assert width * height == 900

    assert 'spam eggs' == "spam eggs"
    assert 'doesn\'t' == "doesn't"
    assert 'spam eggs' != 'some'
    assert '3' != 3
    assert 'test 1' > 'test 0'
    assert 3+4 >= 2+5
    assert 3 < 2*5
    assert 'some str' <= 'some' + ' str'
    assert 4**3-2 > 32

    print("hello, world =)")

test()
