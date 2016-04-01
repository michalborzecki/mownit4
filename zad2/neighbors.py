def get_4_neighbors(image, block):
    """
     x
    xox
     x
    """
    row, col = block
    neighbors = []
    if row > 0:
        neighbors.append((row-1, col))
    if row < len(image) - 1:
        neighbors.append((row+1, col))
    if col > 0:
        neighbors.append((row, col-1))
    if col < len(image) - 1:
        neighbors.append((row, col+1))
    return neighbors


def get_8_neighbors(image, block):
    """
    xxx
    xox
    xxx
    """
    row, col = block
    neighbors = []
    n = len(image)
    if row > 0:
        neighbors.extend([(row-1, c)
                          for c in range(max(col-1, 0), min(col+2, n))])
    if row < len(image) - 1:
        neighbors.extend([(row+1, c)
                          for c in range(max(col-1, 0), min(col+2, n))])
    neighbors.extend([(row, c)
                      for c in range(max(col-1, 0), min(col+2, n))
                      if (row, c) != block])
    return neighbors


def get_12_neighbors(image, block):
    """
      x
     xxx
    xxoxx
     xxx
      x
    """
    row, col = block
    neighbors = get_8_neighbors(image, block)
    if row > 1:
        neighbors.append((row-2, col))
    if row < len(image) - 2:
        neighbors.append((row+2, col))
    if col > 1:
        neighbors.append((row, col-2))
    if col < len(image) - 2:
        neighbors.append((row, col+2))
    return neighbors
