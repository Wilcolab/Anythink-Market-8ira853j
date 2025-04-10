// Router data types
export interface BaseRouter {
    id: string;
    name: string;
    model: string;
    manufacturer: string;
    ipAddress: string;
    status: string;
    type: 'wifi' | 'enterprise' | 'home';
    updatedAt: string; // Add the missing updatedAt property
}

export interface WiFiRouter extends BaseRouter {
    type: 'wifi';
    wifiChannels: number[];
    dualBandSupport: boolean;
}

export interface EnterpriseRouter extends BaseRouter {
    type: 'enterprise';
    portCount: number;
    supportedProtocols: string[];
    throughput: number; // in Gbps
}

export interface HomeRouter extends BaseRouter {
    type: 'home';
    connectedDevices: number;
    parentalControls: boolean;
    maxBandwidth: number; // in Mbps
}

export type Router = WiFiRouter | EnterpriseRouter | HomeRouter;

// Instead of duplicating mock data, use a shared data store
let routersCache: Router[] = [];

// Service methods
export const fetchRouters = (): Promise<Router[]> => {
    // Fetch from API or use existing mock fetch code from your app
    return fetch('/api/routers')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Cache the results for later use
            routersCache = data;
            return data;
        })
        .catch(error => {
            console.error('Error fetching routers:', error);
            // Fall back to previously cached data if available
            if (routersCache.length > 0) {
                return routersCache;
            }
            throw error;
        });
};

export const fetchRouterById = (id: string): Promise<Router> => {
    // Check cache first if available
    if (routersCache.length > 0) {
        const router = routersCache.find(r => r.id === id);
        if (router) {
            return Promise.resolve(router);
        }
    }

    // Otherwise fetch directly
    return fetch(`/api/routers/${id}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .catch(error => {
            console.error(`Error fetching router with id ${id}:`, error);
            throw error;
        });
};

// Type guard functions
export const isWiFiRouter = (router: Router): router is WiFiRouter => {
    return router.type === 'wifi';
};

export const isEnterpriseRouter = (router: Router): router is EnterpriseRouter => {
    return router.type === 'enterprise';
};

export const isHomeRouter = (router: Router): router is HomeRouter => {
    return router.type === 'home';
};
