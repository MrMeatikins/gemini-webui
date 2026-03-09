import json
import urllib.request
import os

# We don't have the API key directly, but we can read it from env if it's there.
# Let's just output a list of IDs from the last list_work_items output if we had saved it.
