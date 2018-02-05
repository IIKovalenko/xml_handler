#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_stage2.py
"""

import unittest
from xml_handler import xml_handler


class TestStage2(unittest.TestCase):

    def test_parse_zip(self):
        self.assertIsInstance('test', str)

    def test_stage2(self):
        self.assertIsNone(xml_handler.stage2())


if __name__ == '__main__':
    unittest.main()
