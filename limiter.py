# limiter.py                                                                                                                                                                                                       
import time
                                                                                                                                                                                                                     
LIMIT = 10      
WINDOW = 60
                                                                                                                                                                                                                     
store = {}  # { ip: {"count": 0, "expiry": 0} }                                                                                                                                                                    
                                                                                                                                                                                                                     
def is_allowed(ip: str) -> bool:                                                                                                                                                                                   
    now = time.time()
    readable_time_string = time.ctime(now)

    if not store or (ip not in store):
        store[ip] = {'count': 1, 'expiry':now+WINDOW}
        return True

    
    #checking for expiry
    expiry_time = store[ip]['expiry']
    if now > expiry_time:
        store[ip]["count"] = 1 #1 because this is indeed a new request right
        store[ip]["expiry"] = now + WINDOW
        
    else:
        curr =  store[ip]["count"]
        if curr >= LIMIT:
            return False
        else:
            store[ip]['count'] = store[ip]['count'] + 1

    return True
        

    



    
    
      


# print(is_allowed("some"))
     

            
                                                                                                                                                                                                                     
      