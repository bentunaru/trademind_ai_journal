import os
import base64
from io import BytesIO
from datetime import datetime
import logging
from supabase_client import SupabaseClient

logger = logging.getLogger(__name__)

def save_base64_screenshot(base64_string: str, trade_id: str = None) -> str:
    """
    Save a base64 encoded screenshot to Supabase Storage
    
    Args:
        base64_string: Base64 encoded image string
        trade_id: Optional trade ID to include in filename
        
    Returns:
        Public URL of the uploaded screenshot
    """
    try:
        # Remove data:image/png;base64, if present
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]
            
        # Decode base64 string
        image_data = base64.b64decode(base64_string)
        
        # Create BytesIO object
        image_buffer = BytesIO(image_data)
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{trade_id}.png" if trade_id else f"{timestamp}.png"
        
        # Upload to Supabase Storage
        public_url = SupabaseClient.upload_screenshot(
            file=image_buffer,
            filename=filename
        )
        
        logger.info(f"Successfully uploaded screenshot: {filename}")
        return public_url
        
    except Exception as e:
        logger.error(f"Error saving screenshot: {str(e)}")
        raise 