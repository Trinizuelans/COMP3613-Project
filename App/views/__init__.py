# blue prints are imported 
# explicitly instead of using *
from .user import user_views
from .index import index_views
from .auth import auth_views
from .staff import staff_views
from .student import student_views
from .review import review_views
from .vote import vote_views

views = [user_views, index_views, auth_views,staff_views,student_views,review_views,vote_views] 
# blueprints must be added to this list