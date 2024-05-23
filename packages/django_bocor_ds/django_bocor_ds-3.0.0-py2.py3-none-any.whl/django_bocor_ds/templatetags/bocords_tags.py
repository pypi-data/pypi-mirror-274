from django.template import Library, loader
from ..forms import AppointmentForm
from ..models import Portfolio, Category
from django.contrib.staticfiles import finders
import os
from _data import bocords


import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.ERROR)


register = Library()

# https://localcoder.org/django-inclusion-tag-with-configurable-template


template_name = bocords.context['template_name']


@register.simple_tag(takes_context=True)
def seo(context):
    t = loader.get_template(template_name + "/seo.html")
    context.update({
        'template_name': template_name,
    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def header(context):
    t = loader.get_template(template_name + "/header.html")
    context.update({
        'template_name': template_name,
    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def hero(context):
    t = loader.get_template(template_name + "/_hero.html")
    context.update({
        'template_name': template_name,
    })
    logger.info(context)
    return t.render(context.flatten())



@register.simple_tag(takes_context=True)
def about(context):
    t = loader.get_template(template_name + "/_about.html")
    context.update({
        'template_name': template_name,
    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def why_us(context):
    t = loader.get_template(template_name + "/_why_us.html")
    context.update({
        'template_name': template_name,
    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def counts(context):
    t = loader.get_template(template_name + "/_counts.html")
    context.update({
        'template_name': template_name,
    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def services(context):
    t = loader.get_template(template_name + "/_services.html")
    context.update({
        'template_name': template_name,
    })
    logger.info(context)
    return t.render(context.flatten())


# 인클루전 태그는 동적으로 html파일을 할당할 수 없어서..
# https://localcoder.org/django-inclusion-tag-with-configurable-template

# 일반적인 방식의 심플태그는 csrf_token을 처리할 수 없어서...
# https://stackoverflow.com/questions/43787700/django-1-11-typeerror-context-must-be-a-dict-rather-than-context


@register.simple_tag(takes_context=True)
def appointment(context):
    t = loader.get_template(template_name + "/_appointment.html")
    context.update({
        'template_name': template_name,
        'form': AppointmentForm(),
        'post_message': context.get('post_message', None),
        'naver_link': context.get('naver', None),
    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def features(context):
    t = loader.get_template(template_name + "/_features.html")
    context.update({
        'template_name': template_name,
    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def team(context):
    t = loader.get_template(template_name + "/_team.html")
    context.update({
        'template_name': template_name,
    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def faq(context):
    t = loader.get_template(template_name + "/_faq.html")
    context.update({
        'template_name': template_name,
    })
    logger.info(context)
    return t.render(context.flatten())

@register.simple_tag(takes_context=True)
def pricing(context):
    t = loader.get_template(template_name + "/_pricing.html")
    context.update({
        'template_name': template_name,
    })
    logger.info(context)
    return t.render(context.flatten())

@register.simple_tag(takes_context=True)
def testimonials(context):
    t = loader.get_template(template_name + "/_testimonials.html")
    context.update({
        'template_name': template_name,
    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def gallery(context):
    t = loader.get_template(template_name + "/_gallery.html")

    # static 파일 경로 찾는 방법
    # https://stackoverflow.com/questions/30430131/get-the-file-path-for-a-static-file-in-django-code
    dir = finders.find('herobiz_ds/gallery')
    logger.info(f'gallery path: {dir}')

    files = []

    # static 갤러리 폴더안의 사진 파일의 수를 세어서 파일명을 리스트로 만든다.
    # https://www.delftstack.com/howto/python/count-the-number-of-files-in-a-directory-in-python/
    # https://stackoverflow.com/questions/3964681/find-all-files-in-a-directory-with-extension-txt-in-python
    if dir:
        for file in os.listdir(dir):
            if os.path.isfile(os.path.join(dir, file)) and file.endswith('.jpg'):
                files.append(file)
        logger.info(files)

    context.update({
        'template_name': template_name,
        'gallery_files': files
    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def contact(context):
    t = loader.get_template(template_name + "/_contact.html")
    context.update({
        'template_name': template_name,
    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def cta(context):
    t = loader.get_template(template_name + "/_cta.html")
    context.update({
        'template_name': template_name,
    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def clients(context):
    t = loader.get_template(template_name + "/_clients.html")
    context.update({
        'template_name': template_name,
    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def portfolio(context):
    t = loader.get_template(template_name + "/_portfolio.html")
    context.update({
        'template_name': template_name,
        'categories': Category.objects,
        'items': Portfolio.objects,
    })
    logger.info(context)
    return t.render(context.flatten())


@register.simple_tag(takes_context=True)
def footer(context):
    t = loader.get_template(template_name + "/footer.html")
    context.update({
        'template_name': template_name,
    })
    logger.info(context)
    return t.render(context.flatten())