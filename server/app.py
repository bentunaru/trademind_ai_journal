from flask import Flask, request, jsonify
import os
from datetime import datetime
import logging
from dotenv import load_dotenv

# Local imports
from supabase_client import SupabaseClient
from ai_feedback import generate_trade_feedback, analyze_market_structure
from screenshot_handler import save_base64_screenshot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
supabase = SupabaseClient()

@app.route('/webhook/structure', methods=['POST'])
def handle_structure():
    """
    Webhook endpoint for receiving BOS/ChoCH structure signals from TradingView
    Expected JSON format:
    {
        "instrument": "ES",
        "structure_type": "BOS" | "CHoCH",
        "price_level": 4500.25,
        "direction": "BULLISH" | "BEARISH",
        "screenshot": "optional_base64_image",
        "notes": "optional_notes"
    }
    """
    try:
        data = request.json
        required_fields = ['instrument', 'structure_type', 'price_level', 'direction']
        
        # Validate required fields
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
                
        # Validate structure_type
        if data['structure_type'] not in ['BOS', 'CHoCH']:
            return jsonify({'error': 'Invalid structure_type. Must be BOS or CHoCH'}), 400
            
        # Validate direction
        if data['direction'] not in ['BULLISH', 'BEARISH']:
            return jsonify({'error': 'Invalid direction. Must be BULLISH or BEARISH'}), 400

        # Handle screenshot if provided
        screenshot_url = None
        if data.get('screenshot'):
            try:
                screenshot_url = save_base64_screenshot(data['screenshot'])
                logger.info(f"Screenshot saved successfully: {screenshot_url}")
            except Exception as e:
                logger.error(f"Error saving screenshot: {str(e)}")

        # Insert structure into Supabase
        structure_data = {
            "instrument": data['instrument'],
            "structure_type": data['structure_type'],
            "price_level": float(data['price_level']),
            "direction": data['direction'],
            "screenshot_url": screenshot_url,
            "notes": data.get('notes')
        }
        
        result = supabase.insert_structure(**structure_data)

        # Generate AI analysis if notes are provided
        analysis = None
        if data.get('notes'):
            try:
                analysis = analyze_market_structure(data)
                # TODO: Update the structure with AI analysis
                logger.info("AI analysis generated successfully")
            except Exception as e:
                logger.error(f"Error generating AI analysis: {str(e)}")
        
        response_data = {**result, "ai_analysis": analysis} if analysis else result
        logger.info(f"Successfully processed structure: {data['structure_type']} on {data['instrument']}")
        return jsonify(response_data), 201
        
    except Exception as e:
        logger.error(f"Error processing structure webhook: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/webhook/trade', methods=['POST'])
def handle_trade():
    """
    Webhook endpoint for receiving trade execution signals from TradingView
    Expected JSON format:
    {
        "instrument": "ES",
        "direction": "LONG" | "SHORT",
        "entry_price": 4500.25,
        "stop_loss": 4480.50,
        "take_profit": 4550.75,
        "screenshot": "optional_base64_image",
        "notes": "optional_notes",
        "risk_reward": 2.5
    }
    """
    try:
        data = request.json
        required_fields = ['instrument', 'direction', 'entry_price', 'stop_loss', 'take_profit']
        
        # Validate required fields
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
                
        # Validate direction
        if data['direction'] not in ['LONG', 'SHORT']:
            return jsonify({'error': 'Invalid direction. Must be LONG or SHORT'}), 400

        # Handle screenshot if provided
        screenshot_url = None
        if data.get('screenshot'):
            try:
                screenshot_url = save_base64_screenshot(data['screenshot'])
                logger.info(f"Screenshot saved successfully: {screenshot_url}")
            except Exception as e:
                logger.error(f"Error saving screenshot: {str(e)}")

        # Calculate risk/reward if not provided
        risk_reward = data.get('risk_reward')
        if not risk_reward:
            entry = float(data['entry_price'])
            sl = float(data['stop_loss'])
            tp = float(data['take_profit'])
            risk = abs(entry - sl)
            reward = abs(tp - entry)
            risk_reward = round(reward / risk, 2) if risk != 0 else 0

        # Insert trade into Supabase
        trade_data = {
            "instrument": data['instrument'],
            "direction": data['direction'],
            "entry_price": float(data['entry_price']),
            "stop_loss": float(data['stop_loss']),
            "take_profit": float(data['take_profit']),
            "screenshot_url": screenshot_url,
            "notes": data.get('notes'),
            "risk_reward": risk_reward
        }
        
        result = supabase.insert_trade(**trade_data)
        
        # Generate AI feedback if notes are provided
        feedback = None
        if data.get('notes'):
            try:
                feedback = generate_trade_feedback(data)
                # TODO: Update the trade with AI feedback
                logger.info("AI feedback generated successfully")
            except Exception as e:
                logger.error(f"Error generating AI feedback: {str(e)}")
        
        response_data = {**result, "ai_feedback": feedback} if feedback else result
        logger.info(f"Successfully processed trade: {data['direction']} {data['instrument']}")
        return jsonify(response_data), 201
        
    except Exception as e:
        logger.error(f"Error processing trade webhook: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/test-supabase')
def test_supabase():
    try:
        # Just try to fetch any data from trades table
        result = supabase.client.table('trades').select('*').limit(1).execute()
        return jsonify({
            "status": "success",
            "message": "Connected to Supabase successfully",
            "data": result.data
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "type": str(type(e))
        }), 500

@app.route('/test-tables')
def test_tables():
    try:
        # Try to create tables if they don't exist
        result = supabase.client.rpc(
            'create_trading_tables',
            params={}
        ).execute()
        return jsonify({"status": "success", "message": "Tables created/verified"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001) 