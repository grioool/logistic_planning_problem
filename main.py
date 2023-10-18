from pulp import *

warehouses_location = ["Lyon", "Bilbao"]
regional_customer_location = ["Portugal", "Spain", "France", "Italy"]
expected_demand = {"Portugal": 1000, "Spain": 1100, "France": 1200, "Italy": 1800}
shipping_costs = {
    ("Lyon", "Italy"): 232,
    ("Lyon", "France"): 212,
    ("Lyon", "Spain"): 230,
    ("Lyon", "Portugal"): 280,
    ("Bilbao", "Italy"): 211,
    ("Bilbao", "France"): 232,
    ("Bilbao", "Spain"): 240,
    ("Bilbao", "Portugal"): 300,
}

# 1 Initialize model
kitchen_oven_manufacturer = LpProblem("Minimize_regional_demand ", LpMinimize)

# 2 Define the decision variables
variables = LpVariable.dicts("Shipping_costs",
                             ((warehouse, regional_customer)
                              for warehouse in warehouses_location
                              for regional_customer in regional_customer_location),
                             lowBound=0)

# 3 Define Objective function
kitchen_oven_manufacturer += sum(variables[(warehouse, regional_customer)]
                                 * shipping_costs[(warehouse, regional_customer)]
                                 for warehouse in warehouses_location
                                 for regional_customer in regional_customer_location)

# 4 Define Constraints
for warehouse in warehouses_location:
    kitchen_oven_manufacturer += sum(variables[(warehouse, regional_customer)]
                                     for regional_customer in regional_customer_location) <= 1

for regional_customer in regional_customer_location:
    kitchen_oven_manufacturer += sum(variables[(warehouse, regional_customer)]
                                     for warehouse in warehouses_location) == expected_demand[regional_customer]

# 5 Solve model
kitchen_oven_manufacturer.solve()

# 6 Print
print(kitchen_oven_manufacturer.status)

print("Optimized shipping plan with the lowest cost:")
for warehouse in warehouses_location:
    for regional_customer in regional_customer_location:
        shipping_plan = variables[(warehouse, regional_customer)].varValue

result = value(kitchen_oven_manufacturer.objective)
print("Minimized regional demand: {}".format(result))
