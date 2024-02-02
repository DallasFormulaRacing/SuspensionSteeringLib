def test_WR_F(test_wheel_load_calculations):
    result = test_wheel_load_calculations.calculate_WR_F()
    assert (result >= 243.10 and result <= 243.5)


def test_WR_R(test_wheel_load_calculations):
    result = test_wheel_load_calculations.calculate_WR_R()
    assert (result >= 243.10 and result <= 243.5)


def test_q(test_wheel_load_calculations):
    result = test_wheel_load_calculations.calculate_consts()
    assert (result >= 243.10 and result <= 243.5)


def test_K_H(test_wheel_load_calculations):
    result = test_wheel_load_calculations.calculate_consts()
    assert (result >= 243.10 and result <= 243.5)


def test_K_R(test_wheel_load_calculations):
    result = test_wheel_load_calculations.calculate_consts()
    assert (result >= 243.10 and result <= 243.5)
