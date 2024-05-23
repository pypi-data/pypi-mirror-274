import pandas as pd
from dataprep_lib.text_cleaner import TextCleaner

def test_text_cleaner():
    data = pd.DataFrame({
        'text': ["This is a test sentence.", "Another test sentence with punctuation!"]
    })
    cleaner = TextCleaner()
    transformed_data = cleaner.transform(data)
    
    expected_data = pd.DataFrame({
        'text': ["test sentence", "another test sentence punctuation"]
    })
    
    pd.testing.assert_frame_equal(transformed_data, expected_data)

# Run the test
if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
