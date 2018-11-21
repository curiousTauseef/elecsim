import pandas as pd

import elecsim.src.scenario.scenario_data as scenario
from elecsim.src.data_manipulation.data_modifications.cost_estimations import ExtrapolateInterpolate
# from elecsim.src.data_manipulation.data_modifications.value_estimations import closest_row
from elecsim.src.plants.plant_costs.estimate_costs.predict_modern_costs import PredictPlantStatistics

from elecsim.src.plants.plant_type.plant_registry import plant_type_to_fuel, plant_registry

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 500)


class LcoeToParameters:
    hist_costs = scenario.power_plant_historical_costs

    def __init__(self, technology, year):
        """
        Class which takes a technology and estimates detailed costing information
        :param technology: type of technology for costing information to be estimated
        """
        self.technology = technology
        self.year = year

        hist_costs = self.hist_costs[self.hist_costs.Technology == technology].dropna()
        print(hist_costs)
        # Uses linear interpolation and extrapolation of historical dataset to predict unknown LCOE costs of a power plant
        self.lcoe = ExtrapolateInterpolate(hist_costs.Year, hist_costs.lcoe)(year)

    def lcoe_to_parameters(self, plant_size):
        CLOSEST_YEAR_TO_HISTORICAL_DATA = 2018

        pp_cost = scenario.power_plant_costs
        pp_cost = pp_cost[pp_cost['Type'] == self.technology]

        if(self.year>2017)
            plant_stats = PredictPlantStatistics(self.technology, plant_size, CLOSEST_YEAR_TO_HISTORICAL_DATA)()

        plant = plant_registry(plant_type_to_fuel(self.technology))(**plant_stats, name="Test", type=self.technology, capacity_mw=plant_size, construction_year = self.year, fuel=self.technology)


        # print(plant.construction_yearly_spend())
        # print(plant.pre_dev_yearly_spend())
        # print(plant.insurance_cost())
        # print(plant.variable_o_and_m_cost())
        # print(plant.fixed_o_and_m_cost())
        # electricity_gen = plant.electricity_generated()
        # print(electricity_gen)
        # print(plant.fuel_costs(electricity_gen))

        print("capex")
        print(plant.capex())
        print("opex")
        print(plant.opex())
        electricity_gen = plant.electricity_generated()
        print("elec gen")
        print(electricity_gen)
        print(sum(electricity_gen))
        print("fuel costs")
        print(plant.fuel_costs(electricity_gen))


        print("total costs")
        print(self.lcoe * sum(electricity_gen))
        print("Lcoe")
        print(self.lcoe)

        print("Plant Object")
        print(plant.__repr__())

LcoeToParameters('CCGT', 2000).lcoe_to_parameters(1200)
