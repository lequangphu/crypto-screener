import React from 'react';

const SearchBar = () => {
    return (
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
            <h2 className="text-2xl font-semibold mb-4 text-white">Search</h2>
            <input
                type="text"
                placeholder="Search protocols..."
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline bg-gray-700 border-gray-600"
            />
        </div>
    );
};

export default SearchBar; 