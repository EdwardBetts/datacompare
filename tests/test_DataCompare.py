import sys
sys.path.append("C:/Users/Josh.Josh-PC/Documents/Beginning Software Engineering/MyProjectDataCompare")
import DataCompare as dc
import imp
imp.reload(dc)

import unittest
import pandas as pd

class TestMyFunctions(unittest.TestCase):
    def test_load_normal(self):
        testdc = dc.DataComp(cnxn_path = "test_cnxn.txt",left_cnxn_name = "GDELT",left_script_path = "test_normal.sql",datetofrom=('2015-09-29','2015-09-30'))
        self.assertEqual(testdc.left_data.shape,(1636, 21),"Normal Test failed")
    def test_load_norows(self):
        with self.assertRaises(AssertionError):
            dc.DataComp("test_cnxn.txt","GDELT","test_load_norows.sql",('2015-09-29','2015-09-30'))
    def test_load_nocols(self):
        with self.assertRaises(AssertionError):
            dc.DataComp("test_cnxn.txt","GDELT","test_load_nocols.sql",('2015-09-29','2015-09-30'))
    ## Using read for a file that may or may not have a UTF-8 BOM can cause issues, so need to test both file types
    def test_load_from_utf8_bom(self):
        testdc = dc.DataComp(cnxn_path = "test_cnxn.txt",left_cnxn_name = "GDELT",left_script_path = "test_load_utf8.sql",datetofrom=('2015-09-29','2015-09-30'))
        self.assertTrue(testdc.left_data.shape[0]>0)
    def test_compare_equal(self):
        testdc = dc.DataComp(cnxn_path = "test_cnxn.txt",left_cnxn_name = "GDELT",left_script_path = "test_normal.sql",datetofrom=('2015-09-29','2015-09-30'))
        testdc.add_right_data("GDELT","test_normal.sql")
        testdc_dict = testdc.compare_data()
        self.assertTrue((testdc_dict["left_not_right_data"].shape[0] == 0) and (testdc_dict["right_not_left_data"].shape[0] == 0)\
            and (testdc_dict["diff_values"] is None),"Same result set comparison failed")
    def test_load_pkduplicate(self):
        with self.assertRaises(AssertionError):
            testdc = dc.DataComp("test_cnxn.txt","GDELT","test_load_pkduplicate.sql",('2015-09-29','2015-09-30'))
            testdc.add_right_data("GDELT","test_normal.sql")
            testdc.compare_data()
    def test_compare_nosharedcol(self):
        with self.assertRaises(AssertionError):
            testdc = dc.DataComp("test_cnxn.txt","GDELT","test_compare_left_noshared.sql",('2015-09-29','2015-09-30'))
            mydf = pd.DataFrame({"a":[1,2],"b":["a","b"],"NumArticles":[1,100]})
            testdc.add_right_data(right_cnxn_name = None,right_script_path = None,source = "DataFrame",DataFrame = mydf)
            testdc.compare_data()
    def test_compare_diffrows(self):
        testdc = dc.DataComp(cnxn_path = "test_cnxn.txt",left_cnxn_name = "GDELT",left_script_path = "test_compare_diffrow_left.sql",datetofrom=('2015-09-29','2015-09-30'))
        testdc.add_right_data("GDELT","test_compare_diffrow_right.sql")
        testdc_dict = testdc.compare_data()
        self.assertTrue((testdc_dict["left_not_right_data"].shape[0] > 0) and (testdc_dict["right_not_left_data"].shape[0] > 0)\
            and (testdc_dict["diff_values"] is None),"Differing rows test failed")
    def test_compare_rowsame_diffval(self):
        pass
    
   
if __name__ == '__main__':
    unittest.main(exit=False)