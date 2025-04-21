import React, { useEffect, useState } from 'react';
import './RouterList.css';

interface Router {
    id: string;
    name: string;
    type: 'wifi' | 'enterprise' | 'home';
    updatedAt: string;
}

export const RouterList: React.FC = () => {
    const [routers, setRouters] = useState<Router[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchRouters = async () => {
            try {
                const response = await fetch(`${process.env.REACT_APP_CODESPACE_BACKEND_URL}/routers`);
                if (!response.ok) {
                    throw new Error('Failed to fetch routers');
                }
                const data = await response.json();
                setRouters(data);
            } catch (err) {
                setError(err instanceof Error ? err.message : 'An error occurred');
            } finally {
                setLoading(false);
            }
        };

        fetchRouters();
    }, []);

    if (loading) {
        return (
            <div className="router-list-container">
                <div className="loading">Loading routers...</div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="router-list-container">
                <div className="error">Error: {error}</div>
            </div>
        );
    }

    return (
        <div className="router-list-container">
            <h2>Routers</h2>
            <div className="router-list">
                {routers.map((router) => (
                    <div key={router.id} className="router-item">
                        <h3>{router.name}</h3>
                        <div className="router-details">
                            <span className="router-type">Type: {router.type}</span>
                            <span className="router-update">
                                Last Updated: {new Date(router.updatedAt).toLocaleString()}
                            </span>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};