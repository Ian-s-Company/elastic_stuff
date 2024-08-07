# Since I don't have an instance of Elastic or Ansible it is not really possible to test the code so this is just a placeholder for an actual test.


import pytest

@pytest.mark.parametrize(
    "test_input,expected",
    [("3+5", 8), ("2+4", 6), pytest.param("6*9", 42, marks=pytest.mark.xfail)],
)
def test_eval(test_input, expected):
    assert eval(test_input) == expected
