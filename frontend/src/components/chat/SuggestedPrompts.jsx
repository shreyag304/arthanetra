function SuggestedPrompts({ onPromptClick })  {

    const prompts = [

        "Help me create a monthly budget",

        "Check if this loan is safe",

        "Find government schemes",

        "Improve my Financial Health Score"

    ];

    return (

        <div className="border-t bg-white px-4 py-3">

            <div className="flex flex-wrap gap-3">

                {prompts.map((prompt) => (
                    
    <button
       key={prompt}
       onClick={() => onPromptClick(prompt)}
       className="rounded-full border px-4 py-2 text-sm hover:bg-blue-50 hover:border-blue-500 transition"
   >


        {prompt}
    </button>
))}

            </div>

        </div>

    );

}

export default SuggestedPrompts;