#import gamea
import sys
import os
import pygame as pg
import game as g

def load_image(name):
  return pg.image.load(os.path.join('img', name + '.png'))

cell = {
  True: load_image('active_cell'),
  False: load_image('inactive_cell')
}
disc = {
  g.Player.black: load_image('black_disc'),
  g.Player.white: load_image('white_disc')
}

size = (width, height) = (cell[True].get_width()*8, cell[True].get_height()*8)
background_color = (255, 255, 255)

if __name__ == '__main__':
  pg.init()
  screen = pg.display.set_mode(size)

  state = g.initialize_game()
  while True:
    for event in pg.event.get():
      if event.type == pg.QUIT:
        sys.exit()
      elif event.type == pg.MOUSEBUTTONUP:
        (cx, cy) = pg.mouse.get_pos()
        cx /= 32
        cy /= 32
        state.update(cx, cy)

    pl = g.playable(state.board, state.turn)
    screen.fill(background_color)
    for y in range(8):
      for x in range(8):
        screen.blit(cell[pl[y,x]], (x*32, y*32))
        if state.board[y,x] != 0:
          screen.blit(disc[g.Player(state.board[y,x])], (x*32, y*32))
    pg.display.flip()

