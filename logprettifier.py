import matplotlib.pyplot as plt

with open('log_mycontainer.txt', 'r') as file:
    tmp = [line.split('  ') for line in file.read().splitlines() if 'BLOCK' not in line]
    data = []
    for line in tmp:
        data.append([i for i in line if '%' in i])

plt.subplot(2, 1, 1)
plt.xlabel("Время, c")
plt.ylabel("Загрузка ЦП, %")
plt.plot(range(len(data)), [float(y[0].replace('%', '')) for y in data])
plt.subplot(2, 1, 2)
plt.xlabel("Время, c")
plt.ylabel("Загрузка ОЗУ, %")
plt.plot(range(len(data)), [float(y[1].replace('%', '')) for y in data])
plt.show()
