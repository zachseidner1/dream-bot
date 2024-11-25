from openai import OpenAI
from pydantic import BaseModel


class IsDream(BaseModel):
    is_dream: bool


def check_dream(text: str, client: OpenAI) -> bool:
    dream_check_prompt = """
    I will provide you with text written by a user. Respond True if the text is describing a real dream that the user had, and respond False if that is not the case.
    If the user just mentions the word dream without describing a real dream they had, you need to repsond False.
    
    Example:
    Text:
        That was an interesting dream!
    Response:
        False
    Reasoning:
        The user just mentioned the word dream, they are not describing a dream that they themselves had.
        
    Example 2:
    Text:
        I had a dream last night that I was on a roler coaster.
    Response:
        True
    Reasoning:
        The user is describing an experience that they had in the dream. There is some sort of story / something that 
        happens to the user and this indicates that they are not just mentioning the word dream but instead are describing
        a dream that they actually had.
        
    Example 3:
    Text:
        Dream that I was listening to music and then someone came up to me and asked me a question. I didn't know this person but it was interesting.
    Response:
        True
    Reasoning:
        The user is again describing a dream they had, so the response is True.
        
    USER TEXT:
    ```
    {}
    ```
    """
    res = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": dream_check_prompt.format(text)
            }
        ],
        response_format=IsDream
    )
    print(f"choice = {res.choices[0].message.parsed.is_dream}")
    return res.choices[0].message.parsed.is_dream
