# udacity_Logs_Project


This project generates a report on the performance of a news website.  The metrics are derived from data contained within a postgres database. The code is written using python 3 along with a number of packages included in the requirements.txt *not all packages will be used in this version*  The following view is generated prior to running the metric scripts.  It is generated on the fly to address concerns around changing path logics.


    create view allNewsDataDN as 
        select
        lg.path,
        lg.title,
        lg.status,
        cast(lg.time as date) as date,
        athr.name
        from
           (select
               path,
               case when path in ('/article/media-obsessed-with-bears') then 'Media obsessed with bears' 
          when path in ('/article/so-many-bears') then 'There are a lot of bears' 
          when path in ('/article/balloon-goons-doomed') then 'Balloon goons doomed' 
          when path in ('/article/trouble-for-troubled') then 'Trouble for troubled troublemakers' 
          when path in ('/article/goats-eat-googles') then 'Goats eat Google''s lawn' 
          when path in ('/article/bad-things-gone') then 'Bad things gone, say good people' 
          when path in ('/article/bears-love-berries') then 'Bears love berries, alleges bear' 
          when path in ('/article/candidate-is-jerk') then 'Candidate is jerk, alleges rival' 
                    else path end as title,
                status,
               time
           from log) lg

        left join articles as artcl
        on artcl.title = lg.title

        left join authors as athr
        on athr.id = artcl.author;
