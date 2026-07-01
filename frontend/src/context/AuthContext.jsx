import { createContext, useState, useEffect, useCallback } from "react";
import { getProfile, clearProfileCache } from "../api/profile";

export const AuthContext = createContext();

function AuthProvider({ children }) {
    const [user, setUser] = useState(() => {
        const storedId = localStorage.getItem("user_id");
        return storedId ? { id: Number(storedId) } : null;
    });
    const [isLoadingProfile, setIsLoadingProfile] = useState(false);

    const fetchUserProfile = useCallback(async (forceRefresh = false) => {
        const storedId = localStorage.getItem("user_id");
        if (!storedId) return null;
        setIsLoadingProfile(true);
        try {
            const profileData = await getProfile({ forceRefresh, userId: storedId });
            setUser((prev) => ({ ...prev, ...profileData }));
            return profileData;
        } catch (error) {
            console.warn("Unable to fetch user profile:", error.message);
            return null;
        } finally {
            setIsLoadingProfile(false);
        }
    }, []);

    useEffect(() => {
        if (localStorage.getItem("user_id")) {
            fetchUserProfile();
        }
    }, [fetchUserProfile]);

    const login = (userData) => {
        setUser(userData);
        if (userData?.id || userData?.user_id) {
            localStorage.setItem("user_id", userData.id || userData.user_id);
        }
    };

    const logout = () => {
        setUser(null);
        localStorage.removeItem("user_id");
        localStorage.removeItem("token");
        clearProfileCache();
    };

    return (
        <AuthContext.Provider
            value={{
                user,
                isLoadingProfile,
                login,
                logout,
                refreshProfile: () => fetchUserProfile(true),
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}

export default AuthProvider;