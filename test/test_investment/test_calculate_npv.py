import logging
logging.getLogger(__name__)
from src.plants.plant_costs.estimate_costs.estimate_costs import create_power_plant

from src.role.investment.calculate_npv import CalculateNPV
import pytest
"""
File name: test_calculate_npv
Date created: 24/12/2018
Feature: #Enter feature description here
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

logging.basicConfig(level=logging.DEBUG)


class TestCalculate_npv:

    @pytest.fixture(scope='function')
    def calculate_latest_NPV(self):
        DISCOUNT_RATE = 0.06
        START_YEAR = 2018
        EXPECTED_PRICE = 70
        npv_calculations = CalculateNPV(DISCOUNT_RATE, START_YEAR, EXPECTED_PRICE)
        return npv_calculations


    @pytest.mark.parametrize("year, plant_type, capacity, expected_output",
                             [
                                 (2018, "CCGT", 1200, 82.55488),
                             ]
                             )
    def test_calculate_expected_cash_flow(self, calculate_latest_NPV, year, plant_type, capacity, expected_output):
        plant = create_power_plant("Test", year, plant_type, capacity)
        assert calculate_latest_NPV.calculate_expected_cash_flow(plant) == pytest.approx([-5280000, -5280000, -1440000, -240000000, -240000000, -135100000, 210756383.1, 206027198.2, 201298013.4, 196602132.7, 191872947.9, 187143763.1, 182447882.4, 177718697.6, 150242799.9, 122766902.2, 95291004.56, 67815106.88, 40339209.2, 12863311.52, -14612586.16, -42088483.84, -69564381.52, -97040279.2, -124516176.9, -151992074.6, -179467972.2, -206943869.9, -234419767.6, -261895665.3, -289371563])


    @pytest.mark.parametrize("year, plant_type, capacity, expected_output",
                             [
                                 (2018, "CCGT", 1200, 247876046.06),
                                 (2018, "PV", 16, 178354.70),
                             ]
                             )
    def test_calculate_expected_npv(self, calculate_latest_NPV, year, plant_type, capacity, expected_output):
        plant = create_power_plant("Test", year, plant_type, capacity)
        assert calculate_latest_NPV.calculate_npv(plant_type, capacity) == pytest.approx(expected_output)

    def test_maximum_npv(self, calculate_latest_NPV):
        calculate_latest_NPV.highest_npv()
        assert 1==1