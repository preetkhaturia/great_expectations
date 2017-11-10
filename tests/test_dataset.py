import json
import hashlib
import datetime
import numpy as np
import pandas as pd

import great_expectations as ge

import unittest

class TestDataset(unittest.TestCase):

    def test_dataset(self):

        D = ge.dataset.PandasDataSet({
            'x' : [1,2,4],
            'y' : [1,2,5],
            'z' : ['hello', 'jello', 'mello'],
        })

        # print D._expectations_config.keys()
        # print json.dumps(D._expectations_config, indent=2)

        self.assertEqual(
            D._expectations_config,
            {
                "dataset_name" : None,
                "expectations" : [{
                    "expectation_type" : "expect_column_to_exist",
                    "kwargs" : { "column" : "x" }
                },{
                    "expectation_type" : "expect_column_to_exist",
                    "kwargs" : { "column" : "y" }
                },{
                    "expectation_type" : "expect_column_to_exist",
                    "kwargs" : { "column" : "z" }
                }]
            }
        )

        self.assertEqual(
            D.get_expectations_config(),
            {
                "dataset_name" : None,
                "expectations" : [{
                    "expectation_type" : "expect_column_to_exist",
                    "kwargs" : { "column" : "x" }
                },{
                    "expectation_type" : "expect_column_to_exist",
                    "kwargs" : { "column" : "y" }
                },{
                    "expectation_type" : "expect_column_to_exist",
                    "kwargs" : { "column" : "z" }
                }]
            }
        )


        #!!! Add tests for expectation and column_expectation
        #!!! Add tests for save_expectation

    def test_set_default_expectation_argument(self):
        df = ge.dataset.PandasDataSet({
            'x' : [1,2,4],
            'y' : [1,2,5],
            'z' : ['hello', 'jello', 'mello'],
        })

        self.assertEqual(
            df.get_default_expectation_arguments(),
            {
                "include_config" : False,
                "catch_exceptions" : False,
                "output_format" : 'BASIC',
            }
        )

        df.set_default_expectation_argument("output_format", "SUMMARY")

        self.assertEqual(
            df.get_default_expectation_arguments(),
            {
                "include_config" : False,
                "catch_exceptions" : False,
                "output_format" : 'SUMMARY',
            }
        )

    def test_format_column_map_output(self):
        df = ge.dataset.PandasDataSet({
            "x" : list("abcdefghijklmnopqrstuvwxyz")
        })

        success = True
        element_count = 20
        nonnull_values = pd.Series(range(15))
        nonnull_count = 15
        boolean_mapped_success_values = pd.Series([True for i in range(15)])
        success_count = 15
        exception_list = []
        exception_index_list = []

        self.assertEqual(
            df.format_column_map_output(
                "BOOLEAN_ONLY",
                success,
                element_count,
                nonnull_values, nonnull_count,
                boolean_mapped_success_values, success_count,
                exception_list, exception_index_list
            ),
            True
        )

        self.assertEqual(
            df.format_column_map_output(
                "BASIC",
                success,
                element_count,
                nonnull_values, nonnull_count,
                boolean_mapped_success_values, success_count,
                exception_list, exception_index_list
            ),
            {
                'success': True,
                'summary_obj': {
                    'exception_percent': 0.0,
                    'partial_exception_list': [],
                    'exception_percent_nonmissing': 0.0,
                    'exception_count': 0
                }
            }
        )

        self.assertEqual(
            df.format_column_map_output(
                "COMPLETE",
                success,
                element_count,
                nonnull_values, nonnull_count,
                boolean_mapped_success_values, success_count,
                exception_list, exception_index_list
            ),
            {
                'success': True,
                'exception_list': [],
                'exception_index_list': [],
            }
        )

        self.assertEqual(
            df.format_column_map_output(
                "SUMMARY",
                success,
                element_count,
                nonnull_values, nonnull_count,
                boolean_mapped_success_values, success_count,
                exception_list, exception_index_list
            ),
            {
                'success': True,
                'summary_obj': {
                    'element_count': 20,
                    'exception_count': 0,
                    'exception_percent': 0.0,
                    'exception_percent_nonmissing': 0.0,
                    'missing_count': 5,
                    'missing_percent': 0.25,
                    'partial_exception_counts': {},
                    'partial_exception_index_list': [],
                    'partial_exception_list': []
                }
            }
        )



    def test_calc_map_expectation_success(self):
        df = ge.dataset.PandasDataSet({
            "x" : list("abcdefghijklmnopqrstuvwxyz")
        })
        self.assertEqual(
            df.calc_map_expectation_success(
                success_count=10,
                nonnull_count=10,
                exception_count=0,
                mostly=None
            ),
            (True, 1.0)
        )

        self.assertEqual(
            df.calc_map_expectation_success(
                success_count=90,
                nonnull_count=100,
                exception_count=0,
                mostly=.9
            ),
            (True, .9)
        )

        self.assertEqual(
            df.calc_map_expectation_success(
                success_count=90,
                nonnull_count=100,
                exception_count=0,
                mostly=.8
            ),
            (True, .9)
        )

        self.assertEqual(
            df.calc_map_expectation_success(
                success_count=80,
                nonnull_count=100,
                exception_count=0,
                mostly=.9
            ),
            (False, .8)
        )

        self.assertEqual(
            df.calc_map_expectation_success(
                success_count=0,
                nonnull_count=0,
                exception_count=0,
                mostly=None
            ),
            (True, None)
        )

        self.assertEqual(
            df.calc_map_expectation_success(
                success_count=0,
                nonnull_count=100,
                exception_count=100,
                mostly=None
            ),
            (False, 0.0)
        )


if __name__ == "__main__":
    unittest.main()
