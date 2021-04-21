from rest_framework.throttling import UserRateThrottle

class UserMinThrottle(UserRateThrottle):
             scope = 'user_min'

class UserDayThrottle(UserRateThrottle):
             scope = 'user_day'