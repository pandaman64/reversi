import sys
import os
import pygame as pg
import game as g

def load_image(name):
  return pg.image.load(os.path.join('img', name + '.png'))

cell = {
  True: load_image('active_cell_big'),
  False: load_image('inactive_cell_big')
}
disc = {
  g.Player.black: load_image('black_disc_big'),
  g.Player.white: load_image('white_disc_big')
}

cell_size = (cell_width, cell_height) = cell[True].get_size()
screen_size = (width, height) = (cell_width*8, cell_height*8+50)
background_color = (255, 255, 255)
font_color = (0, 0, 0)
font_size = 30
text_coord = (10, cell_height*8 + 10)
auto = False

def show_board(state, screen, font, text_pairs):
  screen.fill(background_color)
  for y in range(8):
    for x in range(8):
      coord = (x*cell_width, y*cell_height)
      screen.blit(cell[state.is_valid_move(x, y)], coord)
      if not state.is_cell_empty(x, y):
        screen.blit(disc[state.disc_owner(x, y)], coord)
  for text, coord in text_pairs:
    screen.blit(font.render(text, True, font_color), coord)
  pg.display.flip()

def bounds_check(x, y):
  return x >= 0 and x < 8 and y >= 0 and y < 8

if __name__ == '__main__':
  pg.init()
  screen = pg.display.set_mode(screen_size)
  font = pg.font.SysFont(pg.font.get_default_font(), font_size)

  state = g.initialize_game()
  while True:
    for event in pg.event.get():
      if event.type == pg.QUIT:
        sys.exit()
      elif not auto and event.type == pg.MOUSEBUTTONUP:
        (cx, cy) = pg.mouse.get_pos()
        cx //= cell_width
        cy //= cell_height
        if bounds_check(cx, cy) and state.is_valid_move(cx, cy):
          state = state.update(cx, cy)
          if state.is_game_over():
            pass
          elif state.no_valid_moves():
            state = state.skip_turn()

    status = ""
    if auto:
      pass
    else:
      status += "turn: " + state.turn.name
      status += ", (black, white): " + repr(state.disc_count())
      if state.is_game_over():
        outcome = state.game_outcome()
        if outcome == "tie":
          status += ", tie"
        else:
          status += ", Winner: " + outcome

    show_board(state, screen, font, [(status, text_coord)])

