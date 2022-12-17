def orientation(p, q, r, epsilon = 1e-6):
    '''
    Find the orientation of an ordered triplet (p,q,r)
    function returns the following values:
    0 : Collinear points
    1 : Clockwise points
    2 : Counterclockwise
    '''
    val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
    if (val > epsilon):  # Clockwise orientation
        return 1
    elif (val < -epsilon):  # Counterclockwise orientation
        return 2
    else:  # Collinear orientation
        return 0


def overlap(p, q, r):
    '''
    Given three collinear points p, q, r, the function checks if 
    point q lies on line segment 'pr' 
    '''
    if (
        (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and 
        (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))
    ):
        return True
    return False


def binary_search(arr, low, high, x):
    '''
    Special implementation of binary searching a segment containing a point in sorted array of segments.
    '''
    # Check base case
    if high >= low:
 
        mid = (high + low) // 2
 
        if orientation(arr[mid].left_endpoint, arr[mid].right_endpoint, x) == 0:
            return mid
        elif orientation(arr[mid].left_endpoint, arr[mid].right_endpoint, x) == 1:
            return binary_search(arr, low, mid - 1, x)
        else:
            return binary_search(arr, mid + 1, high, x)
 
    else:
        # Element is not present in the array
        return -1