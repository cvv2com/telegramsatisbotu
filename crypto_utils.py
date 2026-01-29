#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crypto Currency Utilities
Kripto para yardımcı fonksiyonları
"""

import re
from typing import Optional, Tuple


def validate_btc_address(address: str) -> bool:
    """Validate Bitcoin address
    
    Args:
        address: Bitcoin address
        
    Returns:
        True if valid, False otherwise
    """
    if not address:
        return False
    
    # Bitcoin addresses can be:
    # - Legacy (P2PKH): Starts with 1, length 26-35
    # - Script (P2SH): Starts with 3, length 26-35
    # - Bech32 (SegWit): Starts with bc1, length 42-62
    
    # Legacy address pattern
    if re.match(r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$', address):
        return True
    
    # Bech32 address pattern
    if re.match(r'^bc1[a-z0-9]{39,59}$', address.lower()):
        return True
    
    return False


def validate_eth_address(address: str) -> bool:
    """Validate Ethereum address
    
    Args:
        address: Ethereum address
        
    Returns:
        True if valid, False otherwise
    """
    if not address:
        return False
    
    # Ethereum addresses start with 0x followed by 40 hex characters
    return bool(re.match(r'^0x[a-fA-F0-9]{40}$', address))


def validate_usdt_address(address: str, network: str = 'TRC20') -> bool:
    """Validate USDT address
    
    Args:
        address: USDT address
        network: Network type (TRC20, ERC20, OMNI)
        
    Returns:
        True if valid, False otherwise
    """
    if not address:
        return False
    
    network = network.upper()
    
    if network == 'TRC20':
        # TRON addresses start with T
        return bool(re.match(r'^T[a-zA-Z0-9]{33}$', address))
    elif network == 'ERC20':
        # ERC20 uses Ethereum addresses
        return validate_eth_address(address)
    elif network == 'OMNI':
        # OMNI uses Bitcoin addresses
        return validate_btc_address(address)
    
    return False


def validate_ltc_address(address: str) -> bool:
    """Validate Litecoin address
    
    Args:
        address: Litecoin address
        
    Returns:
        True if valid, False otherwise
    """
    if not address:
        return False
    
    # Litecoin addresses can be:
    # - Legacy: Starts with L, length 26-35
    # - Script: Starts with M, length 26-35
    # - Bech32: Starts with ltc1, length 43-62
    
    # Legacy address pattern
    if re.match(r'^[LM][a-km-zA-HJ-NP-Z1-9]{25,34}$', address):
        return True
    
    # Bech32 address pattern
    if re.match(r'^ltc1[a-z0-9]{39,59}$', address.lower()):
        return True
    
    return False


def validate_wallet_address(address: str, currency: str) -> bool:
    """Validate wallet address based on currency
    
    Args:
        address: Wallet address
        currency: Currency type (BTC, ETH, USDT, LTC)
        
    Returns:
        True if valid, False otherwise
    """
    currency = currency.upper()
    
    if currency == 'BTC':
        return validate_btc_address(address)
    elif currency == 'ETH':
        return validate_eth_address(address)
    elif currency == 'USDT':
        # Default to TRC20 for USDT
        return validate_usdt_address(address, 'TRC20')
    elif currency == 'LTC':
        return validate_ltc_address(address)
    
    return False


def validate_tx_hash(tx_hash: str, currency: str) -> bool:
    """Validate transaction hash
    
    Args:
        tx_hash: Transaction hash
        currency: Currency type (BTC, ETH, USDT, LTC)
        
    Returns:
        True if valid, False otherwise
    """
    if not tx_hash:
        return False
    
    currency = currency.upper()
    
    # Bitcoin and Litecoin: 64 hex characters
    if currency in ['BTC', 'LTC']:
        return bool(re.match(r'^[a-fA-F0-9]{64}$', tx_hash))
    
    # Ethereum and ERC20 tokens: 0x + 64 hex characters
    if currency in ['ETH']:
        return bool(re.match(r'^0x[a-fA-F0-9]{64}$', tx_hash))
    
    # USDT TRC20 (TRON): 64 hex characters
    if currency == 'USDT':
        return bool(re.match(r'^[a-fA-F0-9]{64}$', tx_hash))
    
    return False


def format_crypto_amount(amount: float, currency: str, decimals: Optional[int] = None) -> str:
    """Format cryptocurrency amount
    
    Args:
        amount: Amount in cryptocurrency
        currency: Currency type
        decimals: Number of decimal places (auto-detect if None)
        
    Returns:
        Formatted amount string
    """
    currency = currency.upper()
    
    # Auto-detect decimal places if not specified
    if decimals is None:
        if currency in ['BTC', 'LTC']:
            decimals = 8
        elif currency in ['ETH']:
            decimals = 6
        elif currency in ['USDT']:
            decimals = 2
        else:
            decimals = 4
    
    return f"{amount:.{decimals}f}"


def parse_crypto_amount(amount_str: str) -> Optional[float]:
    """Parse cryptocurrency amount from string
    
    Args:
        amount_str: Amount string
        
    Returns:
        Float amount or None if invalid
    """
    try:
        # Remove whitespace and common separators
        amount_str = amount_str.strip().replace(',', '.')
        return float(amount_str)
    except (ValueError, AttributeError):
        return None


def get_currency_symbol(currency: str) -> str:
    """Get currency symbol
    
    Args:
        currency: Currency type
        
    Returns:
        Currency symbol
    """
    symbols = {
        'BTC': '₿',
        'ETH': 'Ξ',
        'USDT': '₮',
        'LTC': 'Ł',
        'USD': '$'
    }
    
    return symbols.get(currency.upper(), currency.upper())


def calculate_crypto_amount(usd_amount: float, exchange_rate: float) -> float:
    """Calculate cryptocurrency amount from USD
    
    Args:
        usd_amount: Amount in USD
        exchange_rate: Exchange rate (1 crypto = X USD)
        
    Returns:
        Amount in cryptocurrency
    """
    if exchange_rate <= 0:
        raise ValueError("Exchange rate must be positive")
    
    return usd_amount / exchange_rate


def calculate_usd_amount(crypto_amount: float, exchange_rate: float) -> float:
    """Calculate USD amount from cryptocurrency
    
    Args:
        crypto_amount: Amount in cryptocurrency
        exchange_rate: Exchange rate (1 crypto = X USD)
        
    Returns:
        Amount in USD
    """
    return crypto_amount * exchange_rate


def get_network_info(currency: str) -> dict:
    """Get network information for a currency
    
    Args:
        currency: Currency type
        
    Returns:
        Dictionary with network information
    """
    networks = {
        'BTC': {
            'name': 'Bitcoin',
            'confirmations_required': 3,
            'avg_confirmation_time_minutes': 10,
            'explorer_url': 'https://blockchain.info/tx/'
        },
        'ETH': {
            'name': 'Ethereum',
            'confirmations_required': 12,
            'avg_confirmation_time_minutes': 2,
            'explorer_url': 'https://etherscan.io/tx/'
        },
        'USDT': {
            'name': 'USDT (TRC20)',
            'confirmations_required': 19,
            'avg_confirmation_time_minutes': 3,
            'explorer_url': 'https://tronscan.org/#/transaction/'
        },
        'LTC': {
            'name': 'Litecoin',
            'confirmations_required': 6,
            'avg_confirmation_time_minutes': 2.5,
            'explorer_url': 'https://live.blockcypher.com/ltc/tx/'
        }
    }
    
    return networks.get(currency.upper(), {
        'name': currency.upper(),
        'confirmations_required': 6,
        'avg_confirmation_time_minutes': 10,
        'explorer_url': ''
    })


def get_explorer_url(tx_hash: str, currency: str) -> str:
    """Get blockchain explorer URL for a transaction
    
    Args:
        tx_hash: Transaction hash
        currency: Currency type
        
    Returns:
        Explorer URL
    """
    network_info = get_network_info(currency)
    base_url = network_info.get('explorer_url', '')
    
    if base_url:
        return f"{base_url}{tx_hash}"
    
    return ""
