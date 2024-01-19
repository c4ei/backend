from core.currency import CoinParams
from cryptocoins.coins.aah.connection import get_w3_c4ex_connection
from cryptocoins.coins.aah.consts import AAH, CODE
from cryptocoins.coins.aah.wallet import aah_wallet_creation_wrapper, is_valid_aah_address
from cryptocoins.utils.register import register_coin

w3 = get_w3_c4ex_connection()

AAH_CURRENCY = register_coin(
    currency_id=AAH,
    currency_code=CODE,
    address_validation_fn=is_valid_aah_address,
    wallet_creation_fn=aah_wallet_creation_wrapper,
    latest_block_fn=lambda currency: w3.eth.get_block_number(),
    blocks_diff_alert=100,
)
