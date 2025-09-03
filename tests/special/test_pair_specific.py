"""Тесты специфичные для конкретных пар"""

import pytest
from utils.api_helpers import fetch_data
from config.settings import BASE_URL

def test_pol_usdt_price_range():
    """Проверяет, что цена POL в USDT находится в разумном диапазоне"""
    response = fetch_data("POL-USDT", "")
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            latest_price = float(data[0]["priceUSD"])
            # Цена POL в USDT должна быть в разумном диапазоне
            assert 0.01 <= latest_price <= 100, (
                f"Неожиданная цена для POL-USDT: {latest_price}. "
                "Ожидалось в диапазоне 0.01-100"
            )

def test_usdt_pol_price_range():
    """Проверяет, что цена USDT в POL находится в разумном диапазоне"""
    response = fetch_data("USDT-POL", "")
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            latest_price = float(data[0]["priceUSD"])
            # Цена USDT в POL должна быть в разумном диапазоне
            assert 0.01 <= latest_price <= 100, (
                f"Неожиданная цена для USDT-POL: {latest_price}. "
                "Ожидалось в диапазоне 0.01-100"
            )

def test_dai_usdt_price_range():
    """Проверяет, что цена DAI в USDT близка к 1 (стейблкоины)"""
    response = fetch_data("DAI-USDT", "")
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            latest_price = float(data[0]["priceUSD"])
            # DAI и USDT - стейблкоины, их цена должна быть близка к 1
            assert 0.9 <= latest_price <= 1.1, (
                f"Неожиданная цена для DAI-USDT: {latest_price}. "
                "Ожидалось около 1 (в диапазоне 0.9-1.1)"
            )

def test_ces_usdt_price_range():
    """Проверяет, что цена CES в USDT находится в разумном диапазоне"""
    response = fetch_data("CES-USDT", "")
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            latest_price = float(data[0]["priceUSD"])
            # Цена CES в USDT должна быть в разумном диапазоне
            assert 0.0001 <= latest_price <= 1, (
                f"Неожиданная цена для CES-USDT: {latest_price}. "
                "Ожидалось в диапазоне 0.0001-1"
            )