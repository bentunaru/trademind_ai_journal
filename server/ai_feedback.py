import os
import logging
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_trade_feedback(trade_data: dict) -> str:
    """
    Generate AI feedback for a trade using OpenAI API
    
    Args:
        trade_data: Dictionary containing trade information
        
    Returns:
        AI-generated feedback string
    """
    try:
        # Construct the prompt
        prompt = f"""
        Analyze this futures trade and provide professional feedback:
        
        Instrument: {trade_data['instrument']}
        Direction: {trade_data['direction']}
        Entry Price: {trade_data['entry_price']}
        Stop Loss: {trade_data['stop_loss']}
        Take Profit: {trade_data['take_profit']}
        Risk/Reward: {trade_data.get('risk_reward', 'Not specified')}
        
        Trader's Notes: {trade_data.get('notes', 'No notes provided')}
        
        Please provide feedback on:
        1. Risk management
        2. Trade setup and execution
        3. Areas for improvement
        4. Overall trade quality score (1-10)
        """
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",  # or another appropriate model
            messages=[
                {"role": "system", "content": "You are an expert futures trading coach specializing in ES and NQ futures. You provide concise, actionable feedback on trades."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        feedback = response.choices[0].message.content
        logger.info(f"Successfully generated AI feedback for {trade_data['instrument']} trade")
        return feedback
        
    except Exception as e:
        logger.error(f"Error generating AI feedback: {str(e)}")
        raise

def analyze_market_structure(structure_data: dict) -> str:
    """
    Generate AI analysis for a market structure (BOS/CHoCH)
    
    Args:
        structure_data: Dictionary containing structure information
        
    Returns:
        AI-generated analysis string
    """
    try:
        # Construct the prompt
        prompt = f"""
        Analyze this market structure formation:
        
        Instrument: {structure_data['instrument']}
        Type: {structure_data['structure_type']}
        Direction: {structure_data['direction']}
        Price Level: {structure_data['price_level']}
        
        Notes: {structure_data.get('notes', 'No notes provided')}
        
        Please provide analysis on:
        1. Significance of this structure
        2. Potential trading opportunities
        3. Key levels to watch
        4. Risk considerations
        """
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",  # or another appropriate model
            messages=[
                {"role": "system", "content": "You are an expert in market structure analysis, specializing in Break of Structure (BOS) and Change of Character (CHoCH) patterns in futures markets."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        analysis = response.choices[0].message.content
        logger.info(f"Successfully generated structure analysis for {structure_data['instrument']}")
        return analysis
        
    except Exception as e:
        logger.error(f"Error generating structure analysis: {str(e)}")
        raise 