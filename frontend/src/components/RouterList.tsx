import React, { useState, useEffect } from 'react';
import { format } from 'date-fns';
import agent from '../agent';
import './RouterList.css';

// Define interface for router data structure
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
        const fetchRouters = async (): Promise<void> => {
            try {
                setLoading(true);
                const response = await agent.Routers.getAll();
                setRouters(response);
                setError(null);
            } catch (err) {
                console.error('Failed to fetch routers:', err);
                setError('Failed to load routers. Please try again later.');
            } finally {
                setLoading(false);
            }
        };

        fetchRouters();
    }, []);

    // Format timestamp to a readable format
    const formatTimestamp = (timestamp: string): string => {
        if (!timestamp) return 'N/A';
        try {
            return format(new Date(timestamp), 'MMM dd, yyyy HH:mm');
        } catch (e) {
            return 'Invalid date';
        }
    };

    if (loading) {
        return <div className="router-list-loading">Loading routers...</div>;
    }

    if (error) {
        return <div className="router-list-error">{error}</div>;
    }

    return (
        <div className="router-list-container">
            <h2>Router List</h2>
            {!routers || routers.length === 0 ? (
                <p>No routers found</p>
            ) : (
                <ul className="router-list">
                    {routers.map((router) => (
                        <li key={router?.id || Math.random().toString()} className="router-item">
                            <div className="router-name">
                                <strong>Name:</strong> {router?.name || 'Unnamed Router'}
                            </div>
                            <div className="router-type">
                                <strong>Type:</strong> {router?.type || 'Unspecified'}
                            </div>
                            <div className="router-updated">
                                <strong>Last Updated:</strong> {formatTimestamp(router?.updatedAt)}
                            </div>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default RouterList;
