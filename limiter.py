# limiter.py                                                                                                                                                                                                       
import time
import redis
r = redis.Redis(host='localhost', port=6379)
                                                                                                                                                                                                                     
LIMIT = 10      
WINDOW = 60
                                                                                                                                                                                                                     
# store = {}  # { ip: {"count": 0, "expiry": 0} } - this is being replaced by redis                                                                                                                                                               
                                                                                                                                                                                                                     
def is_allowed(ip: str) -> bool:                                                                                                                                                                                   
    curr_count = r.incr(ip)
    if curr_count >= LIMIT:
        return False
    
    if curr_count == 1:
        r.expire(ip, WINDOW)

    return True
                                                                                                                                                                                                    
      