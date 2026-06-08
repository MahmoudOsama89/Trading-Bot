from tarfile import NUL
from tokenize import String
from binance.client import Client
import pandas as pd
from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta
import datefinder
import numpy as np
import matplotlib.pyplot as plt
import random
#import mplfinance as mpf
import matplotlib.dates as mdates
import plotly.graph_objects as go
# import talib
from numpy import nan, nanquantile
import threading
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time
import os

if not hasattr(np, "NaN"):
    np.NaN = np.nan
# import pandas_ta as ta
from scipy.signal import savgol_filter, find_peaks
import statsmodels.api as sm
import math
import matplotlib.animation as animation
from scipy import stats
from scipy.stats import norm
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_squared_error,median_absolute_error,explained_variance_score, confusion_matrix, classification_report
from statsmodels.stats.stattools import durbin_watson
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from binance.exceptions import (
    BinanceAPIException, BinanceRequestException, BinanceOrderException
)
from sklearn.model_selection import KFold, cross_val_score
import requests
import gc
import sys
import base64
import time
import json
import threading,websocket
import traceback
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from websocket import create_connection
import os
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key
import base64
import hashlib
from zoneinfo import ZoneInfo
from decimal import Decimal
import copy
from sklearn.ensemble import RandomForestClassifier


# Get the current recursion limit
current_limit = sys.getrecursionlimit()
print(f"Current recursion limit: {current_limit}")

# Set a new recursion limit
new_limit = 20000
sys.setrecursionlimit(new_limit)
x = 0
gc.collect()
if not hasattr(np, "NaN"):
    np.NaN = np.nan
week = 7
month = 30
year = 365
end_time = None
# first_prediction = 0
time_to_dfC = None

api_key = 
api_secret = 
predicted_data = pd.DataFrame(
    columns=['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume',
             'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore'])
#client_a = Client(api_key, api_secret)


def global_data(yf, ticker, start_date, end_date):
    df = yf.download(ticker, start=start_date, end=end_date)
    return df


def color_code():
    return NUL


def random_color_hex():
    """Generates a random hex color code (e.g., '#a3b182')."""
    hex_color = '#'
    for _ in range(6):  # A hex code has 6 hex chars
        hex_color += random.choice('0123456789abcdef')
    return hex_color





def calculate_my_mape(y_true,y_pred):
    length = len(y_true)
    l = len(y_true)
    i = 0
    arr = []
    while l>0:
        result = (y_true[i] - y_pred[i])/y_true[i]
        arr.append(result)
        i+=1
        l-=1
    my_mape = sum(arr)*100/length    
def start_analysis(interval, end_time, duration, symbol,quan,time_frame_test,inc,stock=None):
    start = end_time
    analysis_data = None
    joka = 1
    def calculate_duration(start, duration):
        print("Start & Duration",start,duration)
        
        return start - timedelta(days=duration)
        
    
    def get_data(client, interval, symbol, start_time, end_time):
        start_ms = int(start_time.timestamp() * 1000)
        end_ms = int(end_time.timestamp() * 1000)
        print("Start Time" ,start_time)
        print("End Time Time",end_time)
        try:
            print("firstly I am here")
            #klines = client.get_historical_klines(symbol=symbol, interval=interval, start_str=start_ms,
                                                
            
            url = "https://fapi.binance.com/fapi/v1/klines"
            params = {
                "symbol": symbol.upper(),
                "interval": interval,
                "limit": 1500
            }

            if start_time:
                params["startTime"] = start_ms
            if end_time:
                params["endTime"] = end_ms

            response = requests.get(url, params=params)
            response.raise_for_status()

            data = response.json()
            print("secondly I am here")
            return data
        except BinanceAPIException as e:
            print(f"Binance API Error: {e.code} - {e.message}")
            get_data(client, interval, symbol, start_time, end_time)

        except requests.exceptions.ReadTimeout:
            #print("Read timeout occurred — maybe retrying...")
            # Optionally retry:
            time.sleep(2)
            get_data(client, interval, symbol, start_time, end_time)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            get_data(client, interval, symbol, start_time, end_time)

    start_time = calculate_duration(start, duration)
    dataframe_created = {}
    print("start_time ",start,duration)
    def closest_probability(actual, preds,label):
        print("Label---------",label)
        window = 3  # number of past prices to consider
        actual = np.array(actual)
        preds = np.array(preds)
        window = 3  # rolling window for candidate predictions
        #unit = calculate_period(interval)
        closest_probs = []
        interval_probs = []

        for i in range(len(actual)):
            # --- Rolling window of predicted prices as candidate predictions ---
            start = max(0, i - window + 1)
            candidate_preds = preds[start:i+1]  # candidates from rolling window
            candidate_preds = np.atleast_1d(candidate_preds)  # ensure array

            # --- Closest Probability ---
            distances = np.abs(candidate_preds - actual[i])
            min_distance = np.min(distances)
            prob_closest = np.sum(distances == min_distance) / len(distances)
            closest_probs.append(prob_closest)

            # --- Interval Probability ---
            mean = np.mean(candidate_preds)
            std = np.std(candidate_preds)
            # Add tiny number to std to avoid division by zero
            prob_interval = norm.cdf(actual[i] + 1, loc=mean, scale=std + 1e-6) - \
                            norm.cdf(actual[i] - 1, loc=mean, scale=std + 1e-6)
            interval_probs.append(prob_interval)

        # Convert to arrays
        closest_probs = np.array(closest_probs)
        interval_probs = np.array(interval_probs)

        df = pd.DataFrame({
        'Actual Price': actual,
        'Predicted Price': preds,
        'Closest Probability': closest_probs,
        'Interval Probability': interval_probs
})
        egypt_time = now_date.astimezone(ZoneInfo("Africa/Cairo"))
        egypt_time_string = egypt_time.strftime("%Y-%m-%d %H_%M_%S")
        
        def compare_to_same_period(unit,pred,actual):
            len_of_data = len(pred)
            calc_len = len(pred)-1
            array = []
            if unit != None:
                while calc_len > 0:
                    delta = actual[calc_len] - pred[calc_len]
                    array.append(delta)
                    calc_len-= unit
            return array        
            
        def calculate_period(interval):
            unit = None
            if interval == "1w":
                unit = 4
            elif interval == "1d":
                unit = 7
            elif interval == "4h":
                unit = 6
            elif interval == "1h":
                unit = 24
            elif interval == "15m":
                unit = 4
            elif interval == "5min":
                unit = 12
            elif interval == "3m":
                unit = 20
            elif interval == "1m":    
                unit = 60      

            return unit          
        unit = calculate_period(interval)
        if unit != None:
            array = compare_to_same_period(unit,preds,actual)
        
        """if len(array) > 0:
            df["variance of same period"] = np.array(array)"""
        df.to_csv(r"G:\mahmoud\prop\prop_"+"_"+egypt_time_string+"_"+interval+"_"+label+".csv", index=False, encoding='utf-8')
        #return np.array(interval_probs),mean,std

        

    # --- Function: Interval Probability ---
    def interval_probability(actual, mean, std, window=1.0):
        probabilities = []
        for a, m, s in zip(actual, mean, std):
            lower = a - window
            upper = a + window
            prob = norm.cdf(upper, loc=m, scale=s) - norm.cdf(lower, loc=m, scale=s)
            probabilities.append(prob)
        return np.array(probabilities)

    # --- Run Calculations ---
    #closest_probs = closest_probability(actual_prices, predictions)
    def create_factors_dataframe(col,value,interval=None,status=None): 
        if len(dataframe_created) <  25  or len(dataframe_created)  == 0:
            dataframe_created[col] = [value] 
        else:
             dataframe_created[col].append(value) 
        return dataframe_created

    def base_to_work(X,y,new_value=None):
        X = np.array(X).reshape(-1, 1)
        y = np.array(y)
        """
        Fit logistic regression using sequential (numeric) input and binary output.
        
        Parameters:
            X_seq (array-like): Sequential numeric values (e.g., 1, 2, 3,...)
            y_bin (array-like): Binary target values (0 or 1)
            
        Returns:
            model: trained LogisticRegression model
            prob: predicted probabilities
            preds: predicted binary labels
        """
        split_index = int(0.7 * len(np.array(X)))
        X_train, X_test = X[:split_index], X[split_index:]
        Y_train, Y_test = y[:split_index], y[split_index:]
        X_train_copy = Y_train
        # Create and train the model
        model = LinearRegression()
        model.fit(X_train, Y_train)
        model2 = LinearRegression()
        model2.fit(X,y)
        new_value_predicted = model2.predict(new_value)
        # Make predictions on test data
        y_pred = model.predict(X_test)
        r2 = r2_score(Y_test, y_pred)
        variation = Y_test - y_pred
        binary_arr = (variation > 0).astype(int)
        # Sliding window size (look back)
        window = 1                  
        N = 1  # number of steps to predict ahead

        # Prepare features X and multi-step targets Y
        X, Y = [], []
        """for i in range(window, len(binary_arr) - N + 1):
            X.append(binary_arr[i-window:i])
            Y.append(binary_arr[i:i+N])"""
        i= 0
        while i<len(binary_arr)-1:
            Y.append(binary_arr[i+1])
            i+=1
        X = np.array(binary_arr)
        Y = np.array(Y)
        return X,Y,Y_test,y_pred,r2,new_value_predicted
    def calculate_corr(df,new_value=None):
        if interval == "1d" or interval == "1w" or interval == "5m":    
            from sklearn.multioutput import RegressorChain
            egypt_time = now_date.astimezone(ZoneInfo("Africa/Cairo"))
            egypt_time_string = egypt_time.strftime("%Y-%m-%d %H_%M_%S")
            labels  = ["High","Low","Close"]
            array = []
            df_M = pd.DataFrame()
            df_signal = pd.DataFrame()
            df_accuracy = pd.DataFrame()
            for label in labels:
                print("HEre I am ",df["Open"].head())
                X,Y,Y_test,y_pred,r2,new_value_predicted = base_to_work(df["Open"].iloc[:-1],df[label].iloc[:-1],[[df["Open"].iloc[-1]]])
                
                pred2,acc2,y_pred_return = do_other_staff(X,Y,label)
                print("here is pred2:",pred2)
                dif = Y_test - y_pred
                a = [] 
                percent = math.floor(len(Y_test)*.7)
                a[:percent+2] = np.full(percent+1, np.nan)
                a[percent+2:] = y_pred_return
                df_M["Actual "+label] = Y_test
                df_M["Predicted "+label] = y_pred
                df_M["Delta "+label] = dif
                df_M["predict binary "+label] = a
                df_signal[label] = [int(pred2)]
                df_signal[label+" Accuracy"] = [acc2]
                df_accuracy[label+" Acc"] = [r2]
                df_accuracy[label+" prediction"] = [new_value_predicted]


                
                              
            df_accuracy.to_csv(r"G:\mahmoud\accuracy\accuracy"+"_"+egypt_time_string+"_"+interval+".csv", index=False, encoding='utf-8')
            df_signal.to_csv(r"G:\mahmoud\new_signals\new_signal"+"_"+egypt_time_string+"_"+interval+".csv", index=False, encoding='utf-8')
                    
            df_M.to_csv(r"G:\mahmoud\new_pred\new_try"+"_"+egypt_time_string+"_"+interval+".csv", index=False, encoding='utf-8')    
            


    def do_other_staff(X,y,label):
            from sklearn.multioutput import RegressorChain
            from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
            from sklearn.multioutput import ClassifierChain
            
            for_new_prediction = [X[-1]]

            split_index = int(0.7 * len(X))
            X_train, X_test = X[:split_index], X[split_index:]
            Y_train, Y_test = y[:split_index], y[split_index:]
            X = X.reshape(-1,1)
            base = LogisticRegression(class_weight='balanced', max_iter=1000,solver='liblinear')
            #base = LogisticRegression()
            base = RandomForestClassifier(class_weight='balanced', n_estimators=200)
            chain = RegressorChain(base_estimator=base, order=None, random_state=42)
            chain2 =  RegressorChain(base, order=None)

            c = X[:-1]
            c = c.reshape(-1,1)
            y = np.array(y)
            y = y.reshape(-1,1)
            chain.fit(c,y)
            X_train = X_train.reshape(-1,1)
            Y_train = Y_train.reshape(-1,1)
            chain2.fit(X_train, Y_train)
            X_test = X_test.reshape(-1,1)
            pred = chain.predict([for_new_prediction])[0][0]
            #pred = (pred > 0.5).astype(int)
            y_pred = chain2.predict(X_test[:-1])
            y_pred_binary = (y_pred > 0.5).astype(int)
            #y_pred_proba = chain2.predict_proba(X_test)
            #y_pred_binary = (y_pred_proba[:, 1] > 0.4).astype(int)
            accuracy = accuracy_score(Y_test, y_pred)
            cm = confusion_matrix(Y_test[:-1], y_pred_binary[:-1])
            if label == "High" and interval == "1d":
                print("Confution Metric for me",cm)
                print("here is my y_true",y_pred_binary)
                print("Accuracy: for me",accuracy)
            
            
            return pred,accuracy,y_pred

    def logistic_regression_seq(X, y,label):
        from sklearn.multioutput import RegressorChain
        from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
        from sklearn.multioutput import ClassifierChain

        
        X = np.array(X).reshape(-1, 1)
        y = np.array(y)
        print("HERe is X",x)
        """
        Fit logistic regression using sequential (numeric) input and binary output.
        
        Parameters:
            X_seq (array-like): Sequential numeric values (e.g., 1, 2, 3,...)
            y_bin (array-like): Binary target values (0 or 1)
            
        Returns:
            model: trained LogisticRegression model
            prob: predicted probabilities
            preds: predicted binary labels
        """
        split_index = int(0.7 * len(X))
        X_train, X_test = X[:split_index], X[split_index:]
        Y_train, Y_test = y[:split_index], y[split_index:]
        X_train_copy = Y_train
        # Create and train the model
        model = LinearRegression()
        model.fit(X_train, Y_train)

        # Make predictions on test data
        y_pred = model.predict(X_test)
        variation = Y_test - y_pred
        binary_arr = (variation > 0).astype(int)
        # Sliding window size (look back)
        window = 1                  
        N = 1  # number of steps to predict ahead

        # Prepare features X and multi-step targets Y
        X, Y = [], []
        """for i in range(window, len(binary_arr) - N + 1):
            X.append(binary_arr[i-window:i])
            Y.append(binary_arr[i:i+N])"""
        i= 0
        while i<len(binary_arr)-1:
            Y.append(binary_arr[i+1])
            i+=1
        X = np.array(binary_arr)
        Y = np.array(Y)
        
        pred2,acc2,y_pred_return =  do_other_staff(X,Y,label)   
        # Sequential split (keep order)
        split_index = int(0.7 * len(X))
        X_train, X_test = X[:split_index], X[split_index:]
        Y_train, Y_test = Y[:split_index], Y[split_index:]
        X = X.reshape(-1,1)
        X_train = X_train.reshape(-1,1)
        # Regressor chain
        base_lr = LinearRegression()
        from sklearn.multioutput import RegressorChain
        chain = RegressorChain(base_lr, order=None)
        c = X[:-1].reshape(-1,1)
        Y = Y.reshape(-1,1)
        chain.fit(c, Y)
        chain2 = RegressorChain(base_lr, order=None)
        chain2.fit(X_train.reshape(-1,1),Y_train.reshape(-1,1))
        # Predict continuous values
        Y_pred = chain2.predict(X_test.reshape(-1,1))
        
        # Threshold to binary
        Y_pred_binary = (Y_pred > 0.5).astype(int)
        # Flatten arrays to compute accuracy
        accuracy = accuracy_score(Y_test[:-1].flatten(), Y_pred_binary[:-2].flatten())
        #last_window = np.array([0, 1, 0]).reshape(1, -1)  # last 'window' values
        #next_step_pred = chain.predict(last_window)       # continuous prediction
        # 🔮 Predict N future steps automatically (without assumption)
        N_future = 1
        next_step_binary = chain.predict([X[-1]])[0][0]
        #next_step_binary = int(next_pred > 0.5) # threshold to 0/1
        next_step_binary = (next_step_binary > 0.5).astype(int)
        cm = confusion_matrix(Y_test[:-1], Y_pred_binary[:-2])
        if label == "High":
            print(cm)
        """disp = ConfusionMatrixDisplay(cm, display_labels=[0, 1])
        disp.plot()
        plt.plot(Y_test, label='Actual')
        plt.plot(Y_pred_binary, label='Predicted', linestyle='dashed')
        plt.legend()
        plt.show()"""
        

        return next_step_binary,accuracy,pred2,acc2
        #X_train, X_test, y_train, y_test = train_test_split(X_seq, y_bin, test_size=0.3, random_state=42)
        # Create and train model

   
    def binance_fetch_data(klines=None,inc = 0):
        columns_to_convert = ['Open', 'High', 'Low', 'Close',"Open Time","Close Time"]
        df_prediction = pd.DataFrame()
        analysis_data = pd.DataFrame()
        r2 = None
        r2_low = None
        r2_close = None
        if klines is not  None:
            if stock == None:
                df_M = pd.DataFrame(klines, columns=[
        "Open Time", "Open", "High", "Low", "Close", "Volume", 
        "Close Time", "Quote Asset Volume", "Number of Trades", 
        "Taker Buy Base Asset Volume", "Taker Buy Quote Asset Volume", "Ignore"
    ])
            else:
                 df_M = pd.DataFrame(klines, columns=[
        "Open Time", "Open", "High", "Low", "Close","Close Time", "Volume", 
    ])
            predictions_all_new = {}
            print(df_M.head())
            if stock is not None:
                print("Iam here01",df_M)
                df_M["Close Time"] = df_M["Close Time"].astype('int64')
                print("I am here10",df_M["Close Time"].head())
                df_M["Open Time"] = df_M["Open Time"].astype('int64')
                last_date = df_M["Close Time"].iloc[-1]
            else:
                last_date = df_M["Close Time"].iloc[-1]    
            now_time_utc = time.time() * 1000
            print("---------There is evdince of manuiplating  interval "+interval,df_M["Open"].iloc[-1])
            utc_now = datetime.now(timezone.utc)

            # Convert to a Unix timestamp (seconds since epoch)
            # The timestamp() method returns a float, including fractional seconds
            utc_timestamp_seconds = end_time.timestamp()
            print("end time",end_time.timestamp())
            # Convert seconds to milliseconds and cast to an integer
            utc_milliseconds = int(utc_timestamp_seconds * 1000)

            #print(f"Current UTC time in milliseconds: {utc_milliseconds}")
            #print("------------Last Date------------",last_date)
            #print("------------Now Date------------",utc_milliseconds)

            if last_date > utc_milliseconds or last_date <= utc_milliseconds:
                for col in columns_to_convert:
                    df_M[col] = df_M[col].astype(float) 
                #test_price = 110711
                #array_to_append = np.array(df_M["High"])
                #test_price_and_data = array_to_append.append(test_price)
                #if interval == "1D":
                    #predictions_test_high_of_real = predictions_test(df_M["Open"].values.reshape(-1,1),test_price_and_data,np.array([[df_M["Open"].iloc[-1]]]))
                
                
                print("---------There is evdince of manuiplating  interval "+interval,df_M["Open"].iloc[-1])
                if interval == "1w" and stock ==  None:
                    df_M = df_M[df_M["Open Time"] < int(end_time.timestamp() * 1000)]
                if interval == "1M" and stock ==  None:
                    df_M = df_M[df_M["Open Time"] < int(end_time.timestamp() * 1000)]  
                if interval == "3d" and stock ==  None:
                    df_M = df_M[df_M["Open Time"] < int(end_time.timestamp() * 1000)]   
                #df_M = df_M.dropna()                         
                df_M.set_index("Close Time",inplace=True)
                df_M["Close Time"] = df_M.index
                print("Here is df_M",df_M.head())
                predictions_test_high = predictions_test(df_M["Open"].iloc[:-1].values.reshape(-1,1),df_M["High"].iloc[:-1],np.array([[df_M["Open"].iloc[-1]]]))
                predictions_test_low = predictions_test(df_M["Open"].iloc[:-1].values.reshape(-1,1),df_M["Low"].iloc[:-1],np.array([[df_M["Open"].iloc[-1]]]))
                predictions_test_close = predictions_test(df_M["Open"].iloc[:-1].values.reshape(-1,1),df_M["Close"].iloc[:-1],np.array([[df_M["Open"].iloc[-1]]]))
                #return df_M, columns_to_convert,analysis_data,predictions_test_high ,predictions_test_low 
                MAPE_open,r2_open,bias_open,mae_open,predictions_test_high_new = some_other_factors(df_M["Open"].iloc[:-1].values.reshape(-1, 1),df_M["High"].iloc[:-1],"Open",np.array([[predictions_test_high]]))
                MAPE,r2,bias,mae = some_other_factors(df_M["Open"].iloc[:-1].values.reshape(-1, 1),df_M["High"].iloc[:-1],"High")
                MAPE_low,r2_low,bias_low,mae_low = some_other_factors(df_M["Open"].iloc[:-1].values.reshape(-1, 1),df_M["Low"].iloc[:-1],"Low")
                MAPE_close,r2_close,bias_close,mae_close = some_other_factors(df_M["Open"].iloc[:-1].values.reshape(-1, 1),df_M["Close"].iloc[:-1],"Close")
                accuracy_factor = get_accuracy_factor(r2,MAPE)
                if interval != None:
                    calculate_corr(df_M)
                    print("Columns",list(df_M.columns))
                    print("Here is df_M Open",df_M["Open"])
                    print("---------------------------------")
                    signal_High,accuracy,pred2,acc2 = logistic_regression_seq(df_M["Open"].iloc[:-1], df_M["High"].iloc[:-1],"High")
                    signal_Low,accuracy2,pred2_2,acc2_2 = logistic_regression_seq(df_M["Open"].iloc[:-1], df_M["Low"].iloc[:-1],"Low")
                    signal_Close,accuracy3,pred2_3,acc2_3 =  logistic_regression_seq(df_M["Open"].iloc[:-1], df_M["Close"].iloc[:-1],"Close")
                    df_signal = pd.DataFrame(
                            {
                                "High1": [signal_High],
                                "ACC1": [accuracy],
                                "High2": [pred2],
                                "ACC2": [acc2],
                                "Low": [signal_Low],
                                "ACC1_1": [accuracy2],
                                "Low2": [pred2_2],
                                "ACC2_2": [acc2_2],
                                "Close": [signal_Close],
                                "ACC1_3": [accuracy3],
                                "High2": [pred2_3],
                                "ACC2_3": [acc2_3],
                            }
                        )                    
                    df_signal.to_csv(r"G:\mahmoud\signals\signal"+"_"+egypt_time_string+"_"+interval+".csv", index=False, encoding='utf-8')
                    
                    
                    
                #predictions_test_high-=bias
                #predictions_test_low-=bias_low
                #predictions_test_close-=bias_close
                #accuracy_factor_low = get_accuracy_factor(r2_low,MAPE_low )
                #accuracy_factor_close = get_accuracy_factor(r2_close,MAPE_close )  
                #predictions_test_high =  predictions_test_high * accuracy_factor
                #predictions_test_low = predictions_test_low * accuracy_factor_low
                #predictions_test_close = predictions_test_close * accuracy_factor_close

                #total_ms  = duration_to_ms(interval)
                if interval == "1s":
                    #print("yeah it's 1s")
                    total_ms = 1000
                else:
                    #print("NO it's 1s")
                    total_ms  = duration_to_ms(interval)                    
                open_time = df_M["Open Time"].iloc[-1] 
                close_time = df_M.index[-1] 
                new_row_df = pd.DataFrame([{"Open":df_M["Open"].iloc[-1], "High": predictions_test_high,"Low":predictions_test_low,"Close":predictions_test_close,"Open Time":open_time,"Close Time":close_time}])
                print("Iam here 12",df_M.index)
                if stock is not None:
                    df_M["Close Time"] = df_M.index
                df_M = pd.concat([df_M.iloc[:-1], new_row_df], ignore_index=True)
                print("Iam here 11",df_M["Close Time"].head())
                open_price = df_M["Open"].iloc[-1]
                predictions_all_new["Open"] = [open_price]
                predictions_all_new["Close"] = [predictions_test_close]
                predictions_all_new["High"] = [predictions_test_high]
                predictions_all_new["Low"] = [predictions_test_low]
                predictions_test_high_E = predictions_test(df_M["Open"].iloc[:-1].values.reshape(-1,1),df_M["High"].iloc[:-1],np.array([[df_M["Open"].iloc[-1]]]))
                predictions_test_low_E = predictions_test(df_M["Open"].iloc[:-1].values.reshape(-1,1),df_M["Low"].iloc[:-1],np.array([[df_M["Open"].iloc[-1]]]))
                predictions_test_close_E = predictions_test(df_M["Open"].iloc[:-1].values.reshape(-1,1),df_M["Close"].iloc[:-1],np.array([[df_M["Open"].iloc[-1]]]))
                predictions_all_new["E. Close"] = [predictions_test_close_E]
                predictions_all_new["E. High"] = [predictions_test_high_E]
                predictions_all_new["E. Low"] = [predictions_test_low_E]
                predictions_all_new["Open Time"] = [open_time]
                predictions_all_new["Close Time"] = [close_time]
                df_prediction = new_row_df
                #print("Header-----",predictions_all_new)
                if inc > 0:
                    while inc < 1000 and inc >0:
                        predictions_test_open = predictions_test(df_M["Close"].iloc[:-1].values.reshape(-1,1),df_M["Open"].iloc[1:],np.array([[df_M["Close"].iloc[-1]]]))
                        #predictions_test_open = some_other_factors(df_M["Close"].iloc[:-1].values.reshape(-1,1),df_M["Open"].iloc[1:],np.array([[predictions_test_open]]))
                        predictions_test_high = predictions_test(df_M["Open"].values.reshape(-1,1),df_M["High"],np.array([[predictions_test_open]]))
                        predictions_test_low = predictions_test(df_M["Open"].values.reshape(-1,1),df_M["Low"],np.array([[predictions_test_open]]))
                        predictions_test_close = predictions_test(df_M["Open"].values.reshape(-1,1),df_M["Close"],np.array([[predictions_test_open]]))
                        MAPE,r2,bias,mae = some_other_factors(df_M["Open"].iloc[:-1].values.reshape(-1, 1),df_M["High"].iloc[:-1],"High")
                        MAPE_low,r2_low,bias_low,mae_low = some_other_factors(df_M["Open"].iloc[:-1].values.reshape(-1, 1),df_M["Low"].iloc[:-1],"Low")
                        MAPE_close,r2_close,bias_close,mae_close = some_other_factors(df_M["Open"].iloc[:-1].values.reshape(-1, 1),df_M["Close"].iloc[:-1],"Close")
                        MAPE_open,r2_open,bias_open,mae_open = some_other_factors(df_M["Open"].iloc[:-1].values.reshape(-1, 1),df_M["High"].iloc[:-1],"Open")
                        predictions_test_open-=bias_open
                        predictions_test_high-=bias
                        predictions_test_low-=bias_low
                        predictions_test_close-=bias_close
                        accuracy_factor = get_accuracy_factor(r2,MAPE)
                        accuracy_factor_low = get_accuracy_factor(r2_low,MAPE_low )
                        accuracy_factor_close = get_accuracy_factor(r2_close,MAPE_close )  
                        #predictions_test_high =  predictions_test_high * accuracy_factor
                        #predictions_test_low = predictions_test_low * accuracy_factor_low
                        #predictions_test_close = predictions_test_close * accuracy_factor_close
                        if interval == "1s":
                            #("yeah it's 1s")
                            total_ms = 1000
                        else:
                            #print("NO it's 1s")
                            total_ms  = duration_to_ms(interval)
                        total_ms  = duration_to_ms(interval)
                        open_time = df_M["Close Time"].iloc[-1]
                        close_time = df_M["Close Time"].iloc[-1] + total_ms
                        predictions_all_new["Open"].append(predictions_test_open)
                        predictions_all_new["Close"].append(float(predictions_test_close))
                        predictions_all_new["High"].append(float(predictions_test_high))
                        predictions_all_new["Low"].append(float(predictions_test_low))
                        predictions_all_new["Open Time"].append(open_time)
                        predictions_all_new["Close Time"].append(close_time)
                        predictions_test_open = predictions_test(df_M["Close"].iloc[:-1].values.reshape(-1,1),df_M["Open"].iloc[1:],np.array([[df_M["Close"].iloc[-1]]]))
                        predictions_test_high = predictions_test(df_M["Open"].values.reshape(-1,1),df_M["High"],np.array([[predictions_test_open]]))
                        predictions_test_low = predictions_test(df_M["Open"].values.reshape(-1,1),df_M["Low"],np.array([[predictions_test_open]]))
                        predictions_test_close = predictions_test(df_M["Open"].values.reshape(-1,1),df_M["Close"],np.array([[predictions_test_open]]))
                        predictions_all_new["E. Close"].append(predictions_test_close*r2_close)
                        predictions_all_new["E. High"].append(predictions_test_high_E)
                        predictions_all_new["E. Low"].append(predictions_test_low*(2-r2))
                        predictions_all_new["Open Time"].append(open_time)
                        predictions_all_new["Close Time"].append(close_time)
                        
                        new_row_df = pd.DataFrame([{"Open":predictions_test_open, "High": predictions_test_high,"Low":predictions_test_low,"Close":predictions_test_close,"Open Time":open_time,"Close Time":close_time}])
                        df_M = pd.concat([df_M, new_row_df], ignore_index=True)
                        df_prediction = pd.concat([df_prediction, new_row_df], ignore_index=True)
                        inc-=1
            else:
                #print('1s for first') 
                if inc > 0:
                    for col in columns_to_convert:
                        df_M[col] = df_M[col].astype(float)
                    #print('1s for second')    
                    while inc < 4000 and inc >0:
                        #print('1s for third')
                        # 
                        predictions_test_open = predictions_test(df_M["Close"].iloc[:-1].values.reshape(-1,1),df_M["Open"].iloc[1:],np.array([[df_M["Close"].iloc[-1]]]))
                        predictions_test_high = predictions_test(df_M["Open"].values.reshape(-1,1),df_M["High"],np.array([[predictions_test_open]]))
                        predictions_test_low = predictions_test(df_M["Open"].values.reshape(-1,1),df_M["Low"],np.array([[predictions_test_open]]))
                        predictions_test_close = predictions_test(df_M["Open"].values.reshape(-1,1),df_M["Close"],np.array([[predictions_test_open]]))
                        MAPE,r2,bias,mae = some_other_factors(df_M["Open"].iloc[:-1].values.reshape(-1, 1),df_M["High"].iloc[:-1],"High")
                        MAPE_low,r2_low,bias_low,mae_low = some_other_factors(df_M["Open"].iloc[:-1].values.reshape(-1, 1),df_M["Low"].iloc[:-1],"Low")
                        MAPE_close,r2_close,bias_close,mae_close = some_other_factors(df_M["Open"].iloc[:-1].values.reshape(-1, 1),df_M["Close"].iloc[:-1],"Close")
                        MAPE_open,r2_open,bias_open,mae_open = some_other_factors(df_M["Open"].iloc[:-1].values.reshape(-1, 1),df_M["High"].iloc[:-1],"Open")
                        predictions_test_open-=bias_open
                        predictions_test_high-=bias
                        predictions_test_low-=bias_low
                        predictions_test_close-=bias_close
                        accuracy_factor_low = get_accuracy_factor(r2_low,MAPE_low )
                        accuracy_factor_close = get_accuracy_factor(r2_close,MAPE_close )  
                        #predictions_test_high =  predictions_test_high * accuracy_factor
                        #predictions_test_low = predictions_test_low * accuracy_factor_low
                        #predictions_test_close = predictions_test_close * accuracy_factor_close
                        if interval == "1s":
                            #print("yeah it's 1s")
                            total_ms = 1000
                        else:
                           #print("NO it's 1s")
                            total_ms  = duration_to_ms(interval)
                        total_ms  = duration_to_ms(interval)
                        open_time = df_M["Close Time"].iloc[-1]
                        close_time = df_M["Close Time"].iloc[-1] + total_ms
                        predictions_all_new["Open"].append(float(predictions_test_open))
                        predictions_all_new["Close"].append(float(predictions_test_close))
                        predictions_all_new["High"].append(float(predictions_test_high))
                        predictions_all_new["Low"].append(float(predictions_test_low))
                        predictions_all_new["Open Time"].append(open_time)
                        predictions_all_new["Close Time"].append(close_time)
                        predictions_all_new["Open"].append(float(df_M["Close"].iloc[-1]))
                        predictions_all_new["Close"].append(float(predictions_test_close))
                        predictions_all_new["High"].append(float(predictions_test_high))
                        predictions_all_new["Low"].append(float(predictions_test_low))
                        predictions_all_new["Open Time"].append(open_time)
                        predictions_all_new["Close Time"].append(close_time)
                        predictions_test_high_E = predictions_test(df_M["Open"].iloc[:-1].values.reshape(-1,1),df_M["High"].iloc[:-1],np.array([[df_M["Open"].iloc[-1]*r2]]))
                        predictions_test_low_E = predictions_test(df_M["Open"].iloc[:-1].values.reshape(-1,1),df_M["Low"].iloc[:-1],np.array([[df_M["Open"].iloc[-1]*(2-r2)]]))
                        predictions_test_close_E = predictions_test(df_M["Open"].iloc[:-1].values.reshape(-1,1),df_M["Close"].iloc[:-1],np.array([[df_M["Open"].iloc[-1]*r2_close]]))
                        predictions_all_new["E. Close"].append(predictions_test_close*r2_close)
                        predictions_all_new["E. High"].append(predictions_test_high_E)
                        predictions_all_new["E. Low"].append(predictions_test_low*(2-r2))
                        predictions_all_new["Open Time"].append(open_time)
                        predictions_all_new["Close Time"].append(close_time)
                        new_row_df = pd.DataFrame([{"Open":df_M["Close"].iloc[-1], "High": predictions_test_high,"Low":predictions_test_low,"Close":predictions_test_close,"Open Time":open_time,"Close Time":close_time}])
                        df_M = pd.concat([df_M, new_row_df], ignore_index=True)
                        df_prediction = pd.concat([df_prediction, new_row_df], ignore_index=True)
                        inc-=1

            df_M.to_csv('G:\mahmoud\output\output_'+interval+'.csv', index=False, encoding='utf-8')
        else:
            df = pd.read_csv('output.csv', sep=",", skipfooter=1, engine='python', encoding='utf-8')
            df_l = df.to_dict(orient='records')
            df_M = pd.DataFrame(df_l, columns=['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time',
                                               'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume',
                                               'Taker Buy Quote Asset Volume', 'Ignore'])

        
        # df_M = pd.DataFrame(klines, columns=['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore'])
        # columns_to_convert = ['Open', 'High', 'Low', 'Close', 'Volume', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume']
        try:
            #df_prediction_new = pd.DataFrame(predictions_all_new, dtype='float32')
            #df_prediction_new.to_csv(r"G:\mahmoud\predicted_value_fresh\predictions_"+interval+"_"+now_utc_+".csv", index=False, encoding='utf-8')

            if df_prediction.empty:
                print("Yeah start from here the error",interval)
            else:    
                try:
                    df_prediction["Mean_High"] = df_prediction["High"].mean()
                    df_prediction["Mean_Low"] = df_prediction["Low"].mean()
                    df_prediction["Median_High"] = df_prediction["High"].median()
                    df_prediction["Median_Low"] = df_prediction["Low"].median()
                    df_prediction["Min_High"] = df_prediction["High"].min()
                    df_prediction["Min_Low"] = df_prediction["Low"].min()
                    df_prediction["Max_High"] = df_prediction["High"].max()
                    df_prediction["Max_Low"] = df_prediction["Low"].max()
                    df_prediction["mod_High"] = df_prediction["High"].mode()
                    df_prediction["mod_Low"] = df_prediction["Low"].mode()
                    df_prediction["std_High"] = df_prediction["High"].std()
                    df_prediction["std_Low"] = df_prediction["Low"].std()
                    df_prediction["High_MAE"] = mae
                    df_prediction["Low_MAE"] = mae_low
                    df_prediction["Mean_High"].iloc[1:] = None
                    df_prediction["Mean_Low"].iloc[1:] = None
                    df_prediction["Median_High"].iloc[1:] = None
                    df_prediction["Median_Low"].iloc[1:] = None
                    df_prediction["Min_High"].iloc[1:] = None
                    df_prediction["Min_Low"].iloc[1:] = None
                    df_prediction["Max_High"].iloc[1:] = None
                    df_prediction["Max_Low"].iloc[1:] = None
                    df_prediction["mod_High"].iloc[1:] = None
                    df_prediction["mod_Low"].iloc[1:] = None
                    df_prediction["std_High"].iloc[1:] = None
                    df_prediction["std_Low"].iloc[1:] = None
                    df_prediction["High_MAE"].iloc[1:] = None
                    df_prediction["Low_MAE"].iloc[1:] = None
                    print("Before Export predicted csv",interval)
                    now_utc_ = utc_now.astimezone(ZoneInfo("Africa/Cairo")).strftime("%Y_%m_%d %H_%M_%S")
                    analysis_data = copy.deepcopy(df_prediction)
                    analysis_data["Open"].iloc[1:] = None
                    analysis_data["Close"].iloc[1:] = None
                    analysis_data["High"].iloc[1:] = None
                    analysis_data["Low"].iloc[1:] = None
                    analysis_data["Close Time"].iloc[1:] = None
                    analysis_data["Open Time"].iloc[1:] = None
                    analysis_data["E. High"] = analysis_data["High"]*accuracy_factor
                    analysis_data["E. High"].iloc[1:] = None
                    analysis_data["E. Low"] = analysis_data["Low"]*(2-r2_low)
                    analysis_data["E. Low"].iloc[1:] = None
                    analysis_data["E. Close"] = analysis_data["Close"]*r2_close
                    analysis_data["E. Close"].iloc[1:] = None
                    df_prediction.to_csv(r"G:\mahmoud\predicted_value\predictions_"+interval+"_"+now_utc_+".csv", index=False, encoding='utf-8')
                    #print("Before Export predicted csv",interval)
                    
                except Exception as e:
                    print("Error saving CSV:"+interval, e)
        except Exception as e:
            print("❌ Error while creating df:"+interval, e)
        return df_M, columns_to_convert,analysis_data,predictions_test_high,predictions_test_low

  


    import re
    def duration_to_ms(duration: str) -> int:
        duration = duration.lower().strip()
        total_ms = 0

        # Extract hours, minutes, seconds, milliseconds using regex
        hours = re.search(r"(\d+)\s*h", duration)
        minutes = re.search(r"(\d+)\s*m", duration)
        seconds = re.search(r"(\d+)\s*s", duration)
        millis = re.search(r"(\d+)\s*ms", duration)
        
        if hours:
            total_ms += int(hours.group(1)) * 3600 * 1000
        if minutes:
            total_ms += int(minutes.group(1)) * 60 * 1000
        if seconds:
            total_ms += int(seconds.group(1)) * 1000
        if millis:
            total_ms += int(millis.group(1))
        #print(millis)     # 5415000 ms
        return total_ms

    # 🔥 Examples
         # 45200 ms


    
             
    def intinate_api():
        #api_key = //
        #api_secret = //
    
        api_key = //
        api_secret = //
        #api_key = //
        #private_key = //

        try:
            client = Client(api_key, api_secret)
            #client = Client(api_key,private_key)
        except requests.exceptions.Timeout:
            intinate_api()
        except BinanceAPIException as e:
            print(f"[BinanceAPIException] Status: {e.status_code}, Message: {e.message}")
            intinate_api()
        except BinanceOrderException as e:
            print(f"[BinanceOrderException] {e}")
            intinate_api()
        except BinanceRequestException as e:
            print(f"[BinanceRequestException] {e}")
            intinate_api()
        except requests.exceptions.Timeout as e:
            print(f"[Timeout Error] {e}")
            intinate_api()
        except requests.exceptions.ConnectionError as e:
            print(f"[Connection Error] {e}")
            intinate_api()
        except requests.exceptions.HTTPError as e:
            print(f"[HTTP Error] {e}")
            intinate_api()
        except requests.exceptions.RequestException as e:
            print(f"[General Request Error] {e}")
            intinate_api()
        except Exception as e:
            print(f"[Unexpected Error] {e}")
            intinate_api()
        # info = client.get_account()
        return client
     
    def predictions_test(X,y,new_value):
        model = LinearRegression()
        model.fit(X, y)
        predicted_score = model.predict(new_value)
        r_sq = model.score(X, y)
        print(f"coefficient of determination: {r_sq}")
        #print(f"intercept: {model.intercept_}")
        #print(f"slope: {model.coef_}")
        create_factors_dataframe("coefficient of determination",r_sq)
        create_factors_dataframe("intercept",{model.intercept_})
        create_factors_dataframe("slope",model.coef_)
        test_predictions_randomly(model,X,y)
        test_predictions_not_randomly(model,X,y)
        

        return predicted_score[0]
    
    def some_other_factors(X,y,label=None,new_value=None):
        nonlocal joka
        X = X.reshape(-1)
        #X.reset_index(drop=True)
        y = np.array(y)
        print("Here agiaan",y.shape)
        print("Here x",y.shape)
        #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        #Split data (keep order by not shuffling)
        split_index = int(len(X) * 0.7)  # 70% train, 30% test
        X_train, X_test = X[:split_index], X[split_index:]
        y_train = y[:split_index]
        y_test  = y[split_index:]

        # 3. Train a model on the training data
        model = LinearRegression()
        X_train = X_train.reshape(-1,1)
        print("Not important X",X_train.shape)
        print("Not important y",y_train.shape)
        model.fit(X_train, y_train)
        # 4. Evaluate the model on the testing data
        X_test = X_test.reshape(-1,1)
        y_pred = model.predict(X_test)
        if joka<=4:
            closest_probability(y_test, y_pred,label)
            joka+=1

        
        #y_pred_new = np.argmax(y_pred, axis=1)
        #y_pred_new = np.argmax(y_pred, axis=0)
        

        

        
        # --- Function: Interval Probability ---

        # Example: using model mean and std (can estimate from your predictions)

        def do_some_magic(X,y,new_value):
            model_error = LinearRegression()
            model_error.fit(X,y)
            prediction_new = model_error.predict(new_value)
            return prediction_new[0]
        new_prediction = None
        if new_value != None:
            new_prediction = do_some_magic(np.array(y_pred).reshape(-1,1),y_test,new_value)
            #new_prediction = new_prediction[0]

        X = X.reshape(-1,1)    
        r_sq = model.score(X, y)
        y_true = y_test
        def calculate_mape(y_true, y_pred):
            y_true, y_pred = np.array(y_true), np.array(y_pred)
            # Handle cases where y_true is zero to avoid division by zero
            non_zero_indices = y_true != 0
            return np.mean(
                np.abs((y_true[non_zero_indices] - y_pred[non_zero_indices]) / y_true[non_zero_indices])) * 100

        mape_score = calculate_mape(y_test, y_pred)
        #print(f"MAPE: {mape_score:.2f}%")
        create_factors_dataframe("MAPE",mape_score)
        kf = KFold(n_splits=5, shuffle=True, random_state=42)  # 5-fold cross-validation
        scores = cross_val_score(model, X, y, cv=kf, scoring='neg_mean_squared_error')
        #print("Average MSE:", -scores.mean())
        create_factors_dataframe("Average MSE:",-scores.mean())
        mean_error = np.mean(y_pred - y_test)  # Predicted - Actual
        max_error = np.max(y_pred-y_test)
        #print(f"Mean Error (Bias): {mean_error}")
        create_factors_dataframe("Mean Error (Bias)",mean_error)
        # Training metrics
        train_preds = model.predict(X_train)
        train_mse = mean_squared_error(y_train, train_preds)
        #train_r2 = r2_score(y_train, train_preds)
        mae = mean_absolute_error(y_true, y_pred)
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_true, y_pred)
        n = len(y_true)   # number of observations
        p = 1             # number of features/predictors (set this to match your model!)
        adj_r2 = 1 - (1 - r2) * (n - 1) / (n - p - 1)
        div_R = r2/adj_r2
        # Print results
        """print(f"Mean Absolute Error (MAE): {mae:.4f}")
        print(f"Mean Squared Error (MSE): {mse:.4f}")
        print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
        print(f"R² Score: {r2:.4f}")"""
        create_factors_dataframe(f"Mean Absolute Error (MAE)",f"{mae:.4f}")
        create_factors_dataframe(f"Mean Squared Error (MSE):", f"{mse:.4f}")
        create_factors_dataframe(f"Root Mean Squared Error (RMSE): ", f"{rmse:.4f}")
        create_factors_dataframe(f"R² Score: ", f"{r2:.4f}")
        evs = explained_variance_score(y_true, y_pred)
        #print("Explained Variance Score:", evs)
        create_factors_dataframe("Explained Variance Score", evs)
        # Print results
        """ print(f"Mean Absolute Error (MAE):",f" {mae:.4f}")
        print(f"Mean Squared Error (MSE):",f" {mse:.4f}")
        print(f"Root Mean Squared Error (RMSE):",f" {rmse:.4f}")"""
        create_factors_dataframe(f"Mean Absolute Error (MAE):",f" {mae:.4f}")
        create_factors_dataframe(f"Mean Squared Error (MSE):",f" {mse:.4f}")
        create_factors_dataframe(f"Root Mean Squared Error (RMSE):",f" {rmse:.4f}")
        #r2 = r2_score(y_test, y_pred)
        #print(f"R² Score: {r2:.4f}")
        
        """ pprint(f"R²: {r2:.4f}")
        print(f"Adjusted R²:"," {adj_r2:.4f}")
        print(f"R²: {r2:.4f}")
        print(f"R2 / Adjusted R²:"," {div_R:.4f}")""" 
        create_factors_dataframe(f"R²:",f" {r2:.4f}")
        create_factors_dataframe(f"Adjusted R²: ",f"{adj_r2:.4f}")
        create_factors_dataframe(f"R²:",f" {r2:.4f}")
        create_factors_dataframe(f"R2 / Adjusted R²: ",f"{div_R:.4f}")
        medae = median_absolute_error(y_true, y_pred)
        #print("Median Absolute Error:", medae)
        create_factors_dataframe("Median Absolute Error:", medae)
        residuals = np.array(y_true) - np.array(y_pred)
        dw = durbin_watson(residuals)
        #print("Durbin-Watson:", dw)
        create_factors_dataframe("Durbin-Watson:", dw)
        if new_prediction != None:
            return mape_score,r_sq,mean_error,mean_error,new_prediction
        else:
            return mape_score,r_sq,mean_error,mean_error
        
        # print(f"Mean Error (Bias): {mean_error}")"""
    def test_predictions_randomly(model,X,y):
        #print("This with Random State")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)


        # 3. Train a model on the training data
        model2 = LinearRegression()
        model2.fit(X_train, y_train)

        # 4. Evaluate the model on the testing data
        y_pred = model2.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        """ pprint(f"Mean Squared Error: {mse}")
        print(f"R-squared: {r2}")
        print("---------Mape Calculation Started---------")""" 
        
    def get_accuracy_factor(r2,mape):
        return (r2*(1-mape/100))        
    
    def listen_to_order(API_KEY):
        BASE = "https://fapi.binance.com"
        # create listenKey
        resp = requests.post(BASE + "/fapi/v1/listenKey", headers={"X-MBX-APIKEY": API_KEY})
        listen_key = resp.json()['listenKey']

        def on_message(ws, message):
            data = json.loads(message)
            print("WS event:", data)

        def on_open(ws):
            print("ws opened")

        ws = websocket.WebSocketApp(f"wss://fstream.binance.com/ws/{listen_key}",
                                    on_message=on_message, on_open=on_open)

        thread = threading.Thread(target=ws.run_forever, kwargs={"ping_interval": 60})
        thread.start()
    def test_predictions_not_randomly(model,X,y):
        print("This with NOT Random State")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)


        # 3. Train a model on the training data
        model2 = LinearRegression()
        model2.fit(X_train, y_train)

        # 4. Evaluate the model on the testing data
        y_pred = model2.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        print(f"Mean Squared Error: {mse}")
        print(f"R-squared: {r2}")
    def new_trading_behaviour(df_c=None):
        client = intinate_api()
        columns_to_convert = ['Open', 'High', 'Low', 'Close',"Open Time","Close Time"]
        now_utc = datetime.now(timezone.utc)
        if df_c is None:
            klines = get_data(client,interval,symbol,start_time,now_utc)
            df_m, columns_to_convert,analysis_data = binance_fetch_data(klines,inc)
            for col in columns_to_convert:
                df_m[col] = df_m[col].astype(float)
            
            df_c = df_m
            df_c.set_index("Close Time",inplace = True)
        else:
            print("df_c is not None what Hell is that")

        close_price = np.array([[df_c['Close'].iloc[-1]]])
        #print("----------------Start High Predictions-------------------")
        prediction_high = predictions_test(df_c["Open"].values.reshape(-1, 1), df_c["High"], close_price)
        #print("----------------Start Low Predictions-------------------")
        #print("----------------Start Low Predictions-------------------")
        prediction_low = predictions_test(df_c["Open"].values.reshape(-1, 1), df_c["Low"], close_price)
        #print("prediction_low",prediction_low)
        #print("----------------Start Low Predictions-------------------")
        liq_price = df_c["Close"].iloc[-1] + (1-1/125)
        prediction_high_int = math.trunc(prediction_high)
        #prediction_high = Decimal(prediction_high)
        close_at_price = prediction_high_int - 2 
        MAPE,r2,bias,mae = some_other_factors(df_c["Open"].values.reshape(-1, 1),df_c["High"],"NA")
        MAPE_low,r2_low,bias_low,mae_low = some_other_factors(df_c["Open"].values.reshape(-1, 1),df_c["Low"],"NA")
        accuracy_factor = get_accuracy_factor(r2,MAPE)
        accuracy_factor_low = get_accuracy_factor(r2_low,MAPE_low )
        #print("accuracy_score: ",accuracy_factor)
        #print("accuracy_factor_low: ",accuracy_factor_low)
        #print("---------Mape Calculation Ended---------")  
        create_factors_dataframe("accuracy_score: ",accuracy_factor)
        create_factors_dataframe("accuracy_factor_low: ",accuracy_factor_low)     
        close_price = prediction_high*accuracy_factor
        close_price = math.trunc(close_price)
        close_price_low = prediction_low*accuracy_factor_low
        close_price_low = math.trunc(close_price_low)
        wait_time = (df_c.index[-1] + 420000)/1000
        #print("last_date",df_c.index[-1])
        #print("last_price",df_c["Close"].iloc[-1])
        #print("Enhanced predicted Price: ",close_price)
        #print("Enhanced predicted Price Low: ",close_price_low)
        create_factors_dataframe("last_price: ",accuracy_factor)
        create_factors_dataframe("Enhanced predicted Price: ",close_price) 
        create_factors_dataframe("Enhanced predicted Price Low: ",close_price_low)
        diff_price_low = df_c["Close"].iloc[-1] - close_price_low
        diff_price_high =  close_price - df_c["Close"].iloc[-1] 
        if diff_price_high > diff_price_low :
            side = "BUY"
            position_side = "LONG"
        else:
            side = "SELL"
            position_side = "SHORT"

        #print("-----Side-------"+interval,side) 
        create_factors_dataframe("Side",side)
        create_factors_dataframe("interval",interval) 
        data_frame = pd.DataFrame(dataframe_created)
        data_frame.set_index("interval",inplace=True)
        save_dir = f"G:\mahmoud\dataframes_result\l{interval}.csv" 
        path = os.path.join(save_dir, f"results_{interval}.csv")
        #data_frame.to_csv(save_dir, index=False)
        data_frame_enhanced = pd.DataFrame({"R2":[r2],"R2_Low":[r2_low],"Mape":[MAPE],"Mape_low":[MAPE_low]})
        data_frame_enhanced.to_csv(r'G:\mahmoud\factors_updated\output_'+interval+'.csv', index=False, encoding='utf-8')
        data_frame.to_csv('G:\mahmoud\df_result\output_'+interval+'.csv', index=False, encoding='utf-8')
        if close_price_low < df_c["Close"].iloc[-1] and side == "SELL" :
            if time_frame_test == interval:
                order,api_key,sin = my_new_placing_order(close_price_low,side,position_side)
            
        elif close_price > df_c["Close"].iloc[-1] and side == "BUY" :
            #print("Yes we Are Here")
            if time_frame_test == interval:
                order,api_key,sin = my_new_placing_order(close_price,side,position_side)
            #print(order)
                if  'orderId'  in order :
                    wait_for_time(420000,wait_time,order,api_key,sin,df_c)
                    #print("Yeah Order_id exist",order["orderId"])
        elif close_price_low < df_c["Close"].iloc[-1] and side == "BUY" : 
            if time_frame_test == interval:
                order,api_key,sin = my_new_placing_order_short_and_long(close_price_low,"SELL","SHORT")
        elif close_price > df_c["Close"].iloc[-1] and side == "SELL" :
            if time_frame_test == interval:
                order,api_key,sin = my_new_placing_order_short_and_long(close_price,"BUY","LONG")
        else:
                wait_for_time(420000,wait_time)
        #close_at_price = Decimal(close_at_price)
        return analysis_data
                
            
            

    
    
    def my_new_placing_order_short_and_long(close_at_price,side,position_side):
        try:
            API_KEY=''
            PRIVATE_KEY_PATH=""
            # Load the private key.
            # In this example the key is expected to be stored without encryption,
            # but we recommend using a strong password for improved security.
            with open(PRIVATE_KEY_PATH, 'rb') as f:
                private_key = load_pem_private_key(data=f.read(),
                                                password=None)
        
            key_size = private_key.key_size
            #print(key_size)
            #client = Client(api_key=API_KEY, private_key=private_key)
            #print(client.account())
            # Set up the request parameters
            # Set up the request parameters
            params = {
                'apiKey':        API_KEY,
                'symbol':       symbol,
                'quantity':     quan,
                'side':          side,
                'type':         'LIMIT', 
                "positionSide":position_side ,      
                "timeInForce":"GTC",
                "price": f"{close_at_price:.2f}",
                

            }
            
            # Timestamp the request
            timestamp = int(time.time() * 1000) # UNIX timestamp in milliseconds
            params['timestamp'] = timestamp

            # Sign the request
            payload = '&'.join([f'{param}={value}' for param, value in sorted(params.items())])

            signature = base64.b64encode(private_key.sign(payload.encode('ASCII') ,padding.PKCS1v15(),
                hashes.SHA256()))
            params['signature'] = signature.decode('ASCII')
            #params1['signature'] = signature.decode('ASCII')

            # Send the request
            request = {
                'id': 'my_new_order',
                'method': 'order.place',
                'params': params
            }

            ws = create_connection("wss://ws-fapi.binance.com/ws-fapi/v1")
            ws.send(json.dumps(request))
            result =  ws.recv()
            if "orderId" in result:
                listen_to_order(API_KEY)
            ws.close()
        except  Exception as e:
            print("[ERROR] Failed to get listenKey:", e)
            traceback.print_exc()
        #print(result)
        #print("final_inc",inc)
        #print("last_date",df_c.index[-1])
        print("Stop_price_"+interval,close_at_price)
    

        return result,API_KEY,signature
    
    def my_new_placing_order(close_at_price,side,position_side):
        try:
            API_KEY=''
            PRIVATE_KEY_PATH=""
            # Load the private key.
            # In this example the key is expected to be stored without encryption,
            # but we recommend using a strong password for improved security.
            with open(PRIVATE_KEY_PATH, 'rb') as f:
                private_key = load_pem_private_key(data=f.read(),
                                                password=None)
        
            key_size = private_key.key_size
            #print(key_size)
            #client = Client(api_key=API_KEY, private_key=private_key)
            #print(client.account())
            # Set up the request parameters
            # Set up the request parameters
            params = {
                'apiKey':        API_KEY,
                'symbol':       symbol,
                'quantity':     quan,
                'side':          side,
                'type':         'LIMIT',        
                "timeInForce":"GTC",
                "price": f"{close_at_price:.2f}",
                

            }
            
            # Timestamp the request
            timestamp = int(time.time() * 1000) # UNIX timestamp in milliseconds
            params['timestamp'] = timestamp

            # Sign the request
            payload = '&'.join([f'{param}={value}' for param, value in sorted(params.items())])

            signature = base64.b64encode(private_key.sign(payload.encode('ASCII') ,padding.PKCS1v15(),
                hashes.SHA256()))
            params['signature'] = signature.decode('ASCII')
            #params1['signature'] = signature.decode('ASCII')

            # Send the request
            request = {
                'id': 'my_new_order',
                'method': 'order.place',
                'params': params
            }

            ws = create_connection("wss://ws-fapi.binance.com/ws-fapi/v1")
            ws.send(json.dumps(request))
            result =  ws.recv()
            if "orderId" in result:
                listen_to_order(API_KEY)
            ws.close()
        except  Exception as e:
            print("[ERROR] Failed to get listenKey:", e)
            traceback.print_exc()
        print(result)
        #print("final_inc",inc)
        #print("last_date",df_c.index[-1])
        #print("Stop_price_"+interval,close_at_price)
    

        return result,API_KEY,signature
    
    def compute_close_time(df, symbol, market_open_time='09:30', market_close_time='16:00'):
        """
        df: DataFrame with 'Open Time' column
        symbol: str, the instrument symbol
        market_open_time: string, default '09:30' (local time of the market)
        market_close_time: string, default '16:00' (local time of the market)
        """
        # 1️⃣ Define the instrument timezone mapping
        instrument_timezone = {
            'AAPL': 'America/New_York',  # US stocks
            'NVDA': 'America/New_York',
            'USOil': 'UTC',              # Crude oil futures
            'BTC': 'UTC',                # Crypto
            # add more instruments as needed
        }
        tz = instrument_timezone.get(symbol, 'UTC')  # default UTC

        # 1️⃣ Ensure Open Time is datetime
        df['Open Time'] = pd.to_datetime(df['Open Time'], errors='coerce')

        # 2️⃣ Compute Close Time as difference from Open → Close in hours & minutes
        open_hour, open_minute = map(int, market_open_time.split(':'))
        close_hour, close_minute = map(int, market_close_time.split(':'))

        # Time delta between open and close
        delta_hours = close_hour - open_hour
        delta_minutes = close_minute - open_minute

        df['Close Time'] = df['Open Time'] + pd.Timedelta(hours=delta_hours, minutes=delta_minutes)
        """if stock == "NVDA":
            # 3️⃣ Convert to instrument timezone
            df['Close Time'] = df['Close Time'].dt.tz_localize('UTC').dt.tz_convert(tz)"""

        # 4️⃣ Drop invalid rows
        df = df.dropna(subset=['Close Time'])
        
        return df
    def get_stock_data(interval,stock,start_time,now_utc):
        if interval == "1M":
            interval = "1mo"
        if interval == "1w":
            interval = "1wk"    

        import yfinance as yf

        if stock != "NVDA":
            import MetaTrader5 as mt5
             # --- Configuration ---
            
            SYMBOL = stock
            if interval == "1mo":
                print("fuck yeah")
                TIMEFRAME = mt5.TIMEFRAME_MN1 # Example: 15-minute interval
            elif interval == "1wk":
                TIMEFRAME = mt5.TIMEFRAME_W1  # Example: 15-minute interval
            elif interval == "1d" or interval == "3d":
                TIMEFRAME = mt5.TIMEFRAME_D1  # Example: 15-minute interval 
            elif interval == "5m":
                TIMEFRAME = mt5.TIMEFRAME_M5 
            elif interval == "15m":
                TIMEFRAME = mt5.TIMEFRAME_M15        
            if interval == "3d":
                COUNT = 1501
            else:
                COUNT = 1500 # Number of bars to download
            
            if not mt5.initialize():
                print(f"Initialization failed, error code: {mt5.last_error()}")
                quit()
            else:
                print("MetaTrader 5 initialized successfully.")

            # --- Request Financial Data ---
            # Ensure the symbol is available in the Market Watch window of your MT5 terminal
            symbol_info = mt5.symbol_info(SYMBOL)
            if symbol_info is None:
                print(f"{SYMBOL} not found, please check the symbol name in your MT5 Market Watch.")
                mt5.shutdown()
                quit()

            # Use copy_rates_from_pos to get a specified number of bars from the end of the history
            
            rates = mt5.copy_rates_from_pos(SYMBOL, TIMEFRAME,0 , COUNT)

            # --- Process Data into a Pandas DataFrame ---
            if rates is not None and len(rates) > 0:
                print(f"Downloaded {len(rates)} bars for {SYMBOL}.")
                # Convert the array to a pandas DataFrame
                rates_frame = pd.DataFrame(rates)
                # Convert time in seconds to datetime object
                rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
                # Set time as index
                rates_frame.set_index('time', inplace=True)
                
                print("\nDataFrame (last 5 rows):")
                print(rates_frame.tail())
                df = rates_frame
                #df = rates_frame.tail()
            else:
                print("No data retrieved.")

            # --- Shutdown MT5 Connection ---
            mt5.shutdown()
        
        else:
            stock = yf.Ticker(stock)
            if interval == "3d":
                df = stock.history(start=start_time, end=now_utc, interval="1d")

            else:
             df = stock.history(start=start_time, end=now_utc, interval=interval)
        # Reset index so 'Date' becomes a column
        
        if stock != "NVDA":
            df["Open Time"] = pd.to_datetime(df.index)
            df["Open"] = df["open"]
            df["Close"] = df["close"]
            df["High"] = df["high"]
            df["Low"] = df["low"]
            df.set_index("Open Time",inplace=True)
            df["Open Time"] = df.index
        else:
            df = df.reset_index()
            df['Open Time'] = df['Date']
            df['Open Time'] = pd.to_datetime(df['Open Time'])
        
        
        print("Yes I can ",df["Open Time"])
        if interval == '1d':
            df['Close Time'] = df['Open Time'] + pd.Timedelta(hours=6, minutes=30)  # 09:30 -> 16:00 NY time
        elif interval == '1wk':
            # Week close = Friday 16:00
            df['Close Time'] = df['Open Time'] + pd.offsets.Week(weekday=4) + pd.Timedelta(hours=16) - pd.Timedelta(hours=9, minutes=30)
            print("I am here 0",df)
        elif interval == '1mo':
            # Month close = last calendar day 16:00
            if stock == "NVDA":
                df = compute_close_time(df, 'USOil', market_open_time='00:00', market_close_time='23:59')
            else:
                df = compute_close_time(df, 'NVDA', market_open_time='09:30', market_close_time='16:00')    
            print("We are here",df["Close Time"].head())
            print("Hey here",df["Close Time"].head())
        elif interval == "3d":
            # 1. Make sure datetime is parsed correctly
            df['Open Time'] = pd.to_datetime(df['Open Time'])
            df = df.set_index('Open Time').sort_index()
            if stock == "NVDA":
                df.index = df.index.tz_convert('America/New_York')
            first_date = df.index.min().floor('D')
            # 2. Resample 3-day OHLCV
            df_3d = df.resample('3D', origin=first_date).agg({
                'Open': 'first',
                'High': 'max',
                'Low': 'min',
                'Close': 'last',
            })

            # 3. Remove empty intervals
            #df_3d = df_3d.dropna(how='all')
            df_3d = df_3d.fillna(method='ffill')
            # 4. Add Open Time and Close Time columns
            df_3d['Open Time'] = df_3d.index
            df_3d['Close Time'] = df_3d['Open Time'] + pd.Timedelta(days=3) - pd.Timedelta(minutes=1)
            df = df_3d
            print(df_3d.head())
        elif interval == "5m":
            df["Close Time"] = df["Open Time"] +  timedelta(minutes=5)
        elif interval == "15m":
            df["Close Time"] = df["Open Time"] +  timedelta(minutes=15)    
        # Keep relevant columns
        #df = df[['Open Time', 'Close Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']]
        df["Open Time"] = df["Open Time"].astype('int64')
        print(df.head())
        return df
    def loop_the_trade(mt5):
        if not mt5.initialize():
            print("initialize() failed, error code =", mt5.last_error())
            quit()
    def do_trade_analysis(mt5,current_price,high,low,sell_price,status):
        now = datetime.now()
        minute = now.minute
        print("Minuits",minute)
        # minute inside the 15-minute cycle
        cycle_minute = minute % 15
        if 0 <= cycle_minute <= 4:
            minutes_into_block = now.minute % 5

            # how many minutes left until next 5-min block
            minutes_left = 4 - minutes_into_block

            # how many seconds left in the current minute
            seconds_left_in_minute = 59 - now.second

            # total seconds
            total_seconds = minutes_left * 60 + seconds_left_in_minute
            time.sleep(total_seconds+10)
            a = new_stock_bejaviour(None,0)

        elif 5 <= cycle_minute <= 9:
            if interval == "15m":
                get_analysis = start_analysis(Client.KLINE_INTERVAL_5MINUTE, now_date, 3, bitcon_symbol,quantity,time_frame[6],0,stock)
                print(get_analysis.head())
                new_high = float(get_analysis["High"].iloc[0])
                new_low = float(get_analysis["Low"].iloc[0])
                print("New High",new_high)
                print("New Low",new_low)
                print("You are in the SECOND 5-min block of the 15-min candle.")
                if new_high > high and new_high > current_price:
                    print("High is bigger")
                    return 0,new_high,current_price
                elif new_low < low and new_low < sell_price:
                    print("High is bigger")
                    return 1,new_low,sell_price
                else:
                    print("No trade Available")
                    return None,None,None
            elif interval == "5m":
                return None,None,None    
                minutes_into_block = now.minute % 5

                # how many minutes left until next 5-min block
                minutes_left = 4 - minutes_into_block

                # how many seconds left in the current minute
                seconds_left_in_minute = 59 - now.second

                # total seconds
                total_seconds = minutes_left * 60 + seconds_left_in_minute
                time.sleep(total_seconds)
        else:
            if status == 0:
                if interval == "15m": 
                    print("Status",status)   
                    minutes_into_block = now.minute % 5

                    # how many minutes left until next 5-min block
                    minutes_left = 4 - minutes_into_block

                    # how many seconds left in the current minute
                    seconds_left_in_minute = 59 - now.second

                    # total seconds
                    total_seconds = minutes_left * 60 + seconds_left_in_minute
                    time.sleep(total_seconds+10)
                    a = new_stock_bejaviour()
                else:
                    return None,None,None    
            else:
                if interval == "15m":
                    get_analysis = start_analysis(Client.KLINE_INTERVAL_5MINUTE, now_date, 3, bitcon_symbol,quantity,time_frame[6],0,stock)
                    print(get_analysis.head())
                    new_high = float(get_analysis["High"].iloc[0])
                    new_low = float(get_analysis["Low"].iloc[0])
                    print("New High",new_high)
                    print("New Low",new_low)
                    print("You are in the SECOND 5-min block of the 15-min candle.")
                    if new_high > high and new_high > current_price:
                        print("High is bigger")
                        return 0,new_high,current_price
                    elif new_low < low and new_low < sell_price:
                        print("High is bigger")
                        return 1,new_low,sell_price
                    else:
                        print("No trade Available")
                        return None,None,None
                elif interval == "5m":
                    return None,None,None  

        
        





             
           

    def do_trade(high,low,status):
        now_utc = datetime.now(timezone.utc)
        minute = now_utc.minute
        second = now_utc.second
        import time
        import MetaTrader5 as mt5
        # display data on the MetaTrader 5 package
        print("MetaTrader5 package author: ", mt5.__author__)
        print("MetaTrader5 package version: ", mt5.__version__)
        """MT5_LOGIN =   # Replace with your MT5 Login ID
        MT5_PASSWORD =  # Replace with your MT5 Password
        MT5_SERVER =  # Replace with your Exness server name (e.g., "Exness-MT5Trial")"""
        MT5_LOGIN =   # Replace with your MT5 Login ID
        MT5_PASSWORD =  # Replace with your MT5 Password
        MT5_SERVER =  # Replace with your Exness server name (e.g., "Exness-MT5Trial")
        # establish connection to the MetaTrader 5 terminal
        if not mt5.initialize(login=MT5_LOGIN, server=MT5_SERVER, password=MT5_PASSWORD):
            print("initialize() failed, error code =",mt5.last_error())
            quit()
        
        # prepare the buy request structure
        symbol = stock
        filling = mt5.symbol_info(symbol).filling_mode
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            print(symbol, "not found, can not call order_check()")
            mt5.shutdown()
            quit()
        
        # if the symbol is unavailable in MarketWatch, add it
        if not symbol_info.visible:
            print(symbol, "is not visible, trying to switch on")
            if not mt5.symbol_select(symbol,True):
                print("symbol_select({}}) failed, exit",symbol)
                mt5.shutdown()
                quit()
        
        lot = 0.1
        point = mt5.symbol_info(symbol).point
        price_ask = mt5.symbol_info_tick(symbol).ask
        price_bid = mt5.symbol_info_tick(symbol).ask
        #price_bid = mt5.symbol_info_tick(symbol).bid
        direction,tp,price = do_trade_analysis(mt5,price_ask,high,low,price_bid,status)
        if interval == "5m":
            return
        if direction != None:
            if direction == 0:
                sl = price -0.056
            else:
                sl = 0.04+price
            deviation = 20
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": lot,
                "type": direction,
                "price": price,
                "sl":sl,
                "tp": tp,
                "deviation": deviation,
                "magic": 234000,
                "comment": "python script open",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC ,
            }

            # send a trading request
            result = mt5.order_send(request)
            # check the execution result
            print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol,lot,price,deviation));
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                print("2. order_send failed, retcode={}".format(result.retcode))
                # request the result as a dictionary and display it element by element
                result_dict=result._asdict()
                for field in result_dict.keys():
                    print("   {}={}".format(field,result_dict[field]))
                    # if this is a trading request structure, display it element by element as well
                    if field=="request":
                        traderequest_dict=result_dict[field]._asdict()
                        for tradereq_filed in traderequest_dict:
                            print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
                print("shutdown() and quit")
                mt5.shutdown()
                quit()
                
            
            print("2. order_send done, ", result)
            print("   opened position with POSITION_TICKET={}".format(result.order))
            print("   sleep 2 seconds before closing position #{}".format(result.order))
            now_utc = datetime.now(timezone.utc)
            minute = now_utc.minute
            second = now_utc.second

           # Seconds to next 5-minute mark
            if interval == "15m":
                seconds_to_next_5min = (5 - (minute % 5)) * 60 - second
                print(seconds_to_next_5min)
                    
            elif interval == "5m":
                seconds_to_next_5min = (5 - (minute % 5)) * 60 - second

                print(seconds_to_next_5min)


            # Add 1 second
            seconds_to_next_5min -= 15
            time.sleep(seconds_to_next_5min)
            if direction == 0:
                opposite = 1
            else:
                opposite = 0    
            # create a close request
            position_id=result.order
            if opposite == 0:
                price=mt5.symbol_info_tick(symbol).ask
            else:
                price=mt5.symbol_info_tick(symbol).bid
            
            deviation=20
            request={
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": lot,
                "type": opposite,
                "position": position_id,
                "price": price,
                "deviation": deviation,
                "magic": 234000,
                "comment": "python script close",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            # send a trading request
            result=mt5.order_send(request)
            # check the execution result
            print("3. close position #{}: sell {} {} lots at {} with deviation={} points".format(position_id,symbol,lot,price,deviation));
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                now_utc = datetime.now(timezone.utc)
                minute = now_utc.minute
                second = now_utc.second

                # Seconds to next 5-minute mark
                if interval == "15m":
                    seconds_to_next_5min = (5 - (minute % 5)) * 60 - second

                    # Add 1 second
                    seconds_to_next_5min += 1

                    print(seconds_to_next_5min)
                    
                elif interval == "5m":

                    seconds_to_next_5min = (5 - (minute % 5)) * 60 - second

                    # Add 1 second
                    seconds_to_next_5min += 1

                    print(seconds_to_next_5min)
                time.sleep(seconds_to_next_5min)
                a = new_stock_bejaviour()
                print("4. order_send failed, retcode={}".format(result.retcode))
                print("   result",result)        
            else:
                print("4. position #{} closed, {}".format(position_id,result))
                now_utc = datetime.now(timezone.utc)
                minute = now_utc.minute
                second = now_utc.second

                # Seconds to next 5-minute mark
                if interval == "15m":
                    seconds_to_next_5min = (15 - (minute % 15)) * 60 - second

                    # Add 1 second
                    seconds_to_next_5min += 1

                    print(seconds_to_next_5min)
                    
                elif interval == "5m":

                    seconds_to_next_5min = (5 - (minute % 5)) * 60 - second

                    # Add 1 second
                    seconds_to_next_5min += 1

                    print(seconds_to_next_5min)
                time.sleep(seconds_to_next_5min)
                a = new_stock_bejaviour()
                # request the result as a dictionary and display it element by element
                result_dict=result._asdict()
                for field in result_dict.keys():
                    print("   {}={}".format(field,result_dict[field]))
                    # if this is a trading request structure, display it element by element as well
                    if field=="request":
                        traderequest_dict=result_dict[field]._asdict()
                        for tradereq_filed in traderequest_dict:
                            print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
            
            # shut down connection to the MetaTrader 5 terminal
            mt5.shutdown()
        else:
            now_utc = datetime.now(timezone.utc)
            minute = now_utc.minute
            second = now_utc.second

            # Seconds to next 5-minute mark
            if interval == "15m":
                    seconds_to_next_5min = (5 - (minute % 5)) * 60 - second

                    # Add 1 second

                    print(seconds_to_next_5min)
                    
            elif interval == "5m":

                    seconds_to_next_5min = (5 - (minute % 5)) * 60 - second

                    # Add 1 second

                    print(seconds_to_next_5min)


            # Add 1 second
            seconds_to_next_5min += 10

            print(seconds_to_next_5min)
            print("No trade available")
            time.sleep(seconds_to_next_5min)
            a = new_stock_bejaviour(None,1)        
    def new_stock_bejaviour(df_c = None,status=0):
        columns_to_convert = ['Open', 'High', 'Low', 'Close',"Open Time","Close Time"]
        now_utc = datetime.now(timezone.utc)
        if df_c is None:
            klines = get_stock_data(interval,stock,start_time,now_utc)
            df_m, columns_to_convert,analysis_data,high,low = binance_fetch_data(klines,inc)
            for col in columns_to_convert:
                df_m[col] = df_m[col].astype(float)
            

            if interval == "5m" or interval != None:
                low_constant = 0.0267803504
                high_constant = -0.02182752485

            print("Orignal High",high)
            print("Orignal low",low)
            do_trade(high,low,status)

            return analysis_data
        else:
            print("df_c is not None what Hell is that")

    
    if stock != None:
        analysis_data_fresh = new_stock_bejaviour()
        analysis_data_fresh["Interval"] = interval
        analysis_data_fresh["Interval"].iloc[1:] = None
    else:
        analysis_data_fresh = new_trading_behaviour() 
        analysis_data_fresh["Interval"] = interval  
        analysis_data_fresh["Interval"] = interval 
    
    
    return analysis_data_fresh


    
    

me = ""
bitcon_symbol = 'BTCUSDT'

now_date = datetime(2025, 10, 1, 2, 5, 0, tzinfo=timezone.utc)
now_date = datetime.now(tz=timezone.utc) 
import pytz
from zoneinfo import ZoneInfo


quantity = .02
# inc = 1
time_frame = ["1s","1m", "3m", "5m", "15m", "1m","30m","1h","2h","4h","6h","8h","12h"]
inc = 0
all_anaylsis = None
"""  """
#start_analysis(Client.KLINE_INTERVAL_3MONTH, now_date, 3500, bitcon_symbol,quantity,time_frame[6],3)
"""start_analysis(Client.KLINE_INTERVAL_1MONTH, now_date, 3500, bitcon_symbol,quantity,time_frame[6],3)

start_analysis(Client.KLINE_INTERVAL_1WEEK, now_date, 3500, bitcon_symbol,quantity,time_frame[6],3)
 
#start_analysis(Client.KLINE_INTERVAL_2WEEK, now_date, 3500, bitcon_symbol,quantity,time_frame[6],3)
  
start_analysis(Client.KLINE_INTERVAL_3DAY, now_date, 3500, bitcon_symbol,quantity,time_frame[6],3)
start_analysis(Client.KLINE_INTERVAL_1DAY, now_date, 3500, bitcon_symbol,quantity,time_frame[6],3)
 
start_analysis(Client.KLINE_INTERVAL_4HOUR, now_date, 3500, bitcon_symbol,quantity,time_frame[6],6)
start_analysis(Client.KLINE_INTERVAL_1HOUR, now_date, 12000, bitcon_symbol,quantity,time_frame[6],12)
start_analysis(Client.KLINE_INTERVAL_30MINUTE, now_date, 600, bitcon_symbol,quantity,time_frame[6],32)
start_analysis(Client.KLINE_INTERVAL_15MINUTE, now_date, 150, bitcon_symbol,quantity,time_frame[6],32)
#start_analysis(Client.KLINE_INTERVAL_10MINUTE, now_date, 50, bitcon_symbol,quantity,time_frame[6],32)
start_analysis(Client.KLINE_INTERVAL_5MINUTE, now_date, 50, bitcon_symbol,quantity,time_frame[6],32)
start_analysis(Client.KLINE_INTERVAL_1MINUTE, now_date, 10, bitcon_symbol,quantity,time_frame[6],500)
start_analysis(Client.KLINE_INTERVAL_1SECOND, now_date, 1, bitcon_symbol,quantity,time_frame[6],900)
get_analysis = start_analysis(Client.KLINE_INTERVAL_1WEEK, now_date, 3500, bitcon_symbol,quantity,time_frame[6],3)
all_anaylsis = get_analysis.iloc[[0]]
get_analysis = start_analysis(Client.KLINE_INTERVAL_1DAY, now_date, 3500, bitcon_symbol,quantity,time_frame[6],3)
get_analysis = start_analysis(Client.KLINE_INTERVAL_4HOUR, now_date, 3500, bitcon_symbol,quantity,time_frame[6],6)
all_anaylsis = pd.concat([all_anaylsis, get_analysis.iloc[[0]]], ignore_index=True)

get_analysis = start_analysis(Client.KLINE_INTERVAL_1HOUR, now_date, 12000, bitcon_symbol,quantity,time_frame[6],12)
all_anaylsis = pd.concat([all_anaylsis, get_analysis.iloc[[0]]], ignore_index=True)
get_analysis = start_analysis(Client.KLINE_INTERVAL_15MINUTE, now_date, 150, bitcon_symbol,quantity,time_frame[6],32)
all_anaylsis = pd.concat([all_anaylsis, get_analysis.iloc[[0]]], ignore_index=True)
get_analysis = start_analysis(Client.KLINE_INTERVAL_5MINUTE, now_date, 50, bitcon_symbol,quantity,time_frame[6],32)
all_anaylsis = pd.concat([all_anaylsis, get_analysis.iloc[[0]]], ignore_index=True)
all_anaylsis.to_csv(r"G:\mahmoud\analysis\analysis_"+"_"+egypt_time_string+".csv", index=False, encoding='utf-8')

get_analysis = start_analysis(Client.KLINE_INTERVAL_3MINUTE, now_date, 50, bitcon_symbol,quantity,time_frame[6],50)
get_analysis = start_analysis(Client.KLINE_INTERVAL_1MINUTE, now_date, 10, bitcon_symbol,quantity,time_frame[6],500)
"""
eastern = ZoneInfo("America/New_York")

now_date = datetime.now(tz=timezone.utc)
#now_date = datetime.now(tz=ZoneInfo("America/New_York"))
egypt_time = now_date.astimezone(ZoneInfo("Africa/Cairo"))
egypt_time_string = egypt_time.strftime("%Y-%m-%d %H_%M_%S")
print("run on time utc", now_date)

stock = None
#stock = "NVDA"
#stock = "UKOILm"
#stock = "XALUSDm"
stock = "USOILm"
get_analysis = start_analysis(Client.KLINE_INTERVAL_15MINUTE, now_date, 15, bitcon_symbol,quantity,time_frame[6],0,stock)



"""
get_analysis = start_analysis(Client.KLINE_INTERVAL_1MONTH, now_date , 45000, bitcon_symbol,quantity,time_frame[6],0,stock)
print("get_analysis",get_analysis)
all_anaylsis = get_analysis.iloc[[0]]

get_analysis = start_analysis(Client.KLINE_INTERVAL_1WEEK, now_date , 6000, bitcon_symbol,quantity,time_frame[6],0,stock)
all_anaylsis = pd.concat([all_anaylsis, get_analysis.iloc[[0]]], ignore_index=True)

get_analysis = start_analysis(Client.KLINE_INTERVAL_3DAY, now_date ,4502, bitcon_symbol,quantity,time_frame[6],0,stock)
print("You yeah",get_analysis.head())
all_anaylsis = pd.concat([all_anaylsis, get_analysis.iloc[[0]]], ignore_index=True)

get_analysis = start_analysis(Client.KLINE_INTERVAL_1DAY, now_date, 1500, bitcon_symbol,quantity,time_frame[6],0,stock)
all_anaylsis = pd.concat([all_anaylsis, get_analysis.iloc[[0]]], ignore_index=True)"""
#get_analysis = start_analysis(Client.KLINE_INTERVAL_4HOUR, now_date, 250, bitcon_symbol,quantity,time_frame[6],6)
#all_anaylsis = pd.concat([all_anaylsis, get_analysis.iloc[[0]]], ignore_index=True)

"""if stock is not None:
    all_anaylsis.to_csv(r"G:\mahmoud\analysis\analysis_"+"_"+egypt_time_string+"_"+stock+".csv", index=False, encoding='utf-8')

else:
    all_anaylsis.to_csv(r"G:\mahmoud\analysis\analysis_"+"_"+egypt_time_string+".csv", index=False, encoding='utf-8')"""
"""get_analysis = start_analysis(Client.KLINE_INTERVAL_4HOUR, now_date, 250, bitcon_symbol,quantity,time_frame[6],6)
all_anaylsis = pd.concat([all_anaylsis, get_analysis.iloc[[0]]], ignore_index=True)

get_analysis = start_analysis(Client.KLINE_INTERVAL_1HOUR, now_date, 62, bitcon_symbol,quantity,time_frame[6],12)
all_anaylsis = pd.concat([all_anaylsis, get_analysis.iloc[[0]]], ignore_index=True)
get_analysis = start_analysis(Client.KLINE_INTERVAL_15MINUTE, now_date, 15, bitcon_symbol,quantity,time_frame[6],12)
all_anaylsis = pd.concat([all_anaylsis, get_analysis.iloc[[0]]], ignore_index=True)
get_analysis = start_analysis(Client.KLINE_INTERVAL_5MINUTE, now_date, 3, bitcon_symbol,quantity,time_frame[6],32)
all_anaylsis = pd.concat([all_anaylsis, get_analysis.iloc[[0]]], ignore_index=True)
#all_anaylsis.to_csv(r"G:\mahmoud\analysis\analysis_"+"_"+egypt_time_string+".csv", index=False, encoding='utf-8')
get_analysis = start_analysis(Client.KLINE_INTERVAL_3MINUTE, now_date, 3, bitcon_symbol,quantity,time_frame[6],50)
all_anaylsis = pd.concat([all_anaylsis, get_analysis.iloc[[0]]], ignore_index=True)

get_analysis = start_analysis(Client.KLINE_INTERVAL_1MINUTE, now_date, 1, bitcon_symbol,quantity,time_frame[6],500)

all_anaylsis = pd.concat([all_anaylsis, get_analysis.iloc[[0]]], ignore_index=True)"""

plt.show()


#get_analysis = start_analysis(Client.KLINE_INTERVAL_1DAY, now_date, 1500, bitcon_symbol,quantity,time_frame[6],3)

