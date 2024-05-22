# import unittest
# import pandas as pd
# from unittest.mock import patch, MagicMock
# from tools import FairnessAnalysis
# from metrics import DIR

# def setUp():
#         # Mock dataset
#         data = {
#             'feature1': [1, 0, 1, 0, 1],
#             'feature2': [5, 6, 7, 8, 9],
#             'protected_attribute': ['A', 'B', 'A', 'B', 'A'],
#             'target': [1, 0, 1, 1, 1]
#         }
        
#         test_df = pd.DataFrame(data)
        
        
#         return test_df

# def test_DIR():
#     df = setUp()
    
#     DIRs, RMSDIR = DIR(df, "protected_attribute", "A", "target", 1)
    
    

