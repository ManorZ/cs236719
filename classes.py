from functools import total_ordering
from typing import Union
from utils import orientation, overlap

@total_ordering
class Point:
    '''
    Point class. Ordered by x coordinate (used in Priority Queue)
    '''

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __eq__(self, __o: object) -> bool:
        return ( self.x == __o.x ) and ( self.y == __o.y )

    def __lt__(self, __o: object) -> bool:
        return self.x < __o.x
    
    def __str__(self) -> str:
        return '({:.2f},{:.2f})'.format(self.x, self.y)
    
    def __repr__(self) -> str:
        return '({:.2f},{:.2f})'.format(self.x, self.y)


class Event():
    def __init__(self, point: Point, type: str) -> None:
        self.point = point
        self.type = type
    
    def __str__(self) -> str:
        return f'{self.point}, {self.type}'
    
    def __repr__(self) -> str:
        return f'{self.point}, {self.type}'
    
    def __eq__(self, __o: object) -> bool:
        return self.point == __o.point
    
    def __lt__(self, __o: object) -> bool:
        if self.point == __o.point:
            if self.type == 'LEFT': return True
            elif self.type == 'RIGHT': return False
        return self.point < __o.point


class Segment:
    '''
    Segment class. Ordered by y coordinate of the left endpoint Point
    '''
    def __init__(self, x1, y1, x2, y2) -> None:
        if x1 < x2:
            self.left_endpoint = Point(x1, y1)
            self.right_endpoint = Point(x2, y2)
        else:
            self.left_endpoint = Point(x2, y2)
            self.right_endpoint = Point(x1, y1)
        self.intersection_points = []  # Store intersection points discovered on the fly

    def __str__(self) -> str:
        s = '({:.2f},{:.2f})->({:.2f},{:.2f})'.format(self.left_endpoint.x, self.left_endpoint.y, self.right_endpoint.x, self.right_endpoint.y)
        return s
    
    def __repr__(self) -> str:
        return f'({self.left_endpoint.x},{self.left_endpoint.y})->({self.right_endpoint.x},{self.right_endpoint.y})'
    
    def __eq__(self, __o: object) -> bool:
        _orientation = orientation(__o.left_endpoint, __o.right_endpoint, self.left_endpoint)
        equal = _orientation == 0
        return equal
    
    def __lt__(self, __o: object) -> bool:
        _orientation = orientation(__o.left_endpoint, __o.right_endpoint, self.left_endpoint)
        lower_than = _orientation < 2
        return lower_than
    
    def __gt__(self, __o: object) -> bool:
        _orientation = orientation(__o.left_endpoint, __o.right_endpoint, self.left_endpoint)
        greater_than = _orientation == 2
        return greater_than

    def add_intersection(self, p):
        if p in self.intersection_points:
            raise ValueError(f'Intersection Point {p} already exist in Segment {self}')
        self.intersection_points.append(p)
    
    def intersect(self, __o):
              
        o1 = orientation(self.left_endpoint, self.right_endpoint, __o.left_endpoint)
        o2 = orientation(self.left_endpoint, self.right_endpoint, __o.right_endpoint)
        o3 = orientation(__o.left_endpoint, __o.right_endpoint, self.left_endpoint)
        o4 = orientation(__o.left_endpoint, __o.right_endpoint, self.right_endpoint)
  
        # General case
        if ((o1 != o2) and (o3 != o4)):
            return True
        # p1 , q1 and p2 are collinear and p2 lies on segment p1q1
        if ((o1 == 0) and overlap(self.left_endpoint, __o.left_endpoint, self.right_endpoint)):
            return True
        # p1 , q1 and q2 are collinear and q2 lies on segment p1q1
        if ((o2 == 0) and overlap(self.left_endpoint, __o.right_endpoint, self.right_endpoint)):
            return True
        # p2 , q2 and p1 are collinear and p1 lies on segment p2q2
        if ((o3 == 0) and overlap(self.right_endpoint, self.left_endpoint, __o.right_endpoint)):
            return True
        # p2 , q2 and q1 are collinear and q1 lies on segment p2q2
        if ((o4 == 0) and overlap(self.right_endpoint, __o.left_endpoint, __o.right_endpoint)):
            return True
        return False
    
    def line(self):
        A = (self.left_endpoint.y - self.right_endpoint.y)
        B = (self.right_endpoint.x - self.left_endpoint.x)
        C = (self.left_endpoint.x*self.right_endpoint.y - self.right_endpoint.x*self.left_endpoint.y)
        return A, B, -C

    def find_intersection(self, __o) -> Union[Point, bool]:
        a1, b1, c1 = self.line()
        a2, b2, c2 = __o.line()
        D  = a1 * b2 - b1 * a2
        Dx = c1 * b2 - b1 * c2
        Dy = a1 * c2 - c1 * a2
        if D != 0:
            x = Dx / D
            y = Dy / D
            return Point(x, y)
