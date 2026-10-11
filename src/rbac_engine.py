"""Role based access checks and least privilege findings."""
from .policies import ROLE_ENTITLEMENTS

def allowed(role, entitlement):
    return entitlement in ROLE_ENTITLEMENTS.get(role, set())

def excessive(role, grants):
    return sorted(set(grants) - ROLE_ENTITLEMENTS.get(role, set()))
