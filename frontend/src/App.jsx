import React, { useState, useEffect } from 'react';
import { createRoot } from 'react-dom/client';
import ProtocolTable from './components/ProtocolTable.jsx';
import FilterPanel from './components/FilterPanel.jsx';
import SearchBar from './components/SearchBar.jsx';

const App = () => {
    const [protocols, setProtocols] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchProtocols = async () => {
            try {
                const response = await fetch('http://127.0.0.1:8000/protocols');
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                setProtocols(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };
        fetchProtocols();
    }, []);

    if (loading) return <div className="flex justify-center items-center h-screen text-white text-2xl">Loading...</div>;
    if (error) return <div className="flex justify-center items-center h-screen text-red-500 text-2xl">Error: {error}</div>;

    return (
        <div className="min-h-screen bg-gray-900 text-white p-8">
            <h1 className="text-4xl font-bold text-center mb-8">Crypto Projects Screener</h1>
            <div className="flex flex-col lg:flex-row gap-8">
                <div className="lg:w-1/4">
                    <FilterPanel />
                </div>
                <div className="lg:w-3/4">
                    <SearchBar />
                    <ProtocolTable protocols={protocols} />
                </div>
            </div>
        </div>
    );
};

const container = document.getElementById('root');
if (container) {
    const root = createRoot(container);
    root.render(<App />);
} 