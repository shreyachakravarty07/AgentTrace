"""
Module: agenttrace.logger
Sets up logging for the AgentTrace project.
"""

import logging
from logging import Logger

def setup_logger(name: str, level: int = logging.INFO) -> Logger:
    """
    Configure and return a logger with the specified name and log level.
    
    Args:
        name (str): The name of the logger.
        level (int): Logging level (e.g., logging.INFO). Defaults to INFO.
        
    Returns:
        Logger: The configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    # Prevent duplicate logs if handlers already exist
    if not logger.handlers:
        ch = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger

# Example usage:
if __name__ == "__main__":
    logger = setup_logger("AgentTrace")
    logger.info("Logger setup complete!")
