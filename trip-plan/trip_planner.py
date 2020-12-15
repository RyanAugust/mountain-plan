import datetime
import time

class trip(object):
	def __init__(self, trip_name):
		self.trip_name = trip_name
		self.trip_start = None
		self.trip_end = None
		self.segment_list = []
		self.solution_possible = False

	def add_segment(self, segment_name, segment_time=None, segment_start=None, segment_end=None):
		segment_instance = segment(segment_name=segment_name,
									segment_time=segment_time,
									segment_start=segment_start,
									segment_end=segment_end)
		self.segment_list.append(segment_instance)
	
	def add_trip_detail(self, detail_name, detail_value):
		"""Possible detail names are [start,end] & all values should be datetime objects"""
		assert detail_name in ['start','end'], "Invalid detail name passed"
		# assert type(detail_value)==datetime, "Invalid detail value passed"

		if detail_name == 'start':
			self.trip_start = detail_value
		elif detail_name == 'end':
			self.trip_end = detial_value

	def solver_instance(self, newly_solved):
		# Ensure parity between first and last segment with trip details
		if (self.trip_start == None) or (self.trip_end == None):
			newly_solved += self._apply_trip_details()
		elif (self.segment_list[0].segment_start != None) or (self.segment_list[-1].segment_end != None):
			newly_solved += self._imply_trip_details()
		# Attempt to solve segments with new info
		for segment_number in range(len(self.segment_list)):
			newly_solved += self._segment_solver(segment_number)
			newly_solved += self._segment_adjacency_check(segment_number)
		return newly_solved

	def solver(self, max_depth=20):
		depth = 0
		newly_solved = 1
		while (newly_solved != 0) & (depth<max_depth):
			newly_solved = 0
			newly_solved = self.solver_instance(newly_solved)
			print(newly_solved)
			depth += 1
			time.sleep(2)
		if self._check_solved():
			print('Solved!!')
		else:
			print('Failed to Solve :(')

	def _segment_solver(self, segment_number):
		if self.segment_list[segment_number].solved:
			return 0
		else:
			self.segment_list[segment_number] = self.segment_list[segment_number].solver()
			return 0

	def _check_solved(self):
		segment_count = len(self.segment_list)
		solved_count = 0
		for segment in self.segment_list:
			solved_count += 1 if segment.solved==True else 0
		return segment_count == solved_count
	def _segment_adjacency_check(self, segment_number):
		solve_count = 0
		if segment_number != 0:
			if (self.segment_list[segment_number].segment_start == None) & \
				(self.segment_list[segment_number-1].segment_end != None):
				self.segment_list[segment_number].segment_start = self.segment_list[segment_number-1].segment_end
				solve_count += 1
		else:
			pass
		if segment_number != len(self.segment_list)-1:
			if (self.segment_list[segment_number].segment_end == None) & \
				(self.segment_list[segment_number+1].segment_start != None):
				self.segment_list[segment_number].segment_end = self.segment_list[segment_number+1].segment_start
				solve_count += 1
		return solve_count
	def _apply_trip_details(self):
		solve_count = 0
		if (self.trip_start != None) & (self.segment_list[0].segment_start == None):
			self.segment_list[0].segment_start = self.trip_start
			solve_count += 1
		elif (self.trip_end != None) & (self.segment_list[-1].segment_end == None):
			self.segment_list[-1].segment_end = self.trip_end
			solve_count += 1
		return solve_count
	def _imply_trip_details(self):
		if (self.trip_start == None) & (self.segment_list[0].segment_start != None):
			self.trip_start = self.segment_list[0].segment_start
			solve_count += 1
		elif (self.trip_end == None) & (self.segment_list[-1].segment_end != None):
			self.trip_end = self.segment_list[-1].segment_end
			solve_count += 1
		return solve_count

	def show_segments(self):
		for segment in self.segment_list:
			print(segment)
			print('-----------------------')

	def export_json(self):
		import json
		segments = []
		for segment in self.segment_list:
			segments.append({'segment_name':segment._segment_name,
							 'segment_time':segment.segment_time,
							 'segment_start':segment.segment_start,
							 'segment_end':segment.segment_end})
		return json.dumps(segments)

	def import_json(self, json_input):
		segments_dict = json.loads(json_input)

		for segment in self.segment_list:
			self.add_segment(segment_name=segments_dict['segment_name'],
							segment_time=segments_dict['segment_time'],
							segment_start=segments_dict['segment_start'],
							segment_end=segments_dict['segment_end'])
		return 'Import Complete'


	# def check_segment_solution(self, segment_number):
	# 	segment = self.segment_list[segment_number]
	# 	if segment.solved != True:
	# 		if segment.segment_time_prop_count==len(segment.segment_time_prop_list)-1:
	# 			segment.solver()
	# 			return 'Solved'
	# 		else:


	# 	else:
			# return 'Solved'



class segment(object):
	def __init__(self, segment_name, segment_time=None, segment_start=None, segment_end=None):
		self.segment_name = segment_name
		self.segment_time = segment_time
		self.segment_start = segment_start
		self.segment_end = segment_end
		self.segment_time_prop_list = [self.segment_time, self.segment_start, self.segment_end]

		self.segment_time_prop_count = 0
		for val in self.segment_time_prop_list:
			if val != None:
				self.segment_time_prop_count += 1
		if len(self.segment_time_prop_list) == self.segment_time_prop_count:
			self.solved = True
		else:
			self.solved = False

	
	# def solver(self):
	# 	if (self.segment_time_prop_count > 1) & (self.solved == False):
	# 		self._time_ops()
	# 		self._solve_check()
	# 		return self
	# 	else:
	# 		self._solve_check()
	# 		return self

	def solver(self):
		# if (self.segment_time_prop_count > 1) & (self.solved == False):
		self._time_ops()
		self._solve_check()
		return self
	

	def _solve_check(self):
		solved_count = 0
		for val in self.segment_time_prop_list:
			if val != None:
				solved_count += 1
		self.segment_time_prop_count = solved_count
		if len(self.segment_time_prop_list) == self.segment_time_prop_count:
			self.solved = True
		else:
			self.solved = False
	
	def _time_ops(self):
		if self.segment_start != None:
			if self.segment_time != None:
				self.segment_end = self.segment_start + self.segment_time
			elif self.segment_end != None:
				self.segment_time = self.segment_end - self.segment_start
		elif self.segment_time != None:
			if self.segment_end != None:
				self.segment_start = self.segment_end - self.segment_time
			self.segment_time_prop_count = 3
		else:
			return 'solver_error'
		self.segment_time_prop_list = [self.segment_time, self.segment_start, self.segment_end]

	def __repr__(self):
		segment_details = """Segment Name: {s_name}\nSegment Start Time: {s_start}\nSegment Duration: {s_time}\nSegment End Time: {s_end}""".format(
			s_name=self.segment_name,
			s_start=self.segment_start,
			s_time=self.segment_time,
			s_end=self.segment_end)
		return segment_details