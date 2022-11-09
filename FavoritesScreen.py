### imports ###
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from NewsFeedScreen import NewsFeedScreen
from StandaloneFunctions import fetch_saved_profiles
from StandaloneFunctions import fetch_saved_favorites


### class ###
class FavoritesScreen(Screen):
    def __init__(self, **var_args):
        super(FavoritesScreen, self).__init__(**var_args)


    def on_pre_enter(self, *args):
        print("FavoritesScreen")

        #clear card widgets
        self.ids.boxLayoutPost.clear_widgets()

        #fetch saved profiles
        savedProfiles = fetch_saved_profiles()

        #set saved profiles count
        totalSavedProfiles = len(savedProfiles)

        #set total layout buttons
        totalButtons = len(self.ids.boxLayoutPost.children)

        #fetch saved favorites
        favorites = fetch_saved_favorites()

        #set saved favorites count
        totalFavorites = len(favorites)

        #fill side panel with buttons
        # for x in range(6):
            # NewsFeedScreen.AddFillerButtons(self)

        #create labels
        lbl1 = Label(size_hint_y = None, size_hint_x = 1, height = 10, text = "")
        lbl2 = Label(size_hint_y = 1, size_hint_x = 1, text = str(len(favorites)) + " Saved Posts", bold = True)
        lbl3 = Label(size_hint_y = None, size_hint_x = 1, height = 10, text = "")

        #add widgets
        self.ids.boxLayoutPost.add_widget(lbl1)
        self.ids.boxLayoutPost.add_widget(lbl2)
        for fav in favorites[::-1]:
            if totalButtons < totalFavorites:
                bl = NewsFeedScreen.createNewsCard(self, fav)
                self.ids.boxLayoutPost.add_widget(bl)
        self.ids.boxLayoutPost.add_widget(lbl3)