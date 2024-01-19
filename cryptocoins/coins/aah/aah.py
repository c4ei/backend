import json
import logging
from decimal import Decimal
from typing import Dict, Type

import cachetools.func
from django.conf import settings

from core.consts.currencies import ERC20_CURRENCIES
from core.currency import Currency, TokenParams
from cryptocoins.coins.eth import AAH_CURRENCY
from cryptocoins.evm.manager import register_evm_handler
from cryptocoins.interfaces.common import GasPriceCache
from cryptocoins.interfaces.common import Token
from cryptocoins.interfaces.web3_commons import Web3Manager, Web3Token, Web3Transaction, Web3CommonHandler
from cryptocoins.utils.infura import w3
from exchange.settings import env

log = logging.getLogger(__name__)

ERC20_ABI = json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_from","type":"address"},{"indexed":true,"name":"_to","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_owner","type":"address"},{"indexed":true,"name":"_spender","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Approval","type":"event"}]')  # noqa: 501
DEFAULT_TRANSFER_GAS_LIMIT = 100_000
DEFAULT_TRANSFER_GAS_MULTIPLIER = 2


class EthTransaction(Web3Transaction):
    """Eth tx parser"""


class EthGasPriceCache(GasPriceCache):
    GAS_PRICE_UPDATE_PERIOD = settings.AAH_GAS_PRICE_UPDATE_PERIOD
    GAS_PRICE_COEFFICIENT = settings.AAH_GAS_PRICE_COEFFICIENT
    MIN_GAS_PRICE = settings.AAH_MIN_GAS_PRICE
    MAX_GAS_PRICE = settings.AAH_MAX_GAS_PRICE

    @cachetools.func.ttl_cache(ttl=GAS_PRICE_UPDATE_PERIOD)
    def get_price(self):
        return self.web3.eth.gas_price


class ERC20Token(Web3Token):
    ABI = ERC20_ABI
    BLOCKCHAIN_CURRENCY: Currency = AAH_CURRENCY
    CHAIN_ID = settings.AAH_CHAIN_ID


class AahManager(Web3Manager):
    CURRENCY: Currency = AAH_CURRENCY
    GAS_CURRENCY = settings.AAH_TX_GAS
    TOKEN_CURRENCIES: Dict[Currency, TokenParams] = ERC20_CURRENCIES
    TOKEN_CLASS: Type[Token] = ERC20Token
    GAS_PRICE_CACHE_CLASS: Type[GasPriceCache] = EthGasPriceCache
    CHAIN_ID = settings.AAH_CHAIN_ID
    MIN_BALANCE_TO_ACCUMULATE_DUST = Decimal('0.001')
    COLD_WALLET_ADDRESS = settings.AAH_SAFE_ADDR


aah_manager = AahManager(client=w3)


@register_evm_handler
class AahHandler(Web3CommonHandler):
    CURRENCY = AAH_CURRENCY
    COIN_MANAGER = aah_manager
    TOKEN_CURRENCIES = aah_manager.registered_token_currencies
    TOKEN_CONTRACT_ADDRESSES = aah_manager.registered_token_addresses
    TRANSACTION_CLASS = EthTransaction
    DEFAULT_BLOCK_ID_DELTA = 1000
    SAFE_ADDR = w3.to_checksum_address(settings.AAH_SAFE_ADDR)
    CHAIN_ID = settings.AAH_CHAIN_ID
    BLOCK_GENERATION_TIME = settings.AAH_BLOCK_GENERATION_TIME
    ACCUMULATION_PERIOD = settings.AAH_ERC20_ACCUMULATION_PERIOD
    IS_ENABLED = env('COMMON_TASKS_AAH', default=True)
    W3_CLIENT = w3
