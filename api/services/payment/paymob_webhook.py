import hashlib
import hmac

import api.core.configurations as config

_fields_in_order = (
    'amount_cents', 'created_at', 'currency', 'error_occured',
    'has_parent_transaction', 'id', 'integration_id', 'is_3d_secure',
    'is_auth', 'is_capture', 'is_refunded', 'is_standalone_payment',
    'is_voided', 'order.id', 'owner', 'pending',
    'source_data.pan', 'source_data.sub_type', 'source_data.type', 'success',
)

class PaymobHmacVerifier:
    def __init__(self,hmac_secret=None):
        self._hmac_secret = hmac_secret or config.PaymentsConfig().paymob_hmac_secret
        
    def _build_hmac(self,obj):
        concatenated_string = ''.join(str(self._get(obj,path)) for path in _fields_in_order)
        return hmac.new(self._hmac_secret.encode(), concatenated_string.encode(), hashlib.sha512).hexdigest()

    def _get(self,obj,path):
            value = obj
            for key in path.split('.'):
                value =  value or ({}.get(key))
            if value is not None:
                return value
            else:
                return ''
    def verify(self,obj,received_hmac):
        builded = self._build_hmac(obj)
        return hmac.compare_digest(builded , received_hmac or '')
    