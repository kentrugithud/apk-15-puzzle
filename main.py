from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
import random
import webbrowser

# Константы
GRID_SIZE = 4
EMPTY_TILE = GRID_SIZE * GRID_SIZE
TELEGRAM_LINK = "https://t.me/+UN6Wt3U0MYI2OTgy"
GITHUB_LINK = "https://github.com/kentrugithud/15-puzzle-"

class Puzzle15App(App):
    def build(self):
        self.title = "Пятнашки"
        self.moves = 0
        self.board = list(range(1, EMPTY_TILE + 1))
        self.empty_pos = EMPTY_TILE - 1
        
        # Главный layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Заголовок с счетчиком ходов
        self.moves_label = Label(
            text="Ходы: 0",
            size_hint=(1, 0.1),
            color=get_color_from_hex('#FFFFFF'),
            font_size='20sp'
        )
        main_layout.add_widget(self.moves_label)
        
        # Игровое поле
        self.grid = GridLayout(cols=GRID_SIZE, spacing=5, size_hint=(1, 0.7))
        self.create_tiles()
        main_layout.add_widget(self.grid)
        
        # Кнопки
        buttons_layout = BoxLayout(size_hint=(1, 0.2), spacing=10)
        
        shuffle_btn = Button(
            text="Перемешать",
            background_color=get_color_from_hex('#4682B4'),
            on_press=self.shuffle
        )
        
        github_btn = Button(
            text="GitHub",
            background_color=get_color_from_hex('#2F4F4F'),
            on_press=lambda x: webbrowser.open(GITHUB_LINK)
        )
        
        telegram_btn = Button(
            text="Отзыв",
            background_color=get_color_from_hex('#20B2AA'),
            on_press=lambda x: webbrowser.open(TELEGRAM_LINK)
        )
        
        buttons_layout.add_widget(shuffle_btn)
        buttons_layout.add_widget(github_btn)
        buttons_layout.add_widget(telegram_btn)
        
        main_layout.add_widget(buttons_layout)
        
        self.shuffle()
        return main_layout
    
    def create_tiles(self):
        self.grid.clear_widgets()
        self.tiles = []
        
        for i in range(EMPTY_TILE):
            tile_value = self.board[i]
            if tile_value == EMPTY_TILE:
                # Пустая плитка - не кликабельная
                btn = Button(text="", background_color=get_color_from_hex('#333333'))
                # Не bind on_press для пустой плитки!
            else:
                # Обычная плитка - кликабельная
                btn = Button(
                    text=str(tile_value),
                    background_color=get_color_from_hex('#6495ED'),
                    color=get_color_from_hex('#FFFFFF'),
                    font_size='30sp'
                )
                btn.tile_index = i  # Сохраняем индекс плитки
                btn.bind(on_press=self.on_tile_click)
            
            self.tiles.append(btn)
            self.grid.add_widget(btn)
    
    def on_tile_click(self, instance):
        # Получаем позицию плитки из атрибута
        tile_pos = instance.tile_index
        
        if self.is_valid_move(tile_pos):
            self.swap_tiles(tile_pos)
            self.moves += 1
            self.moves_label.text = f"Ходы: {self.moves}"
            
            if self.is_solved():
                self.show_win_popup()
    
    def is_valid_move(self, pos):
        row1, col1 = self.empty_pos // GRID_SIZE, self.empty_pos % GRID_SIZE
        row2, col2 = pos // GRID_SIZE, pos % GRID_SIZE
        
        # Проверяем, является ли плитка соседней с пустой
        return (abs(row1 - row2) == 1 and col1 == col2) or (abs(col1 - col2) == 1 and row1 == row2)
    
    def swap_tiles(self, pos):
        # Меняем плитки местами
        self.board[self.empty_pos], self.board[pos] = self.board[pos], self.board[self.empty_pos]
        
        # Обновляем визуальное представление
        self.update_tile(self.empty_pos)
        self.update_tile(pos)
        
        # Обновляем позицию пустой плитки
        self.empty_pos = pos
    
    def update_tile(self, pos):
        """Обновляет внешний вид одной плитки"""
        tile_value = self.board[pos]
        
        if tile_value == EMPTY_TILE:
            # Пустая плитка
            self.tiles[pos].text = ""
            self.tiles[pos].background_color = get_color_from_hex('#333333')
            # Убираем обработчик клика
            self.tiles[pos].unbind(on_press=self.on_tile_click)
            if hasattr(self.tiles[pos], 'tile_index'):
                delattr(self.tiles[pos], 'tile_index')
        else:
            # Обычная плитка
            self.tiles[pos].text = str(tile_value)
            self.tiles[pos].background_color = get_color_from_hex('#6495ED')
            # Добавляем обработчик клика
            self.tiles[pos].bind(on_press=self.on_tile_click)
            self.tiles[pos].tile_index = pos  # Сохраняем индекс
    
    def update_tiles(self):
        """Обновляет все плитки"""
        for i in range(EMPTY_TILE):
            self.update_tile(i)
    
    def shuffle(self, instance=None):
        self.moves = 0
        self.moves_label.text = "Ходы: 0"
        self.board = list(range(1, EMPTY_TILE + 1))
        self.empty_pos = EMPTY_TILE - 1
        
        # Делаем случайные ходы для перемешивания
        for _ in range(1000):
            possible_moves = self.get_possible_moves()
            if possible_moves:
                move = random.choice(possible_moves)
                self.swap_tiles(move)
        
        self.update_tiles()
    
    def get_possible_moves(self):
        moves = []
        row, col = self.empty_pos // GRID_SIZE, self.empty_pos % GRID_SIZE
        
        if row > 0:
            moves.append(self.empty_pos - GRID_SIZE)
        if row < GRID_SIZE - 1:
            moves.append(self.empty_pos + GRID_SIZE)
        if col > 0:
            moves.append(self.empty_pos - 1)
        if col < GRID_SIZE - 1:
            moves.append(self.empty_pos + 1)
            
        return moves
    
    def is_solved(self):
        # Проверяем, все ли плитки на своих местах
        for i in range(EMPTY_TILE - 1):  # Проверяем все кроме последней
            if self.board[i] != i + 1:
                return False
        return True
    
    def show_win_popup(self):
        content = BoxLayout(orientation='vertical', spacing=10)
        content.add_widget(Label(text=f"Поздравляем!\nВы решили головоломку за {self.moves} ходов!"))
        
        close_btn = Button(text="OK", size_hint=(1, 0.4))
        popup = Popup(title='Победа!', content=content, size_hint=(0.8, 0.4))
        
        close_btn.bind(on_press=popup.dismiss)
        content.add_widget(close_btn)
        
        popup.open()

if __name__ == '__main__':
    Puzzle15App().run()