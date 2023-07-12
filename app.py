import subprocess
import sys

def update_pip():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

def install_package(package):
    try:
        subprocess.check_output([sys.executable, "-m", "pip", "show", package])
    except subprocess.CalledProcessError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

update_pip()
required_packages = ["openai", "gradio"]
for package in required_packages:
    install_package(package)
    
import openai 
import gradio 

openai.api_key = "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"

start_sequence = "\nAI: "
restart_sequence = "\nHuman: " 

prompt = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: "
# 함수 - 모델 
def openai_create(prompt):
    # 모델 불러오기
    response = openai.Completion.create(
        model = "text-davinci-003",
        prompt = prompt,
        temperature = 0.9,
        max_tokens = 150,
        top_p = 1,
        frequency_penalty = 0, # 대화 문맥에서 많이 언급된 부분을 나오게 할지 알려주는 속성값 : 빈도
        presence_penalty = 0.6,
        stop = ["Human:", " AI:"] # stop 옵션 - 답변을 할때 원하는 답변이 아니면 멈추는 것
    )
    #예측 하는 모델
    return response.choices[0].text

#함수 - 입력들을 관리하고 이것들을 예측값을 다시 받아오는 것
def chatgpt_clone(input, history):  # input : 새로입력한 , history : 전 gpt 대화
    history = history or [] # history의 내용이 있으면 []에 값을 넣고 리스트로 만들어라
    s = list(sum(history, ())) # 한문자, 한배열로 만들어준다
    s.append(input) # 리스트를 문자로 보여주는 것
     # ["a", "b", "c"]
     # "a b c"
    inp = ' '.join(s)
    output = openai_create(inp)
    history.append((input, output))
    print(input, output, history)
    return history, history


block = gradio.Blocks() # 변수 관리

 # 직접적인 실행
with block:
    gradio.Markdown("""<h1><center>나만의 GPT 챗봇</center></h1>""") # 페이지 텍스트
    chatbot = gradio.Chatbot() # UI할당
    message = gradio.Textbox(placeholder=prompt)
    state = gradio.State()
    submit = gradio.Button("SEND") # 버튼 생성
    submit.click(chatgpt_clone, inputs=[message, state], outputs=[chatbot, state]) # 버튼이 눌렸을 때


block.launch(debug=True)

# block.launch(share=True)