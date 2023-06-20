from django import template

register = template.Library()

@register.filter
def divmod_minutes_seconds(duration):
    minutes, seconds = divmod(duration.total_seconds(), 60)
    return f"{int(minutes)} minutes and {int(seconds)} seconds"
