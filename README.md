This repo includes mostly the coding assignment in the course.
There are also some dry assignments, but I can't guarantee their quality...

The coding assignment was to implement a line-sweep algorithm for segments-intersections counting task. 
I choose to implement it in Python.

Some assumptions: 
  *There are no vertical segments.
  No two segments intersect in more than one point.
  No three segments intersect in one point.
  Segment endpoints are well separated, as well as intersections of segments and events of the algorithm are separated enough along the x axis.

Input file:
The input is found in a single Ascii file which contains the following data:
1. Number of test cases (a positive integer number n).
2. n sets of segments, each one containing:
  * Number of segments (a positive number mi, 1 · i · n).
  * mi segments, each one specified by four (4) point coordinates xi1 , yi1 , xi2 , yi2 .
3. The number -1.
