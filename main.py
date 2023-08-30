import function # 기능 모듈
import article_Ai



def main():
    text = function.read_file(text_Route = "wine_text.txt") # 텍스트 데이터 전처리
    keywords = function.extract_keywords(text,n_keywords = 5) # 상위 5개 데이터 추출
    prompt = f"{keywords} \n Write an informative and informative article using the elements of the list"
    openai_api_key = "" # 키를 수정하세요!
    generated_text = article_Ai.generate_text(prompt, 'text-davinci-002',openai_api_key, 200)# generate_text() 함수를 사용하여 기사 생성
    print("추출한 키워드는 : ",keywords)
    print("생성한 기사는 : ",generated_text)

main()
