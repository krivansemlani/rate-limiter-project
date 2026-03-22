import time
import redis


r = redis.Redis(host='redis', port=6379)
refill_rate = 10/60
capacity = 10
failure_count = 0
last_failure_time = 0


lua_script = """
local tokens = tonumber(redis.call('HGET', KEYS[1], 'tokens'))
local last_refill = tonumber(redis.call('HGET', KEYS[1], 'last_refill'))
local now = tonumber(ARGV[1])
local refill_rate = tonumber(ARGV[2])
local capacity = tonumber(ARGV[3])

if tokens == nil then
    tokens = capacity
    last_refill = now
    redis.call('HSET', KEYS[1], 'tokens', tokens - 1, 'last_refill', now)
    redis.call('EXPIRE', KEYS[1], 60)
    return 1
end

local tokens_lazy = (now - last_refill) * refill_rate
if tokens + tokens_lazy > capacity then
    tokens = capacity
else
    tokens = tokens + tokens_lazy
end


if tokens >= 1 then
    redis.call('HSET', KEYS[1], 'tokens', tokens - 1, 'last_refill', now)
    redis.call('EXPIRE', KEYS[1], 60)
    return 1
end

return 0
"""

def is_allowed(ip: str) -> bool:
    global failure_count, last_failure_time 
    now = time.time()
    if failure_count >= 5 and now - last_failure_time < 30:
        return True
    else:
        try:
            result = r.eval(lua_script, 1, ip, now, refill_rate, capacity)
            failure_count = 0
            return result == 1
        except:
            failure_count +=1
            last_failure_time = now
            return True


    