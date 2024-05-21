import cv2


def test_module_processing(frame, frame_number):
	center_x = frame.shape[1] // 2
	center_y = frame.shape[0] // 2

	# Draw a circle at the center
	radius = 50
	color = (0, 255, 0)  # BGR color (here, green)
	thickness = 2
	cv2.circle(frame, (center_x, center_y), radius, color, thickness)
	return {"frame": frame}


def original_frame_processing(frame, frame_number):
	return

modules = [
{ "name": "Original Frame", "package_name": "original", "proccessing": original_frame_processing },
{ "name": "test Module", "package_name": "test_module", "proccessing": test_module_processing },
{ "name": "test Module2", "package_name": "test_module2", "proccessing": original_frame_processing, "options": { "processing_frame": 10 } }
]