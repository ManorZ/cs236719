from classes import Segment


def parser(file: str):
    with open(file, 'r') as f:
        lines = f.readlines()
    lines = list(filter(lambda x: not x.startswith('#'), lines))
    all_tests = []
    N = int(lines.pop(0))
    for n in range(N):
        M = int(lines.pop(0))
        test = []
        for m in range(M):
            test.append(Segment(*[float(x) for x in lines.pop(0).split()]))
        all_tests.append(test)
    return all_tests