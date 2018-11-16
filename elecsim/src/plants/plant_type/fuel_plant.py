""" fuel_plant.py: Child class of power plant which contains functions for a power plant which consumes fuel.
                    Most notably, the functinos contain the ability to calculate the cost of fuel.
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"

from elecsim.src.plants.power_plant import PowerPlant
from elecsim.src.plants.plant_type.fuel import fuel_registry


class FuelPlant(PowerPlant):

    def __init__(self, name, plant_type, capacity_mw, construction_year, average_load_factor, efficiency, pre_dev_period, construction_period, operating_period, pre_dev_spend_years, construction_spend_years, pre_dev_cost_per_kw, construction_cost_per_kw, infrastructure, fixed_o_and_m_per_mw, variable_o_and_m_per_mwh, insurance_cost_per_kw, connection_cost_per_kw, min_running, fuel):
        """
        Initialisation of fuel power plant object.
        :param efficiency: Efficiency of power plant at converting fuel energy into electrical energy.
        :param fuel: Type of fuel that the power plant consumes.
        """
        super().__init__(self, plant_type=plant_type, capacity_mw=capacity_mw, average_load_factor=average_load_factor, pre_dev_period=pre_dev_period, construction_period=construction_period, operating_period=operating_period, pre_dev_spend_years=pre_dev_spend_years, construction_spend_years=construction_spend_years, pre_dev_cost_per_kw=pre_dev_cost_per_kw, construction_cost_per_kw=construction_cost_per_kw, infrastructure=infrastructure, fixed_o_and_m_per_mw=fixed_o_and_m_per_mw, variable_o_and_m_per_mwh=variable_o_and_m_per_mwh, insurance_cost_per_kw=insurance_cost_per_kw, connection_cost_per_kw=connection_cost_per_kw, min_running=min_running, construction_year=construction_year)
        self.efficiency = efficiency
        self.fuel = fuel_registry(fuel)

    def calculate_lcoe(self, discount_rate):
        """
        Function which calculates the levelised cost of electricity for this power plant instance at a
        specified discount rate.
        :param discount_rate: The discount rate that is used for the calculation of the levelised cost of electricity.
        :return: Returns LCOE value for power plant
        """

        # Calculations of capital expenditure, operating expenditure, total expected electricity expenditure and fuel cost
        # This is used to estimate a LCOE price.
        capex = self.capex()
        opex = self.opex()
        elec_gen = self.electricity_generated()
        fuel_costs = self.fuel_costs(elec_gen)
        total_costs = self.total_costs(capex, opex, fuel_costs)

        # Costs discounted using discount_rate variable.
        disc_costs = self.discounted_variable(total_costs, discount_rate)
        disc_elec = self.discounted_variable(elec_gen, discount_rate)

        # All costs summed
        disc_total_costs = sum(disc_costs)
        disc_total_elec = sum(disc_elec)

        # LCOE calculated
        lcoe = disc_total_costs/disc_total_elec

        return lcoe

    def total_costs(self, capex, opex, fuel_costs):
        """
        Function which uses addition to calculate total costs from capital expenditure, operating expenditure and
        fuel costs over the lifetime of the power plant.
        :param capex: Capital expenditure per year
        :param opex: Operating expenditure per year
        :param fuel_costs: Fuel costs per year
        :return: Total costs over lifetime of power plant
        """

        # Addition of operating expenditure and fuel costs, followed by operating expenditure, fuel costs and capital expenditure.
        opex_fuel = [sum(x) for x in zip(opex, fuel_costs)]
        capex.extend(opex_fuel)
        total_costs = [sum(x) for x in zip(opex_fuel, capex)]

        return total_costs

    def fuel_costs(self, electricity_generated):
        """
        Calculates the fuel costs per year based on plant efficiency, electricity generated and endogenous gas prices
        :param electricity_generated: Electricity generated per year
        :return: Returns estimated cost of fuel per year
        """

        fuel_costs = [0]*(self.pre_dev_period+self.construction_period)+[(self.fuel.fuel_price[i] * electricity_generated[i])/self.efficiency for i in range(self.operating_period)]
        return fuel_costs

