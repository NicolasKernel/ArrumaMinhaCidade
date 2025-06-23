class NavigationController:
    def __init__(self, screen_manager):
        self.sm = screen_manager

    def navigate_to(self, screen_name):
        self.sm.current = screen_name