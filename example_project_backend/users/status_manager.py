from typing import List, Optional

from django.db.models import Q

from calls.calls_managers.calls_fetcher_manager import CallsFetcherManager
from calls.consts.calls_responses_status import CallsResponsesStatus
from calls.consts.calls_status import CallsStatus
from calls.models import Call
from calls.serializers.short_call_serializer import ShortCallSerializer
from common.django_utils.serializers.serializer_request_data import SerializerRequestData
from common.django_utils.serializers.serializer_request_data_getter import SerializerRequestDataGetter
from common.time_utils import TimeUtils
from common.type_hints import JSONType
from experts.consts.engagements_hidden_reasons import EngagementsHiddenReasons
from experts.consts.engagements_status_for_experts import EngagementsStatusForExperts
from experts.consts.other_suggested_times_status import OtherSuggestedTimesStatus
from experts.consts.sub_projects_products import SubProjectProducts
from experts.managers.anonymous_manager import AnonymousManager
from experts.managers.engagements_managers.engagements_getter import EngagementsGetter
from experts.managers.experts_managers.expert_engagements_manager import ExpertEngagementsManager
from experts.managers.projects_manager.projects_data_manager import ProjectsDataManager
from experts.models import Project, Engagement, Expert, SubProject
from experts.serializers.engagements_serializers.short_engagement_status_serializer import \
    ShortEngagementStatusSerializer
from experts.serializers.projects_serializers.short_project_serializer import ShortProjectSerializer
from experts.serializers.projects_serializers.short_project_status_serializer import ShortProjectStatusSerializer
from reminders.reminders_creators.expert_new_engagement_reminder_creator import ExpertNewEngagementReminderCreator
from users.consts.action_needed_type import ActionNeededType
from users.models import User
from experts.consts.workflow_enum import ExpertWorkflowEventTrigger
from experts.managers.expert_workflow_event_manager.expert_workflow_event_manager import ExpertWorkflowEventManager


class StatusDataManager:
    NO_NEED_TO_CONFIRM_STATUSES = [CallsStatus.DONE, CallsStatus.CANCELED, CallsStatus.CANCELED_RESCHEDULE]

    def __init__(self, user: User):
        self.user = user
        self.max_projects_amount = 10

        self.serializer_data = SerializerRequestData(
            viewer_type=SerializerRequestDataGetter.get_viewer_type_by_user(user))

    def get_my_status(self) -> JSONType:
        upcoming_calls = list(CallsFetcherManager().retrieve_upcoming_for_user(self.user, Call.objects))
        res = {
            'upcoming_calls': ShortCallSerializer(self.serializer_data).serialize_iterable(upcoming_calls),
            'recent_projects': None,
            'all_projects_status': None,
            'open_projects': None,
            'actions_needed': [],
        }
        actions_needed = []

        if self.user.is_client():
            res['recent_projects'] = self.get_recent_projects()
            res['all_projects_status'] = self.get_all_projects_status()
            res['calls_completed_by_org'] = self.get_calls_completed_by_org()
            res['total_completed_surveys'] = self.get_completed_survey_count()
            res['total_experts'] = Expert.objects.all().count()


            res['trends'] = Expert.objects.all().count()

            actions_needed.extend(self.get_client_suggested_times_needed_actions())
            actions_needed.extend(self.get_confirm_done_calls_needed_actions())
            actions_needed.extend(self.get_schedule_calls_needed_actions())
            actions_needed.extend(self.get_view_trends_actions())
            actions_needed.extend(self.get_out_of_credits_actions())

        if self.user.is_expert():
            res['all_engagements_status'] = self.get_all_engagements_status()
            actions_needed.extend(self.get_screening_questions_actions())
            actions_needed.extend(self.get_suggested_times_actions())
            actions_needed.extend(self.get_fill_availability_actions())
            actions_needed.extend(self.get_update_expert_info_actions())
        actions_needed.extend(self.get_upload_picture_actions())
        actions_needed.extend(self.get_confirm_call_needed_actions(upcoming_calls))

        if self.user.is_client():
            self.add_actions_needed_to_projects(res, actions_needed)
            res['all_projects_status'].sort(key=lambda project_data: project_data['actionable_time'], reverse=True)

        if self.user.is_expert():
            self.add_actions_needed_to_engagements(res, actions_needed)
            res['all_engagements_status'].sort(key=lambda engagement_data: engagement_data['actionable_time'],
                                               reverse=True)

        return res

    def get_recent_projects(self) -> List[JSONType]:
        projects_manager = ProjectsDataManager()
        accessible_projects = projects_manager.get_open_accessible_projects(self.user, Project.objects)
        recent_projects_data = ShortProjectSerializer(self.serializer_data).serialize_iterable(
            projects_manager.get_recent_list(self.user, accessible_projects))
        return recent_projects_data

    def get_all_projects_status(self) -> List[JSONType]:
        projects_manager = ProjectsDataManager()
        accessible_projects = projects_manager.get_my_open_accessible_projects(self.user, Project.objects).order_by('-creation_time')
        recent_projects_data = ShortProjectStatusSerializer(self.serializer_data).serialize_manager(
            accessible_projects)
        return recent_projects_data

    def get_all_engagements_status(self) -> List[JSONType]:
        engagements_getter = EngagementsGetter()
        accessible_engagements = engagements_getter.get_open_by_expert_user(self.user, Engagement.objects)\
            .order_by('-creation_time')
        for engagement in accessible_engagements:
            ExpertWorkflowEventManager().handle_situation(ExpertWorkflowEventTrigger.SAW_ENGAGEMENT_IN_HOME_PAGE, engagement.expert, engagement)
            if not engagement.is_accepted_by_expert():
                ExpertNewEngagementReminderCreator(15).create(engagement)
        recent_engagements_data = ShortEngagementStatusSerializer(self.serializer_data).serialize_manager(
            accessible_engagements)
        return recent_engagements_data

    def get_client_suggested_times_needed_actions(self) -> List[JSONType]:
        projects_manager = ProjectsDataManager()
        accessible_projects = projects_manager.get_accessible_projects(self.user, Project.objects)
        accessible_projects_ids = [project.id for project in accessible_projects.all()]
        wanted_client_status = [OtherSuggestedTimesStatus.SUGGESTED_NOT_ANSWERED, OtherSuggestedTimesStatus.DECLINED]
        engagements_manager = Engagement.objects.filter(
            Q(other_suggested_times_status__in=wanted_client_status) &
            Q(sub_project__project_id__in=accessible_projects_ids) &
            Q(sub_project__project__is_demo=False) &
            Q(sub_project__is_finished=False)
        )
        res = []
        for engagement in engagements_manager.all():
            sub_project = engagement.sub_project

            action_type = ActionNeededType.SUGGESTED_TIMES_TO_CLIENT_WAITING if \
                engagement.other_suggested_times_status == OtherSuggestedTimesStatus.SUGGESTED_NOT_ANSWERED else \
                ActionNeededType.SUGGESTED_TIMES_TO_CLIENT_DECLINED
            res.append({
                'action_type': action_type,
                'action_time': TimeUtils.to_default_str(engagement.other_suggested_times_time),
                'project_id': sub_project.project.id,
                'engagement_id': engagement.id,
                'data': {
                    'engagement_id': engagement.id,
                    'expert_full_name': engagement.expert.get_full_name(),
                }
            })
        return res

    def get_screening_questions_actions(self) -> List[JSONType]:
        expert = self.user.get_expert()
        res = []
        for engagement in ExpertEngagementsManager(expert).get_active_engagements().all():
            if engagement.has_un_answered_question() or \
                    engagement.has_hidden_reason(EngagementsHiddenReasons.NOT_ACCEPTED_YET):
                res.append({
                    'action_type': ActionNeededType.SCREENING_QUESTION,
                    'action_time': TimeUtils.to_default_str(TimeUtils.zero_time()),
                    'project_id': None,
                    'engagement_id': engagement.id,
                    'data': {
                        'engagement_id': engagement.id,
                        'sub_project_name': engagement.sub_project.name,
                    }
                })
        return res

    def get_suggested_times_actions(self) -> List[JSONType]:
        engagements_manager = self.user.expert.engagement_set.filter(
            other_suggested_times_status=OtherSuggestedTimesStatus.SUGGESTED_NOT_ANSWERED)
        res = []
        for engagement in engagements_manager.filter(sub_project__project__is_demo=False):
            sub_project = engagement.sub_project
            organization = sub_project.project.organization
            new_data = AnonymousManager.create_serializer_data_is_anonymous_from_sub_project(
                self.serializer_data, sub_project=sub_project)

            res.append({
                'action_type': ActionNeededType.SUGGESTED_TIMES_TO_EXPERT,
                'action_time': TimeUtils.to_default_str(engagement.other_suggested_times_time),
                'project_id': sub_project.project.id,
                'engagement_id': engagement.id,
                'data': {
                    'engagement_id': engagement.id,
                    'organization_name': AnonymousManager.get_organization_name(new_data, organization),
                }
            })
        return res

    def get_confirm_call_needed_actions(self, upcoming_calls: List[Call]) -> List[JSONType]:
        res = []
        for call in upcoming_calls:
            if self.need_to_confirm_call(call):
                engagement = call.engagement
                sub_project = engagement.sub_project
                organization = sub_project.project.organization
                new_data = AnonymousManager.create_serializer_data_is_anonymous_from_sub_project(
                    self.serializer_data, sub_project=sub_project)

                res.append({
                    'action_type': ActionNeededType.CONFIRM_CALL,
                    'action_time': TimeUtils.to_default_str(call.creation_time),
                    'project_id': sub_project.project.id,
                    'engagement_id': engagement.id,
                    'data': {
                        'call_id': call.id,
                        'organization_name': AnonymousManager.get_organization_name(new_data, organization),
                        'sub_project_name': sub_project.name,
                        'expert_full_name': call.engagement.expert.get_full_name(),
                        'start_time': TimeUtils.to_default_str(call.start_time),
                    }
                })
        return res

    def get_confirm_done_calls_needed_actions(self) -> List[JSONType]:
        res = []
        objects = CallsFetcherManager().retrieve_all_for_user(self.user, Call.objects).filter(status=CallsStatus.DONE)
        for call in objects:
            if call.ask_for_review and not call.is_confirmed():
                sub_project = call.engagement.sub_project
                res.append({
                    'action_type': ActionNeededType.CONFIRM_DONE_CALL,
                    'action_time': TimeUtils.to_default_str(call.start_time),
                    'project_id': sub_project.project.id,
                    'engagement_id': None,
                    'data': {
                        'call_id': call.id,
                        'sub_project_name': sub_project.name,
                        'expert_full_name': call.engagement.expert.get_full_name(),
                        'start_time': TimeUtils.to_default_str(call.start_time),
                    }
                })
        return res

    def get_schedule_calls_needed_actions(self) -> List[JSONType]:
        res = []
        objects = CallsFetcherManager().retrieve_all_for_owner(self.user, Call.objects).filter(
            status=CallsStatus.CANCELED_RESCHEDULE)
        for call in objects:
            sub_project = call.engagement.sub_project
            res.append({
                'action_type': ActionNeededType.RESCHEDULE_CALL,
                'action_time': TimeUtils.to_default_str(call.creation_time),
                'project_id': sub_project.project.id,
                'engagement_id': None,
                'data': {
                    'call_id': call.id,
                    'engagement_id': call.engagement.id,
                    'sub_project_name': sub_project.name,
                    'expert_full_name': call.engagement.expert.get_full_name(),
                }
            })
        return res

    def get_view_trends_actions(self) -> List[JSONType]:
        return [{
            'action_type': ActionNeededType.VIEW_TRENDS,
            'action_time': TimeUtils.to_default_str(TimeUtils.zero_time()),
            'project_id': None,
            'engagement_id': None,
            'data': {}
        }]

    def get_out_of_credits_actions(self) -> List[JSONType]:
        credits_left = self.user.organization.get_credits_left_in_subscription()
        if credits_left < 1:
            return [{
                'action_type': ActionNeededType.OUT_OF_CREDITS,
                'action_time': TimeUtils.to_default_str(TimeUtils.zero_time()),
                'project_id': None,
                'data': {'credits_left': credits_left}
            }]
        if credits_left <= 5:
            return [{
                'action_type': ActionNeededType.CREDITS_RUNNING_LOW,
                'action_time': TimeUtils.to_default_str(TimeUtils.zero_time()),
                'project_id': None,
                'engagement_id': None,
                'data': {'credits_left': credits_left}
            }]
        return []

    def need_to_confirm_call(self, call: Call) -> bool:
        if call.status in self.NO_NEED_TO_CONFIRM_STATUSES:
            return call.owner_response_status == CallsResponsesStatus.WAITING
        if self.user.id == call.owner_id:
            return call.owner_response_status == CallsResponsesStatus.WAITING
        if self.user.id == call.engagement.expert.user_id:
            return call.expert_response_status == CallsResponsesStatus.WAITING
        if call.additional_attendees.filter(id=self.user.id).exists():
            response_status = call.additional_attendees_responses_status.get(self.user.id)
            return response_status == CallsResponsesStatus.WAITING or not response_status
        return False

    def get_fill_availability_actions(self) -> List[JSONType]:
        expert = self.user.get_expert()
        availability = expert.get_availability_schedule_after_time()
        if not availability:
            return [{
                'action_type': ActionNeededType.FILL_AVAILABILITY,
                'action_time': TimeUtils.to_default_str(TimeUtils.zero_time()),
                'project_id': None,
                'engagement_id': None,
                'data': {}
            }]
        return []

    def get_upload_picture_actions(self) -> List[JSONType]:
        if not self.user.pic_url:
            return [{
                'action_type': ActionNeededType.UPLOAD_PICTURE,
                'action_time': TimeUtils.to_default_str(TimeUtils.zero_time()),
                'project_id': None,
                'engagement_id': None,
                'data': {}
            }]
        return []

    def get_update_expert_info_actions(self) -> List[JSONType]:
        expert = self.user.get_expert()
        if not (expert.headline or expert.description):
            return [{
                'action_type': ActionNeededType.UPDATE_EXPERT_INFO,
                'action_time': TimeUtils.to_default_str(TimeUtils.zero_time()),
                'project_id': None,
                'engagement_id': None,
                'data': {}
            }]
        return []

    def add_actions_needed_to_projects(self, res: JSONType, actions_needed: List[JSONType]) -> None:
        if res['all_projects_status'] is None:
            res['actions_needed'] = actions_needed
            return

        remaining_actions_needed = []
        project_id_to_data = {data['id']: data for data in res['all_projects_status']}

        for action in actions_needed:
            action_project_id = action['project_id']
            if action_project_id and action_project_id in project_id_to_data:
                project_data = project_id_to_data[action_project_id]
                project_data['actions_needed'].append(action)
            else:
                remaining_actions_needed.append(action)

            action_time = action.get('action_time')
            if not action_project_id or not action_time:
                continue

            if action_project_id in project_id_to_data:
                prev_action_time = project_id_to_data[action_project_id]['actionable_time']
                project_id_to_data[action_project_id]['actionable_time'] = max(action_time, prev_action_time)

        res['actions_needed'] = remaining_actions_needed

    def add_actions_needed_to_engagements(self, res: JSONType, actions_needed: List[JSONType]) -> None:
        if res['all_engagements_status'] is None:
            res['actions_needed'] = actions_needed
            return

        remaining_actions_needed = []
        engagement_id_to_data = {data['id']: data for data in res['all_engagements_status']}

        for action in actions_needed:
            action_engagement_id = action['engagement_id']
            if action_engagement_id and action_engagement_id in engagement_id_to_data:
                engagement_data = engagement_id_to_data[action_engagement_id]
                engagement_data['actions_needed'].append(action)
            else:
                remaining_actions_needed.append(action)

            action_time = action.get('action_time')
            if not action_engagement_id or not action_time:
                continue

            if action_engagement_id in engagement_id_to_data:
                prev_action_time = engagement_id_to_data[action_engagement_id]['actionable_time']
                engagement_id_to_data[action_engagement_id]['actionable_time'] = max(action_time, prev_action_time)

        res['actions_needed'] = remaining_actions_needed

    def get_calls_completed_by_org(self) -> Optional[int]:
        if not self.user.is_client():
            return None
        organization = self.user.organization
        return Call.objects.filter(owner__organization=organization, status=CallsStatus.DONE, is_demo=False,
                                   ).count()

    def get_completed_survey_count(self) -> Optional[int]:
        if not self.user.is_client():
            return None
        organization = self.user.organization
        engagements = Engagement.objects.filter(sub_project__project__organization=organization,
                                                sub_project__sub_project_product=SubProjectProducts.SURVEY,
                                                onboarding_status=EngagementsStatusForExperts.FINISHED_QUESTIONS)
        return engagements.count()

