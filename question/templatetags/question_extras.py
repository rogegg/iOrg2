
from datareader.models import Question

from django import template
register = template.Library()



### FILTER FOR TEMPLATE
@register.filter
def template_option_list(q):
    print(q.get_option_list())
    return q.get_option_list()
