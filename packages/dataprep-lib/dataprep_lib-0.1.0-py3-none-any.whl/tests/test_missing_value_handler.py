import pandas as pd
import numpy as np
from dataprep_lib.missing_value_handler import MissingValueHandler

def test_missing_value_handler_mean():
    data = pd.DataFrame({
        'A': [1, 2, np.nan, 4, 5],
        'B': [5, 6, 7, np.nan, 9]
    })
    handler = MissingValueHandler(strategy='mean')
    transformed_data = handler.fit_transform(data)
    
    expected_data = pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': [5, 6, 7, 7, 9]
    })
    pd.testing.assert_frame_equal(transformed_data, expected_data)

def test_missing_value_handler_median():
    data = pd.DataFrame({
        'A': [1, 2, np.nan, 4, 5],
        'B': [5, 6, 7, np.nan, 9]
    })
    handler = MissingValueHandler(strategy='median')
    transformed_data = handler.fit_transform(data)
    
    expected_data = pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': [5, 6, 7, 7, 9]
    })
    pd.testing.assert_frame_equal(transformed_data, expected_data)

def test_missing_value_handler_constant():
    data = pd.DataFrame({
        'A': [1, 2, np.nan, 4, 5],
        'B': [5, 6, 7, np.nan, 9]
    })
    handler = MissingValueHandler(strategy='constant', fill_value=0)
    transformed_data = handler.fit_transform(data)
    
    expected_data = pd.DataFrame({
        'A': [1, 2, 0, 4, 5],
        'B': [5, 6, 7, 0, 9]
    })
    pd.testing.assert_frame_equal(transformed_data, expected_data)

def test_missing_value_handler_delete():
    data = pd.DataFrame({
        'A': [1, 2, np.nan, 4, 5],
        'B': [5, 6, 7, np.nan, 9]
    })
    handler = MissingValueHandler(strategy='delete')
    transformed_data = handler.fit_transform(data)
    
    expected_data = pd.DataFrame({
        'A': [1, 2, 5],
        'B': [5, 6, 9]
    })
    pd.testing.assert_frame_equal(transformed_data.reset_index(drop=True), expected_data)
