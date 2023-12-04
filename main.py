import lib
import pygame
import sys
import threading


configuration_filepath = 'common/.config'
fd = lib.FeatureDetection(configuration_filepath)
cam = lib.WatchCam(fd, configuration_filepath)
sprite1 = lib.Sprite(pygame.image.load('misc/faces/default_face/assets/left_eye.png'), lib.Vector2(), 100, 100)
sprite2 = lib.Sprite(pygame.image.load('misc/faces/default_face/assets/right_eye.png'), lib.Vector2(), 100, 100)
sprite3 = lib.Sprite(pygame.image.load('misc/faces/default_face/assets/nose.png'), lib.Vector2(), 33, 20)


def animation():
    pygame.init()
    screen_info = pygame.display.Info()
    width, height = screen_info.current_w, screen_info.current_h
    center_x, center_y = width // 2, height // 2
    bg_color = (22, 22, 22)

    screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
    pygame.display.set_caption("Pygame Borderless Example")

    buffer = pygame.Surface((width, height))

    if pygame.display.get_driver() == 'windib':
        print("Warning: Pygame is not using hardware acceleration. Consider updating your graphics drivers.")
    else:
        print("Pygame is using hardware acceleration.")



    clock = pygame.time.Clock()
    while True:
        # print(fd.predictions)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cam.break_loop = True
                sys.exit()
        
        buffer.fill(bg_color)
        if fd.predictions is not None:
            sprite1.position.x = center_x//2 + fd.predictions["left_eye_center"][0] + 60
            sprite1.position.y = (center_y//2 - 60) + fd.predictions["left_eye_center"][1]
            sprite2.position.x = center_x//2 + fd.predictions["right_eye_center"][0] - 60
            sprite2.position.y = (center_y//2 - 60) + fd.predictions["right_eye_center"][1]
            sprite3.position.x = center_x//2 + fd.predictions["nose_tip"][0]
            sprite3.position.y = (center_y//2 - 60) + fd.predictions["nose_tip"][1]
            sprite1.draw(buffer)
            sprite2.draw(buffer)
            sprite3.draw(buffer)


        pygame.display.update()
        screen.blit(buffer, (0, 0))
        pygame.display.flip()
        clock.tick(30)

thread1 = threading.Thread(target=cam.start_to_watch)
thread2 = threading.Thread(target=animation)

# Start the threads
thread1.start()
thread2.start()

# Wait for both threads to finish
thread1.join()
thread2.join()