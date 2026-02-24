const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"

// Helper function to make authenticated API requests
export async function fetchWithAuth(endpoint, getToken, options={}) {
    const token = await getToken()

    // If no token is available, throw an error
    const response = await fetch(
        `${API_URL}${endpoint}`,
        {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
                ...options.headers
            }
        }
    )
// If the response is not OK, try to parse the error message and throw it
    if (!response.ok) {
        const error = await response.json().catch(() => {})
        throw new Error(error.detail || "Request failed")
    }

    if (response.status === 204) {
        return null
    }

    return response.json()
}
// API functions for tasks
export async function getTasks(getToken) {
    return fetchWithAuth("/api/task", getToken)
}

export async function createTask(getToken, task) {
    return fetchWithAuth("/api/task", getToken, {
        method: "POST",
        body: JSON.stringify(task)
    })
}

export async function updateTask(getToken, taskId, task) {
    return fetchWithAuth(`/api/task/${taskId}`, getToken, {
        method: "PUT",
        body: JSON.stringify(task)
    })
}

export async function deleteTask(getToken, taskId) {
    return fetchWithAuth(`/api/task/${taskId}`, getToken, {
        method: "DELETE"
    })
}