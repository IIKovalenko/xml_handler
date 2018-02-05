#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_stage1.py
"""

import unittest
from xml_handler import xml_handler


class TestStage1(unittest.TestCase):

    def test_make_random_string(self):
        self.assertIsInstance(xml_handler.make_random_string(10), str)
        self.assertEqual(len(xml_handler.make_random_string(10)), 10)

    def test_make_xml(self):
        self.assertIsInstance(xml_handler.make_xml(''), str)

    def test_make_zip(self):
        self.assertIsNone(xml_handler.make_zip('test.zip', [], 1))

    def test_stage1(self):
        self.assertIsNone(xml_handler.stage1())


if __name__ == '__main__':
    unittest.main()
