import openai


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