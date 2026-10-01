from api.models import db, IdempotencyKeys

class IdempotencyService:
    @staticmethod
    def get(key):
        return IdempotencyKeys.query.get(key)

    @staticmethod
    def start(key,request_hash):
        record = IdempotencyKeys(idempotencyKey=key,status='PENDING',request_hash=request_hash)
        db.session.add(record)
        db.session.commit()
        return record

    @staticmethod
    def complete(key,response_code,response_body):
        record = IdempotencyKeys.query.get(key)
        if record:
            record.status = 'COMPLETED'
            record.response_code = response_code
            record.response_body = response_body
            db.session.commit()
        return record