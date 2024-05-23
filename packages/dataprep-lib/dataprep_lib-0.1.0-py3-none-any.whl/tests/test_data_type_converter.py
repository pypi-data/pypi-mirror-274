import pandas as pd
from dataprep_lib.data_type_converter import DataTypeConverter

def test_to_numeric():
    data = pd.DataFrame({
        'A': ['1', '2', '3', 'four'],
        'B': ['10', '20', '30', '40']
    })
    converter = DataTypeConverter()
    transformed_data = converter.to_numeric(data)
    
    expected_data = pd.DataFrame({
        'A': [1, 2, 3, None],
        'B': [10, 20, 30, 40]
    }, dtype='float64')
    
    pd.testing.assert_frame_equal(transformed_data, expected_data)

def test_to_categorical():
    data = pd.DataFrame({
        'A': [1, 2, 3, 4],
        'B': ['x', 'y', 'z', 'w']
    })
    converter = DataTypeConverter()
    transformed_data = converter.to_categorical(data, columns=['B'])
    
    expected_data = pd.DataFrame({
        'A': [1, 2, 3, 4],
        'B': pd.Categorical(['x', 'y', 'z', 'w'])
    })
    
    pd.testing.assert_frame_equal(transformed_data, expected_data)

# Run the test
if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
