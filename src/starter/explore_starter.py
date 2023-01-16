import numpy as np

if __name__ == '__main__':
    x = [1, 2, 3, 4, 5]
    y = [4, 98, 123, 874, 1000]
    z = x

    print('Matrix between x and y: ')
    print(np.corrcoef(x, y))
    print()

    print('Matrix between x dan z: ')
    print(np.corrcoef(x, z))
