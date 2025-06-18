#debug
dbt debug

#compile
dbt compile

#run
dbt run # it literally executes the process

#generate documentation (data lineage,)
dbt docs generate

#run local server to see the project interface
dbt docs serve

#five differents materialization methods:
-table
-view
-incremental
-ephemeral
-materialized view