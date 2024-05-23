def get_email_list():
     import importlib
     
     from zeemee_py.helper_functions import connect_athena
     importlib.reload(connect_athena)
     
     query_string = """
          with cte as (
               select
               distinct o.name as org_name,
               o.id as organization_id,
               u.email as email
               from
               silver.prod_follower_organizations_latest o,
               silver.prod_follower_users_latest u
               where
               o.id = u.official_organization_id
               and u.official_organization_id = o.id
               and u.type = 'AdmissionsRep'
               and u.receive_community_snapshot_emails = 'true'
               and not u.email is null
               and not u.email = ''
               and (
               o.partner_community = 'true'
               or o.partner_pro_community = 'true'
               )
               and o.org_type is null
               union all
               select
               distinct o.name as org_name,
               o.id as organization_id,
               o.vip_emails as email
               from
               silver.prod_follower_organizations_latest o
               where
               not o.vip_emails is null
               and not o.vip_emails = ''
               and (
               o.partner_community = 'true'
               or o.partner_pro_community = 'true'
               )
               and o.org_type is null
               order by
               1
          )
          
          select
          org_name,
          organization_id,
          array_join(array_agg(email),',') as email_list
          from
          cte
          group by
          1,
          2
          order by
          1,
          2
     """
     emails = connect_athena.run_query_in_athena(query_string)
     
     return emails


