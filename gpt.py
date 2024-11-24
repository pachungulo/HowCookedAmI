from openai import OpenAI
import os
from dotenv import load_dotenv

def summarize(originalComments):

    load_dotenv()
    #openai.api_key =os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    summarizedComments = []


    for i in range(len(originalComments)):
        if not originalComments[i]:
            summarizedComments.append([])
        else:
            content = "Summarize the following comments from students about their thoughts on a teacher and a class. The summary must be 3-5 sentences long and cover the main ideas expressed by the comments. Each comment is separated by five forward slashes (/////). "
            for comment in range(len(originalComments[i])):
                if comment==0:
                    content += "comment" + str(comment+1) + ": " + originalComments[i][comment]
                else:
                    content += "///// comment" + str(comment+1) + ": " + originalComments[i][comment]

            # summarizedComments.append(content)
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0.4,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {
                        "role": "user",
                        "content": content
                    }
                ]
            )
            #print(completion)
            #print(completion.choices)
            summarizedComments.append(completion.choices[0].message.content)

            #print(completion.choices[0].message)

    print(summarizedComments)


#summarize([["the teacher is trash", "the teacher is great"]])