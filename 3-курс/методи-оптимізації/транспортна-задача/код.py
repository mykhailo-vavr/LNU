from pulp import *

supply = [30, 25, 45]
demand = [32, 24, 28, 16]
costs = [[9, 7, 8, 4], [6, 6, 7, 5], [4, 7, 9, 5]]

model = LpProblem("Transportation Problem", LpMinimize)

x = []
for i in range(len(supply)):
    x.append([])
    for j in range(len(demand)):
        x[i].append(LpVariable("x" + str(i + 1) + str(j + 1), 0))

total_cost = ""
for i in range(len(supply)):
    for j in range(len(demand)):
        total_cost += costs[i][j] * x[i][j]
model += total_cost

for i in range(len(supply)):
    model += lpSum(x[i]) <= supply[i]
for j in range(len(demand)):
    model += lpSum([x[i][j] for i in range(len(supply))]) == demand[j]

status = model.solve()

print("Optimal Solution: ", value(model.objective))
for i in range(len(supply)):
    for j in range(len(demand)):
        if x[i][j].varValue != 0:
            print(
                "x_%d_%d = %d"
                % (
                    i + 1,
                    j + 1,
                    x[i][j].varValue,
                )
            )
