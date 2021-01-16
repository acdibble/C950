import wgups

packages: list[wgups.Package] = []

with open("packages.csv") as f:
    for line in f:
        values = line.strip().split(";")
        packages.append(wgups.Package(*values))

for p in packages:
    print(p)
