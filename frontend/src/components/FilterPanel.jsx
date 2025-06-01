import React from 'react';

const FilterPanel = () => {
    return (
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
            <h2 className="text-2xl font-semibold mb-4 text-white">Filters</h2>
            <div className="mb-4">
                <label htmlFor="chain-select" className="block text-gray-300 text-sm font-bold mb-2">Chain:</label>
                <select id="chain-select" className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline bg-gray-700 border-gray-600">
                    <option>All Chains</option>
                    {/* Options will be dynamically loaded */}
                </select>
            </div>
            <div className="mb-4">
                <label htmlFor="category-select" className="block text-gray-300 text-sm font-bold mb-2">Category:</label>
                <select id="category-select" className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline bg-gray-700 border-gray-600">
                    <option>All Categories</option>
                    {/* Options will be dynamically loaded */}
                </select>
            </div>
        </div>
    );
};

export default FilterPanel; 