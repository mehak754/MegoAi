# To run this code you need to install the following dependencies:
# pip install google-genai

import base64
import mimetypes
import os
from google import genai
from google.genai import types


def save_binary_file(file_name, data):
    f = open(file_name, "wb")
    f.write(data)
    f.close()
    print(f"File saved to to: {file_name}")


def generate():
    client = genai.Client(
        api_key= "AIzaSyAcrBdhlLszYw2q7DTM1EtsV_9Vdz-Pdic",
    )

    model = "gemini-2.5-flash-image-preview"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""query
"""),
            ],
        ),
        types.Content(
            role="model",
            parts=[
                types.Part.from_text(text="""Subject: Leave Request - [Your Name] - [Your Employee ID]

Dear [HOD's Name],

I am writing to request a leave of absence from [Start Date] to [End Date], inclusive.

The reason for my leave is [briefly state your reason, e.g., \"a family event,\" \"personal matters,\" \"health reasons,\" \"travel plans\"].

I will ensure that all my urgent tasks are completed before my leave begins, and I will make arrangements for colleagues to cover my responsibilities during my absence. I will be reachable via [phone number/email] if anything critical arises.

I kindly request your approval for this leave. Please let me know if any further information is required from my end.

Thank you for your consideration.

Sincerely,

[Your Name]
[Your Designation]"""),
            ],
        ),
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""INSERT_INPUT_HERE"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_modalities=[
            "IMAGE",
            "TEXT",
        ],
    )

    file_index = 0
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if (
            chunk.candidates is None
            or chunk.candidates[0].content is None
            or chunk.candidates[0].content.parts is None
        ):
            continue
        if chunk.candidates[0].content.parts[0].inline_data and chunk.candidates[0].content.parts[0].inline_data.data:
            file_name = f"ENTER_FILE_NAME_{file_index}"
            file_index += 1
            inline_data = chunk.candidates[0].content.parts[0].inline_data
            data_buffer = inline_data.data
            file_extension = mimetypes.guess_extension(inline_data.mime_type)
            save_binary_file(f"{file_name}{file_extension}", data_buffer)
        else:
            print(chunk.text)

if __name__ == "__main__":
    generate()
