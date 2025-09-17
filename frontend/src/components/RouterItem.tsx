import React from 'react';
import { Router } from './RouterList';
import './RouterItem.css';

interface RouterItemProps {
    router: Router;
}

const RouterItem: React.FC<RouterItemProps> = ({ router }) => {
    // Format the updatedAt timestamp to a human-readable format
    const formatLastUpdate = (timestamp: string): string => {
        const date = new Date(timestamp);
        const now = new Date();
        const diffInSeconds = Math.floor((now.getTime() - date.getTime()) / 1000);

        if (diffInSeconds < 60) {
            return 'Just now';
        } else if (diffInSeconds < 3600) {
            const minutes = Math.floor(diffInSeconds / 60);
            return `${minutes} minute${minutes !== 1 ? 's' : ''} ago`;
        } else if (diffInSeconds < 86400) {
            const hours = Math.floor(diffInSeconds / 3600);
            return `${hours} hour${hours !== 1 ? 's' : ''} ago`;
        } else if (diffInSeconds < 604800) {
            const days = Math.floor(diffInSeconds / 86400);
            return `${days} day${days !== 1 ? 's' : ''} ago`;
        } else {
            return date.toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        }
    };

    // Get type-specific icon
    const getTypeIcon = (type: string): string => {
        switch (type) {
            case 'wifi':
                return '📶';
            case 'enterprise':
                return '🏢';
            case 'home':
                return '🏠';
            default:
                return '📡';
        }
    };

    // Get type-specific color class
    const getTypeColorClass = (type: string): string => {
        switch (type) {
            case 'wifi':
                return 'type-wifi';
            case 'enterprise':
                return 'type-enterprise';
            case 'home':
                return 'type-home';
            default:
                return 'type-default';
        }
    };

    return (
        <div className="router-item">
            <div className="router-item-header">
                <div className="router-icon">
                    {getTypeIcon(router.type)}
                </div>
                <div className="router-main-info">
                    <h3 className="router-name">{router.name}</h3>
                    <div className="router-id">ID: {router.id}</div>
                </div>
                <div className={`router-type ${getTypeColorClass(router.type)}`}>
                    {router.type.charAt(0).toUpperCase() + router.type.slice(1)}
                </div>
            </div>

            <div className="router-item-body">
                <div className="router-meta">
                    <div className="last-update">
                        <span className="label">Last Updated:</span>
                        <span className="value">{formatLastUpdate(router.updatedAt)}</span>
                    </div>
                    <div className="coordinates">
                        <span className="label">Location:</span>
                        <span className="value">
                            {router.coordinates.latitude.toFixed(2)}°, {router.coordinates.longitude.toFixed(2)}°
                        </span>
                    </div>
                </div>

                {/* Type-specific information */}
                <div className="router-specs">
                    {router.type === 'wifi' && (
                        <>
                            {router.wifiChannels && (
                                <div className="spec-item">
                                    <span className="spec-label">Channels:</span>
                                    <span className="spec-value">{router.wifiChannels.length} configured</span>
                                </div>
                            )}
                            {router.supportsDualBand !== undefined && (
                                <div className="spec-item">
                                    <span className="spec-label">Dual Band:</span>
                                    <span className="spec-value">{router.supportsDualBand ? 'Yes' : 'No'}</span>
                                </div>
                            )}
                        </>
                    )}

                    {router.type === 'enterprise' && (
                        <>
                            {router.portCount && (
                                <div className="spec-item">
                                    <span className="spec-label">Ports:</span>
                                    <span className="spec-value">{router.portCount}</span>
                                </div>
                            )}
                            {router.throughputGbps && (
                                <div className="spec-item">
                                    <span className="spec-label">Throughput:</span>
                                    <span className="spec-value">{router.throughputGbps} Gbps</span>
                                </div>
                            )}
                            {router.supportedProtocols && (
                                <div className="spec-item">
                                    <span className="spec-label">Protocols:</span>
                                    <span className="spec-value">{router.supportedProtocols.join(', ')}</span>
                                </div>
                            )}
                        </>
                    )}

                    {router.type === 'home' && (
                        <>
                            {router.connectedDevices !== undefined && (
                                <div className="spec-item">
                                    <span className="spec-label">Connected Devices:</span>
                                    <span className="spec-value">{router.connectedDevices}</span>
                                </div>
                            )}
                            {router.maxBandwidthMbps && (
                                <div className="spec-item">
                                    <span className="spec-label">Max Bandwidth:</span>
                                    <span className="spec-value">{router.maxBandwidthMbps} Mbps</span>
                                </div>
                            )}
                            {router.parentalControlsEnabled !== undefined && (
                                <div className="spec-item">
                                    <span className="spec-label">Parental Controls:</span>
                                    <span className="spec-value">{router.parentalControlsEnabled ? 'Enabled' : 'Disabled'}</span>
                                </div>
                            )}
                        </>
                    )}
                </div>
            </div>
        </div>
    );
};

export default RouterItem;