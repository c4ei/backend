from core.currency import CoinParams
from cryptocoins.coins.klay.connection import get_w3_cypress_connection
from cryptocoins.coins.klay.consts import KLAY, CODE
from cryptocoins.coins.klay.wallet import klay_wallet_creation_wrapper, is_valid_klay_address
from cryptocoins.utils.register import register_coin

w3 = get_w3_cypress_connection()

KLAY_CURRENCY = register_coin(
    currency_id=KLAY,
    currency_code=CODE,
    address_validation_fn=is_valid_klay_address,
    wallet_creation_fn=klay_wallet_creation_wrapper,
    latest_block_fn=lambda currency: w3.eth.get_block_number(),
    blocks_diff_alert=100,
)
