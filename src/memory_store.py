class MemoryStore:
    def __init__(self):
        self.history = []

    def update(self, user, ai):
        self.history.append({"user": user, "ai": ai})

    def get_context(self):
        context = ""
        for h in self.history[-3:]:
            context += f"User: {h['user']} | AI: {h['ai']}\n"
        return context
