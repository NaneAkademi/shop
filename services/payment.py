import time
import uuid
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

import config
from db import get_db_session, session_commit
from enums.bot_entity import BotEntity
from enums.cryptocurrency import Cryptocurrency
from enums.payment import PaymentType
from models.nowpayments import NOWPaymentsCreatePaymentRequest
from models.payment import ProcessingPaymentDTO
from repositories.payment import PaymentRepository
from repositories.user import UserRepository
from services.nowpayments import NOWPaymentsService
from utils.localizator import Localizator


class PaymentService:
    @staticmethod
    async def create_nowpayments_order(amount: float, currency: str, user_id: int) -> str:
        """NOWPayments ödeme oluştur"""
        order_id = f"order_{user_id}_{int(time.time())}_{str(uuid.uuid4())[:8]}"

        payment_request = NOWPaymentsCreatePaymentRequest(
            price_amount=amount,
            price_currency=currency,
            order_id=order_id,
            order_description=f"{amount} {currency} bakiye yükleme",
            ipn_callback_url=config.NOWPAYMENTS_WEBHOOK_URL,
            fixed_rate=True,
            is_fee_paid_by_user=True
        )

        try:
            response = await NOWPaymentsService.create_payment(payment_request)
            if response:
                return f"✅ NOWPayments ödeme oluşturuldu:\n\n" \
                       f"💰 Miktar: {response.pay_amount} {response.pay_currency}\n" \
                       f"📍 Adres: `{response.pay_address}`\n" \
                       f"🆔 Ödeme ID: {response.payment_id}\n" \
                       f"⏰ Durum: {response.payment_status}\n\n" \
                       f"Ödemeyi bu adrese yapın ve onay bekleyin."
            else:
                return "❌ NOWPayments ödeme oluşturulurken hata oluştu"
        except Exception as e:
            return f"❌ NOWPayments bağlantı hatası: {str(e)}"

    @staticmethod
    async def create(cryptocurrency: Cryptocurrency, message: Message, session: AsyncSession | Session) -> str:
        user = await UserRepository.get_by_tgid(message.chat.id, session)
        unexpired_payments_count = await PaymentRepository.get_unexpired_unpaid_payments(user.id, session)
        if unexpired_payments_count >= 5:
            return Localizator.get_text(BotEntity.USER, "too_many_payment_request")
        else:
            # NOWPayments ile ödeme oluştur
            currency_map = {
                Cryptocurrency.BTC: "btc",
                Cryptocurrency.ETH: "eth", 
                Cryptocurrency.LTC: "ltc",
                Cryptocurrency.TRX: "trx",
                Cryptocurrency.USDT: "usdttrc20"
            }

            crypto_symbol = currency_map.get(cryptocurrency, "btc")

            # Sabit miktar olarak 25 USD kullan (NOWPayments minimum limiti için)
            amount = 25.0

            print(f"Creating payment with API key: {config.NOWPAYMENTS_API_KEY[:10]}...")
            print(f"Crypto symbol: {crypto_symbol}, Amount: {amount}")

            payment_request = NOWPaymentsCreatePaymentRequest(
                price_amount=amount,
                price_currency="USD",
                pay_currency=crypto_symbol,
                order_id=f"order_{user.id}_{int(time.time())}_{str(uuid.uuid4())[:8]}",
                order_description=f"{amount} USD bakiye yükleme",
                ipn_callback_url=config.NOWPAYMENTS_WEBHOOK_URL,
                fixed_rate=True,
                is_fee_paid_by_user=True
            )

            try:
                print(f"\n=== Creating NOWPayments Payment ===")
                print(f"Request Data: {payment_request.model_dump(exclude_none=True)}")
                print(f"=====================================\n")
                
                response = await NOWPaymentsService.create_payment(payment_request)
                
                if response:
                    print(f"✅ Payment successfully created with ID: {response.payment_id}")
                    
                    # Veritabanına kaydet
                    await PaymentRepository.create(int(response.payment_id), user.id, message.message_id, session)
                    await session_commit(session)

                    return Localizator.get_text(BotEntity.USER, "top_up_balance_msg").format(
                        crypto_name=cryptocurrency.name,
                        addr=response.pay_address,
                        crypto_amount=response.pay_amount,
                        fiat_amount=response.price_amount,
                        currency_text=Localizator.get_currency_text(),
                        status=Localizator.get_text(BotEntity.USER, "status_pending")
                    )
                else:
                    print(f"❌ NOWPayments API yanıt vermedi veya hata döndü")
                    return f"❌ NOWPayments API Hatası:\n" \
                           f"API'den gelen yanıt: 'amountTo is too small' (Miktar çok küçük)\n" \
                           f"Minimum ödeme miktarı daha yüksek olmalı.\n" \
                           f"Lütfen daha yüksek bir miktar deneyin."
            except Exception as e:
                print(f"❌ Payment creation exception: {str(e)}")
                print(f"Exception type: {type(e)}")
                import traceback
                print(f"Traceback: {traceback.format_exc()}")
                
                # Eğer API yanıt hatası varsa göster
                error_msg = str(e)
                if "amountTo is too small" in error_msg:
                    return "❌ Ödeme miktarı çok küçük. NOWPayments minimum ödeme limitini karşılamıyor. Lütfen daha yüksek miktar deneyin."
                elif "BAD_REQUEST" in error_msg:
                    return f"❌ API İsteği Hatası: {error_msg}"
                else:
                    return f"❌ Ödeme oluşturma hatası: {error_msg}"