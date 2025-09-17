# DEX API Test Suite

## Overview
This project is a comprehensive testing framework for a DEX (Decentralized Exchange) platform called W-DEX. The test suite includes both API tests and UI tests using Selenium WebDriver.

## Project Structure
- **config/**: Configuration files including API endpoints, timeframes, and trading pairs
- **tests/**: Test modules organized by category
  - **basic/**: Basic API availability and data structure tests
  - **consistency/**: Tests for inverse pairs and timeframe consistency  
  - **validation/**: Data validation tests (date, price, volume)
  - **special/**: Edge cases and pair-specific tests
  - **UI/**: Selenium-based user interface tests
  - **pages/**: Page object models for UI tests
- **utils/**: Helper utilities for API calls and data validation
- **allure-results/**: Test reporting results directory

## Current State
- ✅ Python 3.11 environment configured
- ✅ All dependencies installed (pytest, requests, selenium, allure-pytest)
- ✅ Test suite workflow configured and running
- ✅ API tests verified working successfully
- ✅ Import issues in conftest.py resolved

## Architecture
**API Testing**: Tests are parameterized to run across multiple trading pairs and timeframes:
- Trading pairs: POL-USDT, USDT-POL, POL-DAI, DAI-POL, POL-CES, CES-POL, DAI-USDT, USDT-DAI, CES-USDT, USDT-CES, CES-DAI, DAI-CES
- Timeframes: 1d (default), 1w, 4h, 1h, 15m
- Base URL: https://dev-graphback.w-dex.ai

**UI Testing**: Selenium-based tests for the swap interface at https://w-dex.ai
- Note: UI tests are excluded by default in Replit environment due to Chrome WebDriver requirements

## How to Run UI Tests
UI tests are excluded by default but can be run with proper setup:
1. **Requirements**: Chrome browser and ChromeDriver must be installed
2. **Command**: `python -m pytest tests/ -v --tb=short -m ui`
3. **Environment**: Not supported in standard Replit environment
4. **Alternative**: Run API tests only with `python -m pytest tests/ -v --tb=short -m "not ui"` (default)

## Recent Changes (September 17, 2025)
- Set up Python 3.11 environment with required packages
- Fixed import path issues in conftest.py to resolve LSP diagnostics
- Modified WebDriver fixture to only run for UI tests to prevent conflicts with API tests
- Created "Test Suite" workflow to run pytest with verbose output and short traceback
- Verified API tests are running successfully and passing

## User Preferences
- Console-based test execution preferred for this testing project
- Comprehensive test coverage across all trading pairs and timeframes
- Test results displayed with verbose output for debugging