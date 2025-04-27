#!/usr/bin/python3

import os
import math
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import AssistantMessage, SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# Azure endpoint and model configuration
endpoint = "https://nateg-m9ac3h3h-swedencentral.services.ai.azure.com/models"
model_name = "DeepSeek-V3"

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential("2WppAntLvGn0dkDw0LaSCGu3ov0SsitsgrA4yo94s1QHy0o84BAsJQQJ99BDACfhMk5XJ3w3AAAAACOGFhIL"),

)

# Output file for summaries
output_file = "academizer-overview.txt"

# Function to split content into chunks
def split_into_chunks(content, max_chunks=10):
    lines = content.splitlines()
    total_lines = len(lines)
    chunk_size = math.ceil(total_lines / max_chunks)
    chunks = [lines[i:i + chunk_size] for i in range(0, total_lines, chunk_size)]
    return ['\n'.join(chunk) for chunk in chunks]

# Open the output file for writing
with open(output_file, "w", encoding="utf-8") as summary_file:
    # Iterate over all text files in the current directory
    for file_name in os.listdir("."):
        if file_name.endswith(".txt"):  # Check if the file is a text file
            with open(file_name, "r", encoding="utf-8") as file:
                content = file.read()  # Read the file content

            # Split the content into chunks
            chunks = split_into_chunks(content)

            print(f"Processing {file_name} with {len(chunks)} chunks...")

            # Process each chunk
            for i, chunk in enumerate(chunks):
                print(f"Summarizing chunk {i + 1} of {len(chunks)}...")
                # Generate summary using Azure AI service
                response = client.complete(
                    messages=[
                        SystemMessage(content="You are a helpful assistant who summarizes text files."),
                        UserMessage(content=f"Summarize the following text:\n{chunk}")
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

                # Write the summary to the output file
                summary_file.write(f"Summary for {file_name}, Chunk {i + 1}:\n{summary}\n\n")

                # Tee the summary to the command line
                print(f"Summary for {file_name}, Chunk {i + 1}:\n{summary}\n")

print(f"Summaries saved to {output_file}")
