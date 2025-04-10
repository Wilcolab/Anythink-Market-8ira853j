import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Router } from '../services/RouterService';
import agent from '../agent'; // Import the agent for API calls
import './RouterList.css';

type FilterType = 'all' | 'wifi' | 'enterprise' | 'home';
type SortField = 'name' | 'updatedAt';
type SortDirection = 'asc' | 'desc';

const RouterList: React.FC = () => {
    const [routers, setRouters] = useState<Router[]>([]);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState<FilterType>('all');
    const [sortField, setSortField] = useState<SortField>('name');
    const [sortDirection, setSortDirection] = useState<SortDirection>('asc');

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

    // Filter routers based on selected type
    const filteredRouters = filter === 'all'
        ? routers
        : routers.filter(router => router.type?.toLowerCase() === filter);

    // Sort the filtered routers
    const sortedRouters = [...filteredRouters].sort((a, b) => {
        if (sortField === 'name') {
            const nameA = (a.name || '').toLowerCase();
            const nameB = (b.name || '').toLowerCase();
            return sortDirection === 'asc'
                ? nameA.localeCompare(nameB)
                : nameB.localeCompare(nameA);
        } else {
            const dateA = new Date(a.updatedAt || 0).getTime();
            const dateB = new Date(b.updatedAt || 0).getTime();
            return sortDirection === 'asc'
                ? dateA - dateB
                : dateB - dateA;
        }
    });

    // Toggle sort direction or change sort field
    const handleSort = (field: SortField) => {
        if (sortField === field) {
            setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
        } else {
            setSortField(field);
            setSortDirection('asc');
        }
    };

    return (
        <div className="router-list-container">
            <h2>Router List</h2>

            <div className="router-controls">
                <div className="filter-controls">
                    <label>Filter by type: </label>
                    <select
                        value={filter}
                        onChange={(e) => setFilter(e.target.value as FilterType)}
                        className="filter-select"
                    >
                        <option value="all">All Types</option>
                        <option value="wifi">WiFi</option>
                        <option value="enterprise">Enterprise</option>
                        <option value="home">Home</option>
                    </select>
                </div>

                <div className="sort-controls">
                    <label>Sort by: </label>
                    <button
                        className={`sort-button ${sortField === 'name' ? 'active' : ''}`}
                        onClick={() => handleSort('name')}
                    >
                        Name {sortField === 'name' && (sortDirection === 'asc' ? '↑' : '↓')}
                    </button>
                    <button
                        className={`sort-button ${sortField === 'updatedAt' ? 'active' : ''}`}
                        onClick={() => handleSort('updatedAt')}
                    >
                        Last Updated {sortField === 'updatedAt' && (sortDirection === 'asc' ? '↑' : '↓')}
                    </button>
                </div>
            </div>

            {filteredRouters.length === 0 ? (
                <p>No routers found with the selected filter</p>
            ) : (
                <>
                    <p className="results-info">
                        Showing {filteredRouters.length} {filter !== 'all' ? filter : ''} router(s)
                    </p>
                    <ul className="router-list">
                        {sortedRouters.map((router) => (
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
                </>
            )}
        </div>
    );
};

export default RouterList;
