import openai


# 這個是所有訊息可以共用的 ChatCompletion 的呼叫函式
def get_completion_from_messages(messages,
        model="gpt-3.5-turbo",  # 語言模型
        temperature=0,  # 回應溫度
        max_tokens=500, # 最大的 token 數
        verbose=False, # 是否顯示除錯除錯訊息
        ):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    if verbose:
        print(response)
    return response.choices[0].message["content"]


def is_moderation_check_passed(checking_text, verbose=False):
    """
    檢查輸入的 checking_text 是否通過合適性檢查。
    我們先簡單有任何不合適跡象的訊息都判斷為不合適
    """
    response = openai.Moderation.create(
        input=checking_text
    )

    moderation_result = response["results"][0]

    if verbose:
        print(f'Moderation result: {moderation_result}')

    if moderation_result['flagged'] == True:
        return False
    elif moderation_result['categories']['sexual'] == True or   \
        moderation_result['categories']['hate'] == True or  \
        moderation_result['categories']['harassment'] == True or   \
        moderation_result['categories']['self-harm'] == True or   \
        moderation_result['categories']['sexual/minors'] == True or    \
        moderation_result['categories']['hate/threatening'] == True:
        return False

    return True


def moderation_warning_prompt(user_message):
    """
    這裏是專門對不合適訊息，進行回覆的地方
    """
    messages = [
        {
            'role':'system',
            'content': f"下方使用者訊息應該已經違反我們的使用規範，請使用和緩的口氣，跟使用這說明它已經違反我們的規劃所以無法繼續使用。"
        },
        user_message
    ]

    ai_response = get_completion_from_messages(messages)

    return ai_response