import pandas as pd
from dataprep_lib.categorical_encoder import CategoricalEncoder

def test_onehot_encoder():
    data = pd.DataFrame({
        'A': ['cat', 'dog', 'cat', 'bird']
    })
    encoder = CategoricalEncoder(method='onehot')
    transformed_data = encoder.fit_transform(data)
    
    expected_data = pd.DataFrame({
        'A_bird': [0.0, 0.0, 0.0, 1.0],
        'A_cat': [1.0, 0.0, 1.0, 0.0],
        'A_dog': [0.0, 1.0, 0.0, 0.0]
    })
    
    pd.testing.assert_frame_equal(transformed_data, expected_data)

def test_label_encoder():
    data = pd.DataFrame({
        'A': ['cat', 'dog', 'cat', 'bird']
    })
    encoder = CategoricalEncoder(method='label')
    transformed_data = encoder.fit_transform(data)
    
    expected_data = pd.DataFrame({
        'A': [1, 2, 1, 0]
    })
    
    pd.testing.assert_frame_equal(transformed_data, expected_data)

# Run the test
if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
