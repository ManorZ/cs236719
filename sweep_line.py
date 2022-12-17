from typing import List
import numpy as np
import matplotlib.pyplot as plt
from queue import PriorityQueue
import bisect

from classes import Segment, Point, Event
from utils import binary_search, orientation
from file_parser import parser

class LineSweepIntersection:
    def __init__(self, segments: List[Segment]) -> None:
        
        self.segments = segments

        self.event_prio_queue = PriorityQueue()
        for segment in segments:
            self.event_prio_queue.put(Event(segment.left_endpoint, 'LEFT'))
            self.event_prio_queue.put(Event(segment.right_endpoint, 'RIGHT'))

        self.sweep_line_status = []
        
    def plot_event_prio_queue(self):
        while not self.event_prio_queue.empty():
            print(self.event_prio_queue.get())
    
    def plot(self):
        fig,ax = plt.subplots()
        minx = np.inf
        maxx = -np.inf
        miny = np.inf
        maxy = -np.inf
        for segment in self.segments:
            minx = min(minx, segment.left_endpoint.x, segment.right_endpoint.x)
            maxx = max(maxx, segment.left_endpoint.x, segment.right_endpoint.x)
            miny = min(miny, segment.left_endpoint.y, segment.right_endpoint.y)
            maxy = max(maxy, segment.left_endpoint.y, segment.right_endpoint.y)
            ax.plot(
                (segment.left_endpoint.x, segment.right_endpoint.x),
                (segment.left_endpoint.y, segment.right_endpoint.y), linestyle='-', marker='o')
        ax.set_xlim(left=minx, right=maxx)
        ax.set_ylim(bottom=miny, top=maxy)
        ax.grid(which='both')   
        
        fig.show()
    
    def __call__(self):
        intersection_points = []
        while not self.event_prio_queue.empty():
            new_event = self.event_prio_queue.get()
            if new_event.type == 'LEFT':
                new_segment = list(filter(lambda x: x.left_endpoint == new_event.point, self.segments))[0]  # TODO: handle the case where two segments intersect on the left endpoint
                bisect.insort(self.sweep_line_status, new_segment)
                i = binary_search(self.sweep_line_status, 0, len(self.sweep_line_status)-1, new_event.point)
                # print(self.sweep_line_status)
                if len(self.sweep_line_status) > 1:
                    if i > 0:
                        below_intersection = new_segment.intersect(self.sweep_line_status[i-1])
                        if below_intersection:
                            intersection_point = new_segment.find_intersection(self.sweep_line_status[i-1])
                            if intersection_point.x > new_event.point.x:  # Intersection point to the right of sweep line
                                self.event_prio_queue.put(Event(intersection_point, 'INTER'))
                                self.sweep_line_status[i].add_intersection(intersection_point)
                                self.sweep_line_status[i-1].add_intersection(intersection_point)
                    if i < len(self.sweep_line_status) - 1:
                        above_intersection = new_segment.intersect(self.sweep_line_status[i+1])
                        if above_intersection:
                            intersection_point = new_segment.find_intersection(self.sweep_line_status[i+1])
                            if intersection_point.x > new_event.point.x:  # Intersection point to the right of sweep line
                                self.event_prio_queue.put(Event(intersection_point, 'INTER'))
                                self.sweep_line_status[i].add_intersection(intersection_point)
                                self.sweep_line_status[i+1].add_intersection(intersection_point)
            if new_event.type == 'RIGHT':
                new_segment = list(filter(lambda x: x.right_endpoint == new_event.point, self.segments))[0]  # TODO: handle the case where two segments intersect on the right endpoint    
                i = binary_search(self.sweep_line_status, 0, len(self.sweep_line_status)-1, new_event.point)
                last = False
                if i == len(self.sweep_line_status)-1: last = True
                del self.sweep_line_status[i]
                # print(self.sweep_line_status)
                if last: i -= 1
                if len(self.sweep_line_status) > 2:
                    if i > 0:
                        intersection = self.sweep_line_status[i].intersect(self.sweep_line_status[i-1])
                        if intersection:
                            intersection_point = self.sweep_line_status[i].find_intersection(self.sweep_line_status[i-1])
                            if intersection_point.x > new_event.point.x:  # Intersection point to the right of sweep line
                                if Event(intersection_point, 'INTER') not in self.event_prio_queue.queue:  # And we haven't seen that point yet
                                    self.event_prio_queue.put(Event(intersection_point, 'INTER'))
                                    self.sweep_line_status[i].add_intersection(intersection_point)
                                    self.sweep_line_status[i-1].add_intersection(intersection_point)
                
            if new_event.type == 'INTER':
                intersection_points.append(new_event.point)
                intersecting_segments = list(filter(lambda x: new_event.point in x.intersection_points, self.sweep_line_status))
                if len(intersecting_segments) > 2:
                    raise ValueError(f'More than 2 segments intersect on {new_event.point}. They are: {intersecting_segments}')
                if len(intersecting_segments) == 1:
                    raise ValueError(f'Only 1 segment has found with {new_event.point} intersection. It is: {intersecting_segments}')
                if len(intersecting_segments) == 0:
                    raise ValueError(f'WTF? No segments have found with {new_event.point} intersection')
                i = binary_search(self.sweep_line_status, 0, len(self.sweep_line_status)-1, new_event.point)
                if i == 0:
                    j = i+1
                elif i == len(self.sweep_line_status)-1:
                    j = i-1
                elif orientation(self.sweep_line_status[i-1].left_endpoint, self.sweep_line_status[i-1].right_endpoint, new_event.point) == 0:
                    j = i - 1
                elif orientation(self.sweep_line_status[i+1].left_endpoint, self.sweep_line_status[i+1].right_endpoint, new_event.point) == 0:
                    j = i + 1
                else:
                    raise ValueError('Oh Oh')
                self.sweep_line_status[i], self.sweep_line_status[j] = self.sweep_line_status[j], self.sweep_line_status[i]
                # print(self.sweep_line_status)
                if min(i,j) > 0:
                    below_intersection = self.sweep_line_status[min(i,j)].intersect(self.sweep_line_status[min(i,j)-1])
                    if below_intersection:
                        intersection_point = self.sweep_line_status[min(i,j)].find_intersection(self.sweep_line_status[min(i,j)-1])
                        if intersection_point.x > new_event.point.x:  # Intersection point to the right of sweep line
                            if Event(intersection_point, 'INTER') not in self.event_prio_queue.queue:  # And we haven't seen that point yet
                                self.event_prio_queue.put(Event(intersection_point, 'INTER'))
                                self.sweep_line_status[min(i,j)].add_intersection(intersection_point)
                                self.sweep_line_status[min(i,j)-1].add_intersection(intersection_point)
                if max(i,j) < len(self.sweep_line_status)-1:
                    above_intersection = self.sweep_line_status[max(i,j)].intersect(self.sweep_line_status[max(i,j)+1])
                    if above_intersection:
                        intersection_point = self.sweep_line_status[max(i,j)].find_intersection(self.sweep_line_status[max(i,j)+1])
                        if intersection_point.x > new_event.point.x:  # Intersection point to the right of sweep line
                            if Event(intersection_point, 'INTER') not in self.event_prio_queue.queue:  # And we haven't seen that point yet
                                self.event_prio_queue.put(Event(intersection_point, 'INTER'))
                                self.sweep_line_status[max(i,j)].add_intersection(intersection_point)
                                self.sweep_line_status[max(i,j)+1].add_intersection(intersection_point)
                           
        return intersection_points


if __name__ == '__main__':
    file = 'input.txt'
    all_test = parser(file)
    for test in all_test:
        line_sweep_algo = LineSweepIntersection(test)
        line_sweep_algo.plot()
        # line_sweep_algo.debug()
        print(line_sweep_algo())
        print('-'*100)