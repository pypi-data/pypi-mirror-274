import pandas as pd
from dataprep_lib.feature_engineer import FeatureEngineer

def test_feature_engineer():
    data = pd.DataFrame({
        'A': [1, 2, 3, 4],
        'B': [10, 20, 30, 40]
    })
    new_features = {
        'A+B': lambda row: row['A'] + row['B'],
        'A*B': lambda row: row['A'] * row['B']
    }
    engineer = FeatureEngineer()
    transformed_data = engineer.add_features(data, new_features)
    
    expected_data = pd.DataFrame({
        'A': [1, 2, 3, 4],
        'B': [10, 20, 30, 40],
        'A+B': [11, 22, 33, 44],
        'A*B': [10, 40, 90, 160]
    })
    
    pd.testing.assert_frame_equal(transformed_data, expected_data)

# Run the test
if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
