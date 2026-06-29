import { useState } from "react";
import { useNavigate } from "react-router-dom";
import LanguageSelector from "../components/chat/LanguageSelector";
function Login() {

    const navigate = useNavigate();
    const [language, setLanguage] = useState(
  localStorage.getItem("language") || "English"
);

    function handleLogin() {

        // Temporary login
         localStorage.setItem("language", language);

        navigate("/workspace");
       
    }
   

    return (

        <div className="min-h-screen bg-slate-100 flex items-center justify-center p-6">

            <div className="bg-white rounded-3xl shadow-xl w-full max-w-md p-10">

                <h1 className="text-4xl font-bold text-center text-blue-700">

                    ArthaNetra

                </h1>

                <p className="text-center text-gray-500 mt-3">

                    AI Financial Assistant for Everyone

                </p>
                <div className="mt-6">
  <label className="font-medium">
    Select Language
  </label>

  <div className="mt-2">
    <LanguageSelector
      language={language}
      setLanguage={setLanguage}
    />
  </div>
</div>

                <div className="mt-10">

                    <label className="font-medium">

                        Mobile Number

                    </label>

                    <input

                        type="tel"

                        placeholder="Enter mobile number"

                        className="w-full border rounded-xl p-4 mt-2"

                    />

                </div>

                <button

                    onClick={handleLogin}

                    className="w-full bg-blue-700 hover:bg-blue-800 text-white rounded-xl py-4 mt-8 font-semibold"

                >

                    Continue

                </button>

                <div className="mt-8 text-center text-sm text-gray-400">

                    Secure • Multilingual • AI Powered

                </div>

            </div>

        </div>

    );

}

export default Login;