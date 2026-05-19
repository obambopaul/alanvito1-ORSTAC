import websocket
import json

# Replace 1089 with your own App ID from api.deriv.com
APP_ID = "1089" 
WS_URL = f"wss://ws.binaryws.com/websockets/v3?app_id={APP_ID}"

def on_open(ws):
    print("✅ Connected to Deriv API!")
    
    # Send a request to subscribe to Volatility 100 Index ticks
    request = json.dumps({
        "ticks": "R_100",
        "subscribe": 1
    })
    ws.send(request)
    print("📡 Subscribed to R_100 ticks...")

def on_message(ws, message):
    # Parse the incoming JSON data
    data = json.loads(message)
    
    # Check if the message contains tick data
    if 'tick' in data:
        price = data['tick']['quote']
        time = data['tick']['epoch']
        
        # Get the last digit of the price (what the "ProfitPlus" app looks at)
        price_str = str(price)
        last_digit = price_str[-1]
        
        print(f"Price: {price} | Last Digit: {last_digit}")

def on_error(ws, error):
    print(f"❌ Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("🔴 Connection Closed")

# Start the connection
if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        WS_URL,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    # Run the loop forever to keep receiving live data
    ws.run_forever()
