import lib
import pygame
import sys
import threading
import configparser


configuration_filepath = 'common/.config'
face_filepath = 'misc/faces/default_face/.config'

config = configparser.ConfigParser()
config.read(configuration_filepath)

fd = lib.FeatureDetection(configuration_filepath)
cam = lib.WatchCam(fd, configuration_filepath)
fm = lib.FeatureManager()
BuildFace = lib.BuildFace(fm, fd, face_filepath)

def animation():
    pygame.init()
    screen_info = pygame.display.Info()
    width, height = screen_info.current_w, screen_info.current_h
    center_x, center_y = width // 2, height // 2
    bg_color = (22, 22, 22)

    screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
    pygame.display.set_caption("Pygame Borderless Sex")

    buffer = pygame.Surface((width, height))
    ui = pygame.Surface((width, height))

    if pygame.display.get_driver() == 'windib':
        print("Warning: Pygame is not using hardware acceleration. Consider updating your graphics drivers.")
    else:
        print("Pygame is using hardware acceleration.")


    clock = pygame.time.Clock()
    screen.fill(bg_color)
    while True:
        # print(fd.predictions)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cam.break_loop = True
                sys.exit()
        
        buffer.fill(bg_color)
        
        if fd.predictions is not None:
            # put the FPS on screen
            font = pygame.font.SysFont('Arial', 30)
            fps = font.render("FPS: "+str(int(clock.get_fps())), True, pygame.Color('white'))
            buffer.blit(fps, (50, 50))

            fm.update(1)
            fm.render(buffer)

            if config.getboolean("Debug", "debug_mode"):
                pygame.draw.circle(buffer, (255, 255, 23), fd.predictions["left_eye_center"] , 5)
                pygame.draw.circle(buffer, (255, 23, 255), fd.predictions["right_eye_center"] , 5)
                pygame.draw.circle(buffer, (23, 255, 255), fd.predictions["nose_tip"] , 5)
            
        pygame.display.update()

        screen.blit(buffer, (center_x // 2, center_y // 2))


        pygame.display.flip()
        clock.tick(60)

thread1 = threading.Thread(target=cam.start_to_watch)
thread2 = threading.Thread(target=animation)

# Start the threads
thread1.start()
thread2.start()

# Wait for both threads to finish
thread1.join()
thread2.join()