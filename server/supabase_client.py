import os
from datetime import datetime
from typing import Optional, Dict, Any, BinaryIO
from dotenv import load_dotenv
from supabase import create_client, Client
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class SupabaseClient:
    def __init__(self):
        """Initialize Supabase client with environment variables."""
        self.client = create_client(
            os.getenv("SUPABASE_URL", ""),
            os.getenv("SUPABASE_KEY", "")
        )

    def insert_trade(
        self,
        instrument: str,
        direction: str,
        entry_price: float,
        stop_loss: float,
        take_profit: float,
        screenshot_url: Optional[str] = None,
        notes: Optional[str] = None,
        risk_reward: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Insert a new trade into the trades table.
        
        Args:
            instrument: Trading instrument (e.g., "ES", "NQ")
            direction: Trade direction ("LONG" or "SHORT")
            entry_price: Entry price of the trade
            stop_loss: Stop loss price
            take_profit: Take profit price
            screenshot_url: Optional URL to the trade screenshot
            notes: Optional trading notes
            risk_reward: Optional risk/reward ratio
            
        Returns:
            Dict containing the inserted trade data
        """
        try:
            trade_data = {
                "instrument": instrument,
                "direction": direction,
                "entry_price": entry_price,
                "stop_loss": stop_loss,
                "take_profit": take_profit,
                "screenshot_url": screenshot_url,
                "notes": notes,
                "risk_reward": risk_reward
            }
            
            result = self.client.table("trades").insert(trade_data).execute()
            logger.info(f"Successfully inserted trade for {instrument}")
            return result.data[0]
            
        except Exception as e:
            logger.error(f"Error inserting trade: {str(e)}")
            raise

    def insert_structure(
        self,
        instrument: str,
        structure_type: str,  # "BOS" or "CHoCH"
        price_level: float,
        direction: str,  # "BULLISH" or "BEARISH"
        screenshot_url: Optional[str] = None,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Insert a new market structure into the structures table.
        
        Args:
            instrument: Trading instrument
            structure_type: Type of structure ("BOS" or "CHoCH")
            price_level: Price level where the structure formed
            direction: Structure direction ("BULLISH" or "BEARISH")
            screenshot_url: Optional URL to structure screenshot
            notes: Optional notes about the structure
            
        Returns:
            Dict containing the inserted structure data
        """
        try:
            structure_data = {
                "instrument": instrument,
                "structure_type": structure_type,
                "price_level": price_level,
                "direction": direction,
                "screenshot_url": screenshot_url,
                "notes": notes
            }
            
            result = self.client.table("structures").insert(structure_data).execute()
            logger.info(f"Successfully inserted {structure_type} structure for {instrument}")
            return result.data[0]
            
        except Exception as e:
            logger.error(f"Error inserting structure: {str(e)}")
            raise

    def upload_screenshot(
        self,
        file: BinaryIO,
        filename: str
    ) -> str:
        """
        Upload a screenshot to the screenshots bucket and return its public URL.
        
        Args:
            file: File object to upload
            filename: Name to give the file in storage
            
        Returns:
            Public URL of the uploaded file
        """
        try:
            # Upload file to Supabase Storage
            result = self.client.storage.from_("screenshots").upload(
                path=filename,
                file=file,
                file_options={"content-type": "image/png"}
            )
            
            # Generate public URL
            public_url = self.client.storage.from_("screenshots").get_public_url(filename)
            
            logger.info(f"Successfully uploaded screenshot: {filename}")
            return public_url
            
        except Exception as e:
            logger.error(f"Error uploading screenshot: {str(e)}")
            raise
