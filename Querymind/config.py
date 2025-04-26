#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Configuration Module for Querymind

This module defines configuration settings, model providers, and path management
for the Querymind application.
"""

# Standard library imports
import os
import random
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

# Third-party imports
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class ModelProvider(str, Enum):
    """
    Enum representing supported LLM providers.
    
    Attributes:
        OLLAMA: Local model provider
        GROQ: Cloud-based model provider
    """
    OLLAMA = "ollama"
    GROQ = "groq"


@dataclass
class ModelConfig:
    """
    Configuration settings for language models.
    
    Attributes:
        name (str): Name of the model
        temperature (float): Temperature setting for generation
        provider (ModelProvider): The provider of the model
    """
    name: str
    temperature: float
    provider: ModelProvider


# Model configurations ollama
QWEN_2_5 = ModelConfig("qwen2.5", 0.0, ModelProvider.OLLAMA)
GEMMA_3 = ModelConfig("gemma3-tools:12b", 0.7, ModelProvider.OLLAMA)  # Moderate temperature for more creative responses
DEEPSEEK = ModelConfig("deepseek-r1:7b", 0.7, ModelProvider.OLLAMA)
SQLCODER = ModelConfig("sqlcoder", 0.7, ModelProvider.OLLAMA)



# Model configurations groq

# LLaMA 3.3 70B
LLAMA_3_3 = ModelConfig("llama-3.3-70b-versatile", 0.0, ModelProvider.GROQ)# Zero temperature for deterministic outputs

# LLaMA 4 Maverick 17B-NOTWORKING
LLAMA_4_MAVERICK = ModelConfig("llama-4-maverick-17b-128e-instruct", 0.0, ModelProvider.GROQ)

# LLaMA 4 Scout 17B-NOTWORKING
LLAMA_4_SCOUT = ModelConfig("llama-4-scout-17b-16e-instruct", 0.0, ModelProvider.GROQ)

# Mixtral 8x7B Chat-NOTWORKING
MIXTRAL_8x7B = ModelConfig("mixtral-8x7b-32768", 0.0, ModelProvider.GROQ)

# Gemma 2 9B Instruction
GEMMA2_9B_IT = ModelConfig("gemma2-9b-it", 0.0, ModelProvider.GROQ)

class Config:
    """
    Main configuration class for the application.
    
    Contains settings for models, API keys, and file paths.
    """
    # Application settings
    SEED = 42
    MODEL = LLAMA_3_3
    OLLAMA_CONTEXT_WINDOW = 2048  # increase to allow longer conversations but slower response

    # API keys
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')

    class Path:
        """
        Path management for application directories and files.
        """
        # Directory structure
        APP_HOME = Path(os.getenv("APP_HOME", Path(__file__).parent.parent))
        DATA_DIR = APP_HOME / "data"
        UPLOADED_DB_DIR = DATA_DIR / "uploaded_databases"
        
        # Create uploaded database directory if it doesn't exist
        UPLOADED_DB_DIR.mkdir(parents=True, exist_ok=True)
        
        # This will be dynamically set in the app
        DATABASE_PATH = None


def seed_everything(seed: int = Config.SEED):
    """
    Set random seeds for reproducibility.
    
    Args:
        seed (int): Seed value for random number generators
    """
    random.seed(seed)

# No default database path is set - will be assigned at runtime