import lib

configuration_filepath = 'common/.config'
fd = lib.FeatureDetection(configuration_filepath)
cam = lib.WatchCam(fd, configuration_filepath)
cam.start_to_watch()