from django.conf import settings

# TODO: I'm pretty sure settings is already available from the default
# context processors. Get rid of this if so.
def site_prefs(request):
    """Makes settings available as site_prefs."""
    return {"site_prefs": settings}
