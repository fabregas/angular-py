
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

    s = "test" * 3
    assert s == "testtesttest"
    ss = "new"
    res = 4*ss+"NEW"
    cnt = res.count("new")
    assert cnt == 4
    assert res == "newnewnewnewNEW"

    s = "Python"
    assert s[0] == 'P'
    assert s[-1] == 'n'
    assert s[-2] == 'o'
    assert s[6-12] == 'P'
    assert s[0:2] == 'Py'
    assert s[2:5] == 'tho'
    assert s[:2] + s[2:] == 'Python'
    assert s[:4] + s[4:] == 'Python'
    assert s[-2:] == 'on'
    assert s[4:42] == 'on'
    assert s[42:] == ''
    assert 'J' + s[1:] == 'Jython'

    s = 'supercalifragilisticexpialidocious'
    assert len(s) == 34

    #lists
    squares = [1, 4, 9, 16, 25]
    assert squares[0] == 1
    assert squares[-1] == 25
    assert squares[1:3] == [4, 9]
    assert squares[-3:] == [9, 16, 25]
    assert squares[:] == [1, 4, 9, 16, 25]
    assert squares + [36, 49, 64, 81] == [1, 4, 9, 16, 25, 36, 49, 64, 81]

    cubes = [1, 8, 27, 65, 125]
    #######FIXME
    #######cubes[3] = 64
    #######assert cubes == [1, 8, 27, 64, 125]
    cubes.append(33)
    assert cubes == [1, 8, 27, 65, 125, 33]
    assert len(cubes) == 6

    a = ['a', 'b', 'c']
    n = [1, 2, 3]
    x = [a, n]
    assert x == [['a', 'b', 'c'], [1, 2, 3]]
    assert x[0][1] == 'b'

test()
