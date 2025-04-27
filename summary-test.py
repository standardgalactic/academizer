#!/usr/bin/python3

import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import AssistantMessage, SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# Azure endpoint and model configuration
endpoint = "https://nateg-m9ac3h3h-swedencentral.services.ai.azure.com/models"
model_name = "DeepSeek-V3"

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential("<Azure Key>"),
)

# Function to truncate content to fit within the model's context length
def truncate_content(content, max_tokens=160000):
    return content[:max_tokens]  # Truncate content to a safe token estimate

# Output file for summaries
output_file = "short-summaries.txt"

# Function to write to both terminal and output file
def tee_output(file, message):
    print(message)  # Print to terminal
    file.write(message + "\n")  # Write to file with a newline

# Open the output file for writing
with open(output_file, "w", encoding="utf-8") as summary_file:
    # Iterate over all text files in the current directory
    for file_name in os.listdir("."):
        if file_name.endswith(".txt"):  # Check if the file is a text file
            tee_output(summary_file, f"Processing file: {file_name}")
            try:
                with open(file_name, "r", encoding="utf-8") as file:
                    content = file.read()  # Read the file content

                # Truncate content if it exceeds the token limit
                truncated_content = truncate_content(content)

                # Generate summary using Azure AI service
                response = client.complete(
                    messages=[
                        SystemMessage(content="You are a helpful assistant who summarizes text files."),
                        UserMessage(content=f"Summarize the following text:\n{truncated_content}")
                    ],
                    max_tokens=2048,
                    temperature=0.8,
                    top_p=0.1,
                    presence_penalty=0.0,
                    frequency_penalty=0.0,
                    model=model_name
                )

                # Extract summary from the response
                summary = response.choices[0].message.content

                # Write the summary to both terminal and the output file
                tee_output(summary_file, f"Summary for {file_name}:\n{summary}\n")
                tee_output(summary_file, f"Successfully summarized: {file_name}")

            except Exception as e:
                # Handle errors and log them to both terminal and summary file
                error_message = f"Failed to summarize {file_name}: {e}"
                tee_output(summary_file, error_message)

tee_output(summary_file, f"Summaries saved to {output_file}")
