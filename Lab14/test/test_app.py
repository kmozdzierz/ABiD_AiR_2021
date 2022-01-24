from importlib_metadata import collections
from app import *
import pytest
import numpy as np

# def test_hello():
#     got = hello("Aleksandra")
#     want = "Hello Aleksandra"

#     assert got == want

# testdata1 = ["I think today will be a great day"]

# @pytest.mark.parametrize('sample', testdata1)
# def test_extract_sentiment(sample):

#     sentiment = extract_sentiment(sample)

#     assert sentiment > 0

# testdata2 = [
#     ('There is a duck in this text', 'duck', True),
#     ('There is nothing here', 'duck', False)
#     ]

# @pytest.mark.parametrize('sample, word, expected_output', testdata2)
# def test_text_contain_word(sample, word, expected_output):

#     assert text_contain_word(word, sample) == expected_output






frob_test_data = [
    (np.array([4,2,3,4]), np.array([[0, 1, 0], [0, 0, 1], [-4,-3,-2]])),
    (np.array([10,12,3,4,5]), np.array([[0, 1, 0, 0], [0, 0, 1,0], [0, 0, 0, 1], [-5,-4,-3,-12]])),
    (np.array([1,2,3,4,-7,-3]), np.array([[0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0],[0, 0, 0, 0, 1], [3, 7, -4, -3,-2]])),
    ([1,2,3], None)
    ]

@pytest.mark.parametrize('sample_coeffs, matrix', frob_test_data)
def test_Frobenius_mtx(sample_coeffs, matrix):
    
    frob_result = Frobenius_mtx(sample_coeffs)
    
    if isinstance(matrix, np.ndarray):
        assert (matrix == frob_result).all()
    else:
        assert matrix == frob_result