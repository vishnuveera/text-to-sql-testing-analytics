import os  
import sys  
import logging  
import configparser  
from datetime import datetime  

fallback_logger = logging.getLogger(__name__)

def setup_logger(logger_name: str, log_file: str) -> logging.Logger:
    """
    Creates an isolated logger that saves to its own file and prevents duplicate logs.
    """
    logger = logging.getLogger(logger_name)
    
    logger.propagate = False
    
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')
        
        # 1. Terminal Output
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # 2. File Output
        if log_file:
            log_dir = "Run"
            os.makedirs(log_dir, exist_ok=True)
            
            # Combine the folder path with your file name (e.g., "Run/intent.logs")
            full_log_path = os.path.join(log_dir, log_file)
            
            # Pass the full path to the FileHandler
            file_handler = logging.FileHandler(full_log_path, mode='a', encoding='utf-8')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            
    return logger 
  
def load_configurations(tool_config_path: str, keys_config_path: str, custom_logger=None) -> None:  
    """  
    Load configurations from the provided .cfg files and set them in environment variables.  
    Args:  
        tool_config_path (str): Path to the tool configuration file.  
        keys_config_path (str): Path to the keys configuration file.  
    Raises:  
        SystemExit: If the configuration files cannot be read.  
    """  
    logger = custom_logger or fallback_logger
    logger.info(f"Loading configurations from {tool_config_path}...")
    # Read the .cfg files
    config = configparser.ConfigParser()

    if not config.read([tool_config_path, keys_config_path]):
        raise FileNotFoundError(f"ERROR: Could not read configuration files at {tool_config_path} or {keys_config_path}")
        sys.exit(1)

    # Push the keys into the OS memory
    for section in config.sections():
        for key, value in config.items(section):
            os.environ[key.upper()] = value