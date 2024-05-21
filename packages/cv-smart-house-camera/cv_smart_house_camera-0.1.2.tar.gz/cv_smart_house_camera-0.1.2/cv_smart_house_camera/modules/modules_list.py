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
{ "name": "Original Frame", "package_name": "internal", "proccessing": original_frame_processing },
]