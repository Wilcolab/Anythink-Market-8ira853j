import React, { useEffect, useState } from 'react';
import './RouterList.css';

interface Router {
    id: string;
    name: string;
    type: string;
    updatedAt: string;
}

const RouterList: React.FC = () => {
    const [routers, setRouters] = useState<Router[]>([]);
    const [isLoading, setIsLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchRouters = async () => {
            try {
                setIsLoading(true);
                const response = await fetch('/routers');

                if (!response.ok) {
                    throw new Error(`Error: ${response.status}`);
                }

                const data = await response.json();
                setRouters(data);
                setError(null);
            } catch (err) {
                setError('Failed to fetch router data');
                console.error(err);
            } finally {
                setIsLoading(false);
            }
        };

        fetchRouters();
    }, []);

    // Format date to a more readable format
    const formatDate = (dateString: string): string => {
        const date = new Date(dateString);
        return new Intl.DateTimeFormat('en-US', {
            year: 'numeric',
            month: 'short',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
        }).format(date);
    };

    if (isLoading) {
        return (
            <div className="router-list-loading">
                <div className="loading-spinner"></div>
                <p>Loading routers...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="router-list-error">
                <div className="error-icon">⚠️</div>
                <p>{error}</p>
                <button onClick={() => window.location.reload()}>Try Again</button>
            </div>
        );
    }

    return (
        <div className="router-list">
            <h2>Network Routers</h2>
            {routers.length === 0 ? (
                <p>No routers found.</p>
            ) : (
                <ul className="router-items">
                    {routers.map((router) => (
                        <li key={router.id} className="router-item">
                            <div className="router-name">{router.name}</div>
                            <div className="router-type">Type: {router.type}</div>
                            <div className="router-updated">
                                Updated: {formatDate(router.updatedAt)}
                            </div>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default RouterList;
