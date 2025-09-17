import React, { useState, useEffect } from 'react';
import RouterItem from './RouterItem';
import './RouterList.css';

export interface Router {
    id: string;
    name: string;
    type: string;
    createdAt: string;
    updatedAt: string;
    coordinates: {
        latitude: number;
        longitude: number;
    };
    // Type-specific fields
    wifiChannels?: number[];
    supportsDualBand?: boolean;
    portCount?: number;
    supportedProtocols?: string[];
    throughputGbps?: number;
    connectedDevices?: number;
    parentalControlsEnabled?: boolean;
    maxBandwidthMbps?: number;
}

const RouterList: React.FC = () => {
    const [routers, setRouters] = useState<Router[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchRouters = async () => {
            try {
                setLoading(true);
                setError(null);

                const response = await fetch(`${process.env.REACT_APP_CODESPACE_BACKEND_URL}/routers`);

                if (!response.ok) {
                    throw new Error(`Failed to fetch routers: ${response.status} ${response.statusText}`);
                }

                const data = await response.json();
                setRouters(data);
            } catch (err) {
                setError(err instanceof Error ? err.message : 'An unknown error occurred');
                console.error('Error fetching routers:', err);
            } finally {
                setLoading(false);
            }
        };

        fetchRouters();
    }, []);

    if (loading) {
        return (
            <div className="router-list-container">
                <div className="loading-state">
                    <div className="loading-spinner"></div>
                    <p>Loading routers...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="router-list-container">
                <div className="error-state">
                    <div className="error-icon">⚠️</div>
                    <h3>Error Loading Routers</h3>
                    <p>{error}</p>
                    <button
                        onClick={() => window.location.reload()}
                        className="retry-button"
                    >
                        Retry
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="router-list-container">
            <div className="router-list-header">
                <h2>Router Management</h2>
                <div className="router-count">
                    {routers.length} router{routers.length !== 1 ? 's' : ''} found
                </div>
            </div>

            {routers.length === 0 ? (
                <div className="empty-state">
                    <div className="empty-icon">📡</div>
                    <h3>No Routers Found</h3>
                    <p>There are currently no routers to display.</p>
                </div>
            ) : (
                <div className="router-list">
                    {routers.map((router) => (
                        <RouterItem key={router.id} router={router} />
                    ))}
                </div>
            )}
        </div>
    );
};

export default RouterList;