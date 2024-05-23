from __future__ import annotations

from typing import TYPE_CHECKING, Union, List

if TYPE_CHECKING:
    from pybehave.GUIs.GUI import GUI

import pygame

from pybehave.Elements.Element import Element


class InfoBoxElement(Element):

    def __init__(self, tg: GUI, x: int, y: int, w: int, h: int, label: str, label_pos: str, text: list[str], f_size: int = 14, SF: float = None):
        super().__init__(tg, x, y, pygame.Rect(x, y, w, h), SF)
        self.label_pos = label_pos  # 'TOP','LEFT','RIGHT', or 'BOTTOM'
        self.surface_color = (255, 255, 255)
        bw = int(self.SF*2)
        self.label = label
        self.text = text
        self.buffer_text = text
        self.f_size = int(self.SF * f_size)
        w = self.SF * w
        h = self.SF * h
        self.border = pygame.Rect(self.x-bw, self.y-bw, w+2*bw, h+2*bw)
        self.pt1 = self.x, self.y
        self.pt2 = self.x+w, self.y
        self.pt3 = self.x+w, self.y+h
        self.pt4 = self.x, self.y+h
        self.font = pygame.font.SysFont('arial', self.f_size)
        self._lbl = self.font.render(self.label, True, (0, 0, 0))

    def has_updated(self) -> bool:
        return self.text != self.buffer_text

    def set_text(self, new_text: Union[str, List]):
        if isinstance(new_text, str):
            self.text = [new_text]
        else:
            self.text = new_text

    def draw(self) -> None:
        self.buffer_text = self.text
        # Draw Box
        pygame.draw.rect(self.screen, (0, 0, 0), self.border)
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect)
        txt_color = (0, 0, 0)

        # WRITE LABEL
        lbl_ht = self._lbl.get_height()
        lbl_wd = self._lbl.get_width()
        if self.label_pos == 'BOTTOM':
            lbl_x = (self.rect.width - lbl_wd)/2  # Center in box
            lbl_y = self.rect.height  # Below Box
        elif self.label_pos == 'TOP':
            lbl_x = (self.rect.width - lbl_wd)/2  # Center in box
            lbl_y = - 20 * self.SF  # Above box
        elif self.label_pos == 'LEFT':
            lbl_x = - lbl_wd - 5 * self.SF
            lbl_y = (self.rect.height - lbl_ht)/2
        else:
            lbl_x = self.rect.width + 5 * self.SF
            lbl_y = (self.rect.height - lbl_ht)/2

        self.screen.blit(self._lbl, self.rect.move(lbl_x,  lbl_y+1))

        # WRITE TEXT
        lines_in_txt = len(self.buffer_text)
        if lines_in_txt > 0:  # NOT EMPTY BOX, No info_boxes
            msg_in_font = self.font.render(self.buffer_text[0], True, (0, 0, 0))
            msg_ht = msg_in_font.get_height()
            msg_wd = msg_in_font.get_width()

            if lines_in_txt == 1:  # simple info box
                msg_x = (self.rect.width - msg_wd)/2  # Center in box
            else:  # lines_in_txt > 1:
                msg_x = +5 * self.SF  # MULTIPLE LINE INFO BOX: Indent 5 pixels from box left

            ln_count = 0
            for line in self.text:
                msg_in_font = self.font.render(line, True, txt_color)
                msg_y = ln_count * msg_ht - 2 * self.SF
                self.screen.blit(msg_in_font, self.rect.move(msg_x,  msg_y+1))
                ln_count += 1
