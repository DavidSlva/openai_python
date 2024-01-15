import uuid
from openai import OpenAI
import json
from libs.mongo.models import store_conversation, ChatConversation
class OpenAIChatManager:

    def __init__(self, api_key, store_in_mongo = False):
        """
        Constructor de la clase.
        :param api_key: Clave de API para autenticar las solicitudes a OpenAI.
        Inicializa un cliente de OpenAI con la clave de API proporcionada y
        crea un diccionario `user_contexts` para almacenar los contextos de los usuarios.
        """
        self.client = OpenAI(api_key=api_key)
        self.user_contexts =  ChatConversation.retrieve_all_conversations()
        self.tools = []  # Aquí se almacenan las funciones
        self.functions = {}
        self.store_in_db = store_in_mongo

    def add_tool(self, tool):
        """
        Añade una función al contexto del bot.
        :param tool: Un diccionario que representa la tool a añadir.
        """
        if tool.get("type") == "function":
            print("Función añadida")
            self.tools.append(tool)
        else:
            raise ValueError("The object is not a valid function")
        
    def add_function(self, name, func):
        """
        Añade una función al diccionario de funciones disponibles para ser llamadas.
        
        :param name: El nombre bajo el cual se registrará la función.
        :param func: La función a registrar. Debe ser un objeto de función.
        """
        self.functions[name] = func

    def execute_function_call(self, message, user_id, send_result_to_openai=False):
        """
        Ejecuta una función basada en una llamada de mensaje y opcionalmente envía el resultado a OpenAI para obtener una respuesta.
        
        :param message: Un diccionario que representa el mensaje entrante que puede contener una llamada a la función.
        :param user_id: El identificador del usuario para el que se está ejecutando la función. Necesario para mantener el contexto en la conversación.
        :param send_result_to_openai: Un booleano que determina si el resultado de la función se envía a OpenAI para generar una respuesta basada en él.
        :return: El resultado de la función llamada o una respuesta de OpenAI, dependiendo del valor de 'send_result_to_openai'.
        """

        if hasattr(message, 'tool_calls') and message.tool_calls is not None:
            for tool_call in message.tool_calls:
                print("\n##############################TOOL CALL####################\n")
                print(tool_call)
                print("\n##############################TOOL CALL####################\n")
                if tool_call.type == "function":
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    if function_name in self.functions:
                        results = self.functions[function_name](**function_args)
                        self._add_tool_message(tool_call, results, user_id)
                    else:
                        print(f"Error: function {function_name} does not exist")
                        return None
        else:
            print("No function call found in the message")
            return message
        



    def create_user(self, userId=None):
        """
        Crea o utiliza un identificador de usuario.
        Si se proporciona un userId, se usa ese. Si no, se crea uno nuevo.
        :param userId: Identificador de usuario opcional.
        :return: El identificador de usuario.
        """
        # Usa userId proporcionado o genera uno nuevo si es None
        user_id = userId if userId else str(uuid.uuid4())
        
        self.user_contexts[user_id] = []
        store_conversation(user_id, [])
        print(f"USUARIO CREADO {user_id}")
        return user_id


    def add_message(self, user_id, message):
        if user_id in self.user_contexts:
            # Clona la lista de mensajes antes de modificarla
            messages = list(self.user_contexts[user_id])
            messages.append({"role": "user", "content": message})

            self.user_contexts[user_id] = messages
            store_conversation(user_id, [{"role": "user", "content": message}])
        else:
            raise ValueError("User not found")
        
    def _add_tool_message(self, tool_message, content, user_id):
        print(f"Tool {tool_message}  CONTENT {content} USERID {user_id}")
        tool_call_id = tool_message.id
        name = tool_message.function.name
                 
        store_conversation(user_id, [{"role": "tool", "tool_call_id": tool_call_id, "name": name, "content": content}])
        # self.user_contexts[user_id].append({"role": "tool", "tool_call_id": tool_call_id, "name": name, "content": content})
    # def add_db_message(self, user_id, message):
    #     store_conversation(user_id, messages)

    def serialize_tool_calls(self, tool_call):
            return {
                "id": tool_call.id,
                "function": {
                    "name": tool_call.function.name,
                    "arguments": tool_call.function.arguments
                },
                "type": tool_call.type
            }

    def get_response(self, user_id):
        """
        Obtiene la respuesta del asistente para un usuario específico.
        :param user_id: El identificador del usuario.
        :return: El contenido de la respuesta del asistente.
        Si el usuario no existe, se lanza un error `ValueError`.
        Esta función llama al método de completions de OpenAI, pasando el contexto actual del usuario.
        La respuesta obtenida se agrega al contexto del usuario y luego se devuelve.
        """
        if user_id not in self.user_contexts:
            raise ValueError("User not found")
        conversation = ChatConversation.retrieve_conversation(user_id)
        # print(conversation)
        response = self.client.chat.completions.create(
            # model="ft:gpt-3.5-turbo-1106:personal::8V1SG1IO",
            model="gpt-4",
            messages=conversation,
            tools=self.tools
        )
        message = response.choices[0].message
        if message.tool_calls is not None:
            # Serializa cada tool_call antes de almacenarlo
            # message.tool_calls[0].model_json_schema()
            serialized_tool_calls = [self.serialize_tool_calls(tc) for tc in message.tool_calls]
            print(f"SERIALIZADO {serialized_tool_calls}")
            store_conversation(user_id, [{"role": message.role, "content": message.content, "tool_calls": serialized_tool_calls}])
        else:
            store_conversation(user_id, [{"role": message.role, "content": message.content}])
        # store_conversation(user_id, [{"role": "user", "content": message}])
        
        # print(f"ANTES: {message.content}")
        # message.content = str(message.tool_calls[0].function)
        # print(f"DESPUES: {message.content}")


        result = self.execute_function_call(message, user_id)
        result = None
        if result is None:
            response_content = message.content
            self.user_contexts[user_id].append({"role": "assistant", "content": response_content})
            return response_content
        else:
            return result
        
        
