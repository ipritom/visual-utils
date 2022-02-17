"""
NETWORK VIDEO RECORDER

This scripts attempt to replicate NVR device. 
It records video from multiple cameras.

"""
from camera_config.camera import CameraStream
import cv2
import time
import datetime
import os


_BASE_PATH = os.getcwd()

def get_feed_name(timestamp, camera_name='Unknown'):
    '''
    Returns video file names with timestamp and camera name

	Name Format: cameraname_timestampint_timestampdecimal_.filetype
    '''
    time_str = str(timestamp).split('.')
    name = camera_name + "_" + time_str[0] + '_' + time_str[1] +'_.avi'
    print(" ### FEED NAME ###:", name)
    return name 

def _resolve_storage_paths(path):
	if os.path.isdir(path) == False:
		print(f'--- path created : {path}')
		os.mkdir(path)


class CameraNode:
	def __init__(self, camera_name, source, resolution) -> None:
		self.camera_name = camera_name
		self.source = source
		self.resolution = resolution
		self.video_writer_fourcc = None
		self.video_writer = None
		self.camera_dump_path = None
		self.flie_dump_path = None

class CameraRecorder:
	def __init__(self) -> None:
		self.camera_node_list = list()
	
	def record(self):
		if len(self.camera_node_list) == 0:
			pass
		dump_path = os.path.join(_BASE_PATH, "records")
		
		# resolving camera storage paths
		_resolve_storage_paths(dump_path)
		
		for node in self.camera_node_list:
			camera_dump_path = os.path.join(dump_path, node.camera_name)
			_resolve_storage_paths(camera_dump_path)
			node.camera_dump_path = camera_dump_path
	

		while True:
			# generating flie_dump_path for each camera node.
			for node in self.camera_node_list:
				timestamp = time.time()
				feed_name = get_feed_name(timestamp, node.camera_name)
				datetime_tupple = datetime.datetime.fromtimestamp(timestamp)
				
				# resolving file_dump_path, path format : camera_name/year/month/day/hour
				year_path = os.path.join(node.camera_dump_path, str(datetime_tupple.year))
				_resolve_storage_paths(year_path)

				month_path = os.path.join(year_path, str(datetime_tupple.month))
				_resolve_storage_paths(month_path)

				day_path = os.path.join(month_path, str(datetime_tupple.day))
				_resolve_storage_paths(day_path)

				hour_path = os.path.join(day_path, str(datetime_tupple.hour))
				_resolve_storage_paths(hour_path)

				# file_dump_path
				node.flie_dump_path = os.path.join(hour_path, feed_name)

			frame_count = 0
			LIMIT = 1020 # how many frames will be recorded for each video file
			FLAG_LIMIT = True # Limit flag for each video file
			
			# Video writer for each camera node 
			for node in self.camera_node_list:
				node.video_writer_fourcc = cv2.VideoWriter_fourcc(*'XVID')
				node.video_writer = cv2.VideoWriter(node.flie_dump_path, node.video_writer_fourcc, 60, node.resolution)
			

			while FLAG_LIMIT:

				if frame_count > LIMIT:
					#FLAG_LIMIT = False
					break

				#NOTE: Beware
				#Reshaping is required

				# Read/Write from cams
				for node in self.camera_node_list:
					ret, frame = node.source.read()

					# if frame retrival succeed -> Write to video file
					if ret:
						node.video_writer.write(frame)
					else:
						print("--- Failed at ", node.camera_name)
		
				# Increment frame count
				frame_count +=1

				#For exiting
				key = cv2.waitKey(1)
				if key & 0xFF == ord('q'):
					cv2.destroyAllWindows()
					break

			for node in self.camera_node_list:
				node.video_writer.release()

		source_1.stop()
		source_2.stop()

if __name__ == "__main__":

	camera1 = "" # camera rtsp link here
	camera2 = "" # camera rtsp link here



	# Multiple sources # NOTE: start() is required?
	source_1 = CameraStream(src=camera1).start()
	source_2 = CameraStream(src=camera2).start()

	recorder = CameraRecorder()
	camera_node_1 = CameraNode("Camera1", source_1, (1920,1080))
	camera_node_2 = CameraNode("Camera2", source_2, (1280,720))
	recorder.camera_node_list = [camera_node_1, camera_node_2]
	recorder.record()
