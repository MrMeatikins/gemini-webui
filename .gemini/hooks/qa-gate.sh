#!/bin/bash
input=$(cat)
tool_name=$(echo "$input" | jq -r '.tool_name')

# Proceed if the tool is one of the shell aliases
if [[ "$tool_name" =~ run_shell_command|Bash|shell ]]; then
    command=$(echo "$input" | jq -r '.tool_input.command')
    
    # Intercept AI git commit commands unless explicitly bypassed
    if [[ "$command" =~ ^git[[:space:]]+commit ]] && [[ ! "$command" =~ SKIP_QA=1 ]] && [[ ! "$command" =~ pytest ]]; then
        
        modified_cmd="echo '--- AI QA GATE ---' && \
TICKET_FILE='/tmp/gemini-webui-ticket.txt' && \
if [ ! -f \$TICKET_FILE ] || [ ! -s \$TICKET_FILE ]; then \
    echo 'Error: /tmp/gemini-webui-ticket.txt is missing or empty. Please save the Kanban ticket ID.'; \
    exit 1; \
fi && \
TICKET_AGE=\$(find \$TICKET_FILE -mmin -1 -print) && \
if [ -z \"\$TICKET_AGE\" ]; then \
    echo 'Error: The ticket file /tmp/gemini-webui-ticket.txt was not created or modified within the last 60 seconds.'; \
    echo 'Please rewrite the ticket ID to the file to confirm it is currently active: echo \"GEMWE-XYZ\" > /tmp/gemini-webui-ticket.txt'; \
    exit 1; \
fi && \
TICKET_ID=\$(cat \$TICKET_FILE) && \
echo \"Running unit tests for ticket \$TICKET_ID...\" && \
RESULTS_FILE='/tmp/gemini-webui-unit-test-results.txt' && \
source .venv/bin/activate && PYTHONPATH=. pytest tests/ > \$RESULTS_FILE 2>&1; \
PYTEST_EXIT=\$?; \
if grep -qE '([0-9]+ failed|[0-9]+ skipped)' \$RESULTS_FILE || [ \$PYTEST_EXIT -ne 0 ]; then \
    echo '--- QA REJECTED: TESTS FAILED ---'; \
    cat \$RESULTS_FILE; \
    exit 1; \
fi && \
echo 'Tests passed. Asking reality-checker...' && \
REALITY_FILE='/tmp/gemini-webui-reality-results.txt' && \
TICKET_CONTENT_FILE='/tmp/current_ticket_content.txt' && \
gemini -y -p \"Fetch and print the full details for kanban ticket \$TICKET_ID using the retrieve_work_item or list_work_items tool.\" > \$TICKET_CONTENT_FILE 2>&1 && \
echo '>>>' > /tmp/d && \
cat ~/.gemini/agents/reality-checker.md /tmp/d \$TICKET_CONTENT_FILE /tmp/d /tmp/d \$RESULTS_FILE /tmp/d | gemini -y -p \"An agent has decided this ticket is completed. You are provided the ticket, the test results, and you have full access to the code. Please validate or respond with NEEDS WORK and a detailed comment\" > \$REALITY_FILE 2>&1 && \
if grep -q 'NEEDS WORK' \$REALITY_FILE; then \
    echo '--- QA REJECTED BY REALITY-CHECKER ---'; \
    cat \$REALITY_FILE; \
    exit 1; \
else \
    echo '--- QA APPROVED ---'; \
    $command && ./scripts/increment_version.sh; \
fi"
        
        jq -n --arg cmd "$modified_cmd" '{decision: "modify", modified_args: {command: $cmd}}'
        exit 0
    fi
fi

echo '{"decision": "allow"}'
