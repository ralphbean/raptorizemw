from pyramidraptorized.models import DBSession
from pyramidraptorized.models import MyModel

def my_view(request):
    dbsession = DBSession()
    root = dbsession.query(MyModel).filter(MyModel.name==u'root').first()
    return {'root':root, 'project':'pyramid-raptorized'}
