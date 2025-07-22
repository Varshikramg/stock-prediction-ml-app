# Stock Prediction ML App

A full-stack machine learning application that predicts stock prices for 20 major companies using TensorFlow, Python Flask backend, and React/Next.js frontend.

## Features

- **AI-Powered Predictions**: Advanced LSTM neural networks analyze historical data patterns
- **Real-Time Data**: Live market data from Yahoo Finance API for accurate predictions
- **20 Major Companies**: Predictions for FAANG stocks and other market leaders
- **Interactive Charts**: Beautiful visualizations using Recharts
- **Modern UI**: Clean, responsive design with Tailwind CSS

## Tech Stack

### Backend
- **Python Flask**: RESTful API server
- **TensorFlow**: Machine learning model for stock prediction
- **yfinance**: Real-time stock data fetching
- **NumPy & Pandas**: Data processing and analysis

### Frontend
- **Next.js 15**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Modern styling
- **Recharts**: Interactive charts and visualizations
- **Axios**: HTTP client for API calls

## Setup Instructions

### Prerequisites
- Python 3.8+ installed
- Node.js 18+ installed
- npm or yarn package manager

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Start the Flask server:
```bash
python start.py
```

The backend will be available at `http://localhost:5000`

### Frontend Setup

1. Navigate to the project root directory:
```bash
cd ..
```

2. Install Node.js dependencies:
```bash
npm install --legacy-peer-deps
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:8000`

## Usage

1. **Start Backend**: Make sure the Python Flask server is running on port 5000
2. **Open Frontend**: Navigate to `http://localhost:8000` in your browser
3. **Navigate to Stocks**: Click "Start Predicting Stocks" or go to `/stocks`
4. **Generate Predictions**: Click "Generate AI Predictions" to get ML-powered stock predictions
5. **View Results**: Analyze predictions in tables and interactive charts

## API Endpoints

### Backend API (Flask - Port 5000)

- `GET /health` - Health check endpoint
- `POST /predict` - Generate stock predictions for all 20 companies
- `GET /company/<symbol>` - Get historical data for a specific company

### Example API Response

```json
{
  "success": true,
  "data": [
    {
      "company": "Apple Inc.",
      "symbol": "AAPL",
      "predictedPrice": 185.42,
      "timestamp": "2024-01-15T10:30:00"
    }
  ],
  "message": "Predictions generated for 20 companies"
}
```

## Companies Included

The app predicts stock prices for these 20 major companies:

1. Apple Inc. (AAPL)
2. Microsoft Corporation (MSFT)
3. Amazon.com Inc. (AMZN)
4. Alphabet Inc. (GOOGL)
5. Tesla Inc. (TSLA)
6. Meta Platforms Inc. (META)
7. NVIDIA Corporation (NVDA)
8. Netflix Inc. (NFLX)
9. Adobe Inc. (ADBE)
10. Salesforce Inc. (CRM)
11. PayPal Holdings Inc. (PYPL)
12. Intel Corporation (INTC)
13. Cisco Systems Inc. (CSCO)
14. Comcast Corporation (CMCSA)
15. PepsiCo Inc. (PEP)
16. Coca-Cola Company (KO)
17. Walt Disney Company (DIS)
18. Mastercard Inc. (MA)
19. Johnson & Johnson (JNJ)
20. Procter & Gamble Co. (PG)

## Machine Learning Model

The application uses a simple LSTM (Long Short-Term Memory) neural network built with TensorFlow:

- **Input Features**: Historical stock data (Open, High, Low, Close, Volume)
- **Architecture**: Multi-layer LSTM with dropout for regularization
- **Prediction**: Next-day stock price prediction
- **Data Source**: Yahoo Finance API via yfinance library

## Development

### Project Structure

```
├── backend/
│   ├── app.py              # Flask application
│   ├── requirements.txt    # Python dependencies
│   └── start.py           # Startup script
├── src/
│   ├── app/
│   │   ├── layout.tsx     # Root layout
│   │   ├── page.tsx       # Home page
│   │   └── stocks/
│   │       └── page.tsx   # Stock predictions page
│   └── components/        # Reusable components
├── package.json           # Node.js dependencies
└── README.md             # This file
```

### Adding New Features

1. **New Companies**: Add to the `COMPANIES` list in `backend/app.py`
2. **Enhanced ML Model**: Modify the `StockPredictor` class
3. **UI Components**: Add new components in `src/components/`
4. **New Pages**: Create new pages in `src/app/`

## Troubleshooting

### Backend Issues

- **Port 5000 in use**: Change the port in `backend/app.py`
- **Python dependencies**: Ensure all packages in `requirements.txt` are installed
- **API timeout**: Increase timeout in frontend axios calls

### Frontend Issues

- **Dependency conflicts**: Use `npm install --legacy-peer-deps`
- **TypeScript errors**: Check type definitions and imports
- **Build errors**: Clear `.next` cache and rebuild

### Common Errors

1. **Backend Offline**: Ensure Flask server is running on port 5000
2. **CORS Issues**: Flask-CORS is configured to allow all origins
3. **API Timeout**: ML predictions may take 30-60 seconds for all companies

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational purposes. Stock predictions are not financial advice.

## Disclaimer

This application is for educational and demonstration purposes only. The stock predictions generated by this ML model should not be used for actual trading or investment decisions. Always consult with financial professionals before making investment choices.
