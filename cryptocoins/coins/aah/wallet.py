import logging
import secrets

from django.conf import settings
from django.db import transaction
from web3 import Web3

from core.consts.currencies import BlockchainAccount
from eth_account.account import Account
from lib.cipher import AESCoderDecoder

log = logging.getLogger(__name__)

def create_aah_address():
    while 1:
        private_key = "0x" + secrets.token_hex(32)
        account = Account.from_key(private_key)

        encrypted_key = AESCoderDecoder(settings.CRYPTO_KEY).encrypt(private_key)
        decrypted_key = AESCoderDecoder(settings.CRYPTO_KEY).decrypt(encrypted_key)

        if decrypted_key.startswith('0x') and len(decrypted_key) == 66:
            break
    return account.address, encrypted_key


def create_new_blockchain_account() -> BlockchainAccount:
    address, encrypted_pk = create_aah_address()
    return BlockchainAccount(
        address=address,
        private_key=AESCoderDecoder(settings.CRYPTO_KEY).decrypt(encrypted_pk),
    )

@transaction.atomic
def get_or_create_aah_wallet(user_id, is_new=False):
    """
    Make new user wallet and related objects if not exists
    """
    # implicit logic instead of get_or_create
    from core.models.cryptocoins import UserWallet
    from cryptocoins.coins.aah import AAH_CURRENCY

    user_wallet = UserWallet.objects.filter(
        user_id=user_id,
        currency=AAH_CURRENCY,
        blockchain_currency=AAH_CURRENCY,
    ).order_by('-id').first()

    if not is_new and user_wallet is not None:
        return user_wallet

    address, encrypted_key = create_aah_address()

    user_wallet = UserWallet.objects.create(
        user_id=user_id,
        address=address,
        private_key=encrypted_key,
        currency=AAH_CURRENCY,
        blockchain_currency=AAH_CURRENCY
    )

    return user_wallet


@transaction.atomic
def get_or_create_bep20_wallet(user_id, currency, is_new=False):
    from core.models.cryptocoins import UserWallet
    from cryptocoins.coins.aah import AAH_CURRENCY

    aah_wallet = get_or_create_aah_wallet(user_id, is_new=is_new)

    bep20_wallet = UserWallet.objects.filter(
        user_id=user_id,
        currency=currency,
        blockchain_currency=AAH_CURRENCY
    ).first()

    if not is_new and bep20_wallet is not None:
        return bep20_wallet

    address, encrypted_key = create_aah_address()

    bep20_wallet = UserWallet.objects.create(
        user_id=user_id,
        address=address,
        private_key=encrypted_key,
        currency=currency,
        blockchain_currency=AAH_CURRENCY
    )

    return bep20_wallet


def aah_wallet_creation_wrapper(user_id, is_new=False, **kwargs):
    from core.models.cryptocoins import UserWallet

    wallet = get_or_create_aah_wallet(user_id, is_new=is_new)
    return UserWallet.objects.filter(id=wallet.id)


def bep20_wallet_creation_wrapper(user_id, currency, is_new=False, **kwargs):
    from core.models.cryptocoins import UserWallet

    wallet = get_or_create_bep20_wallet(user_id, currency=currency, is_new=is_new)
    return UserWallet.objects.filter(id=wallet.id)


def is_valid_aah_address(address):
    return Web3.is_address(address)
