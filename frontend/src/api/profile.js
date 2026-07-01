import client from "./client";

let profileCache = null;
let profilePromise = null;

/**
 * Fetches the authenticated user's profile data.
 * Implements in-memory caching, request deduplication, and structured error handling.
 *
 * @param {Object} [options={}] - Options for profile retrieval
 * @param {boolean} [options.forceRefresh=false] - If true, ignores cached data and fetches fresh profile
 * @param {number|string} [options.userId=null] - Optional specific user ID to query
 * @returns {Promise<Object>} User profile JSON payload
 */
export async function getProfile({ forceRefresh = false, userId = null } = {}) {
  const endpoint = userId ? `/profile/${userId}` : "/profile";

  // Return cached profile if available and refresh is not requested
  if (!userId && !forceRefresh && profileCache) {
    return profileCache;
  }

  // Deduplicate concurrent requests for the current user profile
  if (!userId && !forceRefresh && profilePromise) {
    return profilePromise;
  }

  const fetchRequest = (async () => {
    try {
      const response = await client.get(endpoint);
      if (!userId) {
        profileCache = response.data;
      }
      return response.data;
    } catch (error) {
      const errorMessage =
        error.response?.data?.detail ||
        error.response?.data?.message ||
        error.message ||
        "Failed to retrieve user profile data.";
      const enhancedError = new Error(errorMessage);
      enhancedError.status = error.response?.status;
      enhancedError.originalError = error;
      throw enhancedError;
    } finally {
      if (!userId) {
        profilePromise = null;
      }
    }
  })();

  if (!userId && !forceRefresh) {
    profilePromise = fetchRequest;
  }

  return fetchRequest;
}

/**
 * Updates the authenticated user's profile metadata.
 * Automatically synchronizes the local profile cache upon success.
 *
 * @param {Object} profileData - Key-value payload of profile attributes to update
 * @returns {Promise<Object>} Updated profile JSON payload
 */
export async function updateProfile(profileData) {
  try {
    const response = await client.put("/profile", profileData);
    profileCache = response.data;
    return response.data;
  } catch (error) {
    const errorMessage =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      error.message ||
      "Failed to update user profile.";
    const enhancedError = new Error(errorMessage);
    enhancedError.status = error.response?.status;
    throw enhancedError;
  }
}

/**
 * Clears the in-memory profile cache and any pending requests.
 * Should be called upon user logout or session termination.
 */
export function clearProfileCache() {
  profileCache = null;
  profilePromise = null;
}