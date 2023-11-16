from datetime import datetime
from time import sleep

from openai import OpenAI

client = OpenAI()

# Step 1: Create an Assistant
assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You are a personal math tutor. Write and run code to answer math questions.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4-1106-preview",
)
print(assistant.id)

# Step 2: Create a Thread
thread = client.beta.threads.create()

# Step 3: Add a Message to a Thread
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="I need to solve the equation `3x + 11 = 14`. Can you help me?",
)

# list Messages in Thread
thread_messages = client.beta.threads.messages.list(thread.id)
# print(thread_messages.data)

# Step 4: Run the Assistant
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="Please address the user as Jane Doe. The user has a premium account.",
)

# Step 5: Check the Run status
while True:
    count = 1
    print(f"Checking Run status... (attempt {count}), {datetime.now()}")
    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    if run.status == "completed":
        print("Run completed at {}".format(run.completed_at))
        break
    print("Run not completed yet.")
    sleep(10)

print(run)

# Step 6: Display the Assistant's Response
messages = client.beta.threads.messages.list(thread_id=thread.id, order="asc")
print(messages)
print("-----------------------------")
for message in messages.data:
    content = [content.text.value for content in message.content]
    print(f"{message.role}: {' '.join(content)}")
