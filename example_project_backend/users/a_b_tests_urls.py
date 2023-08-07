from django.urls import path

from users.views.a_b_tests_views.a_b_test_full_item_by_admin_view import ABTestFullItemByAdminView
from users.views.a_b_tests_views.a_b_test_item_by_admin_view import ABTestItemByAdminView
from users.views.a_b_tests_views.a_b_tests_list_by_admin_view import ABTestsListByAdminView

urlpatterns = [
    path(r"<int:object_id>/by-admin/", ABTestItemByAdminView.as_view()),
    path(r"<int:object_id>/full/by-admin/", ABTestFullItemByAdminView.as_view()),
    path(r"by-admin/", ABTestsListByAdminView.as_view()),
]
