from cryptocoins.coins.aah.connection import get_w3_connection
from cryptocoins.coins.aah.wallet import aah_wallet_creation_wrapper
from cryptocoins.coins.aah.wallet import is_valid_aah_address
from cryptocoins.utils.register import register_coin


AAH = 99
CODE = 'AAH'
DECIMALS = 8

AAH_CURRENCY = register_coin(
    currency_id=AAH,
    currency_code=CODE,
    address_validation_fn=is_valid_aah_address,
    wallet_creation_fn=aah_wallet_creation_wrapper,
    latest_block_fn=lambda currency: get_w3_connection().eth.get_block_number(),
    blocks_diff_alert=100,
)
