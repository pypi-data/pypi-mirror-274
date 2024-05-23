import pandas as pd
import numpy as np
from dataprep_lib.outlier_handler import OutlierHandler

def test_outlier_handler_iqr():
    data = pd.DataFrame({
        'A': [1, 2, 3, 4, 100],
        'B': [10, 20, 30, 40, 500]
    })
    handler = OutlierHandler(method='iqr', threshold=1.5)
    transformed_data = handler.fit_transform(data)
    
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    expected_data = data.clip(lower=lower_bound, upper=upper_bound, axis=1)
    
    pd.testing.assert_frame_equal(transformed_data, expected_data)

# Run the test
if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
