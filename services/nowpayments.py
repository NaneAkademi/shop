
import aiohttp
import config
from models.nowpayments import (
    NOWPaymentsCreatePaymentRequest, 
    NOWPaymentsCreatePaymentResponse,
    NOWPaymentsStatusResponse
)
from typing import Optional


class NOWPaymentsService:
    BASE_URL = "https://api.nowpayments.io/v1"
    SANDBOX_URL = "https://api.sandbox.nowpayments.io/v1"
    
    @staticmethod
    def _get_headers() -> dict:
        """API başlıklarını oluştur"""
        return {
            "x-api-key": config.NOWPAYMENTS_API_KEY,
            "Content-Type": "application/json"
        }
    
    @staticmethod
    async def get_available_currencies() -> list:
        """Mevcut para birimlerini al"""
        url = f"{NOWPaymentsService.BASE_URL}/currencies"
        headers = NOWPaymentsService._get_headers()
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('currencies', [])
                return []
    
    @staticmethod
    async def get_estimate(amount: float, currency_from: str, currency_to: str) -> dict:
        """Ödeme tahmini al"""
        url = f"{NOWPaymentsService.BASE_URL}/estimate"
        headers = NOWPaymentsService._get_headers()
        params = {
            "amount": amount,
            "currency_from": currency_from,
            "currency_to": currency_to
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    return await response.json()
                return {}
    
    @staticmethod
    async def create_payment(payment_request: NOWPaymentsCreatePaymentRequest) -> Optional[NOWPaymentsCreatePaymentResponse]:
        """Ödeme oluştur"""
        url = f"{NOWPaymentsService.BASE_URL}/payment"
        headers = NOWPaymentsService._get_headers()
        
        print(f"NOWPayments URL: {url}")
        print(f"NOWPayments Headers: {headers}")
        print(f"NOWPayments Request: {payment_request.model_dump(exclude_none=True)}")
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payment_request.model_dump(exclude_none=True), headers=headers) as response:
                response_text = await response.text()
                print(f"\n=== NOWPayments API Response ===")
                print(f"Status Code: {response.status}")
                print(f"Response Headers: {dict(response.headers)}")
                print(f"Response Body: {response_text}")
                print(f"================================\n")
                
                if response.status == 201:
                    try:
                        data = await response.json()
                        print(f"✅ Payment created successfully: {data}")
                        return NOWPaymentsCreatePaymentResponse.model_validate(data)
                    except Exception as e:
                        print(f"❌ JSON parse error: {e}")
                        print(f"Raw response: {response_text}")
                        return None
                else:
                    print(f"❌ NOWPayments API Error - Status: {response.status}")
                    try:
                        error_data = await response.json()
                        print(f"Error Details: {error_data}")
                        
                        # Hata mesajını kullanıcı dostu hale getir
                        if 'message' in error_data:
                            print(f"Error Message: {error_data['message']}")
                        if 'errors' in error_data:
                            print(f"Validation Errors: {error_data['errors']}")
                            
                    except Exception as json_error:
                        print(f"Could not parse error JSON: {json_error}")
                        print(f"Raw error response: {response_text}")
                    return None
    
    @staticmethod
    async def get_payment_status(payment_id: str) -> Optional[NOWPaymentsStatusResponse]:
        """Ödeme durumunu kontrol et"""
        url = f"{NOWPaymentsService.BASE_URL}/payment/{payment_id}"
        headers = NOWPaymentsService._get_headers()
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return NOWPaymentsStatusResponse.model_validate(data)
                return None
