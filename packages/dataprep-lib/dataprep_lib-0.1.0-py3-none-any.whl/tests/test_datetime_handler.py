import pandas as pd
from dataprep_lib.datetime_handler import DateTimeHandler

def test_to_datetime():
    data = pd.DataFrame({
        'date': ['2020-01-01', '2021-02-02', '2022-03-03']
    })
    handler = DateTimeHandler()
    transformed_data = handler.to_datetime(data, columns=['date'])
    
    expected_data = pd.DataFrame({
        'date': pd.to_datetime(['2020-01-01', '2021-02-02', '2022-03-03'])
    })
    
    pd.testing.assert_frame_equal(transformed_data, expected_data)

def test_extract_datetime_features():
    data = pd.DataFrame({
        'date': pd.to_datetime(['2020-01-01 01:01:01', '2021-02-02 02:02:02', '2022-03-03 03:03:03'])
    })
    handler = DateTimeHandler()
    transformed_data = handler.extract_datetime_features(data, columns=['date'])
    
    expected_data = pd.DataFrame({
        'date': pd.to_datetime(['2020-01-01 01:01:01', '2021-02-02 02:02:02', '2022-03-03 03:03:03']),
        'date_year': [2020, 2021, 2022],
        'date_month': [1, 2, 3],
        'date_day': [1, 2, 3],
        'date_hour': [1, 2, 3],
        'date_minute': [1, 2, 3],
        'date_second': [1, 2, 3]
    })
    
    pd.testing.assert_frame_equal(transformed_data, expected_data)

# Run the test
if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
