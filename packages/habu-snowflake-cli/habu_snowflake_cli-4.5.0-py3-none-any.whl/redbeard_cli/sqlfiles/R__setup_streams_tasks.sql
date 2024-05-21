BEGIN

CREATE OR REPLACE PROCEDURE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.SETUP_STREAM_TASKS(ORGANIZATON_ID VARCHAR, HABU_ACCOUNT_ID  VARCHAR, CUSTOMER_ACCOUNT_ID VARCHAR)
returns string
language javascript
execute as owner as
$$
    // at this point, we have accepted the share for the organization database from the habu account
    // habu_org_xxx_db contains a table called clean_room_requests that is shared with the customer
    // we are now going to setup a stream for the clean_room_requests table so that we can setup
    // the machinery for db-rpc
    var sf_org_id = ORGANIZATON_ID.replace(/-/g, '').toUpperCase();
    var setup_stream_sql = "CREATE OR REPLACE STREAM CLEAN_ROOM.CLEAN_ROOM_REQUESTS_STREAM \
        ON TABLE HABU_ORG_" + sf_org_id + "_SHARE_DB.CLEAN_ROOM.CLEAN_ROOM_REQUESTS \
        APPEND_ONLY=TRUE \
        COMMENT = 'HABU_" + CUSTOMER_ACCOUNT_ID + "'";
    snowflake.execute({ sqlText: setup_stream_sql });
    // stream has been setup, now create a task that listens to the stream and triggers the
    // PROCESS_ORG_REQUEST stored procedure to process pending clean room requests
    var copy_task_sql = "CREATE OR REPLACE TASK CLEAN_ROOM.CLEAN_ROOM_REQUESTS_TASK \
        SCHEDULE = '1 MINUTE' \
        ALLOW_OVERLAPPING_EXECUTION = TRUE \
        USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = 'XSMALL' \
        WHEN SYSTEM$STREAM_HAS_DATA('CLEAN_ROOM.CLEAN_ROOM_REQUESTS_STREAM') \
        AS CALL CLEAN_ROOM.PROCESS_ORG_REQUEST()"
    snowflake.execute({ sqlText: copy_task_sql });
    var new_clean_rooms_task = "CREATE OR REPLACE TASK CLEAN_ROOM.HANDLE_NEW_CLEAN_ROOMS_TASK \
        USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = 'XSMALL' \
        AFTER CLEAN_ROOM.CLEAN_ROOM_REQUESTS_TASK \
        AS CALL CLEAN_ROOM.HANDLE_NEW_CLEAN_ROOMS()"
    snowflake.execute({ sqlText: new_clean_rooms_task });
    var new_datasets_task = "CREATE OR REPLACE TASK CLEAN_ROOM.HANDLE_NEW_DATASETS_TASK \
        USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = 'XSMALL' \
        AFTER CLEAN_ROOM.CLEAN_ROOM_REQUESTS_TASK \
        AS CALL CLEAN_ROOM.HANDLE_NEW_DATASETS()"
    snowflake.execute({ sqlText: new_datasets_task });
    var question_run_data_share_task = "CREATE OR REPLACE TASK CLEAN_ROOM.HANDLE_QUESTION_RUN_DATA_SHARE_TASK \
        USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = 'XSMALL' \
        AFTER CLEAN_ROOM.CLEAN_ROOM_REQUESTS_TASK \
        AS CALL CLEAN_ROOM.HANDLE_QUESTION_RUN_DATA_SHARE()"
    snowflake.execute({ sqlText: question_run_data_share_task });
    var question_run_cleanup_task = "CREATE OR REPLACE TASK CLEAN_ROOM.HANDLE_QUESTION_RUN_CLEANUP_TASK \
        USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = 'XSMALL' \
        AFTER CLEAN_ROOM.CLEAN_ROOM_REQUESTS_TASK \
        AS CALL CLEAN_ROOM.HANDLE_QUESTION_RUN_CLEANUP()"
    snowflake.execute({ sqlText: question_run_cleanup_task });
    var question_run_result_share_task = "CREATE OR REPLACE TASK CLEAN_ROOM.HANDLE_QUESTION_RUN_RESULT_SHARE_TASK \
        USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = 'XSMALL' \
        AFTER CLEAN_ROOM.CLEAN_ROOM_REQUESTS_TASK \
        AS CALL CLEAN_ROOM.HANDLE_QUESTION_RUN_RESULT_SHARE()"
    snowflake.execute({ sqlText: question_run_result_share_task });
    var question_run_accept_result_share_task = "CREATE OR REPLACE TASK CLEAN_ROOM.HANDLE_QUESTION_RUN_ACCEPT_RESULT_SHARE_TASK \
        USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = 'XSMALL' \
        AFTER CLEAN_ROOM.CLEAN_ROOM_REQUESTS_TASK \
        AS CALL CLEAN_ROOM.HANDLE_QUESTION_RUN_ACCEPT_RESULT_SHARE()"
    snowflake.execute({ sqlText: question_run_accept_result_share_task });
    var post_run_query_task = "CREATE OR REPLACE TASK CLEAN_ROOM.HANDLE_POST_RUN_QUERY_TASK \
        WAREHOUSE = HABU_CLEAN_ROOM_COMMON_XLARGE_WH \
        AFTER CLEAN_ROOM.CLEAN_ROOM_REQUESTS_TASK \
        AS CALL CLEAN_ROOM.HANDLE_POST_RUN_QUERY()"
    snowflake.execute({ sqlText: post_run_query_task });
    mgmt_commands_task = "CREATE OR REPLACE TASK CLEAN_ROOM.HANDLE_MGMT_COMMANDS_TASK \
        USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = 'XSMALL' \
        AFTER CLEAN_ROOM.CLEAN_ROOM_REQUESTS_TASK \
        AS CALL CLEAN_ROOM.HANDLE_MANAGEMENT_COMMANDS()"
    snowflake.execute({ sqlText: mgmt_commands_task });
    add_data_connection_task = "CREATE OR REPLACE TASK CLEAN_ROOM.HANDLE_ADD_DATA_CONNECTION_TASK \
            USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = 'XSMALL' \
            AFTER CLEAN_ROOM.CLEAN_ROOM_REQUESTS_TASK \
            AS CALL CLEAN_ROOM.HANDLE_ADD_DATA_CONNECTION()"
    snowflake.execute({ sqlText: add_data_connection_task });
    // tasks are created in 'suspend' mode root and all dependent tasks need to be enabled explicitly
    // TODO: fails with error - SQL compilation error: Query called from a stored procedure contains a function with side effects [SYSTEM$TASK_DEPENDENTS_ENABLE]
    // snowflake.execute({ sqlText: "SELECT SYSTEM$TASK_DEPENDENTS_ENABLE('CLEAN_ROOM.CLEAN_ROOM_REQUESTS_TASK')" });
    // Since recursively resuming all the dependent task tied to root task is not working,
    // explicitly resuming all the tasks in reverse order. Children tasks muste be started before the root task.
    snowflake.execute({ sqlText: "ALTER TASK CLEAN_ROOM.HANDLE_POST_RUN_QUERY_TASK RESUME" });
    snowflake.execute({ sqlText: "ALTER TASK CLEAN_ROOM.HANDLE_ADD_DATA_CONNECTION_TASK RESUME" });
    snowflake.execute({ sqlText: "ALTER TASK CLEAN_ROOM.HANDLE_MGMT_COMMANDS_TASK RESUME" });
    snowflake.execute({ sqlText: "DROP TASK IF EXISTS CLEAN_ROOM.HANDLE_NEW_QUESTION_RUNS_TASK" });
    snowflake.execute({ sqlText: "ALTER TASK CLEAN_ROOM.HANDLE_QUESTION_RUN_CLEANUP_TASK RESUME" });
    snowflake.execute({ sqlText: "ALTER TASK CLEAN_ROOM.HANDLE_QUESTION_RUN_RESULT_SHARE_TASK RESUME" });
    snowflake.execute({ sqlText: "ALTER TASK CLEAN_ROOM.HANDLE_QUESTION_RUN_ACCEPT_RESULT_SHARE_TASK RESUME" });
    snowflake.execute({ sqlText: "ALTER TASK CLEAN_ROOM.HANDLE_QUESTION_RUN_DATA_SHARE_TASK RESUME" });
    snowflake.execute({ sqlText: "ALTER TASK CLEAN_ROOM.HANDLE_NEW_DATASETS_TASK RESUME" });
    snowflake.execute({ sqlText: "ALTER TASK CLEAN_ROOM.HANDLE_NEW_CLEAN_ROOMS_TASK RESUME" });

    const warehouseSizes = ['XSMALL', 'XLARGE', 'X2LARGE', 'X3LARGE', 'X4LARGE', 'SNOWPARK_XLARGE', 'SNOWPARK_X2LARGE'];

    warehouseSizes.forEach(warehouseSize => {
        var pendingMessageTaskName = `CHECK_QUESTION_RUN_REQUESTS_FOR_${warehouseSize}_TASK`;
        var handlePendingMessageTaskName = `HANDLE_NEW_QUESTION_RUNS_WITH_${warehouseSize}_TASK`;

         var new_question_runs_check_task = `CREATE OR REPLACE TASK CLEAN_ROOM.${pendingMessageTaskName} \
            USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = 'XSMALL' \
            AFTER CLEAN_ROOM.CLEAN_ROOM_REQUESTS_TASK \
            AS CALL CLEAN_ROOM.PENDING_MESSAGE_COUNT_FOR_WAREHOUSE_TYPE('${warehouseSize}')`
        snowflake.execute({ sqlText: new_question_runs_check_task });

        var new_question_runs_handle_task = `CREATE OR REPLACE TASK CLEAN_ROOM.${handlePendingMessageTaskName} \
            WAREHOUSE = HABU_CLEAN_ROOM_COMMON_${warehouseSize}_WH \
            AFTER CLEAN_ROOM.${pendingMessageTaskName} \
            WHEN SYSTEM$GET_PREDECESSOR_RETURN_VALUE() != '0' \
            AS CALL CLEAN_ROOM.HANDLE_NEW_QUESTION_RUNS()`
        snowflake.execute({ sqlText: new_question_runs_handle_task });

        snowflake.execute({ sqlText: `ALTER TASK CLEAN_ROOM.${pendingMessageTaskName} RESUME` });
        snowflake.execute({ sqlText: `ALTER TASK CLEAN_ROOM.${handlePendingMessageTaskName} RESUME` });
    });

    snowflake.execute({ sqlText: "ALTER TASK CLEAN_ROOM.CLEAN_ROOM_REQUESTS_TASK RESUME" });

return "Setup of stream and tasks successful";
$$;

CREATE OR REPLACE PROCEDURE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.PENDING_MESSAGE_COUNT_FOR_WAREHOUSE_TYPE(WAREHOUSE_SIZE VARCHAR)
RETURNS STRING
LANGUAGE JAVASCRIPT
EXECUTE AS CALLER
AS $$

    var cnt_result = 0;
    var sql_command = "select count(request_data:warehouse_size) as cnt \
        from habu_clean_room_common.clean_room.clean_room_requests \
        where request_type = 'NEW_QUESTION_RUN' and request_status = 'PENDING' \
        and request_data:warehouse_size = '" + WAREHOUSE_SIZE + "'";
    var stmt = snowflake.createStatement({sqlText: sql_command});
    var rs = stmt.execute();
    if(rs.next()) {
       cnt_result = rs.getColumnValue(1);
    }

    snowflake.createStatement({sqlText:`call system$set_return_value('${cnt_result}');`}).execute();
$$;



end;

