import requests

def call_llm(prompt, temperature=0.1):
    response = requests.post(
        'http://localhost:11434/api/generate',
        json={
            'model': 'qwen3:8b',
            'prompt': prompt,
            'temperature': temperature,
            'stream': False
        }
    ).json()
    answer = response['response']
    total_duration = response['total_duration']
    total_duration = round(total_duration/(10**9),2)
    eval_count = response['eval_count']
    eval_duration = response['eval_duration']
    eval_duration = round(eval_duration/(10**9),2)
    return answer, total_duration, round(eval_count/eval_duration, 2)

if __name__ == '__main__':
    prompt = '你好，请问你是什么模型？'
    answer, duration, tps = call_llm(prompt)
    print(answer)
    print(duration)
    print(tps)