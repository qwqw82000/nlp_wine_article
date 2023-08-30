import openai


def generate_text(prompt, model, key, max_tokens=100,):
    openai.api_key = key # OpenAI API 키 입력
    # OpenAI API를 사용하여 prompt를 전달하여 생성된 텍스트 반환
    response = openai.Completion.create(
      engine=model,
      prompt=prompt,
      max_tokens=max_tokens
    )
    text = response.choices[0].text
    with open("wine_article_result.txt", "w", encoding="utf-8") as file:
        file.write(text)
    return text