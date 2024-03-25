from example_app.models import ExampleModel

from django.db.models import QuerySet

from common.simple_rest.query_filters.base_query_filter import BaseQueryFilter


class GeneralExampleModelBaseQueryFilter(BaseQueryFilter[ExampleModel]):
    async def run(self, query: QuerySet[ExampleModel]) -> QuerySet[ExampleModel]:
        return query
