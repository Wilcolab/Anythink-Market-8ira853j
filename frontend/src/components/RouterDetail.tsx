import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
    Router,
    isWiFiRouter,
    isEnterpriseRouter,
    isHomeRouter
} from '../services/RouterService';
import agent from '../agent'; // Import agent for API calls

const RouterDetail: React.FC = () => {
    const params = useParams<{ id: string }>();
    const id = params.id;

    const [router, setRouter] = useState<Router | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        setLoading(true);

        // Use the agent method to get router by ID
        agent.Routers.getById(id)
            .then(foundRouter => {
                if (foundRouter) {
                    // Type assertion to handle the Router type differences
                    setRouter(foundRouter as unknown as Router);
                    setLoading(false);
                } else {
                    setError('Router not found');
                    setLoading(false);
                }
            })
            .catch(err => {
                setError(err.message || 'Failed to fetch router data');
                setLoading(false);
            });
    }, [id]);

    if (loading) return <div className="loading">Loading...</div>;
    if (error) return <div className="error">Error: {error}</div>;
    if (!router) return <div className="no-data">No router found</div>;

    return (
        <div className="router-detail">
            <div className="router-detail-header">
                <Link to="/" className="back-link">← Back to routers</Link>
                <h2>{router.name}</h2>
                {router.status && (
                    <span className={`status-badge ${router.status.toLowerCase()}`}>
                        {router.status}
                    </span>
                )}
            </div>

            <div className="router-detail-card">
                <div className="router-basic-info">
                    <h3>Basic Information</h3>
                    <div className="info-grid">
                        <div className="info-item">
                            <label>Model:</label>
                            <span>{router.model || 'N/A'}</span>
                        </div>
                        <div className="info-item">
                            <label>Manufacturer:</label>
                            <span>{router.manufacturer || 'N/A'}</span>
                        </div>
                        <div className="info-item">
                            <label>IP Address:</label>
                            <span>{router.ipAddress || 'N/A'}</span>
                        </div>
                        <div className="info-item">
                            <label>Type:</label>
                            <span className="router-type">
                                {router.type ? router.type.charAt(0).toUpperCase() + router.type.slice(1) : 'Unknown'}
                            </span>
                        </div>
                    </div>
                </div>

                {/* Type-specific information */}
                <div className="router-specific-info">
                    <h3>{router.type ? (router.type.charAt(0).toUpperCase() + router.type.slice(1)) : 'Unknown'} Router Details</h3>

                    {isWiFiRouter(router) && (
                        <div className="wifi-info">
                            <div className="info-grid">
                                <div className="info-item">
                                    <label>WiFi Channels:</label>
                                    <span>{router.wifiChannels.join(', ')}</span>
                                </div>
                                <div className="info-item">
                                    <label>Dual Band Support:</label>
                                    <span>{router.dualBandSupport ? 'Yes' : 'No'}</span>
                                </div>
                            </div>
                        </div>
                    )}

                    {isEnterpriseRouter(router) && (
                        <div className="enterprise-info">
                            <div className="info-grid">
                                <div className="info-item">
                                    <label>Port Count:</label>
                                    <span>{router.portCount}</span>
                                </div>
                                <div className="info-item">
                                    <label>Throughput:</label>
                                    <span>{router.throughput} Gbps</span>
                                </div>
                                <div className="info-item protocols">
                                    <label>Supported Protocols:</label>
                                    <div className="protocol-tags">
                                        {router.supportedProtocols.map(protocol => (
                                            <span key={protocol} className="protocol-tag">{protocol}</span>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}

                    {isHomeRouter(router) && (
                        <div className="home-info">
                            <div className="info-grid">
                                <div className="info-item">
                                    <label>Connected Devices:</label>
                                    <span>{router.connectedDevices}</span>
                                </div>
                                <div className="info-item">
                                    <label>Parental Controls:</label>
                                    <span>{router.parentalControls ? 'Enabled' : 'Disabled'}</span>
                                </div>
                                <div className="info-item">
                                    <label>Maximum Bandwidth:</label>
                                    <span>{router.maxBandwidth} Mbps</span>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default RouterDetail;
