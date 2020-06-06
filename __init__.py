from mycroft.skills.core import MycroftSkill, intent_file_handler
import requests


class ChatScript(MycroftSkill):
    chatting = False

    @intent_file_handler("start_parrot.intent")
    def handle_start_parrot_intent(self, message):
        self.chatting = True
        self.speak_dialog("chat_start", expect_response=True)

    @intent_file_handler("stop_parrot.intent")
    def handle_stop_parrot_intent(self, message):
        if self.chatting:
            self.chatting = False
            self.speak_dialog("chat_stop")
        else:
            self.speak_dialog("not_chatting")

    def stop(self):
        if self.chatting:
            self.chatting = False
            self.speak_dialog("chat_stop")
            return True
        return False

    def converse(self, utterances, lang="en-us"):
        if self.chatting:
            # check if stop intent will trigger
            if self.voc_match(utterances[0], "StopKeyword") and self.voc_match(utterances[0], "ChatKeyword"):
                return False

            # Variables for the payload
            # url = "http://productionlb003-460876522.us-east-1.elb.amazonaws.com/BETTER/ui.php"
            url = "http://localhost:1024/SIMPLE/index.php"
            user = 'Winston'
            # utterance = message.data.get('utterance')
            utterance = utterances

            # Constructing the payload
            # data = {user + '|' + utterance}
            data = {'user': user, 'send': '', 'message': utterance}
            print(data)

            # Initiating a POST request
            post = requests.post(url, data=data)
            self.speak(post.text, expect_response=True)
            return True
        else:
            return False


def create_skill():
    return ChatScript()
