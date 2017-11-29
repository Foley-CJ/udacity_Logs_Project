# Logs Analysis [Udacity Full Stack Nanodegree ]


### This project generates a report on the performance of a news website.  The metrics are derived from data contained within a postgres database. The code is written using python 3 along with the psycopg2 python package.  

### Report Questions

What are the three most popular articles?

Who are the most popular authors, how many views have they had?

When did the site generate an excessive amount of errors (>1%)?


### Requirements 

Language: Python3

Packages: Psycopg2 

Virtual Machine: https://d17h27t6h515a5.cloudfront.net/topher/2017/August/59822701_fsnd-virtual-machine/fsnd-virtual-machine.zip

Database:  News
    - The data for the News database can be loaded from a sql script contained in the following zip:
       https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip
    - Command to load data after unzipping: psql -d news -f newsdata.sql.

### View Generation Script

In order to efficiently calculate these report metrics, a view was created ontop of the base data.  This view is generated on the fly within the report_generation.py file and is not needed to be created ahead of time, however is outlined below for your convience.

    create or replace view allNewsDataDN as
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
    

 
