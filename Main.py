import ast
import configparser
import copy
import json
import sys
import traceback
from datetime import datetime, time
from sys import platform

import pyqtgraph as pg
import requests
from PySide2 import QtGui
from PySide2.QtCore import QRunnable, Slot, QThreadPool, Signal, QObject, QTimer, QTime, Qt
from PySide2.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QWidget, QMessageBox, QListWidgetItem, \
    QDialog
from pytz import timezone

from Logic.IBKRWorker import IBKRWorker
# The bid price refers to the highest price a buyer will pay for a security.
# The ask price refers to the lowest price a seller will accept for a security.
# from Research.tipRanksScrapperRequestsHtmlThreaded import get_tiprank_ratings_to_Stocks
# UI Imports
from UI.MainWindow import Ui_MainWindow
from UI.NewStockWindow import Ui_newStockDlg
from UI.SettingsWindow import Ui_fmSettings
from UI.pos import Ui_position_canvas

LOGFILE = "LOG/log.txt"

global window
global settings


class SettingsCandidate:
    def __init__(self):
        self.ticker = ''
        self.reason = ''


class TimeAxisItem(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        return [datetime.fromtimestamp(value).strftime("%H:%M") for value in values]


class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        `tuple` (exctype, value, traceback.format_exc() )

    result
        `object` data returned from processing, anything

    progress
        `int` indicating % progress

    """
    finished = Signal()  # QtCore.Signal
    error = Signal(tuple)
    result = Signal(object)  # returned by end of function
    status = Signal(object)  # to update a status bar
    notification = Signal(object)  # to update a Console
    progress = Signal(int)  # to use for progress if needed


# noinspection PyUnresolvedReferences
class Worker(QRunnable):
    """
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    """

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['notification_callback'] = self.signals.notification
        self.kwargs['status_callback'] = self.signals.status

    @Slot()
    def run(self):
        """
        Initialise the runner function with passed args, kwargs.
        """

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


class TraderSettings():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.read_config()

    def read_config(self):
        self.config.read('config.ini')
        self.PORT = self.config['Connection']['port']
        self.ACCOUNT = self.config['Account']['acc']
        self.INTERVALUI = self.config['Connection']['INTERVALUI']
        self.INTERVALWORKER = self.config['Connection']['INTERVALWORKER']
        if platform == "linux" or platform == "linux2":
            self.PATHTOWEBDRIVER = self.config['Connection']['linuxpathtowebdriver']
        elif platform == "darwin":  # mac os
            self.PATHTOWEBDRIVER = self.config['Connection']['macPathToWebdriver']
        elif platform == "win32":
            self.PATHTOWEBDRIVER = self.config['Connection']['winPathToWebdriver']
        # alg
        self.PROFIT = self.config['Algo']['gainP']
        self.LOSS = self.config['Algo']['lossP']
        self.TRAIL = self.config['Algo']['trailstepP']
        self.BULCKAMOUNT = self.config['Algo']['bulkAmountUSD']
        self.TRANDINGSTOCKS = ast.literal_eval(self.config['Algo']['TrandingStocks'])

        self.CANDIDATES = []
        candidates_string = self.config['Algo']['candidates']
        jdata = json.loads(candidates_string)
        for c in jdata:
            ticker = c['ticker']
            reason = c['reason']
            ca = SettingsCandidate()
            ca.ticker = ticker
            ca.reason = reason
            self.CANDIDATES.append(ca)

        self.TECHFROMHOUR = self.config['Connection']['techfromHour']
        self.TECHFROMMIN = self.config['Connection']['techfromMin']
        self.TECHTOHOUR = self.config['Connection']['techtoHour']
        self.TECHTOMIN = self.config['Connection']['techtoMin']

        self.UIDEBUG=self.config['Soft']['uidebug']

    def write_config(self):
        self.config['Connection']['port'] = self.PORT
        self.config['Account']['acc'] = self.ACCOUNT
        self.config['Connection']['INTERVALUI'] = str(self.INTERVALUI)
        self.config['Connection']['INTERVALWORKER'] = str(self.INTERVALWORKER)
        if platform == "linux" or platform == "linux2":
            self.config['Connection']['linuxpathtowebdriver'] = self.PATHTOWEBDRIVER
        elif platform == "darwin":  # mac os
            self.config['Connection']['macPathToWebdriver'] = self.PATHTOWEBDRIVER
        elif platform == "win32":
            self.config['Connection']['winPathToWebdriver'] = self.PATHTOWEBDRIVER
        # alg
        self.config['Algo']['gainP'] = str(self.PROFIT)
        self.config['Algo']['lossP'] = str(self.LOSS)
        self.config['Algo']['trailstepP'] = str(self.TRAIL)
        self.config['Algo']['bulkAmountUSD'] = str(self.BULCKAMOUNT)
        self.config['Algo']['TrandingStocks'] = str(self.TRANDINGSTOCKS)
        json_string = json.dumps([ob.__dict__ for ob in self.CANDIDATES])
        self.config['Algo']['Candidates'] = json_string
        self.config['Connection']['techfromHour'] = str(self.TECHFROMHOUR)
        self.config['Connection']['techfromMin'] = str(self.TECHFROMMIN)
        self.config['Connection']['techtoHour'] = str(self.TECHTOHOUR)
        self.config['Connection']['techtoMin'] = str(self.TECHTOMIN)

        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, settings):
        # mandatory
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.settings = settings
        self.ibkrworker = IBKRWorker(self.settings)
        self.threadpool = QThreadPool()
        self.setWindowTitle("Algo Traider v 1.0")

        sys.stderr = open('LOG/errorLog.txt', 'w')

        self.create_open_positions_grid()

        # # redirecting Cosole to UI and Log
        # sys.stdout = OutLog(self.consoleOut, sys.stdout)
        # sys.stderr = OutLog(self.consoleOut, sys.stderr)

        # setting a timer for Worker

        self.uiTimer = QTimer()
        self.uiTimer.timeout.connect(self.update_ui)

        self.workerTimer = QTimer()
        self.workerTimer.timeout.connect(self.run_worker)

        # connecting a buttons
        self.chbxProcess.stateChanged.connect(self.process_checked)
        self.btnSettings.pressed.connect(self.show_settings)

        self.statusbar.showMessage("Ready")
        self.update_session_state()

        self.connect_to_ibkr()

        # if not bool(self.settings.UIDEBUG):
        #     self.connect_to_ibkr()
        # else:
        #     self.btnSettings.setEnabled(True)
        StyleSheet = '''
        #lcdPNLgreen {
            border: 3px solid green;
        }
        #lcdPNLred {
            border: 3px solid red;
        }
        '''
        self.setStyleSheet(StyleSheet)

    # noinspection PyUnresolvedReferences
    def connect_to_ibkr(self):
        """
Starts the connection to the IBKR terminal in separate thread
        """

        connector = Worker(self.ibkrworker.connect_and_prepare)  # Any other args, kwargs are passed to the run function
        connector.signals.result.connect(self.update_ui)
        connector.signals.status.connect(self.update_status)
        connector.signals.notification.connect(self.update_console)
        # Execute
        self.threadpool.start(connector)

    def process_checked(self):
        """
Starts the Timer with interval from Config file
        """
        if self.chbxProcess.isChecked():
            self.run_worker()
            self.workerTimer.start(int(self.settings.INTERVALWORKER) * 1000)
        else:
            self.workerTimer.stop()

    # noinspection PyUnresolvedReferences
    def run_worker(self):
        """
Executed the Worker in separate thread
        """
        currentTime = QTime().currentTime()
        fromTime = QTime(int(self.settings.TECHFROMHOUR), int(self.settings.TECHFROMMIN))
        toTime = QTime(int(self.settings.TECHTOHOUR), int(self.settings.TECHTOMIN))
        sessionState = self.lblMarket.text()
        if currentTime > fromTime and currentTime < toTime:
            print("Worker skept-Technical break : ", fromTime.toString("hh:mm"), " to ", toTime.toString("hh:mm"))
            self.update_console("Technical break untill " + toTime.toString("hh:mm"))

        else:
            self.update_console("Starting Worker- UI Paused")
            self.uiTimer.stop()  # to not cause an errors when lists will be resetted
            worker = Worker(
                self.ibkrworker.process_positions_candidates)  # Any other args, kwargs are passed to the run function
            worker.signals.result.connect(self.update_ui)
            worker.signals.status.connect(self.update_status)
            worker.signals.notification.connect(self.update_console)
            # Execute
            self.threadpool.start(worker)

    def update_ui(self):
        """
Updates UI after connection/worker execution
        """
        # main data
        self.lAcc.setText(self.settings.ACCOUNT)
        # self.lExcessLiquidity.setText(str(self.ibkrworker.app.excessLiquidity))
        # self.lSma.setText(str(self.ibkrworker.app.sMa))
        if hasattr(self.ibkrworker.app, 'smaWithSafety'):
            self.lSma.setText(str(round(self.ibkrworker.app.smaWithSafety,1)))
        else:
            self.lSma.setText(str(round(self.ibkrworker.app.sMa,1)))
        self.lMarketValue.setText(str(self.ibkrworker.app.netLiquidation))
        self.lblAvailTrades.setText(str(self.ibkrworker.app.tradesRemaining))
        self.lcdPNL.display(self.ibkrworker.app.dailyPnl)
        if self.ibkrworker.app.dailyPnl > 0:
            palette = self.lcdPNL.palette()
            palette.setColor(palette.WindowText, QtGui.QColor(51, 153, 51))
            self.lcdPNL.setPalette(palette)
        elif self.ibkrworker.app.dailyPnl < 0:
            palette = self.lcdPNL.palette()
            palette.setColor(palette.WindowText, QtGui.QColor(255, 0, 0))
            self.lcdPNL.setPalette(palette)

        total_positions_value = 0
        for p in self.ibkrworker.app.openPositions.values():
            total_positions_value += p["Value"]
        self.lPositionsTotalValue.setText(str(round(total_positions_value, 1)))

        self.update_open_positions()
        self.update_live_candidates()
        self.update_open_orders()

        # everything disabled for safety - is now enabled
        self.chbxProcess.setEnabled(True)
        self.btnSettings.setEnabled(True)

        self.update_session_state()

        if not self.uiTimer.isActive():
            self.update_console("UI resumed.")
        self.uiTimer.start(int(self.settings.INTERVALUI) * 1000)  # reset the ui timer

    def update_session_state(self):
        est = timezone('US/Eastern')
        fmt = '%Y-%m-%d %H:%M:%S'
        self.est_dateTime = datetime.now(est)
        self.est_current_time = QTime(self.est_dateTime.hour, self.est_dateTime.minute, self.est_dateTime.second)
        self.lblTime.setText(self.est_current_time.toString())
        dStart = QTime(4, 00)
        dEnd = QTime(20, 00)
        tStart = QTime(9, 30)
        tEnd = QTime(16, 0)
        if self.est_current_time > dStart and self.est_current_time <= tStart:
            self.ibkrworker.trading_session_state = "Pre Market"
            self.lblMarket.setText("Pre Market")
        elif self.est_current_time > tStart and self.est_current_time <= tEnd:
            self.ibkrworker.trading_session_state = "Open"
            self.lblMarket.setText("Open")
        elif self.est_current_time > tEnd and self.est_current_time <= dEnd:
            self.ibkrworker.trading_session_state = "After Market"
            self.lblMarket.setText("After Market")
        else:
            self.ibkrworker.trading_session_state = "Closed"
            self.lblMarket.setText("Closed")

    def progress_fn(self, n):
        msgBox = QMessageBox()
        msgBox.setText(str(n))
        retval = msgBox.exec_()

    def update_status(self, s):
        """
Updates StatusBar on event of Status
        :param s:
        """
        self.statusbar.showMessage(s)

    def update_console(self, n):
        """
Adds Message to console- upon event
        :param n:
        """
        self.consoleOut.append(n)
        self.log_message(n)

    def log_message(self, message):
        """
Adds message to the standard log
        :param message:
        """
        with open(LOGFILE, "a") as f:
            currentDt = datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
            message = "\n" + currentDt + '---' + message
            f.write(message)

    def update_live_candidates(self):
        """
Updates Candidates table
        """

        liveCandidates = self.ibkrworker.app.candidatesLive
        try:
            line = 0
            self.tCandidates.setRowCount(len(liveCandidates))
            for k, v in liveCandidates.items():
                self.tCandidates.setItem(line, 0, QTableWidgetItem(v['Stock']))
                self.tCandidates.setItem(line, 1, QTableWidgetItem(str(v['Open'])))
                self.tCandidates.setItem(line, 2, QTableWidgetItem(str(v['Close'])))
                self.tCandidates.setItem(line, 3, QTableWidgetItem(str(v['Bid'])))
                self.tCandidates.setItem(line, 4, QTableWidgetItem(str(v['Ask'])))
                if v['Ask'] < v['target_price'] and v['Ask'] != -1:
                    self.tCandidates.item(line, 4).setBackground(QtGui.QColor(0, 255, 0))
                if v['target_price'] is float:
                    self.tCandidates.setItem(line, 5, QTableWidgetItem(str(round(v['target_price'], 2))))
                else:
                    self.tCandidates.setItem(line, 5, QTableWidgetItem(str(v['target_price'])))
                self.tCandidates.setItem(line, 6, QTableWidgetItem(str(round(v['averagePriceDropP'], 2))))
                self.tCandidates.setItem(line, 7, QTableWidgetItem(str(v['tipranksRank'])))
                if int(v['tipranksRank']) > 7:
                    self.tCandidates.item(line, 7).setBackground(QtGui.QColor(0, 255, 0))
                self.tCandidates.setItem(line, 8, QTableWidgetItem(str(v['LastUpdate'])))

                line += 1
        except Exception as e:
            if hasattr(e, 'message'):
                self.update_console("Error in updating Candidates: " + str(e.message))
            else:
                self.update_console("Error in updating Candidates: " + str(e))

    def update_open_positions(self):
        """
Updates Positions grid
        """
        open_positions = self.ibkrworker.app.openPositions
        allKeys = [*open_positions]
        lastUpdatedWidget = 0
        try:
            for i in range(len(open_positions)):  # Update positions Panels

                widget = self.gp.itemAt(i).widget()
                key = allKeys[i]
                values = open_positions[key]
                if 'stocks' in values.keys():
                    if values['stocks'] != 0:
                        widget.update_view(key, values)
                        widget.show()
                        lastUpdatedWidget = i
                    else:
                        widgetToRemove = self.gp.itemAt(i).widget()
                        widgetToRemove.hide()
                else:
                    print("value not yet received")

            for i in range(self.gp.count()):  # Hide the rest of the panels
                if i > lastUpdatedWidget:
                    widgetToRemove = self.gp.itemAt(i).widget()
                    widgetToRemove.hide()
        except Exception as e:
            if hasattr(e, 'message'):
                self.update_console("Error in refreshing Positions: " + str(e.message))
            else:
                self.update_console("Error in refreshing Positions: " + str(e))

    def create_open_positions_grid(self):
        """
Creates Open positions grid with 99 Positions widgets
        """

        counter = 0
        col = 0
        row = 0

        for i in range(0, 99):
            if counter % 3 == 0:
                col = 0
                row += 1
            self.gp.addWidget(PositionPanel(), row, col)
            counter += 1
            col += 1

    def update_open_orders(self):
        """
Updates Positions table
        """
        openOrders = self.ibkrworker.app.openOrders
        try:
            line = 0
            self.tOrders.setRowCount(len(openOrders))
            for k, v in openOrders.items():
                self.tOrders.setItem(line, 0, QTableWidgetItem(k))
                self.tOrders.setItem(line, 1, QTableWidgetItem(v['Action']))
                self.tOrders.setItem(line, 2, QTableWidgetItem(v['Type']))
                line += 1
        except Exception as e:
            if hasattr(e, 'message'):
                self.update_console("Error in Updating open Orders : " + str(e.message))
            else:
                self.update_console("Error in Updating open Orders : " + str(e))

    def thread_complete(self):
        """
After threaded task finished
        """
        print("TREAD COMPLETE (good or bad)!")

    def show_settings(self):

        self.settingsWindow = SettingsWindow(self.settings)
        self.settingsWindow.show()  # Показываем окно
        # maybe not needed
        self.settingsWindow.changedSettings = False

    def restart_all(self):
        """
Restarts everything after Save
        """
        self.threadpool.waitForDone()
        self.update_console("UI paused- for restart")
        self.uiTimer.stop()

        self.workerTimer.stop()
        self.update_console("Configuration changed - restarting everything")
        self.chbxProcess.setEnabled(False)
        self.chbxProcess.setChecked(False)
        self.btnSettings.setEnabled(False)
        self.ibkrworker.app.disconnect()
        while self.ibkrworker.app.isConnected():
            print("waiting for disconnect")
            time.sleep(1)

        self.ibkrworker = None
        self.ibkrworker = IBKRWorker(self.settings)
        self.connect_to_ibkr()

        i = 4


class PositionPanel(QWidget):
    # def __init__(self, stock, values):
    #     super(PositionPanel, self).__init__()
    #     self.ui = Ui_position_canvas()
    #     self.ui.setupUi(self)
    #
    #
    #     self.update_view()

    def __init__(self):
        super(PositionPanel, self).__init__()
        self.ui = Ui_position_canvas()
        self.ui.setupUi(self)

        # to be able to address it  on refresh
        date_axis = TimeAxisItem(orientation='bottom')
        self.graphWidget = pg.PlotWidget(axisItems={'bottom': date_axis})
        self.ui.gg.addWidget(self.graphWidget)

    def update_view(self, stock, values):
        # Data preparation
        try:
            stock = stock
            number_of_stocks = values['stocks']
            bulk_value = 0
            profit = 0
            bid_price = str(round(values['cost'], 2))
            if 'Value' in values.keys():
                bulk_value = str(round(values['Value'], 2))
            if 'UnrealizedPnL' in values.keys():
                unrealized_pnl = str(round(values['UnrealizedPnL'], 2))
                profit = values['UnrealizedPnL'] / values['Value'] * 100
            if 'LastUpdate' in values.keys():
                last_updatestr = (values['LastUpdate'])
            if 'HistoricalData' in values.keys():
                print("Updating Graph for " + stock + " using " + str(len(values['HistoricalData'])) + " points")
                if len(values['HistoricalData']) > 0:
                    hist_data = values['HistoricalData']
                    dates = []
                    counter = []
                    values = []
                    i = 0
                    for item in hist_data:
                        d = item.date
                        date = datetime.strptime(item.date, '%Y%m%d %H:%M:%S')
                        dates.append(date)
                        values.append(item.close)
                        counter.append(i)
                        i += 1

                    # graph

                    penStock = pg.mkPen(color=(0, 0, 0))
                    penProfit = pg.mkPen(color=(0, 255, 0))
                    penLoss = pg.mkPen(color=(255, 0, 0))

                    self.graphWidget.clear()
                    # self.graphWidget.plot( y=values, pen=penProfit)
                    xline = [x.timestamp() for x in dates]
                    self.graphWidget.plot(x=xline, y=values, pen=penStock, title="1 Last Hour ")
                    self.graphWidget.setBackground('w')
                    self.graphWidget.setTitle(values[-1], color="#d1d1e0", size="16pt")
                    # self.graphWidget.hideAxis('bottom')

            # UI set
            self.ui.lStock.setText(stock)
            self.ui.lVolume.setText(str(int(number_of_stocks)))
            self.ui.lBulckValue.setText(str(bulk_value))
            self.ui.lProfitP.setText(str(round(profit, 2)))

            # setting progressBar and percent label
            self.ui.prgProfit.setTextVisible(False)
            if profit > 0:
                self.ui.prgProfit.setMinimum(0)
                if profit >= int(settings.PROFIT):
                    self.ui.prgProfit.setMaximum(profit * 10)
                else:
                    self.ui.prgProfit.setMaximum(int(settings.PROFIT) * 10)
                self.ui.prgProfit.setValue(int(profit * 10))
                self.ui.prgProfit.setStyleSheet("QProgressBar"
                                                "{"
                                                "border: 2px solid green;"
                                                "}"
                                                "QProgressBar::chunk"
                                                "{"
                                                "background-color: green;"
                                                "}"
                                                )

                palette = self.ui.lProfitP.palette()
                palette.setColor(palette.WindowText, QtGui.QColor(51, 153, 51))
                self.ui.lProfitP.setPalette(palette)
                self.ui.lp.setPalette(palette)

            else:
                self.ui.prgProfit.setMinimum(0)
                if profit <= int(settings.LOSS):
                    self.ui.prgProfit.setMaximum(profit * -10)
                else:
                    self.ui.prgProfit.setMaximum(int(settings.LOSS) * -10)
                self.ui.prgProfit.setValue(int(profit * -10))
                self.ui.prgProfit.setStyleSheet("QProgressBar"
                                                "{"
                                                "border: 2px solid red;"
                                                "}"
                                                "QProgressBar::chunk"
                                                "{"
                                                "background-color: #F44336;"
                                                "}"
                                                )

                palette = self.ui.lProfitP.palette()
                palette.setColor(palette.WindowText, QtGui.QColor(255, 0, 0))
                self.ui.lProfitP.setPalette(palette)
                self.ui.lp.setPalette(palette)
        except Exception as e:
            if hasattr(e, 'message'):
                self.update_console("Error in updating position: " + str(e.message))
            else:
                self.update_console("Error in updating position : " + str(e))


class SettingsWindow(QMainWindow, Ui_fmSettings):
    def __init__(self, inSettings):
        super().__init__()
        self.dlg = StockWindow()
        self.setupUi(self)
        # code
        self.settings = inSettings
        self.settingsBackup = copy.deepcopy(self.settings)
        self.changedSettings = False

    def setting_change(self):
        self.settings.PROFIT = self.spProfit.value()
        self.settings.TRAIL = self.spTrail.value()
        self.settings.LOSS = self.spLoss.value()
        self.settings.BULCKAMOUNT = self.spBulck.value()
        self.settings.ACCOUNT = self.txtAccount.text()
        self.settings.PORT = self.txtPort.text()
        self.settings.INTERVALUI = self.spIntervalUi.value()
        self.settings.INTERVALWORKER = self.spIntervalWorker.value()
        self.settings.TECHFROMHOUR = self.tmTechFrom.time().hour()
        self.settings.TECHFROMMIN = self.tmTechFrom.time().minute()
        self.settings.TECHTOHOUR = self.tmTechTo.time().hour()
        self.settings.TECHTOMIN = self.tmTechTo.time().minute()

        self.changedSettings = True
        print("Setting was changed.")

    def showEvent(self, event):
        self.btnRemoveC.setEnabled(False)
        self.redraw_candidates_list()
        self.lstCandidates.itemClicked.connect(self.candidate_selected)

        self.spProfit.setValue(int(self.settings.PROFIT))
        self.spProfit.valueChanged.connect(self.setting_change)

        self.spTrail.setValue(int(self.settings.TRAIL))
        self.spTrail.valueChanged.connect(self.setting_change)

        self.spLoss.setValue(int(self.settings.LOSS))
        self.spLoss.valueChanged.connect(self.setting_change)

        self.spBulck.setValue(int(self.settings.BULCKAMOUNT))
        self.spBulck.valueChanged.connect(self.setting_change)

        self.txtAccount.setText(self.settings.ACCOUNT)
        self.txtAccount.textChanged.connect(self.setting_change)

        self.txtPort.setText(self.settings.PORT)
        self.txtPort.textChanged.connect(self.setting_change)

        self.spIntervalWorker.setValue(int(self.settings.INTERVALWORKER))
        self.spIntervalWorker.valueChanged.connect(self.setting_change)

        self.spIntervalUi.setValue(int(self.settings.INTERVALUI))
        self.spIntervalUi.valueChanged.connect(self.setting_change)

        self.tmTechFrom.setTime(QTime(int(self.settings.TECHFROMHOUR), int(self.settings.TECHFROMMIN)))
        self.tmTechFrom.timeChanged.connect(self.setting_change)

        self.tmTechTo.setTime(QTime(int(self.settings.TECHTOHOUR), int(self.settings.TECHTOMIN)))
        self.tmTechTo.timeChanged.connect(self.setting_change)

        self.btnRemoveC.clicked.connect(self.remove_candidate)
        self.btnAddC.clicked.connect(self.add_candidate)

        self.btnGet.clicked.connect(self.update_stocks_from_cloud)
        self.btnClear.clicked.connect(self.clear_candidates)

    def redraw_candidates_list(self):
        self.lstCandidates.clear()

        for candidate in settings.CANDIDATES:
            ticker = candidate.ticker
            reason = candidate.reason
            o = 3
            item_to_add = QListWidgetItem()
            item_to_add.setText(ticker)
            item_to_add.setToolTip(reason)
            self.lstCandidates.addItem(item_to_add)
        self.btnRemoveC.setEnabled(False)
        self.set_clear_button_state()

    def set_clear_button_state(self):
        if self.lstCandidates.count() > 0:
            self.btnClear.setEnabled(True)
        else:
            self.btnClear.setEnabled(False)

    def remove_candidate(self):
        stock_to_remove = self.lstCandidates.selectedItems()[0].text()
        for x in self.settings.CANDIDATES:
            if x.ticker == stock_to_remove:
                self.settings.CANDIDATES.remove(x)
                break
        self.changedSettings = True
        self.redraw_candidates_list()

    def add_candidate(self):
        self.dlg = StockWindow()
        if self.dlg.exec_():
            ca = SettingsCandidate()
            ca.ticker = self.dlg.txtTicker.text().upper()
            ca.reason = self.dlg.txtReason.toPlainText()
            self.settings.CANDIDATES.append(ca)
            self.changedSettings = True
            self.redraw_candidates_list()
        else:
            print("Adding Canceled")

    def candidate_selected(self):
        self.btnRemoveC.setEnabled(True)

    def closeEvent(self, event):
        if self.changedSettings:
            reply = QMessageBox.question(self, 'Settings Changed',
                                         'Accepting requires manual restart-automatic-to be delivered-save changes?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                event.accept()
                self.settings.write_config()
                print("Settings were changed.Saved to file")
                window.restart_all()
            else:
                self.settings = copy.deepcopy(self.settingsBackup)

    def update_stocks_from_cloud(self):
        received_stocks = []
        try:
            x = requests.get('https://147u4tq4w4.execute-api.eu-west-3.amazonaws.com/default/ptest')
            received_stocks = json.loads(x.text)
            self.settings.CANDIDATES = received_stocks
            for s in received_stocks:
                self.lstCandidates.addItem(s['ticker'])
                i = self.lstCandidates.findItems(s['ticker'], Qt.MatchExactly)
                i[0].setToolTip(s['reason'])
            self.set_clear_button_state()
            self.setting_change()

        except:
            print('Failed to get the stocks from cloud')

    def clear_candidates(self):
        self.lstCandidates.clear()
        self.setting_change()


class StockWindow(QDialog, Ui_newStockDlg):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def addStock(self):
        ca = SettingsCandidate()
        ca.ticker = self.txtTicker
        ca.reason = self.txtReason
        self.settings.CANDIDATES.append(ca)


def main():
    app = QApplication(sys.argv)
    global settings
    settings = TraderSettings()
    settings.write_config()
    global window
    window = MainWindow(settings)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
