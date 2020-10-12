import time
import threading
from datetime import datetime
from Logic.ApiWrapper import IBapi, createContract, createTrailingStopOrder, create_limit_buy_order, createMktSellOrder
from pytz import timezone
from Research.UpdateCandidates import get_yahoo_stats_for_candidate
from Research.tipRanksScrapper import get_tiprank_ratings_to_Stocks


class IBKRWorker():
    def __init__(self, settings):
        self.app = IBapi()
        self.settings = settings

    def connect_and_prepare(self, status_callback, notification_callback):
        """
Connecting to IBKR API and initiating the connection instance
        :return:
        """
        status_callback.emit("Connecting")
        notification_callback.emit("Begin connect and prepare")
        self.connect_to_tws(notification_callback)
        self.start_tracking_excess_liquidity(notification_callback)
        # start tracking open positions
        self.update_open_positions(notification_callback)
        # start tracking candidates
        self.evaluate_and_track_candidates(notification_callback)
        self.update_target_price_for_tracked_stocks(notification_callback)
        notification_callback.emit("Connected to IBKR and READY")
        status_callback.emit("Connected and ready")


    def connect_to_tws(self, notification_callback):
        """
Creates the connection - starts listner for events
        """
        notification_callback.emit("Starting connection to IBKR")
        self.app.connect('127.0.0.1', int(self.settings.PORT), 123)
        self.app.nextorderId = None
        # Start the socket in a thread
        api_thread = threading.Thread(target=self.run_loop, name='ibkrConnection', daemon=True)
        api_thread.start()
        # Check if the API is connected via orderid
        while True:
            if isinstance(self.app.nextorderId, int):
                notification_callback.emit('Successfully connected to API')
                break
            else:
                notification_callback.emit('Waiting for connection...')
                time.sleep(1)
        # General Account info:
        # self.request_current_PnL()
        # start tracking liquidity

    def add_yahoo_stats_to_live_candidates(self, notification_callback=None):
        """
gets a Yahoo statistics to all tracked candidates and adds it to them
        """
        for k, v in self.app.candidatesLive.items():
            notification_callback.emit("Getting Yahoo market data for " + v['Stock'])
            drop, change = get_yahoo_stats_for_candidate(v['Stock'],notification_callback)
            self.app.candidatesLive[k]["averagePriceDropP"] = drop
            self.app.candidatesLive[k]["averagePriceSpreadP"] = change
            notification_callback.emit(
                "Yahoo market data for " + v['Stock'] + " shows average " + str(drop) + " % drop")

    def add_ratings_to_liveCandidates(self, notification_callback=None):
        """
getting and updating tiprank rank for live candidates
        """
        notification_callback.emit("Getting ranks for :" + str(self.settings.TRANDINGSTOCKS))
        ranks = get_tiprank_ratings_to_Stocks(self.settings.TRANDINGSTOCKS, self.settings.PATHTOWEBDRIVER)
        for k, v in self.app.candidatesLive.items():
            v["tipranksRank"] = ranks[v["Stock"]]
            notification_callback.emit("Updated " + str(v["tipranksRank"]) + " rank for " + v["Stock"])

    def evaluate_and_track_candidates(self, notification_callback=None):
        """
Starts tracking the Candidates and adds the statistics
        """
        notification_callback.emit("Starting to track " + str(len(self.settings.TRANDINGSTOCKS)) + " Candidates")
        # starting querry
        trackedStockN = 1
        for s in self.settings.TRANDINGSTOCKS:
            id = self.app.nextorderId
            notification_callback.emit(
                "starting to track: " + str(trackedStockN) + " of " + str(len(self.settings.TRANDINGSTOCKS)) + " " + s +
                " traking with Id:" +
                str(id))
            c = createContract(s)
            self.app.candidatesLive[id] = {"Stock": s,
                                           "Close": "-",
                                           "Open": "-",
                                           "Bid": "-",
                                           "Ask": "-",
                                           "LastPrice": "-",
                                           "averagePriceDropP": "-",
                                           "averagePriceSpreadP": "-",
                                           "tipranksRank": "-",
                                           "LastUpdate": "-"}
            self.app.reqMarketDataType(1)
            self.app.reqMktData(id, c, '', False, False, [])
            lastID = id
            self.app.nextorderId += 1
            trackedStockN += 1
        time.sleep(1)
        # while self.app.candidatesLive[lastID]["LastPrice"] == '-':
        #     time.sleep(1)
        #     notification_callback.emit("Waiting for last Stock market data to receive")

        # updateYahooStatistics
        self.add_yahoo_stats_to_live_candidates(notification_callback)

        # update TipranksData
        self.add_ratings_to_liveCandidates(notification_callback)

        notification_callback.emit(str(len(self.app.candidatesLive)) + " Candidates evaluated and started to track")

    def process_positions(self, notification_callback=None):
        """
Processes the positions to identify Profit/Loss
        """
        notification_callback.emit("Processing profits")
        for s, p in self.app.openPositions.items():
            profit = p["UnrealizedPnL"] / p["Value"] * 100
            notification_callback.emit("The profit for "+ s+ " is "+ str(profit)+ " %")
            if profit > float(self.settings.PROFIT):
                orders = self.app.openOrders
                if s in orders:
                    notification_callback.emit("Order for "+ s+ "already exist- skipping")
                else:
                    notification_callback.emit("Profit for: "+ s+ " is "+ str(profit)+
                                               "Creating a trailing Stop Order to take a Profit")
                    contract = createContract(s)
                    order = createTrailingStopOrder(p["stocks"], self.settings.TRAIL)
                    self.app.placeOrder(self.app.nextorderId, contract, order)
                    self.app.nextorderId = self.app.nextorderId + 1
                    notification_callback.emit("Created a Trailing Stop order for "+s+ " at level of "+
                                               str(self.settings.TRAIL)+ "%")
                    self.log_decision("profits.txt",
                                      "Created a Trailing Stop order for " + s + " at level of " + self.settings.TRAIL + "%")
            elif profit < float(self.settings.LOSS):
                orders = self.app.openOrders
                if s in orders:
                    notification_callback.emit("Order for "+ s+ "already exist- skipping")
                else:
                    notification_callback.emit("loss for: "+ s+ " is "+ str(profit)+
                                               "Creating a Market Sell Order to minimize the Loss")
                    contract = createContract(s)
                    order = createMktSellOrder(p['stocks'])
                    self.app.placeOrder(self.app.nextorderId, contract, order)
                    self.app.nextorderId = self.app.nextorderId + 1
                    notification_callback.emit("Created a Market Sell order for "+ s)
                    self.log_decision("loses.txt", "Created a Market Sell order for " + s)

    def evaluate_stock_for_buy(self, s, notification_callback=None):
        """
Evaluates stock for buying
        :param s:
        """
        notification_callback.emit("Evaluating "+ s+ "for a Buy")
        # finding stock in Candidates
        for c in self.app.candidatesLive.values():
            if c["Stock"] == s:
                ask_price = c["Ask"]
                average_daily_dropP = c["averagePriceDropP"]
                tipRank = c["tipranksRank"]
                target_price = c["target_price"]
                break

        if ask_price == -1:  # market is closed
            notification_callback.emit('The market is closed skipping...')
        elif ask_price < target_price and float(tipRank) > 8:
            self.buy_the_stock(ask_price, s)
        else:
            notification_callback.emit("The price of :"+str(ask_price)+ "was not in range of :"+ str(average_daily_dropP)+ " % "+
                                       " Or the Rating of "+ str(tipRank)+ " was not good enough")

        pass

    def update_target_price_for_tracked_stocks(self, notification_callback=None):
        """
Update target price for all tracked stocks
        :return:
        """
        notification_callback.emit("Updating target prices for Candidates")
        for c in self.app.candidatesLive.values():
            notification_callback.emit("Updating target price for " + c["Stock"])
            ask_price = c["Ask"]
            close = c["Close"]
            open = c["Open"]
            last = c["LastPrice"]
            average_daily_dropP = c["averagePriceDropP"]
            tipRank = c["tipranksRank"]
            notification_callback.emit("Close:" + str(c["Close"]))
            notification_callback.emit("Open:" + str(c["Open"]))
            notification_callback.emit("LastPrice:" + str(c["LastPrice"]))

            if open != '-':  # market is closed
                c["target_price"] = open - open / 100 * average_daily_dropP
                notification_callback.emit("Target price for " + str(c["Stock"]) + " updated to " + str(
                    c["target_price"]) + " based on Open price")
            elif close != '-':  # market is open
                c["target_price"] = close - close / 100 * average_daily_dropP
                notification_callback.emit("Target price for " + str(c["Stock"]) + " updated to " + str(
                    c["target_price"]) + " based on Close price")
            else:
                c["target_price"] = last - last / 100 * average_daily_dropP
                notification_callback.emit("Target price for " + str(c["Stock"]) + " updated to " + str(
                    c["target_price"]) + " based on last price")

    def buy_the_stock(self, price, s, notification_callback=None):
        """
Creates order to buy a stock at specific price
        :param price: price to buy at limit
        :param s: Stocks to buy
        """
        contract = createContract(s)
        stocksToBuy = int(int(self.settings.BULCKAMOUNT) / price)
        if stocksToBuy > 0:
            order = create_limit_buy_order(stocksToBuy, price)
            self.app.placeOrder(self.app.nextorderId, contract, order)
            self.app.nextorderId = self.app.nextorderId + 1
            notification_callback.emit("Issued the BUY order at ", price, "for ", stocksToBuy, " Stocks of ", s)
            self.log_decision("buys.txt", "Issued the BUY order at " + price + "for " + stocksToBuy + " Stocks of " + s)
        else:
            notification_callback.emit("The single stock is too expensive - skipping")

    def process_candidates(self, notification_callback=None):
        """
processes candidates for buying
        :return:
        """
        excessLiquidity = self.app.excessLiquidity
        if float(excessLiquidity) < 1000:
            notification_callback.emit("Excess liquidity is ", excessLiquidity, " it is less than 1000 - skipping buy")
            return
        else:
            notification_callback.emit("The Excess liquidity is :"+str(excessLiquidity)+ " searching candidates")
            # updating the targets if market was open in the middle
            self.update_target_price_for_tracked_stocks(notification_callback)
            res = sorted(self.app.candidatesLive.items(), key=lambda x: x[1]['tipranksRank'], reverse=True)
            notification_callback.emit(str(len(res))+ "Candidates found,sorted by Tipranks ranks")
            for i, c in res:
                if c['Stock'] in self.app.openPositions:
                    notification_callback.emit("Skipping "+c['Stock']+ " as it is in open positions.")
                    continue
                else:
                    self.evaluate_stock_for_buy(c['Stock'],notification_callback)

    def process_positions_candidates(self, status_callback, notification_callback):
        """
Process Open positions and Candidates
        """
        status_callback.emit("Processing Positions-Candidates ")
        est = timezone('EST')
        fmt = '%Y-%m-%d %H:%M:%S'
        local_time = datetime.now().strftime(fmt)
        est_time = datetime.now(est).strftime(fmt)
        notification_callback.emit("-------Starting Worker...----EST Time: "+ est_time+ "--------------------")

        notification_callback.emit("Checking connection")
        conState = self.app.isConnected()
        if conState:
            notification_callback.emit("Connection is fine- proceeding")
        else:
            notification_callback.emit("Connection lost-reconnecting")
            self.connect_to_tws()

        # collect and update
        self.update_open_orders(notification_callback)
        self.update_open_positions(notification_callback)

        # process
        self.process_candidates(notification_callback)
        self.process_positions(notification_callback)
        notification_callback.emit("...............Worker finished....."+local_time+"....................")


    def run_loop(self):
        self.app.run()

    def update_open_positions(self, notification_callback=None):
        """
updating all openPositions
        """
        # update positions from IBKR
        notification_callback.emit("Updating open Positions:")
        self.app.openPositionsLiveDataRequests = {}  # reset requests dictionary
        self.app.reqPositions()  # requesting open positions
        time.sleep(1)
        lastId = 0
        for s, p in self.app.openPositions.items():  # start tracking one by one
            if s not in self.app.openPositionsLiveDataRequests.values():
                id = self.app.nextorderId
                p["tracking_id"] = id
                self.app.openPositionsLiveDataRequests[id] = s
                self.app.reqPnLSingle(id, self.settings.ACCOUNT, "", p["conId"])
                notification_callback.emit("Started tracking " + s + " position PnL")
                lastId = s
                self.app.nextorderId += 1

        time.sleep(3)
        notification_callback.emit(str(len(self.app.openPositions)) + " open positions updated")

    def update_open_orders(self, notification_callback=None):
        """
Requests all open orders
        """
        notification_callback.emit("Updating all open orders")
        self.app.openOrders = {}
        self.app.reqAllOpenOrders()
        time.sleep(1)

        notification_callback.emit(str(len(self.app.openOrders))+ " open orders found ")

    def start_tracking_excess_liquidity(self, notification_callback=None):
        """
Start tracking excess liquidity - the value is updated every 3 minutes
        """
        # todo: add safety to not buy faster than every 3 minutes
        notification_callback.emit("Starting to track Excess liquidity")
        id = self.app.nextorderId
        self.app.reqAccountSummary(id, "All", "ExcessLiquidity")
        self.app.nextorderId += 1

    def request_current_PnL(self, notification_callback=None):
        """
Creating a PnL request the result will be stored in generalStarus
        """
        global id, status
        id = self.app.nextorderId
        notification_callback.emit("Requesting Daily PnL")
        self.app.reqPnL(id, self.settings.ACCOUNT, "")
        time.sleep(0.5)
        self.app.nextorderId = self.app.nextorderId + 1
        notification_callback.emit(self.app.generalStatus)

    def log_decision(self, logFile, order):
        with open(logFile, "a") as f:
            currentDt = datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
            order = currentDt + '---' + order
            f.write(order)
