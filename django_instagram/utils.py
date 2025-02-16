

def form_errors_to_string(form):
    """
    Django Form의 errors를 하나의 문자열로 변환하는 함수.
    
    :param form: Django Form 객체
    :return: 문자열 형태의 오류 메시지
    """
    return ", ".join([msg for msgs in form.errors.values() for msg in msgs])
