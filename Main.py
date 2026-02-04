import database
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout


# def popup(message):
#     layout = FloatLayout()
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

def popup(message):

    layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

    layout.add_widget(Label(text=message))
    close_btn = Button(text="OK", size_hint_y=None, height="40dp")
    layout.add_widget(close_btn)

    popup = Popup(content=layout,size_hint=(0.6, 0.3),auto_dismiss=False)
    close_btn.bind(on_release=popup.dismiss)
    popup.open()



# define screens to be referred to in kivy file
class HomeScreen(Screen):
    def deletion(self):
        # clears database then rebuilds it
        database.remove_table("companies")
        database.remove_table("traders")
        database.init_db()
        database.repopulate_db()

class FinancialStatementScreen(Screen):
    def on_enter(self):
        # runs every time you enter this screen
        companies = database.extract_table("companies")
        self.ids.table.clear_widgets()
        # headings for the table
        self.ids.table.add_widget(Label(text="Ticker",color=(0,0,0,1)))
        self.ids.table.add_widget(Label(text="Name",color=(0,0,0,1)))
        self.ids.table.add_widget(Label(text="Share Price",color=(0,0,0,1)))
        self.ids.table.add_widget(Label(text="Market Cap",color=(0,0,0,1)))
        self.ids.table.add_widget(Label(text="Revenue",color=(0,0,0,1)))
        self.ids.table.add_widget(Label(text="Cost",color=(0,0,0,1)))
        self.ids.table.add_widget(Label(text="Profit",color=(0,0,0,1)))
        self.ids.table.add_widget(Label(text="EPS",color=(0,0,0,1)))
        self.ids.table.add_widget(Label(text="Debt",color=(0,0,0,1)))
        # inserting data into the table
        for company in companies:
            for data in company:
                self.ids.table.add_widget(Label(text=str(data),color=(0,0,0,1)))


class PlaceOrderScreen(Screen):
    def buy(self):

        # ensure all values are the correct type
        try:
            ticker = int(self.ids.buy_company_input.text)
            num_of_shares = float(self.ids.buy_num_of_shares_input.text)
            share_price = int(self.ids.buy_share_price_input.text)
        except ValueError:
            popup("Invalid data type entered\n All values must be numbers")
            return
        # ensure all values are not negative
        if ticker < 0 or num_of_shares < 0 or share_price < 0:
            popup("Negative value entered")
            return
        # ensure ticker is within range
        if ticker < 0 or ticker > 11:
            popup("Invalid ticker entered")
            return
        # check if user has enough money
        capital = database.extract_table("traders")[0][1]
        required_capital = num_of_shares * share_price
        if capital < required_capital:
            message = "Insufficient capital. Current Capital: " + str(capital)
            popup(message)
            return

        capital -= required_capital
        database.change_capital(ticker, capital)
        message = "Successfully placed order. Current Capital: " + str(capital)
        popup(message)


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("kivy.kv")
#create an app class that when instantiated runs the app
class Stock_Market_Simulator(App):
    def build(self):
        #runs once when the app starts before any UI is shown
        database.init_db()
        database.repopulate_db()
        return kv


if __name__ == "__main__":
     Stock_Market_Simulator().run()























