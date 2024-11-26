import { useEffect, useState } from "react";

export default function ItemsList() {
    const [items, setItems] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch('/api/items') // Ensure your backend serves this endpoint
            .then((res) => {
                if (!res.ok) throw new Error('Failed to fetch items');
                return res.json();
            })
            .then((data) => setItems(data))
            .catch((err) => setError(err.message));
    }, []);

    if (error) return <div>Error: {error}</div>;

    return (
        <div>
            <h2>Items</h2>
            <ul>
                {items.map((item) => (
                    <li key={item.item_id}>
                        <strong>{item.name}</strong> ({item.rarity})
                    </li>
                ))}
            </ul>
        </div>
    );
}
