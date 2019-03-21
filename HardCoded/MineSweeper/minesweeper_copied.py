import tkinter
import functools
import random
from tkinter.simpledialog import askstring, Dialog
from tkinter.messagebox import showinfo
import os.path


################################################################################

class Game(tkinter.Frame):

    @classmethod
    def main(cls, width, height, mines, auto=None):
        root = tkinter.Tk()
        root.resizable(False, False)
        root.title('MineSweep')
        window = cls(root, width, height, mines, auto)
        root.protocol('WM_DELETE_WINDOW', window.close)
        root.mainloop()

    ################################################################################

    def __init__(self, master, width, height, mines, auto):
        super().__init__(master)
        self.__width = width
        self.__height = height
        self.__mines = mines
        self.__wondering = width * height
        self.__started = False
        self.__playing = True
        self.__build_timer()
        self.__build_buttons()
        self.grid()

        self.auto = auto

        self.run()

    def run(self):
        while self.__playing:
            grids = []
            for row in self.__buttons:
                grids.append([button['text'] for button in row])

            x, y = self.auto(grids)  # coordinates of the button to push

            self.__buttons[x][y].invoke()

    def close(self):
        self.quit()

    def __build_timer(self):
        self.__secs = tkinter.IntVar()
        self.__timer = tkinter.Label(textvariable=self.__secs)
        self.__timer.grid(columnspan=self.__width, sticky=tkinter.EW)
        self.__after_handle = None

    def __build_buttons(self):
        self.__reset_button = tkinter.Button(self)
        self.__reset_button['text'] = 'Reset'
        self.__reset_button['command'] = self.__reset
        self.__reset_button.grid(column=0, row=1,
                                 columnspan=self.__width, sticky=tkinter.EW)
        self.__reset_button.blink_handle = None
        self.__buttons = []
        for y in range(self.__height):
            row = []
            for x in range(self.__width):
                button = tkinter.Button(self, width=2, height=1,
                                        text='?', fg='red')
                button.grid(column=x, row=y + 2)
                command = functools.partial(self.__push, x, y)
                button['command'] = command
                row.append(button)
            self.__buttons.append(row)

    def __reset(self):
        for row in self.__buttons:
            for button in row:
                button.config(text='?', fg='red')
        self.__started = False
        self.__playing = True
        self.__wondering = self.__width * self.__height
        if self.__after_handle is not None:
            self.after_cancel(self.__after_handle)
            self.__after_handle = None
        self.__secs.set(0)

    def __push(self, x, y, real=True):
        button = self.__buttons[y][x]
        if self.__playing:
            if not self.__started:
                self.__build_mines()
                while self.__buttons[y][x].mine:
                    self.__build_mines()
                self.__started = True
                self.__after_handle = self.after(1000, self.__tick)
            if not button.pushed:
                self.__push_button(button, x, y)
            elif real:
                self.__blink(button, button['bg'], 'red')
        elif real:
            self.__blink(button, button['bg'], 'red')

        '''print('=' * 20)
        for row in self.__buttons:
            for button in row:
                print(button['text'], end=' ')
            print()'''

    def __blink(self, button, from_bg, to_bg, times=8):
        if button.blink_handle is not None and times == 8:
            return
        button['bg'] = (to_bg, from_bg)[times & 1]
        times -= 1
        if times:
            blinker = functools.partial(self.__blink, button,
                                        from_bg, to_bg, times)
            functools.update_wrapper(blinker, self.__blink)
            button.blink_handle = self.after(250, blinker)
        else:
            button.blink_handle = None

    def __tick(self):
        self.__after_handle = self.after(1000, self.__tick)
        self.__secs.set(self.__secs.get() + 1)

    def __push_button(self, button, x, y):
        button.pushed = True
        if button.mine:
            button['text'] = 'X'
            self.__playing = False
            self.after_cancel(self.__after_handle)
            self.__after_handle = None
            self.__blink(self.__reset_button, button['bg'], 'red')
        else:
            button['fg'] = 'SystemButtonText'
            count = self.__total(x, y)
            button['text'] = count and str(count) or ' '
            self.__wondering -= 1
            if self.__wondering == self.__mines:
                self.after_cancel(self.__after_handle)
                self.__after_handle = None
                self.__finish_game()

    def __finish_game(self):
        self.__playing = False
        self.score = self.__secs.get()
        for row in self.__buttons:
            for button in row:
                if button.mine:
                    button['text'] = 'X'

    def __total(self, x, y):
        count = 0
        for x_offset in range(-1, 2):
            x_index = x + x_offset
            for y_offset in range(-1, 2):
                y_index = y + y_offset
                if 0 <= x_index < self.__width and 0 <= y_index < self.__height:
                    count += self.__buttons[y_index][x_index].mine
        if not count:
            self.__propagate(x, y)
        return count

    def __propagate(self, x, y):
        for x_offset in range(-1, 2):
            x_index = x + x_offset
            for y_offset in range(-1, 2):
                y_index = y + y_offset
                if 0 <= x_index < self.__width and 0 <= y_index < self.__height:
                    self.__push(x_index, y_index, False)

    def __build_mines(self):
        mines = [True] * self.__mines
        empty = [False] * (self.__width * self.__height - self.__mines)
        total = mines + empty
        random.shuffle(total)
        iterator = iter(total)
        for row in self.__buttons:
            for button in row:
                button.mine = next(iterator)
                button.pushed = False
                button.blink_handle = None


################################################################################

if __name__ == '__main__':
    Game.main(10, 10, 10)
