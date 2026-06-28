function ChatMessage({ sender, text }) {

    const isUser = sender === "user";

    return (

        <div
            className={`flex ${
                isUser ? "justify-end" : "justify-start"
            }`}
        >

            <div
                className={`max-w-[75%] rounded-2xl px-5 py-3 text-sm shadow

                ${
                    isUser
                        ? "bg-blue-600 text-white"
                        : "bg-white border"
                }`}
            >

                {text}

            </div>

        </div>

    );

}

export default ChatMessage;