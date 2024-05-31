from roboflow import Roboflow
rf = Roboflow(api_key="oMjehIs6m5IK1UqNzdnR")
project = rf.workspace("trylogy").project("ripo-vopt8")
version = project.version(3)
dataset = version.download("yolov8")

