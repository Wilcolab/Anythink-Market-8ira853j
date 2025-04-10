import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Router } from '../services/RouterService';
import agent from '../agent'; // Import the agent for API calls
import './RouterList.css';

const RouterList: React.FC = () => {
    const [routers, setRouters] = useState<Router[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Use the agent to fetch routers instead of the direct service
        agent.Routers.getAll()
            .then(data => {
                // Use type assertion to tell TypeScript this data matches our Router type
                setRouters(data as unknown as Router[]);
                setLoading(false);
            })
            .catch(error => {
                console.error("Error fetching routers:", error);
                setLoading(false);
            });
    }, []);

    if (loading) return <div className="loading">Loading routers...</div>;

    if (!routers || routers.length === 0) {
        return <p>No routers found</p>;
    }

    return (
        <div className="router-list-container">
            <h2>Router List</h2>
            <ul className="router-list">
                {routers.map((router) => (
                    <li key={router?.id || Math.random().toString()} className="router-item">
                        <div className="router-name">
                            <strong>Name:</strong> <Link to={`/router/${router.id}`} className="router-link">{router?.name || 'Unnamed Router'}</Link>
                        </div>
                        <div className="router-type">
                            <strong>Type:</strong> {router?.type || 'Unspecified'}
                        </div>
                        <div className="router-updated">
                            <strong>Last Updated:</strong> {router?.updatedAt}
                        </div>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default RouterList;
