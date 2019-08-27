from django.db import models
import json
import logging
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter
from django.utils.safestring import mark_safe

logger = logging.getLogger(__name__)

FORM_TYPES = (
    ('initial', 'INITIAL'),
    ('other', 'OTHER'),
)


class Result(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created at',
    )
    submitted_at = models.DateTimeField(
        blank=False, null=False, verbose_name='Submitted at'
    )
    form = models.ForeignKey(
        'TypeForm', models.CASCADE,
        null=True, blank=True,
        verbose_name='Form ID',
        related_name='results',
    )
    name = models.CharField(
        max_length=255, verbose_name='Name',
        blank=True, null=True
    )
    content = models.TextField(
        verbose_name='Content',
        blank=False, null=False,
    )
    hidden_id = models.CharField(
        blank=True, null=True, max_length=100,
        verbose_name='Hidden ID'
    )
    hidden_data = models.CharField(
        blank=True, null=True, max_length=100,
        verbose_name='Hidden fields'
    )
    score = models.IntegerField(
        null=True, blank=True,
        verbose_name='Score'
    )
    answers = models.TextField(
        verbose_name='Answers',
        null=True, blank=True
    )

    def __str__(self):
        return self.name

    def pretty_content(self):
        if not self.answers:
            return ''
        try:
            points = json.dumps(
                json.loads(self.content), sort_keys=True,
                indent=2, ensure_ascii=False
            )
        except Exception as e:
            logger.error('Parsing content error %s' % e)
            return ''
        formatter = HtmlFormatter(style='colorful')
        output = highlight(points, JsonLexer(), formatter)
        style = "<style>" + formatter.get_style_defs() + "</style><br>"
        return mark_safe(style + output)
    pretty_content.allow_tags = True
    pretty_content.short_description = 'Content'

    def pretty_answers(self):
        if not self.answers:
            return ''
        try:
            points = json.dumps(
                json.loads(self.answers), sort_keys=True,
                indent=2, ensure_ascii=False
            )
        except Exception as e:
            logger.error('Parsing content error %s' % e)
            return ''
        formatter = HtmlFormatter(style='colorful')
        output = highlight(points, JsonLexer(), formatter)
        style = "<style>" + formatter.get_style_defs() + "</style><br>"
        return mark_safe(style + output)
    pretty_answers.allow_tags = True
    pretty_answers.short_description = 'Answers'

    class Meta:
        verbose_name = 'TypeForm result'
        verbose_name_plural = 'TypeForm results'


class TypeForm(models.Model):
    form_id = models.CharField(
        max_length=20, verbose_name='Typeform ID'
    )
    name = models.CharField(
        max_length=500, verbose_name='Form name'
    )
    form_type = models.CharField(
        null=True, blank=True,
        choices=FORM_TYPES, max_length=40,
        verbose_name='Form type'
    )

    class Meta:
        verbose_name = "Typeform"
        verbose_name_plural = "Typeforms"

    def __str__(self):
        return self.name


class TypeFormQuestion(models.Model):
    form = models.ForeignKey(
        TypeForm, related_name='questions',
        verbose_name='TypeForm', on_delete=None
    )
    question_id = models.CharField(
        max_length=20, verbose_name='Question ID'
    )
    field_name = models.CharField(
        max_length=500, verbose_name='Field name'
    )

    class Meta:
        verbose_name = "TypeForm question"
        verbose_name_plural = "TypeForm questions"
