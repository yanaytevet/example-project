import logging
import secrets
from urllib.parse import parse_qs, unquote
import requests
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.views import View
from rest_framework import status
from rest_framework.exceptions import APIException

from configurations import gui_urls_creator
from experts.apis_checkers.experts_api_checkers import ExpertSecretIdAPIChecker
from experts.consts.experts_hidden_reasons import ExpertsHiddenReasons
from experts.consts.workflow_enum import ExpertWorkflowEventTrigger
from experts.managers.expert_workflow_event_manager.expert_workflow_event_manager import ExpertWorkflowEventManager
from experts.managers.experts_managers.experts_onboarding_manager import ExpertsOnBoardingManager
from experts.models import Expert
from users.consts.email_source import EmailSource
from users.models import User, PersonInfo, EmailAddress
from configurations.models import ExpertsConfigurations, GUIConfigurations
from configurations.gui_urls_creator import GuiUrlsCreator

# Initialize logger
logger = logging.getLogger(__name__)


class LinkedInAuthUtil:
    def get_access_token(self, code: str, linkedin_redirect_uri: str) -> str:
        expert_conf = ExpertsConfigurations.get()
        gui_conf = GUIConfigurations.get()
        access_token_data = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': gui_conf.linkedin_client_id,
            'client_secret': expert_conf.linkedin_client_secret,
            'redirect_uri': linkedin_redirect_uri
        }
        response = requests.post('https://www.linkedin.com/oauth/v2/accessToken', data=access_token_data)
        response.raise_for_status()
        return response.json().get('access_token')

    def get_user_data(self, access_token):
        headers = {'Authorization': f"Bearer {access_token}"}
        response = requests.get(
            'https://api.linkedin.com/v2/me?projection=(id,localizedFirstName,localizedLastName,profilePicture(displayImage~:playableStreams))',
            headers=headers)
        response.raise_for_status()
        return response.json()

    def get_user_email(self, access_token):
        headers = {'Authorization': f"Bearer {access_token}"}
        response = requests.get('https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))',
                                headers=headers)
        response.raise_for_status()
        return response.json().get('elements')[0].get('handle~').get('emailAddress')


class LinkedInAuthRegisterView(View):
    def get(self, request):
        util = LinkedInAuthUtil()
        gui_urls_creator = GuiUrlsCreator()  # Initialize gui_urls_creator here

        error = request.GET.get('error')

        if error:
            return redirect(gui_urls_creator.get_main_page())

        code = request.GET.get('code')
        state = unquote(request.GET.get('state')).replace("|", "&")

        parsed_state = parse_qs(state)
        expert_id = parsed_state.get('expert_id', [None])[0]
        secret_id = parsed_state.get('secret_id', [None])[0]

        term_services_url = gui_urls_creator.get_expert_onboarding_term_services_page_url(expert_id, secret_id)

        if code is None:
            raise APIException("Invalid request", code=status.HTTP_400_BAD_REQUEST)

        expert = Expert.objects.filter(id=expert_id).first()
        if not expert:
            raise APIException(f"Invalid expert ID {expert_id}", code=status.HTTP_400_BAD_REQUEST)
        ExpertSecretIdAPIChecker().raise_exception_if_not_valid(expert, secret_id)

        gui_conf = GUIConfigurations.get()
        linkedin_register_redirect_uri = gui_conf.backend_hostname + 'auth/register-with-linkedin/'
        access_token = util.get_access_token(code, linkedin_register_redirect_uri)
        user_data = util.get_user_data(access_token)
        first_name = user_data['localizedFirstName']
        last_name = user_data['localizedLastName']
        profile_pic = \
        user_data.get('profilePicture', {}).get('displayImage~', {}).get('elements', [{}])[0].get('identifiers', [{}])[
            0].get('identifier', '')
        email = util.get_user_email(access_token)
        user = User.objects.filter(username=email).first()
        if not user:
            person_info: PersonInfo = expert.get_person_info()
            person_info.first_name = first_name
            person_info.last_name = last_name
            person_info.pic_url = profile_pic
            person_info.save()
            person_info.set_primary_email(email, EmailSource.LINKEDIN)
            new_password = secrets.token_hex(16)
            ExpertsOnBoardingManager(expert).finish_on_boarding(new_password, False, check_for_pin=False)
            login(request, expert.user)
            request.session['as_other'] = False
            ExpertWorkflowEventManager().handle_situation(ExpertWorkflowEventTrigger.FINISH_LINKEDIN_REGISTRATION, expert)
            return redirect(term_services_url)


class LinkedInAuthLoginView(View):
    def get(self, request):
        util = LinkedInAuthUtil()
        gui_urls_creator = GuiUrlsCreator()  # Initialize gui_urls_creator here

        error = request.GET.get('error')

        if error:
            return redirect(gui_urls_creator.get_main_page())

        code = request.GET.get('code')
        main_page = gui_urls_creator.get_main_page()
        if code is None:
            raise APIException("Invalid request", code=status.HTTP_400_BAD_REQUEST)

        gui_conf = GUIConfigurations.get()

        linkedin_login_redirect_uri = gui_conf.backend_hostname + 'auth/login-with-linkedin/'
        access_token = util.get_access_token(code, linkedin_login_redirect_uri)
        email = util.get_user_email(access_token)

        user = User.objects.filter(username=email).first()
        if user is None:
            return redirect(main_page + 'login?login_failed=true')
        else:
            login(request, user)
            request.session['as_other'] = False
            return redirect(main_page)
