from rest_framework import response, status
from django.conf import settings
from rest_framework import permissions
from rest_framework.exceptions import APIException

from omnihr_assignment.utils.processing import _dumps_dict_for_hash_map, _loads_dict_for_hash_map
import redis, base64, json
redisClient = redis.StrictRedis(host=settings.REDIS_HOST,port=6379,db=3)

class RateLimitException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {'error': True, 'message': 'You are reaching rate limit.'}
    default_code = 'rate_limit'


class RateLimitPermission(permissions.BasePermission):

    def has_permission(self, request, view): 
        user = request.user
        path = request.path
        base64_path = base64.b64encode(path.encode("utf-8")).decode("utf-8")
        rate_limit_hash = f"RL_{user}_{base64_path}"
        rate_limit_data = redisClient.hgetall(name=rate_limit_hash)
        if not rate_limit_data:
            rl_config = settings.RATE_LIMIT.split('/')
            thresh = int(rl_config[0])
            formatted_data = _dumps_dict_for_hash_map({"count": 1, "thresh": thresh})
            redisClient.hset(name=rate_limit_hash, mapping=formatted_data)
            
            if rl_config[1] == 'second':
                expiration = 1
            elif rl_config[1] == 'minute':
                expiration = 60
            elif rl_config[1] == 'hours':
                expiration = 60*60
            redisClient.expire(name=rate_limit_hash, time=expiration)
        else:
            rate_limit_data = _loads_dict_for_hash_map(rate_limit_data  )
            if rate_limit_data["count"] + 1 > rate_limit_data["thresh"]:
                raise RateLimitException()

            formatted_data = _dumps_dict_for_hash_map({"count": rate_limit_data["count"] + 1 , "thresh": rate_limit_data["thresh"]})
            redisClient.hset(name=rate_limit_hash, mapping=formatted_data)

        return True
    