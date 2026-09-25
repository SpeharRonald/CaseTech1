import sys
import os

#константи задачі
GRID_SIZE = 10# сітка 10x10 (координати від 1 до 10)
INITIAL_COINS = 1000000# початковий баланс монет свого мотиву в місті
PORTION = 1000# "представницька частка": 1 монета на кожні PORTION монет
MAX_DAYS = 50000# запобіжник від нескінченного циклу

# Дані беруться з input.txt поруч зі скриптом.
if sys.stdin.isatty():
    input_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input.txt')
    if not os.path.exists(input_path):
        print(f"Файл {input_path} не знайдено. Створіть input.txt поруч зі скриптом "
              f"або запустіть програму з перенаправленням: python {os.path.basename(__file__)} < input.txt")
        sys.exit(1)
    with open(input_path, encoding='utf-8') as f:
        raw = f.read()
else:
    raw = sys.stdin.read()

data = [line for line in raw.split('\n') if line.strip() != '']
pos = 0
result = []
case = 0

while pos < len(data):
    c = int(data[pos]); pos += 1
    if c == 0:
        break
    case += 1

    names, xl, yl, xh, yh = [], [], [], [], []
    for i in range(c):
        p = data[pos].split(); pos += 1
        if len(p) != 5:
            print(f"Помилка формату вводу в рядку {pos}: "
                  f"очікується 'назва xl yl xh yh', отримано: {data[pos - 1]!r}")
            sys.exit(1)
        names.append(p[0])
        xl.append(int(p[1])); yl.append(int(p[2]))
        xh.append(int(p[3])); yh.append(int(p[4]))

    # країна кожної клітинки сітки (-1, якщо міста немає)
    grid = [[-1] * (GRID_SIZE + 1) for _ in range(GRID_SIZE + 1)]
    for i in range(c):
        for x in range(xl[i], xh[i] + 1):
            for y in range(yl[i], yh[i] + 1):
                grid[x][y] = i

    # список міст: (x, y, номер_країни)
    cities = [(x, y, grid[x][y])
              for x in range(1, GRID_SIZE + 1)
              for y in range(1, GRID_SIZE + 1)
              if grid[x][y] != -1]
    n = len(cities)

    # сусіди кожного міста (за індексами у списку cities)
    neighbors = []
    for x, y, _ in cities:
        nb = []
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 1 <= nx <= GRID_SIZE and 1 <= ny <= GRID_SIZE and grid[nx][ny] != -1:
                for j, (x2, y2, _) in enumerate(cities):
                    if x2 == nx and y2 == ny:
                        nb.append(j)
                        break
        neighbors.append(nb)

    # баланс монет: coins[місто][тип_монети]
    coins = [[0] * c for _ in range(n)]
    for i, (_, _, country) in enumerate(cities):
        coins[i][country] = INITIAL_COINS

    done = [None] * c

    def check(day):
        for i in range(c):
            if done[i] is not None:
                continue
            complete = True
            for j, (_, _, country) in enumerate(cities):
                if country == i and 0 in coins[j]:
                    complete = False
                    break
            if complete:
                done[i] = day

    check(0)
    day = 0
    while None in done and day < MAX_DAYS:
        day += 1
        send = [[coins[i][t] // PORTION for t in range(c)] for i in range(n)]
        new_coins = [row[:] for row in coins]
        for i in range(n):
            k = len(neighbors[i])
            for t in range(c):
                new_coins[i][t] -= send[i][t] * k
            for j in neighbors[i]:
                for t in range(c):
                    new_coins[i][t] += send[j][t]
        coins = new_coins
        check(day)

    # захист: якщо якась країна не завершилась за MAX_DAYS, done[i] лишиться None —
    # такий запис виводимо окремо, щоб sorted() не впав на порівнянні None з int
    unfinished = [i for i in range(c) if done[i] is None]
    finished = [i for i in range(c) if done[i] is not None]
    order = sorted(finished, key=lambda i: (done[i], names[i]))
    order += sorted(unfinished, key=lambda i: names[i])

    result.append(f"Case Number {case}")
    for i in order:
        status = done[i] if done[i] is not None else f"не завершено за {MAX_DAYS} днів"
        result.append(f"{names[i]} {status}")
print('\n'.join(result))