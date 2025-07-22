from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import tensorflow as tf
from tensorflow import keras
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# List of 20 major companies with their stock symbols
COMPANIES = [
    {"name": "Apple Inc.", "symbol": "AAPL"},
    {"name": "Microsoft Corporation", "symbol": "MSFT"},
    {"name": "Amazon.com Inc.", "symbol": "AMZN"},
    {"name": "Alphabet Inc.", "symbol": "GOOGL"},
    {"name": "Tesla Inc.", "symbol": "TSLA"},
    {"name": "Meta Platforms Inc.", "symbol": "META"},
    {"name": "NVIDIA Corporation", "symbol": "NVDA"},
    {"name": "Netflix Inc.", "symbol": "NFLX"},
    {"name": "Adobe Inc.", "symbol": "ADBE"},
    {"name": "Salesforce Inc.", "symbol": "CRM"},
    {"name": "PayPal Holdings Inc.", "symbol": "PYPL"},
    {"name": "Intel Corporation", "symbol": "INTC"},
    {"name": "Cisco Systems Inc.", "symbol": "CSCO"},
    {"name": "Comcast Corporation", "symbol": "CMCSA"},
    {"name": "PepsiCo Inc.", "symbol": "PEP"},
    {"name": "Coca-Cola Company", "symbol": "KO"},
    {"name": "Walt Disney Company", "symbol": "DIS"},
    {"name": "Mastercard Inc.", "symbol": "MA"},
    {"name": "Johnson & Johnson", "symbol": "JNJ"},
    {"name": "Procter & Gamble Co.", "symbol": "PG"}
]

class StockPredictor:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.sequence_length = 60
        
    def create_model(self, input_shape):
        """Create a simple LSTM model for stock prediction"""
        model = keras.Sequential([
            keras.layers.LSTM(50, return_sequences=True, input_shape=input_shape),
            keras.layers.Dropout(0.2),
            keras.layers.LSTM(50, return_sequences=True),
            keras.layers.Dropout(0.2),
            keras.layers.LSTM(50),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(25),
            keras.layers.Dense(1)
        ])
        
        model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
        return model
    
    def get_stock_data(self, symbol, period="1y"):
        """Fetch stock data using yfinance"""
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(period=period)
            return data
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {str(e)}")
            return None
    
    def prepare_data(self, data):
        """Prepare data for training/prediction"""
        if data is None or len(data) < self.sequence_length:
            return None, None
            
        # Use closing prices
        prices = data['Close'].values.reshape(-1, 1)
        
        # Simple normalization (min-max scaling)
        min_price = np.min(prices)
        max_price = np.max(prices)
        normalized_prices = (prices - min_price) / (max_price - min_price)
        
        # Create sequences
        X, y = [], []
        for i in range(self.sequence_length, len(normalized_prices)):
            X.append(normalized_prices[i-self.sequence_length:i, 0])
            y.append(normalized_prices[i, 0])
        
        return np.array(X), np.array(y), min_price, max_price
    
    def predict_stock_price(self, symbol):
        """Predict next day stock price for a given symbol"""
        try:
            # Get historical data
            data = self.get_stock_data(symbol)
            if data is None:
                return None
            
            # Prepare data
            X, y, min_price, max_price = self.prepare_data(data)
            if X is None:
                return None
            
            # Create and train a simple model (in production, you'd load a pre-trained model)
            model = self.create_model((self.sequence_length, 1))
            
            # For demo purposes, we'll use a very simple training or just return a prediction
            # In a real scenario, you'd have a pre-trained model
            X = X.reshape((X.shape[0], X.shape[1], 1))
            
            # Simple prediction based on recent trend
            recent_data = X[-1:].reshape(1, self.sequence_length, 1)
            
            # For demo, create a simple prediction based on moving average and trend
            recent_prices = data['Close'].tail(10).values
            trend = np.mean(np.diff(recent_prices))
            current_price = data['Close'].iloc[-1]
            
            # Simple prediction: current price + trend with some randomness
            predicted_price = current_price + trend + np.random.normal(0, abs(current_price * 0.02))
            
            return max(predicted_price, 0.01)  # Ensure positive price
            
        except Exception as e:
            logger.error(f"Error predicting for {symbol}: {str(e)}")
            return None

# Initialize predictor
predictor = StockPredictor()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Stock prediction API is running"})

@app.route('/predict', methods=['POST'])
def predict_stocks():
    """Predict stock prices for all companies"""
    try:
        logger.info("Starting stock prediction for all companies")
        predictions = []
        
        for company in COMPANIES:
            logger.info(f"Predicting for {company['name']} ({company['symbol']})")
            
            predicted_price = predictor.predict_stock_price(company['symbol'])
            
            if predicted_price is not None:
                predictions.append({
                    "company": company['name'],
                    "symbol": company['symbol'],
                    "predictedPrice": round(predicted_price, 2),
                    "timestamp": datetime.now().isoformat()
                })
            else:
                # Fallback prediction if real data fails
                fallback_price = np.random.uniform(50, 500)
                predictions.append({
                    "company": company['name'],
                    "symbol": company['symbol'],
                    "predictedPrice": round(fallback_price, 2),
                    "timestamp": datetime.now().isoformat(),
                    "note": "Fallback prediction due to data unavailability"
                })
        
        logger.info(f"Successfully generated predictions for {len(predictions)} companies")
        
        return jsonify({
            "success": True,
            "data": predictions,
            "message": f"Predictions generated for {len(predictions)} companies"
        })
        
    except Exception as e:
        logger.error(f"Error in predict_stocks: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Failed to generate predictions",
            "message": str(e)
        }), 500

@app.route('/company/<symbol>', methods=['GET'])
def get_company_data(symbol):
    """Get historical data for a specific company"""
    try:
        data = predictor.get_stock_data(symbol.upper())
        if data is None:
            return jsonify({"success": False, "error": "Company not found"}), 404
        
        # Return last 30 days of data
        recent_data = data.tail(30)
        result = {
            "symbol": symbol.upper(),
            "data": [
                {
                    "date": date.strftime('%Y-%m-%d'),
                    "open": round(row['Open'], 2),
                    "high": round(row['High'], 2),
                    "low": round(row['Low'], 2),
                    "close": round(row['Close'], 2),
                    "volume": int(row['Volume'])
                }
                for date, row in recent_data.iterrows()
            ]
        }
        
        return jsonify({"success": True, "data": result})
        
    except Exception as e:
        logger.error(f"Error getting company data for {symbol}: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
