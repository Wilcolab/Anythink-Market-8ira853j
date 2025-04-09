import React, { useState, useEffect } from 'react';
import { format } from 'date-fns';

interface Router {
    id: string;
    name: string;
    type: string;
    updatedAt: string;
}

const RouterList: React.FC = () => {
    const [routers, setRouters] = useState<Router[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchRouters = async () => {
            try {
                const response = await fetch('https://friendly-space-eureka-vppjxv44p63xrvp-3001.app.github.dev/routers');

                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                const data = await response.json();
                setRouters(data);
                setLoading(false);
            } catch (err) {
                setError(`Failed to fetch routers: ${err instanceof Error ? err.message : 'Unknown error'}`);
                setLoading(false);
            }
        };

        fetchRouters();
    }, []);

    const formatDate = (dateString: string) => {
        try {
            return format(new Date(dateString), 'MMM dd, yyyy, h:mm a');
        } catch (e) {
            return 'Invalid date';
        }
    };

    if (loading) {
        return (
            <div className="router-list-container">
                <div className="loading-spinner">Loading...</div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="router-list-container">
                <div className="error-message">
                    <h3>Error</h3>
                    <p>{error}</p>
                    <button onClick={() => window.location.reload()}>Try Again</button>
                </div>
            </div>
        );
    }

    return (
        <div className="router-list-container">
            <h2>Network Routers</h2>
            {routers.length === 0 ? (
                <p>No routers found</p>
            ) : (
                <ul className="router-list">
                    {routers.map((router) => (
                        <li key={router.id} className="router-item">
                            <div className="router-details">
                                <h3 className="router-name">{router.name}</h3>
                                <span className="router-type">Type: {router.type}</span>
                                <span className="router-updated">Last Updated: {formatDate(router.updatedAt)}</span>
                            </div>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default RouterList;