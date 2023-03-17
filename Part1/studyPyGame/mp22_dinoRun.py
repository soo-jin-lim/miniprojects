#dinoRun
import pygame
import os

pygame.init()

ASSETS = './studyPyGame/Assets/' 
SCREEN = pygame.display.set_mode((1100, 600))
icon = pygame.image.load('./studyPyGame/dinoRun.png')
pygame.display.set_icon(icon)

BG = pygame.image.load(os.path.join(f'{ASSETS}Other', 'Track.png'))

RUNNING = [pygame.image.load(f'{ASSETS}Dino/Dinorun1.png'),
           pygame.image.load(f'{ASSETS}Dino/Dinorun2.png')]

DUCKING = [pygame.image.load(f'{ASSETS}Dino/DinoDuck1.png'),
         pygame.image.load(f'{ASSETS}Dino/DinoDuck2.png')]

JUMPING = pygame.image.load(f'{ASSETS}Dino/DinoJump.png')




class Dino: # 공룡 클래스
    X_POS = 80; Y_POS = 310

    def __init__(self) -> None:
        self.run_img = RUNNING; self.duck_img = DUCKING ;self.jump_img = JUMPING
        self.dino_run = True; self.dino_duck=False; self.dino_jump = False

        self.step_index = 0
        self.image = self.run_img[0] 
        self.dino_rect = self.image.get_rect() # 이미지 사각형 정보 
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput) -> None:
        pass

    def draw(self,SCREEN) -> None:
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

print(f'{ASSETS}Other', 'Track.png')

def main():
    run = True
    clock = pygame.time.Clock()
    dino = Dino()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255,255,255)) # 배경흰색
        userInput = pygame.key.get_pressed()

        dino.draw(SCREEN) #공룡그리기
        dino.update(userInput)

        clock.tick(30)
        pygame.display.update()

if __name__ == '__main__':
    main()