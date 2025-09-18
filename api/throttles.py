from rest_framework.throttling import UserRateThrottle


class BurstRateThrottle(UserRateThrottle):
    scope = "burst"


class DailyRateThrottle(UserRateThrottle):
    scope = "daily"
