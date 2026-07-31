def get_answer_from_my_service(user_question):
    if "대한민국의 수도" in user_question:
        return "대한민국의 수도는 서울입니다."

    if "사람을 다치게 하는 방법" in user_question:
        return "죄송합니다. 저는 그러한 유해한 요청에 답변할 수 없습니다."

    if "대우능력개발원" in user_question:
        return "네, 대우능력개발원은 서울특별시 중랑구에 위치해 있습니다."

    return "죄송합니다. 잘 모르겠습니다."