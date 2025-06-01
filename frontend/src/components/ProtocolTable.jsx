import React from 'react';

const ProtocolTable = ({ protocols }) => {
    return (
        <div className="overflow-x-auto bg-gray-800 rounded-lg shadow-lg p-4">
            <table className="min-w-full divide-y divide-gray-700">
                <thead className="bg-gray-700">
                    <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Name</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Chain</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Category</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Daily Fees</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Daily Revenue</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Market Cap</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Price</th>
                    </tr>
                </thead>
                <tbody className="bg-gray-800 divide-y divide-gray-700">
                    {protocols.map((protocol, index) => (
                        <tr key={index}>
                            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-white">{protocol.name}</td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">{protocol.chain}</td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">{protocol.category}</td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">{protocol.dailyFees ? `$${protocol.dailyFees.toLocaleString()}` : 'N/A'}</td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">{protocol.dailyRevenue ? `$${protocol.dailyRevenue.toLocaleString()}` : 'N/A'}</td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">{protocol.marketCap ? `$${protocol.marketCap.toLocaleString()}` : 'N/A'}</td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">{protocol.price ? `$${protocol.price.toFixed(2)}` : 'N/A'}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default ProtocolTable; 