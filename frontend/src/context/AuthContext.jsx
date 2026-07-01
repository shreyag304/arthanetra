import { createContext, useState } from "react";

export const AuthContext = createContext();

function AuthProvider({ children }) {

    const [user, setUser] = useState(null);

    const login = (userData) => {
        setUser(userData);
        localStorage.setItem("user_id" , userData.id)
    };

    const logout = () => {
        setUser(null);
    };

    return (
        <AuthContext.Provider
            value={{
                user,
                login,
                logout,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}

export default AuthProvider;