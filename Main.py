import database
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label


# define screens to be referred to in kivy file
class HomeScreen(Screen):
    def deletion(self):
        # clears database then rebuilds it
        database.remove_companies()
        database.init_db()
        database.repopulate_db()

class FinancialStatementScreen(Screen):
    def on_enter(self):
        companies = database.extract_table("companies")
        self.ids.table.clear_widgets()
        self.ids.table.add_widget(Label(text="Ticker",color=(0,0,0,1)))
        self.ids.table.add_widget(Label(text="Name",color=(0,0,0,1)))
        self.ids.table.add_widget(Label(text="Share Price",color=(0,0,0,1)))
        self.ids.table.add_widget(Label(text="Market Cap",color=(0,0,0,1)))
        self.ids.table.add_widget(Label(text="Revenue",color=(0,0,0,1)))
        self.ids.table.add_widget(Label(text="Cost",color=(0,0,0,1)))
        self.ids.table.add_widget(Label(text="Profit",color=(0,0,0,1)))
        self.ids.table.add_widget(Label(text="EPS",color=(0,0,0,1)))
        self.ids.table.add_widget(Label(text="Debt",color=(0,0,0,1)))

        for company in companies:
            for data in company:
                self.ids.table.add_widget(Label(text=str(data),color=(0,0,0,1)))


class PlaceOrderScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("kivy.kv")
#create an app class that when instantiated runs the app
class Stock_Market_Simulator(App):
    def build(self):
        database.init_db()
        database.repopulate_db()
        return kv


if __name__ == "__main__":
     Stock_Market_Simulator().run()























