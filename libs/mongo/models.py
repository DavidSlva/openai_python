from mongoengine import Document, StringField, connect, ListField, DoesNotExist


# Paso 1: Definición del Modelo
class ChatConversation(Document):
    user_id = StringField(required=True)
    messages = ListField(StringField())
    def connect_db():
        connect(host="mongodb+srv://davidslva:20419-0Dav@cluster0.0jplo1z.mongodb.net/gpt_conversations")

    @staticmethod
    def retrieve_conversation(user_id):
        ChatConversation.connect_db()

        try:
            # Busca la conversación por user_id
            conversation = ChatConversation.objects.get(user_id=user_id)
            # print(f"Conversación {conversation.messages} del id {user_id}")
            return conversation.messages
        except DoesNotExist:
            # Si no existe, devuelve una lista vacía
            return []
    @staticmethod
    def retrieve_all_conversations():
        ChatConversation.connect_db()

        # Recupera todas las conversaciones
        # Recupera todas las conversaciones
        all_conversations = ChatConversation.objects()
        return {conv.user_id: conv.messages for conv in all_conversations}
    
def store_conversation(user_id, new_message):
    ChatConversation.connect_db()

    try:
        # Intenta encontrar un documento existente con el mismo user_id
        conversation = ChatConversation.objects.get(user_id=user_id)
        # Si existe, actualiza los mensajes
        conversation.update(push_all__messages=new_message)
    except DoesNotExist:
        # Si no existe, crea uno nuevo
        conversation = ChatConversation(user_id=user_id, messages=new_message)
        conversation.save()

