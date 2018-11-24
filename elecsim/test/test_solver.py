'''
File name: test_solver
Date created: 24/11/2018
Feature: #Enter feature description here
'''
from unittest import TestCase
from elecsim.src.plants.delete_me import Solver

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


class TestSolver(TestCase):
    def test_adder(self):
        s = Solver()
        self.assertEquals(s.adder(1, 1), 2)