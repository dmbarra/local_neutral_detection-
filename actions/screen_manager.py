import tkinter as tk


class ScreenAreaSelector:
    def __init__(self, root, area_limit=2):
        self.start_x = None
        self.start_y = None
        self.rect_id = None
        self.selected_areas = []  # To store selected areas (x, y, width, height)
        self.area_limit = area_limit  # Number of areas to select
        self.callback = None  # Callback for when areas are selected

        self.root = root
        self.overlay = tk.Toplevel(self.root)  # Create an overlay window
        self.overlay.attributes("-fullscreen", True)  # Make the window fullscreen
        self.overlay.attributes("-alpha", 0.3)  # Set transparency to 30%
        self.overlay.config(cursor="cross")  # Use a cross cursor for selection

        # Create a canvas for drawing
        self.canvas = tk.Canvas(self.overlay, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Bind mouse events
        self.canvas.bind("<Button-1>", self.start_selection)  # Left mouse button pressed
        self.canvas.bind("<B1-Motion>", self.update_selection)  # Mouse dragging
        self.canvas.bind("<ButtonRelease-1>", self.end_selection)  # Left mouse button released

    def start_selection(self, event):
        """
        Start drawing a rectangle.
        """
        self.start_x = event.x
        self.start_y = event.y
        self.rect_id = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y, outline="red", width=2
        )

    def update_selection(self, event):
        """
        Update the rectangle as the user drags the mouse.
        """
        if self.rect_id is not None:
            self.canvas.coords(self.rect_id, self.start_x, self.start_y, event.x, event.y)

    def end_selection(self, event):
        """
        Finalize the rectangle and save its coordinates.
        """
        if self.rect_id is not None:
            x1, y1, x2, y2 = self.canvas.coords(self.rect_id)
            x, y = min(x1, x2), min(y1, y2)  # Top-left corner
            width, height = abs(x2 - x1), abs(y2 - y1)  # Width and height
            self.selected_areas.append((x, y, width, height))

            # Check if we've reached the area limit
            if len(self.selected_areas) == self.area_limit:
                self.overlay.destroy()  # Close the selector overlay
                if self.callback:
                    self.callback(self.selected_areas)  # Trigger the callback with the areas

    def run(self, callback):
        """
        Run the selection tool and set a callback for the selected areas.
        """
        self.callback = callback
        self.overlay.grab_set()  # Lock focus to the overlay
