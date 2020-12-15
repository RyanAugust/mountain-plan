# Trip Planner
Trip timing planner.

Given a limited number of details about segment timing the solver will attempt to return a full schedule of segments.

`segments` are given their own class and can be used independently 
`trip` constitutets a collection of `segment`s with `trip.segment_list` being an ordered list of those `segment`s each with it's own timing properties. `trip` also contains an array of functions for access `segment` internal solver as well as a solver for connecting `segment`s (ie. Start of one segment vs end of the previous).
