from django.db import connection



def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def process_config_request(config_request, formula):
    query = """
            Select {formula} from cloudconfig_configrequest 
            where hashed_id='{request_id}';
            """.format(formula=formula, request_id=config_request.hashed_id)
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = dictfetchall(cursor)
        return result
