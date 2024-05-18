import unittest
import pandas as pd
import sys
sys.path.append("expviz/")
from expviz import *

class TestTableConversion(unittest.TestCase):
    
    def setUp(self):
        self.data = {
            "exp1": {"Score1": 10.1, "Score2": "NaN"},
            "exp2": {"Score1": 30, "Score2": 40}
        }

    def test_dict_to_dataframe(self):
        df = dict_to_dataframe(self.data)
        expected_df = pd.DataFrame(self.data).T
        pd.testing.assert_frame_equal(df, expected_df)
        
    def test_to_latex(self):
        latex_code = to_latex(self.data)
        self.assertIsInstance(latex_code, str)
        self.assertIn('\\begin{table}', latex_code)
        self.assertIn('\\end{table}', latex_code)
        
    def test_to_markdown(self):
        markdown_table = to_markdown(self.data)
        self.assertIsInstance(markdown_table, str)
        self.assertTrue(markdown_table.startswith('|'))
        self.assertTrue(markdown_table.endswith('|'))
        
    def test_show(self):
        # Testing `show` function can be tricky as it doesn't return anything, 
        # it just displays the DataFrame in Jupyter. You might check if 
        # it runs without errors with different inputs.
        try:
            show(self.data)
        except Exception as e:
            self.fail(f"show raised exception {e}")

if __name__ == '__main__':
    unittest.main()
