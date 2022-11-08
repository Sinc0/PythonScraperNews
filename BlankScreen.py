from kivy.uix.screenmanager import ScreenManager, Screen

class BlankScreen(Screen):
    def __init__(self, **var_args):
        super(BlankScreen, self).__init__(**var_args)
    

    def on_pre_enter(self, *args):
        print("BlankScreen")