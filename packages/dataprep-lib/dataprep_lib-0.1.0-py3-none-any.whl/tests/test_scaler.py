import pandas as pd
from dataprep_lib.scaler import Scaler

def test_standard_scaler():
    data = pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': [10, 20, 30, 40, 50]
    })
    scaler = Scaler(method='standard')
    transformed_data = scaler.fit_transform(data)
    
    expected_data = pd.DataFrame({
        'A': (data['A'] - data['A'].mean()) / data['A'].std(),
        'B': (data['B'] - data['B'].mean()) / data['B'].std()
    })
    
    pd.testing.assert_frame_equal(transformed_data, expected_data)

def test_minmax_scaler():
    data = pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': [10, 20, 30, 40, 50]
    })
    scaler = Scaler(method='minmax')
    transformed_data = scaler.fit_transform(data)
    
    expected_data = (data - data.min()) / (data.max() - data.min())
    
    pd.testing.assert_frame_equal(transformed_data, expected_data)

# Run the test
if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
