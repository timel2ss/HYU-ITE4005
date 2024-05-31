import sys
import math

epsilon: int = -1
minPts: int = -1
label_idx: int = 0

data_points: list[tuple] = []
clusters: list[list] = []
labels: list[int] = [] # 0: undefined, -1: noise, others: cluster_id

def dbscan():
    for p in data_points:
        if labels[p[0]] != 0:
            continue

        neighbors_p: set[tuple] = rangeQuery(p)
        if len(neighbors_p) < minPts:
            labels[p[0]] = -1 # noise
            continue

        label: int = next_cluster_label()
        labels[p[0]] = label
        clusters[-1].append(p)
        neighbors_p.remove(p)
        seed_set: set = set(neighbors_p)

        while seed_set:
            q = seed_set.pop()
            if labels[q[0]] == -1:
                labels[q[0]] = label
            if labels[q[0]] != 0:
                continue
            
            clusters[-1].append(q)
            neighbors_q: set[tuple] = rangeQuery(q)
            labels[q[0]] = label

            if (len(neighbors_q) < minPts):
                continue

            seed_set = seed_set.union(neighbors_q)

def distance(p: tuple, q: tuple) -> float:
    return math.sqrt(((p[1] - q[1]) ** 2) + ((p[2] - q[2]) ** 2))

def rangeQuery(p: tuple) -> set[tuple]:
    neighbors: list = []
    for point in data_points:
        if distance(p, point) <= epsilon:
            neighbors.append(point)
    return set(neighbors)

def next_cluster_label():
    global label_idx
    label_idx += 1
    clusters.append([])
    return label_idx

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(f'usage: python {sys.argv[0]} [input data file] [number of clusters] [Epsilon] [MinPts]')
        quit()
    
    input_file_name: str = sys.argv[1]
    n: int = int(sys.argv[2])
    epsilon: int = int(sys.argv[3])
    minPts: int = int(sys.argv[4])

    with open(file = input_file_name, mode = 'rt') as input_file:
        while True:
            line: str = input_file.readline().strip()
            if not line:
                break

            id, x, y = line.split('\t')
            id = int(id)
            x = float(x)
            y = float(y)
            data_points.append((id, x, y))
            labels.append(0) # undefined

    dbscan()
    clusters.sort(key=len, reverse=True)

    for i in range(n):
        output_file_name: str = f'input{input_file_name[-5]}_cluster_{i}.txt'
        with open(file = output_file_name, mode = 'wt') as output_file:
            clusters[i].sort()
            for j in clusters[i]:
                output_file.write(f'{j[0]}\n')