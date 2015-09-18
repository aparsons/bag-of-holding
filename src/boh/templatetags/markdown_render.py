import markdown

from markdown.extensions import Extension

from django import template
from django.utils.safestring import mark_safe


register = template.Library()


# http://pythonhosted.org//Markdown/release-2.6.html#safe_mode-deprecated
class EscapeHtml(Extension):
    def extendMarkdown(self, md, md_globals):
        del md.preprocessors['html_block']
        del md.inlinePatterns['html']


@register.filter
def markdown_render(value):
    return mark_safe(markdown.markdown(value, extensions=[EscapeHtml(), 'markdown.extensions.codehilite', 'markdown.extensions.toc']))
