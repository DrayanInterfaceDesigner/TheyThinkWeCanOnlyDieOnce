import lib
import pygame
import sys
import threading


configuration_filepath = 'common/.config'
face_filepath = 'misc/faces/default_face/.config'
fd = lib.FeatureDetection(configuration_filepath)
cam = lib.WatchCam(fd, configuration_filepath)
fm = lib.FeatureManager()
BuildFace = lib.BuildFace(fm, fd, face_filepath)



sprite1 = lib.Sprite('misc/faces/default_face/assets/left_eye.png', lib.Vector2(), 30, 30)

sprite3 = lib.Sprite('misc/faces/default_face/assets/nose.png', lib.Vector2(), 33, 20)

spritet = lib.Sprite('misc/faces/default_face/assets/left_eye.png', lib.Vector2(), 30, 30)



def lerp(a, b, t):
    return a + (b - a) * t

def animation():
    pygame.init()
    screen_info = pygame.display.Info()
    width, height = screen_info.current_w, screen_info.current_h
    center_x, center_y = width // 2, height // 2
    bg_color = (22, 22, 22)

    
    velo = lib.Vector2(0, 0)
    eyes = lib.Vector2(0, 0)
    image = pygame.image.load('misc/faces/default_face/assets/nose.png')
    image = pygame.transform.scale(image, (33, 20))

    eye = pygame.image.load('misc/faces/default_face/assets/left_eye.png')
    eye = pygame.transform.scale(eye, (100, 100))
    sprite2 = lib.Sprite('misc/faces/default_face/assets/right_eye.png', lib.Vector2(0, 0), 30, 30)

    feature = lib.Feature(fm, sprite2, fd, "left_eye_center")

    screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
    pygame.display.set_caption("Pygame Borderless Sex")

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
            # sprite2.position.x = center_x//2 + fd.predictions["right_eye_center"][0] - 60
            # sprite2.position.y = (center_y//2 - 60) + fd.predictions["right_eye_center"][1]
            # sprite3.position.x = center_x//2 + fd.predictions["nose_tip"][0]
            # sprite3.position.y = (center_y//2 - 60) + fd.predictions["nose_tip"][1]


            # put the FPS on screen
            font = pygame.font.SysFont('Arial', 30)
            fps = font.render("FPS: "+str(int(clock.get_fps())), True, pygame.Color('white'))
            buffer.blit(fps, (50, 50))

            velo.x = lerp(velo.x, fd.predictions["nose_tip"][0], 0.1)
            velo.y = lerp(velo.y, fd.predictions["nose_tip"][1], 0.1)
            eyes.x = lerp(eyes.x, fd.predictions["left_eye_center"][0], 0.1)
            eyes.y = lerp(eyes.y, fd.predictions["left_eye_center"][1], 0.1)


            sprite3.position.x = velo.x - (sprite3.width // 2)
            sprite3.position.y = velo.y - (sprite3.height // 2)
            sprite2.position.x = eyes.x - (sprite2.width // 2)
            sprite2.position.y = eyes.y - (sprite2.height // 2)
            
            # buffer.blit(image, (velo.x, velo.y ))
            feature.update(1)
            feature.render(buffer)
            # buffer.blit(sprite2.image, sprite2.position.__tuple__())
            
            # sprite1.draw(buffer)
            # sprite2.render(buffer)
            # sprite3.render(buffer)

            fm.update(1)
            fm.render(buffer)

            pygame.draw.circle(buffer, (255, 255, 23), fd.predictions["left_eye_center"] , 5)
            pygame.draw.circle(buffer, (255, 23, 255), fd.predictions["right_eye_center"] , 5)
            pygame.draw.circle(buffer, (23, 255, 255), fd.predictions["nose_tip"] , 5)
        
            # spritet.draw(buffer)
            # sprite1.draw(buffer)
            # sprite2.draw(buffer)
            


        pygame.display.update()
        screen.blit(buffer, (0, 0))
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