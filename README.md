# Stock Trading Signals with Kafka

This project implements a real-time stock trading signal system using Apache Kafka and the moving average strategy. The system fetches intraday stock price data for IBM from Alpha Vantage, processes it with Kafka, and generates trading signals based on a 50-period moving average.

## Project Overview

In this project, we developed a system to track stock prices and generate trading signals using the moving average strategy. Here's a concise explanation of the project's components and workflows:

### Data Source
- **Alpha Vantage**: We use Alpha Vantage's API to obtain intraday stock price data for IBM at 5-minute intervals.

### Kafka Integration
- **Producer**: Fetches stock data from Alpha Vantage and publishes it to a Kafka topic named `stock_prices`.
- **Consumer**: Subscribes to the `stock_prices` topic, reads messages, and calculates the 50-period moving average (MA50).

### Moving Average Strategy
- **Indicator**: 50-period Moving Average (MA50)
- **Buy Signal**: Generated when the current stock price crosses above the MA50.
- **Sell Signal**: Generated when the current stock price falls below the MA50.

This strategy aims to capitalize on trends by comparing the current price to the MA50 to make trading decisions.
