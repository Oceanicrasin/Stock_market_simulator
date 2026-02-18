import database
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
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

def check_for_buy_match(b_trader_id,ticker,b_share_price,num_of_shares,total_value):
    while True:
        offers = database.extract_company_orders("sell", ticker)
        database.add_order("buy",b_trader_id, ticker, b_share_price, num_of_shares, total_value)
        buy_offer = database.get_last_record("buy_order_book","buy_order_id")[0]
        # end the function if there are no sell orders
        if not offers:
            return
        offer = offers[0]
        sell_price = offer[3]
        # end function is buy order is below lowest sell offer
        if b_share_price < sell_price:
            return
        # else try to match with the lowest sell offer
        s_num_of_shares = offer[4]
        s_total_value = offer[5]
        if num_of_shares < s_num_of_shares:
            # execute on common shares
            execute_trade(buy_offer,offer,sell_price,num_of_shares)
            s_num_of_shares -= num_of_shares
            s_total_value = s_num_of_shares * sell_price
            s_trader_id = offer[1]
            # create new sell order on remaining shares
            database.add_order("sell",s_trader_id ,ticker, sell_price, s_num_of_shares, s_total_value)
            return
        elif num_of_shares == s_num_of_shares:
            execute_trade(buy_offer,offer,sell_price,num_of_shares)
            return
        else:
            # execute on common shares
            execute_trade(buy_offer,offer,sell_price,s_num_of_shares)
            # repeat the function but with the buy order having less shares
            num_of_shares -= s_num_of_shares
            total_value = num_of_shares * b_share_price

def check_for_sell_match(s_trader_id,ticker,s_share_price,num_of_shares,total_value):
    while True:
        offers = database.extract_company_orders("buy", ticker)
        database.add_order("sell",s_trader_id, ticker, s_share_price, num_of_shares, total_value)
        sell_offer = database.get_last_record("sell_order_book","sell_order_id")[0]
        # end the function if there are no sell orders
        if not offers:
            return
        offer = offers[0]
        buy_price = offer[3]
        # end function is sell order is above highest buy offer
        if s_share_price > buy_price:
            return
        # else try to match with the highest buy offer
        b_num_of_shares = offer[4]
        b_total_value = offer[5]
        if num_of_shares < b_num_of_shares:
            # execute on common shares
            execute_trade(offer,sell_offer,buy_price,num_of_shares)
            b_num_of_shares -= num_of_shares
            b_total_value = b_num_of_shares * buy_price
            b_trader_id = offer[1]
            # create new buy order on remaining shares
            database.add_order("buy",b_trader_id ,ticker, buy_price, b_num_of_shares,b_total_value)
            return
        elif num_of_shares == b_num_of_shares:
            execute_trade(offer,sell_offer,buy_price,num_of_shares)
            return
        else:
            # execute on common shares
            execute_trade(offer,sell_offer,buy_price,b_num_of_shares)
            # repeat the function but with the buy order having less shares
            num_of_shares -= b_num_of_shares
            total_value = num_of_shares * s_share_price


def execute_trade(b_offer, s_offer,share_price,num_of_shares):
    b_trader_id = b_offer[1]
    ticker = b_offer[2]
    b_share_price = b_offer[3]
    s_trader_id = s_offer[1]
    s_share_price = s_offer[3]
    total_value = share_price * num_of_shares
    #1 Remove sell and buy offer from table
    database.remove_order("sell",s_offer[0])
    database.remove_order("buy", b_offer[0])
    #2 Add the record to transaction_history
    database.add_transaction(b_trader_id,"buy",ticker,share_price,num_of_shares,total_value)
    database.add_transaction(s_trader_id, "sell", ticker, share_price, num_of_shares, total_value)
    #3 Update the sellers capital
    database.update_capital(s_trader_id,total_value)
    #4 Update sellers current positions
    s_position = database.extract_current_portfolio(s_trader_id,ticker)
    if num_of_shares == s_position[0][3]:
        #remove record
        database.remove_position(s_trader_id,ticker)
    elif num_of_shares < s_position[0][3]:
        #update record
        post_num_of_shares = s_position[0][3] - num_of_shares
        database.update_position_amount(s_trader_id,ticker,post_num_of_shares,s_position[0][2])
    #5 Update buyers positions
    b_position = database.extract_current_portfolio(b_trader_id,ticker)
    if not b_position:
        #add record
        database.add_position(b_trader_id,ticker,s_share_price,num_of_shares,total_value)
    else:
        #update record
        pre_num_of_shares = b_position[0][3]
        pre_avg_price = b_position[0][2]
        post_num_of_shares = pre_num_of_shares + num_of_shares

        avg_price = ((pre_avg_price * pre_num_of_shares) + (share_price * num_of_shares)) / post_num_of_shares
        database.update_position_amount(b_trader_id,ticker,post_num_of_shares,avg_price)
    #6 update the buyers capital
    # add back capital that was deducted at time of order then subtract capital used in the order
    capital_change = (b_share_price*num_of_shares)- (share_price * num_of_shares)
    database.update_capital(b_trader_id,capital_change)
    #7 update the share price values
    database.update_share_price(share_price,ticker)



# define screens to be referred to in kivy file
class HomeScreen(Screen):
    def deletion(self):
        # clears database then rebuilds it
        database.print_db("companies")
        database.print_db("traders")
        database.print_db("current_positions")
        database.print_db("transaction_history")
        database.clear_db()
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
            num_of_shares = int(self.ids.buy_num_of_shares_input.text)
            share_price = float(self.ids.buy_share_price_input.text)
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
        database.set_capital(ticker, capital)
        check_for_buy_match(0,ticker,share_price,num_of_shares,required_capital)
        database.print_db("buy_order_book")
        message = "Successfully placed order. Current Capital: " + str(capital)
        popup(message)



    def sell(self):

        # ensure all values are the correct type
        try:
            ticker = int(self.ids.sell_company_input.text)
            num_of_shares = float(self.ids.sell_num_of_shares_input.text)
            share_price = int(self.ids.sell_share_price_input.text)
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
        # check if user has a sufficient amount of shares
        positions = database.extract_table("current_positions")
        for position in positions:
            if position[1] == ticker:
                if position[3] >= num_of_shares:
                    message = "Successfully placed order."
                    popup(message)
                    check_for_sell_match(0, ticker, share_price, num_of_shares, share_price*num_of_shares)
                    database.print_db("sell_order_book")
                    return
                else:
                    popup("You do not own enough of this stock")
                    return
        popup("You do not own this stock")
        return


class PortfolioScreen(Screen):
    def on_enter(self):
        # runs every time you enter this screen
        positions = database.extract_table("current_positions")
        capital = database.extract_table("traders")[0][1]
        print("Test Capital:"+str(database.extract_table("traders")[1][1]))
        self.add_widget(Label(text="Current Capital:"+str(capital), color=(0, 0, 0, 1)))
        self.ids.portfolio_table.clear_widgets()
        # headings for the table
        self.ids.portfolio_table.add_widget(Label(text="Trader_id",color=(0,0,0,1)))
        self.ids.portfolio_table.add_widget(Label(text="Ticker",color=(0,0,0,1)))
        self.ids.portfolio_table.add_widget(Label(text="Avg_price",color=(0,0,0,1)))
        self.ids.portfolio_table.add_widget(Label(text="Num_of_shares",color=(0,0,0,1)))
        self.ids.portfolio_table.add_widget(Label(text="Total Value",color=(0,0,0,1)))
        self.ids.portfolio_table.add_widget(Label(text="Profit",color=(0,0,0,1)))
        # inserting data into the table
        for position in positions:
            for data in position:
                self.ids.portfolio_table.add_widget(Label(text=str(data),color=(0,0,0,1)))


class WindowManager(ScreenManager):
    pass

class OrderBook(Screen):
    def on_enter(self):
        # runs every time you enter this screen
        buy_orders = database.extract_table("buy_order_book")
        self.ids.buy_order_table.clear_widgets()
        # headings for the table
        self.ids.buy_order_table.add_widget(Label(text="Buy_order_id",color=(0,0,0,1)))
        self.ids.buy_order_table.add_widget(Label(text="Trader_id",color=(0,0,0,1)))
        self.ids.buy_order_table.add_widget(Label(text="Ticker",color=(0,0,0,1)))
        self.ids.buy_order_table.add_widget(Label(text="Share_price",color=(0,0,0,1)))
        self.ids.buy_order_table.add_widget(Label(text="Num_of_shares",color=(0,0,0,1)))
        self.ids.buy_order_table.add_widget(Label(text="total_value",color=(0,0,0,1)))
        # inserting data into the table
        for order in buy_orders:
            for data in order:
                self.ids.buy_order_table.add_widget(Label(text=str(data),color=(0,0,0,1)))
        sell_orders = database.extract_table("sell_order_book")
        self.ids.sell_order_table.clear_widgets()
        # headings for the table
        self.ids.sell_order_table.add_widget(Label(text="Sell_order_id",color=(0,0,0,1)))
        self.ids.sell_order_table.add_widget(Label(text="Trader_id",color=(0,0,0,1)))
        self.ids.sell_order_table.add_widget(Label(text="Ticker",color=(0,0,0,1)))
        self.ids.sell_order_table.add_widget(Label(text="Share_price",color=(0,0,0,1)))
        self.ids.sell_order_table.add_widget(Label(text="Num_of_shares",color=(0,0,0,1)))
        self.ids.sell_order_table.add_widget(Label(text="total_value",color=(0,0,0,1)))
        for order in sell_orders:
            for data in order:
                self.ids.sell_order_table.add_widget(Label(text=str(data),color=(0,0,0,1)))



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
