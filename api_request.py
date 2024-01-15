import uuid
from openai import OpenAI
from libs.OpenAIManager import OpenAIChatManager



api_key = "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"

chat_manager = OpenAIChatManager(api_key=api_key)
asistente_hipotecario = OpenAIChatManager(api_key=api_key)

# user_id = chat_manager.create_user()

def sumar2(number1, number2):
    return f'La suma mala de {number1} y {number2} es : {number1*number2}'

chat_manager.add_function("sumarmaldosnumeros", lambda numero1, numero2: sumar2(numero1, numero2))



chat_manager.add_tool({
    "type": "function",
    "function": {
        "name": "sumarmaldosnumeros",
        "description": "Sumar mal dos números, el usuario debe definir claramente cuál es el numero 1  y el número 2, no se debe inferir qué números se deben sumar mal.",
        "parameters": {
            "type": "object",
            "properties": {
                "numero1": {
                    "type": "number",
                    "description": "Es el primer número que se debe sumar mal, el usuario debe señalar qué número se debe ingresar, no se debe inferir.",
                },
                "numero2": {
                    "type": "number",
                    "description": "Es el segúndonúmer que se debe sumar mal, el usuario debe señalar qué número se debe ingresar, no se debe inferir.",
                },
            },
            "required": ["numero1", "numero2"],
        },
    },
})

# print(user_id + ' User ID ')
# chat_manager.add_message(user_id, "Holaa, necesito que recuerdes que mi perrita se llama Moly")
# chat_manager.add_message(user_id, "Holaa, Cuál es el nombre de mi perrita?")
# response = chat_manager.get_response(user_id)
# print(response)
# other_id = chat_manager.create_user()
# chat_manager.add_message(other_id, "Holaa, cuál es mi nombre?")
# response = chat_manager.get_response(other_id)
# print(response)
# chat_manager.add_message('071323e1-46e7-4a4b-b489-3e1623dd6840', "Cuál es el nombre de mi perrita?")
# mollyResponse = chat_manager.get_response('071323e1-46e7-4a4b-b489-3e1623dd6840')
# print(mollyResponse)



print(f'############# FUNCTION CALLING #############')


# result = chat_manager.execute_function_call("Hola, necesito sumar mal el número 1 y el número 2", user_id, send_result_to_openai=True)
# chat_manager.add_message(user_id, "Necesito sumar mal dos números")

# print(f'Respuesta: {chat_manager.get_response(user_id)}')
# chat_manager.add_message(user_id, "Quiero sumar mal el 1 y el 2")
# print(f'Respuesta: {chat_manager.get_response(user_id)}')
# user_id = chat_manager.create_user()
# print(user_id)
david_user_id = '23a2d6f6-fd26-4709-bf44-88e44a369cf0'
chat_manager.create_user(david_user_id)
chat_manager.add_message(david_user_id, "Mi perrita se llama Molición")
mollyResponse = chat_manager.get_response(david_user_id)
print(f"PRIMERA RESPUESTA : {mollyResponse}")
chat_manager.add_message(david_user_id, "Cómo se llama mi perrita?")
mollyResponse = chat_manager.get_response(david_user_id)
print(mollyResponse, chat_manager.user_contexts[david_user_id])

chat_manager.add_message(david_user_id, "SABES COMO SE SUMA MAL DOS NÚMEROS?")
mollyResponse = chat_manager.get_response(david_user_id)
print(mollyResponse, chat_manager.user_contexts[david_user_id])

# mongodb+srv://davidslva:20419-0Dav@cluster0.0jplo1z.mongodb.net/
# mongodb+srv://davidslva:20419-0Dav@cluster0.0jplo1z.mongodb.net/