from monitor.models import LastUpdate
from datetime import datetime

def add_variable_to_context(request):
    last = LastUpdate.objects.all()
    if last.count() > 0:
        last = last.latest('id')
        updated_at = last.created_at
    else:
        updated_at = datetime.strptime("25-07-2022 10:00", "%d-%m-%Y %H:%M")
    return {
        'updated_at': updated_at
    }