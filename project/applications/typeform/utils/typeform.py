import json
import logging
import random

from django.contrib.auth.models import User, Group
from django.utils import timezone

from hpcconfig.models import ConfigRequest
from typeform.models import TypeForm
from django.conf import settings

from core.utils.send_credentials import send_credentials_mail

logger = logging.getLogger(__name__)


def parse_typeform_answers(instance):
    def get_answer_name(form, answer_id):
        if not form:
            return answer_id
        if not form.questions.count():
            return answer_id
        question = form.questions.filter(question_id=answer_id).last()
        if not question:
            return answer_id
        return question.field_name

    content = json.loads(instance.content)
    form_id = content.get('form_id')
    form = None

    if TypeForm.objects.count():
        form = TypeForm.objects.filter(form_id=form_id).last()

    answers = {}
    for answer in content.get('answers'):
        answer_type = answer.get('type')
        if answer_type:
            answer_id = answer.get('field').get('id')
            answer_name = get_answer_name(form, answer_id)
            if answer_type == 'choice':
                answers[answer_name] = answer.get('choice').get('label')
            else:
                answers[answer_name] = answer.get(answer_type)

    instance.answers = json.dumps(answers, ensure_ascii=False, sort_keys=True)
    instance.form = form
    instance.save(update_fields=['answers', 'form'])
    logger.info('Typeform answers parsed')
    return form


def process_form(instance):
    content = json.loads(instance.content)
    form_id = content.get('form_id')
    form = None

    if TypeForm.objects.count():
        form = TypeForm.objects.filter(form_id=form_id).last()

    if form.form_type == 'initial':
        if instance.hidden_id:
            user = User.objects.get(pk=instance.hidden_id)
        else:
            email = json.loads(instance.answers).get('email')
            user = User.objects.filter(email__icontains=email).last()
            if not user:
                symbols = 'ab1cd2ef3gh4ij5kl6mn7op8qr9stuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
                pwd = ''.join([random.choice(symbols) for i in range(8)])
                user = User.objects.create(
                    is_staff=True,
                    email=email,
                    username=email
                )
                group = Group.objects.get(name='clients')
                user.groups.add(group)
                user.set_password(pwd)
                user.save()
                if settings.SEND_CREDENTIALS_TF:
                    send_credentials_mail(pwd, email)

        conf_req = ConfigRequest.objects.create(
            user=user,
            data=instance.answers,
            created_at=timezone.now()
        )
        conf_req.save()