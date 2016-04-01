def get_4_neighbors(size, block):
    """
     x
    xox
     x
    """
    row, col = block
    neighbors = set()
    if row > 0:
        neighbors.add((row-1, col))
    if row < size - 1:
        neighbors.add((row+1, col))
    if col > 0:
        neighbors.add((row, col-1))
    if col < size - 1:
        neighbors.add((row, col+1))
    return neighbors


def get_8_neighbors(size, block):
    """
    xxx
    xox
    xxx
    """
    row, col = block
    neighbors = set()
    if row > 0:
        neighbors.update({(row-1, c)
                          for c in range(max(col-1, 0), min(col+2, size))})
    if row < size - 1:
        neighbors.update({(row+1, c)
                          for c in range(max(col-1, 0), min(col+2, size))})
    neighbors.update({(row, c)
                      for c in range(max(col-1, 0), min(col+2, size))
                      if (row, c) != block})
    return neighbors


def get_12_neighbors(size, block):
    """
      x
     xxx
    xxoxx
     xxx
      x
    """
    row, col = block
    neighbors = get_8_neighbors(size, block)
    if row > 1:
        neighbors.add((row-2, col))
    if row < size - 2:
        neighbors.add((row+2, col))
    if col > 1:
        neighbors.add((row, col-2))
    if col < size - 2:
        neighbors.add((row, col+2))
    return neighbors
