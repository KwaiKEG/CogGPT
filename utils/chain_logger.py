import sys
import time


ACTION_TEXTS = {
    "search": "搜索:",
    "observation": "我发现:",
    "click": "点击:",
    "execute": "执行:",
    "thinking": "思考中...",
    "thought": "想法:",
    "reading": "阅读中...",
    "reason": "理由:",
    "finish": "结束",
    "conclusion": "总结中...",
    "fail": "失败",
    "chain_end": "",
}

ACTION_TEXTS_EN = {
    "search": "search:",
    "observation": "observation:",
    "click": "click:",
    "execute": "execute:",
    "thinking": "thinking...",
    "thought": "thought:",
    "reading": "reading...",
    "reason": "reason:",
    "finish": "finish",
    "conclusion": "concluding...",
    "fail": "fail",
    "chain_end": "",
}

ACTION_ICONS = {
    "search": "🔍",
    "click": "🖱️",
    "thinking": "🤔",
    "reason": "⭐️",
    "execute": "🚀",
    "thought": "💡",
    "reading": "📖",
    "finish": "✅",
    "observation": "🔭",
    "conclusion": "💬",
    "fail": "🤦",
    "chain_end": ""
}

COLORS = [
    "\033[91m\033[1m{}\033[0m\033[0m",
    "\033[92m\033[1m{}\033[0m\033[0m",
    "\033[93m\033[1m{}\033[0m\033[0m",
    "\033[94m\033[1m{}\033[0m\033[0m",
    "\033[95m\033[1m{}\033[0m\033[0m",
    "\033[96m\033[1m{}\033[0m\033[0m",
    "\033[97m\033[1m{}\033[0m\033[0m",
    "\033[98m\033[1m{}\033[0m\033[0m"
] * 100
ACTION_COLORED_TEXTS = {
    key: COLORS[idx].format(val)
    for idx, (key, val) in enumerate(ACTION_TEXTS.items())
}
ACTION_COLORED_TEXTS_EN = {
    key: COLORS[idx].format(val)
    for idx, (key, val) in enumerate(ACTION_TEXTS_EN.items())
}

class ChainMessageLogger(object):
    def __init__(self, output_streams=[sys.stdout], lang="en"):
        self.chain_msgs = list()
        self.chain_msgs_str = ""
        self.output_streams = output_streams
        self.llm_prompt_responses = list()
        self.last_time = time.time()
        self.lang = lang

    def __str__(self):
        s = "output stream list: {}".format([str(t) for t in self.output_streams])
        return s

    def cut_text_into_short(self, long_text: str):
        return long_text.strip()[:100]

    def put_prompt_response(self, prompt: str, response: str, session_id: str, mtype: str, llm_name: str):
        self.llm_prompt_responses.append({
            "prompt": prompt,
            "response": response,
            "session_id": session_id,
            "type": mtype,
            "llm_name": llm_name
        })

    def put(self, action: str, text: str = ""):
        text = str(text)
        chain_msg = {
            "index": len(self.chain_msgs),
            "action": action,
            "text": text,
            "short_text": self.cut_text_into_short(text),
            "finish_time": time.time()
        }
        self.chain_msgs.append(chain_msg)

        action = chain_msg["action"]
        icon = ACTION_ICONS[action]


        if self.lang == "zh":
            action_text = ACTION_TEXTS[action]
            colored_action_text = ACTION_COLORED_TEXTS[action]
        else:
            action_text = ACTION_TEXTS_EN[action]
            colored_action_text = ACTION_COLORED_TEXTS_EN[action]

        text = chain_msg["text"]
        chain_string= f"{icon} {action_text} {text}\n"
        duration = "{:.3f}s".format(chain_msg["finish_time"] - self.last_time)
        self.last_time = chain_msg["finish_time"]
        colored_chain_string = f"{icon} {colored_action_text} {text}\n"
        # colored_chain_string = f"{icon} {colored_action_text} {text}\nexecution duration: {duration}\n"

        for os in self.output_streams:
            os.write(colored_chain_string)
        self.chain_msgs_str += chain_string

    def info(self, text: str):
        text = "{}".format(text)
        for os in self.output_streams:
            os.write(text)

    def clear(self):
        del self.chain_msgs
        del self.llm_prompt_responses
        self.chain_msgs = list()
        self.chain_msgs_str = ""
        self.llm_prompt_responses = list()