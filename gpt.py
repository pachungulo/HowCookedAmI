from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize(originalComments):

    
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
    return summarizedComments


def generateImage(difficulty):
    if difficulty<40:
        message = "Generate an image of a university student that is relaxing on the beach with a drink and enjoying the sun and waves."
    elif difficulty<75:
        message = "Generate an image of a university student who is putting effort to study and do well in classes. The student is not particularly stressed but is not particularly relaxed."
    else:
        message = "Generate an image of a university student that is going crazy because of the large amount of workload. The student is crying, losing hair and has acne."
    response = client.images.generate(
        model="dall-e-3",
        prompt=message,
        size="1024x1024",
        quality="standard",
        n=1,
        )

    image_url = response.data[0].url
    print(image_url)
    return image_url
#generateImage(5)
#summarize([["the teacher is trash", "the teacher is great"]])