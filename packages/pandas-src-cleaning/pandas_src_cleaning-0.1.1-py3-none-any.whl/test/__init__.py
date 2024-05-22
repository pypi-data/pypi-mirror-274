# tests/__init__.py

import sys
import os
import pandas as pd
import pytest

# Append the src directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.missing_value_handler import MissingValueHandler
from src.outlier_handler import OutlierHandler
from src.scaler import Scaler
from src.text_cleaner import TextCleaner
from src.feature_engineer import FeatureEngineer
from src.data_type_converter import DataTypeConverter
from src.categorical_encoder import CategoricalEncoder
from src.date_time_handler import DateTimeHandler

# Load sample data
@pytest.fixture(scope="session")
def sample_data():
    df = pd.read_csv('synthetic_sample_data.csv')
    return df

# Define fixtures for each handler
@pytest.fixture(scope="session")
def missing_value_handler():
    return MissingValueHandler()

@pytest.fixture(scope="session")
def outlier_handler():
    return OutlierHandler()

@pytest.fixture(scope="session")
def scaler():
    return Scaler()

@pytest.fixture(scope="session")
def text_cleaner():
    return TextCleaner()

@pytest.fixture(scope="session")
def feature_engineer():
    return FeatureEngineer()

@pytest.fixture(scope="session")
def data_type_converter():
    return DataTypeConverter()

@pytest.fixture(scope="session")
def categorical_encoder():
    return CategoricalEncoder()

@pytest.fixture(scope="session")
def date_time_handler():
    return DateTimeHandler()
