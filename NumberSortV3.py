import tkinter as tk
import random

# I didn’t use any particular references to go look up and research what a AVLTree was and just utilized the instruction you gave in class.
# The only assistance/resources I had and utilized really was ChatGPT to help iron out the bugs and help determine a platform to build it on.


def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    left = []
    right = []
    for i in range(1, len(arr)):
        if arr[i] < pivot:
            left.append(arr[i])
        else:
            right.append(arr[i])
    return quicksort(left) + [pivot] + quicksort(right)


class SortingGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sorting Game")
        self.label = tk.Label(self.root, text="Sort the numbers in ascending order:")
        self.label.pack()
        self.canvas = tk.Canvas(self.root, width=400, height=100)
        self.canvas.pack()
        self.button = tk.Button(self.root, text="Solve", command=self.solve, state="disabled")
        self.button.pack()
        self.numbers = [random.randint(1, 100) for _ in range(10)]
        self.draw_numbers()
        self.unsorted_label = tk.Label(self.root, text="Unsorted: {}".format(self.count_unsorted()))
        self.unsorted_label.pack()
        self.dragging = False
        self.dragged_item = None
        self.misplaced = self.count_unsorted()
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.time_left = 60
        self.timer_label = tk.Label(self.root, text="Time left: {}".format(self.time_left))
        self.timer_label.pack()
        self.start_button = tk.Button(self.root, text="Start", command=self.start_game)
        self.start_button.pack()
        self.game_started = False
        self.timer_id = None
        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack()
        self.cheated = False
        self.swapping_enabled = False


    def draw_numbers(self):
        self.canvas.delete("all")
        for i, num in enumerate(self.numbers):
            x = 50 + i * 30
            y = 50
            self.canvas.create_text(x, y, text=str(num))

    def count_unsorted(self):
        count = 0
        for i in range(len(self.numbers) - 1):
            if self.numbers[i] > self.numbers[i+1]:
                count += 1
        return count

    def update_unsorted_label(self):
        self.unsorted_label.config(text="Unsorted: {}".format(self.misplaced))

    def solve(self):
        self.numbers = quicksort(self.numbers)
        self.draw_numbers()
        self.misplaced = 0
        self.update_unsorted_label()
        self.cheated = True

    def on_mouse_down(self, event):
        if not self.swapping_enabled:  # check if swapping is enabled
            return
        item = self.canvas.find_closest(event.x, event.y)[0]
        self.dragging = True
        self.dragged_item = item
        self.canvas.tag_raise(item)

    def on_mouse_drag(self, event):
        if not self.swapping_enabled:  # check if swapping is enabled
            return
        if self.dragging:
            x, y = event.x, event.y
            self.canvas.coords(self.dragged_item, x, y)

    def on_mouse_up(self, event):
        if not self.swapping_enabled:  # check if swapping is enabled
            return
        if self.dragging:
            item = self.dragged_item
            x, y = event.x, event.y
            index = (x - 50) // 30
            if index < 0:
                index = 0
            if index >= len(self.numbers):
                index = len(self.numbers) - 1
            self.numbers.remove(int(self.canvas.itemcget(item, "text")))
            self.numbers.insert(index, int(self.canvas.itemcget(item, "text")))
            self.draw_numbers()
            new_misplaced = self.count_unsorted()
            if new_misplaced < self.misplaced:
                self.misplaced = new_misplaced
                self.update_unsorted_label()
            self.dragging = False
            self.dragged_item = None

    def update_game(self):
        self.time_left -= 1
        self.timer_label.config(text="Time left: {}".format(self.time_left))
        if self.time_left == 0 or self.count_unsorted() == 0:
            self.new_game_button = tk.Button(self.root, text="New Game", command=self.new_game)
            self.new_game_button.pack()
            self.game_started = False
            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<ButtonRelease-1>")
            self.start_button.config(state="normal")
            self.button.config(state="disabled")
            if self.count_unsorted() == 0:
                if self.cheated:  # check if the user clicked the Solve button
                    self.result_label.config(text="You cheated! Try again.")
                else:
                    self.result_label.config(text="You won! Time taken: {} seconds".format(60 - self.time_left))
            else:
                self.result_label.config(text="You lost! Try again.")
        else:
            self.timer_id = self.root.after(1000, self.update_game)

    def new_game(self):
        self.numbers = [random.randint(1, 100) for _ in range(10)]
        self.draw_numbers()
        self.time_left = 60
        self.timer_label.config(text="Time left: {}".format(self.time_left))
        self.unsorted_label.config(text="Unsorted: {}".format(self.count_unsorted()))
        self.game_started = False
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.start_button.config(state="normal")
        self.button.config(state="disabled")
        self.new_game_button.pack_forget()  # hide the New Game button when starting a new game

    def start_game(self):
        self.game_started = True
        self.start_button.config(state="disabled")
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.button.config(state="normal")
        self.timer_label.config(text="Time left: {}".format(self.time_left))
        self.swapping_enabled = True
        # Schedule a call to update_game() every second
        self.root.after(1000, self.update_game)
        self.root.mainloop()

    def start(self):
        self.root.mainloop()


game = SortingGame()
game.start()
