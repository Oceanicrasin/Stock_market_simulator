import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen


class HomeScreen(Screen):
    pass

class PlaceOrderScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("kivy.kv")
class Stock_Market_Simulator(App):
    def build(self):
        return kv


if __name__ == "__main__":
     Stock_Market_Simulator().run()























