import superagentPromise from 'superagent-promise';
import _superagent from 'superagent';

const superagent = superagentPromise(_superagent, global.Promise);

// Determine the API base URL from environment variables
const getApiUrl = (): string => {
    // First check for Codespace backend URL
    if (process.env.REACT_APP_CODESPACE_BACKEND_URL) {
        return `${process.env.REACT_APP_CODESPACE_BACKEND_URL}`;
    }

    // Fall back to generic API root environment variable
    if (process.env.REACT_APP_API_ROOT) {
        return process.env.REACT_APP_API_ROOT;
    }

    // Default to environment variable with fallback
    return process.env.REACT_APP_API_URL || 'http://localhost:3001';
};

const API_ROOT = getApiUrl();

// Request helpers
const responseBody = (res: any) => res.body;

let token: string | null = null;
const tokenPlugin = (req: any) => {
    if (token) {
        req.set('authorization', `Token ${token}`);
    }
};

const requests = {
    del: (url: string) =>
        superagent.del(`${API_ROOT}${url}`).use(tokenPlugin).then(responseBody),
    get: (url: string) =>
        superagent.get(`${API_ROOT}${url}`).use(tokenPlugin).then(responseBody),
    put: (url: string, body: any) =>
        superagent.put(`${API_ROOT}${url}`, body).use(tokenPlugin).then(responseBody),
    post: (url: string, body: any) =>
        superagent.post(`${API_ROOT}${url}`, body).use(tokenPlugin).then(responseBody),
};

interface Router {
    id: string;
    name: string;
    type: string;
    updatedAt: string;
}

const Routers = {
    getAll: (): Promise<Router[]> => requests.get('/routers'),
};

const agent = {
    Routers,
    setToken: (_token: string) => { token = _token; }
};

export default agent;