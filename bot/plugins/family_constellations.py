from plugin import Plugin

class FamilyConstellationsPlugin(Plugin):
    """
    A custom plugin that modifies the assistant's behavior based on predefined commands.
    """

    PROMPTS = {
        "family_constellations": (
            "Ты действуешь как Системный Расстановщик по Берту Хеллингеру, духовный учитель и отвечаешь на вопросы. "
            "Отвечай нормальным человеческим языком, по стилю будь легким в ответах. "
            "Обращайся к собеседнику на ты. "
            "Отвечай в контексте системных расстановок."
        )
    }

    def __init__(self):
        super().__init__()  # Removed undefined `config`
        self.current_mode = None  # Consistently track active mode

    def get_source_name(self) -> str:
        return "FamilyConstellationsPlugin"

    def get_spec(self):
        return [
            {
                "name": "set_preset_mode",
                "description": "Switch ChatGPT to a predefined conversation mode.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "mode": {
                            "type": "string",
                            "enum": list(self.PROMPTS.keys()),  # Ensure consistency
                            "description": "The mode to activate family constellations mode in ChatGPT."
                        }
                    },
                    "required": ["mode"]
                }
            }
        ]

    def set_preset_mode(self, mode):
        if mode in self.PROMPTS:
            self.current_mode = mode
            return {"status": "success", "message": f"Switched to {mode} mode."}
        return {"status": "error", "message": f"Mode {mode} not supported."}

    def modify_prompt(self, user_message):
        """Modifies the prompt based on the selected mode."""
        if self.current_mode in self.PROMPTS:
            return [
                {"role": "system", "content": self.PROMPTS[self.current_mode]},
                {"role": "user", "content": user_message}
            ]
        return [{"role": "user", "content": user_message}]

    def process_message(self, user_message, openai_helper):
        """Processes the message using OpenAI with the adjusted prompt."""
        messages = self.modify_prompt(user_message)
        response = openai_helper.chat_completion(messages)
        return response

    async def execute(self, function_name, helper, **kwargs):
        if function_name == "set_preset_mode":
            mode = kwargs.get("mode")
            return self.set_preset_mode(mode)
        return {"status": "error", "message": "Unknown function"}
