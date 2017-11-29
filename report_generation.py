#!/usr/bin/python3

from datetime import datetime
from psycopg2 import connect, Error
from report_constants import fileName, q


def query_execute(query, query_type, conn_string="dbname='news'"):
    """This is a module to connect to a postgres database where host,
       user, and password have been preconfigured. The connection and cursor
       are purged upon completion.

       Parameters:  query  -  the query that needs to be executed
                              against the database
                    conn_string (optional) - data base the query
                                             will be executed against"""
    try:
        with connect(conn_string) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                if query_type == 'extract':
                    return cur.fetchall()
                elif query_type == 'view':
                    conn.commit()
                else:
                    print('''please provide 'extract' or 'view' 
                             for queryType variable''')
    except Error as e:
        print('Connection Exception error:{}'.format(e))


def generate_view_script(view_name):
    """This module is used to dynamically build the script used to generate
       the view. It in self does not build the script, the "build_view"
       function should be used for that. This module uses the constant
       "mappingList" from the report_constants file to build
       the case statement logic used in the view."""

    view_build_query = '''create or replace view {query_view_name} as
                            select
                            lg.path,
                            artcl.title,
                            lg.status,
                            cast(lg.time as date) as date,
                            athr.name
                            from log as lg
                            
                            left join articles as artcl
                            on artcl.slug = substr(lg.path,10,length(lg.path))
                            
                            left join authors as athr
                            on athr.id = artcl.author;
                            '''.format(query_view_name=view_name)
    return view_build_query


def build_view(view_name='allNewsDataDN'):
    """This helper function is used in conjunction with the
       "genereate_view_script" in order to build the view the rest of
       the queries rely on.  This function will first remove the
       view with the provided name and then attempt to generate it.
       Although the viewName is a variable, the viewName of 'allNewsDataDN'
       is hardcoded into the queries found in the constants"""

    view_script = generate_view_script(view_name)

    try:
        query_execute(view_script, 'view')
    except ConnectionError:
        print('Could not connect to database. Please ensure proper setup.')


def report_writer():
    """This is the primary driver function of the script.  It leverages
       the view build by "build_view", the connection protocol from
       "query_execute" and the query information from "report_constants.py"
       in order to generate a text file containing 3
       different report metrics."""

    f = open(fileName, 'a+')
    f.write("Report generated on {0}. \n".format(datetime.now()))

    for report_entity in q:
        f.write(report_entity['question'])
        data = query_execute(report_entity['query'], 'extract')
        for result in data:
            f.write(report_entity['formattedString'].format(*result))
    f.close()


if __name__ == "__main__":
    build_view()
    report_writer()
