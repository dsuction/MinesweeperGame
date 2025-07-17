from rich.console import Console, Style
from rich.table import Table
from rich.progress import Progress
from rich import box
from random import randint


DANGER_STYLE = Style(color='red', blink=True, bold=True)
WIN_STYLE = Style(color='green', blink=True, bold=True)


class Sapper:
    processing_functions = {'w': lambda pos, size_map: {'x': pos['x'], 'y': (pos['y'] - 1) % size_map},
                            'a': lambda pos, size_map: {'x': (pos['x'] - 1) % size_map, 'y': pos['y']},
                            's': lambda pos, size_map: {'x': pos['x'], 'y': (pos['y'] + 1) % size_map},
                            'd': lambda pos, size_map: {'x': (pos['x'] + 1) % size_map, 'y': pos['y']}
                            }
    replacement = {'f': '[red] f ', '#': ' # ', ' ': '   ', '1': '[blue] 1 ', '2': '[green] 2 ',
                   '3': '[#b80404] 3 ', '4': '[#a10303] 4 ', '5': '[#8c0303] 5 ', '6': '[#780202] 6 ',
                   '7': '[#630202] 7 ', '8': '[#4d0202] 8 '}

    def __init__(self, console: Console, size_map: int) -> None:
        self.console = console
        self.size_map = size_map
        self.first_use_e = True
        self.running = True
        self.pos_player = {'x': 0, 'y': 0}
        self.pos_bomb = []
        self.table = [[' ' for _ in range(size_map)] for _ in range(size_map)]

    def progress_bar(self) -> None:
        with Progress() as progress:
            task1 = progress.add_task("[red]Bombs...", total=int(self.size_map ** 2 * 0.25) ** 2)
            for _ in range(sum([row.count('f') for row in self.table])):
                progress.update(task1, advance=int(self.size_map ** 2 * 0.25))

    def process_event(self, event) -> None:
        if event in 'wasd':
            self.move(event)
        elif event == 'e':
            self.open_cell()
        elif event == 'f':
            self.put_flag()

    def move(self, event) -> None:
        self.pos_player: dict = self.processing_functions[event](self.pos_player, self.size_map)

    def put_flag(self) -> None:
        if self.table[self.pos_player['y']][self.pos_player['x']] == ' ':
            self.table[self.pos_player['y']][self.pos_player['x']] = 'f'

    def open_cell(self) -> None:
        recursion_memory = []

        def calculate_value_cells(pos_player: dict) -> None:
            if pos_player in recursion_memory:
                return
            recursion_memory.append(pos_player)
            positions = []
            count_bomb = 0
            for i in (-1, 0, 1):
                for j in (-1, 0, 1):
                    if 0 <= pos_player['x'] + i < self.size_map and 0 <= pos_player['y'] + j < self.size_map:
                        if (pos_player['x'] + i, pos_player['y'] + j) not in self.pos_bomb:
                            positions.append({'x': pos_player['x'] + i, 'y': pos_player['y'] + j})
                        else:
                            count_bomb += 1
            if count_bomb == 0:
                self.table[pos_player['y']][pos_player['x']] = '#'
                for pos in positions:
                    calculate_value_cells(pos)
            else:
                self.table[pos_player['y']][pos_player['x']] = str(count_bomb)

        if self.first_use_e:
            self.pos_bomb = self.generate_pos_bomb(self.size_map, self.pos_player)
            self.first_use_e = False

        if (self.pos_player['x'], self.pos_player['y']) in self.pos_bomb:
            self.running = False
            return
        calculate_value_cells(self.pos_player)

    def print_table(self) -> None:
        self.console.print(self.convert_table())
        self.progress_bar()
        self.check_result_game()

    def convert_table(self) -> Console:
        if not self.running:
            for x, y in self.pos_bomb:
                self.table[y][x] = ' * '
        table_copy: list[list[str]] = [row[:] for row in self.table]
        for y in range(len(self.table)):
            for x in range(len(self.table[y])):
                table_copy[y][x]: str = self.replacement.get(self.table[y][x], '[red] * ')

        if table_copy[y := self.pos_player['y']][x := self.pos_player['x']][-2] != ' ':
            table_copy[y][x] = f'[yellow] {table_copy[self.pos_player['y']][self.pos_player['x']][-2]} '
        else:
            table_copy[y][x] = '[yellow] # '

        rich_table = Table(title='ПОЛЕ', box=box.DOUBLE, show_header=False, show_lines=True)

        for _ in range(len(self.table)):
            rich_table.add_column()
        for index in range(len(self.table)):
            rich_table.add_row(*table_copy[index])

        return rich_table

    def check_result_game(self) -> None:
        if not self.running:
            self.console.print('ВЫ ПРОИГРАЛИ', style=DANGER_STYLE)
            return

        if sum([row.count(' ') + row.count('f') for row in self.table]) == len(self.pos_bomb):
            self.console.print('ВЫ ВЫИГРАЛИ', style=WIN_STYLE)
            self.running = False

    @staticmethod
    def generate_pos_bomb(size_map: int, pos_player: dict) -> list[tuple[int, int]]:
        pos_bomb = []
        count_bomb = 0
        while count_bomb <= int(size_map ** 2 * 0.25):
            x, y = randint(0, size_map - 1), randint(0, size_map - 1)
            if ((x, y) not in ((pos_player['x'] + i, pos_player['y'] + j) for i in (-1, 0, 1) for j in (-1, 0, 1))
                    and [x, y] not in pos_bomb):
                pos_bomb.append((x, y))
                count_bomb += 1
        return pos_bomb


def get_size(console: Console) -> int:
    console.print('Введите размер поля от [green]4[/green] до [green]16[/green]: ', style='blue', end='')
    while True:
        size = input()
        if size.isdigit():
            if 5 <= int(size) <= 16:
                break
            else:
                if int(size) < 5:
                    console.print('Число должно быть больше либо равно 5 :warning:', style=DANGER_STYLE)
                else:
                    console.print('Число должно быть меньше либо равно 16 :warning:', style=DANGER_STYLE)
        else:
            console.print('Некорректный ввод, введите число :warning:', style=DANGER_STYLE)
    console.print('[green]ok[/green]')
    return int(size)


def get_event(console: Console) -> str:
    console.print('Движениe - [green]wasd[/green], поставить флаг - [green]f[/green],'
                  ' открыть клетку - [green]e[/green]', style='blue')
    console.print('Введите команду: ', end='', style='blue')
    while True:
        event = input()
        if event in list('wasdfe'):
            break
        console.print('Нет такой команды :warning:', style=DANGER_STYLE)
    return event


def main():
    console = Console()
    size_map: int = get_size(console)
    sapper = Sapper(console, size_map)
    sapper.print_table()
    while True:
        sapper.process_event(get_event(console))
        sapper.print_table()
        if not sapper.running:
            break


if __name__ == '__main__':
    main()
