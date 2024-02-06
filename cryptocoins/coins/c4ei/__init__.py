from core.currency import CoinParams
from cryptocoins.coins.c4ei.connection import get_w3_cfei_connection
from cryptocoins.coins.c4ei.consts import C4EI, CODE
from cryptocoins.coins.c4ei.wallet import c4ei_wallet_creation_wrapper, is_valid_c4ei_address
from cryptocoins.utils.register import register_coin

w3 = get_w3_cfei_connection()

C4EI_CURRENCY = register_coin(
    currency_id=C4EI,
    currency_code=CODE,
    address_validation_fn=is_valid_c4ei_address,
    wallet_creation_fn=c4ei_wallet_creation_wrapper,
    latest_block_fn=lambda currency: w3.eth.get_block_number(),
    blocks_diff_alert=100,
)
