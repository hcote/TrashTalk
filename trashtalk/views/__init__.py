"""
APPLICATION ENDPOINTS

View modules are registered programmatically in the `create_app()`
factory, which looks for the `bp` attribute when initializing the app.

All new view modules MUST:
    - Use Blueprints
    - Blueprint var MUST be named `bp`

NOTE: HTML *forms* only allow get and post methods. Views using put or
delete must manually handle those form requests.
"""
