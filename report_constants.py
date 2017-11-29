#!/usr/bin/python3

fileName = 'log_report_file.txt'


q = [{'question': '\nWhat are the three most popular articles of all time?\n',
      'query': '''select * from ( select title, count(*) as views,
row_number()over(partition by Null order by count(*) desc) as rank
from allNewsDataDN
where title not in ('/')
and status in ('200 OK')
group by 1) data
where rank <=3;''',
      'formattedString': '''\t{2}: "{0}" with a total view count of {1}.\n'''},
     {'question': '\nWho are the most popular authors of all time?\n',
      'query': '''select name, count(*) as views from allNewsDataDN
where title not in ('/')
and status in ('200 OK')
group by 1
order by 2 desc;''',
      'formattedString': '''\t{0} with a total view count of {1}.\n'''},
     {'question': '\nWhen did more than 1% of requests lead to an error?\n',
      'query': '''select date,
sum(case when status not in ('200 OK') then 1 else 0 end)
*100.00/count(*) as percentError
from allNewsDataDN 
group by 1
having sum(case when status not in ('200 OK') then 1 else 0 end)
*100.00/count(*) >1;''',
      'formattedString': '''\t{0} had a error rate of {1:0.2f}%.\n'''}]
