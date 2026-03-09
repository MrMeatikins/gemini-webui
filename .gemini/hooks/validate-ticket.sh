#!/usr/bin/env bash

# Read JSON input from Gemini CLI
input=$(cat)

# Extract tool name
tool_name=$(echo "$input" | jq -r '.tool_name')

# Check if the tool is update_work_item
if [ "$tool_name" = "update_work_item" ]; then
    # Extract the new state and the ticket ID
    state=$(echo "$input" | jq -r '.tool_input.state')
    ticket_id=$(echo "$input" | jq -r '.tool_input.work_item_id')
    project_id=$(echo "$input" | jq -r '.tool_input.project_id')
    
    # Check if the state is 'Needs Validation'
    if [ "$state" = "40a62c46-993b-4ca3-a0d9-be3fe9c31877" ]; then
        echo "Ticket $ticket_id moved to Needs Validation. Triggering automated validation pipeline..." >&2
        
        # Define the pipeline prompt
        PROMPT="You are an automated Quality Assurance Pipeline Agent.
A Kanban ticket ($ticket_id) in project $project_id was just moved to 'Needs Validation'.
Follow these exact steps:
1. Use 'retrieve_work_item' to read the ticket details and its acceptance criteria.
2. Use the 'codebase_investigator' agent to analyze the workspace and determine if the code changes meet the ticket's requirements and tests.
3. Pass the findings from the codebase investigator, along with any other evidence you gather, to the 'reality-checker' agent for a final assessment.
4. If the 'reality-checker' agent APPROVES the ticket for production:
   - Call 'update_work_item' to change the state to 'Done' (ae56a905-81b7-4f9a-a2e5-7a842d66b8f4).
   - Add a comment to the ticket with 'create_work_item_comment' confirming it passed QA.
5. If the 'reality-checker' agent REJECTS the ticket (NEEDS WORK):
   - Call 'update_work_item' to change the state back to 'In Progress' (d142bbba-7042-4eab-88bc-88dea4f60ba9).
   - Use 'create_work_item_comment' to post the detailed rejection reasons and required fixes.
Work autonomously and do not ask for user input. Finish your process once the ticket state is updated."

        # Execute headless Gemini in the background to avoid blocking the current session
        nohup gemini -p "$PROMPT" -y > "/tmp/gemini_validate_${ticket_id}.log" 2>&1 &
    fi
fi

# Always allow the tool execution to proceed normally
echo '{"decision": "allow"}'
