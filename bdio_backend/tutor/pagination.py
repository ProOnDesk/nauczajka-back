from core.pagination import CustomPagination
from tutor.models import Tutor

class ReviewPagination(CustomPagination):
    def get_paginated_response(self, data):
        tutor_id = getattr(self, 'tutor_id', None)
        
        response = super().get_paginated_response(data)
        
        if tutor_id is not None:
            tutor = Tutor.objects.get(id=tutor_id)
            response.data['avg_rating'] = tutor.avg_rating
            
        return response
    
    def get_paginated_response_schema(self, schema):

        return {
            'type': 'object',
            'properties': {
                'count': {
                    'type': 'integer',
                    'example': 123,
                },
                'next': {
                    'type': 'string',
                    'nullable': True,
                    'format': 'uri',
                    'example': 'http://api.example.org/accounts/?{page_query_param}=4'.format(
                        page_query_param=self.page_query_param)
                },
                'previous': {
                    'type': 'string',
                    'nullable': True,
                    'format': 'uri',
                    'example': 'http://api.example.org/accounts/?{page_query_param}=2'.format(
                        page_query_param=self.page_query_param)
                },
                'results': schema,
                'avg_rating': {
                    'type': 'decimal',
                    'example': 4.5
                }
            },
        }
        