class Direction:
    Left = (-1, 0)
    Up = (0, -1)
    Right = (1, 0)
    Down = (0, 1)

def oppositeDirection(dir):
    if dir == Direction.Left:
        return Direction.Right
    if dir == Direction.Right:
        return Direction.Left
    if dir == Direction.Up:
        return Direction.Down
    if dir == Direction.Down:
        return Direction.Up

def getDirectionsToCheck(dir):
    r = [Direction.Left,Direction.Up,Direction.Right,Direction.Down]
    r.remove(oppositeDirection(dir))
    return r

def directionToNumber(dir):
    return [Direction.Left,Direction.Up,Direction.Right,Direction.Down].index(dir)