import { LineChart, Line, ResponsiveContainer, YAxis } from 'recharts';

export function Sparkline({ data, dataKey = 'value', color = '#1fc2a0', width = 60, height = 20 }) {
  if (!data || data.length < 2) {
    return <div style={{ width, height }} />;
  }

  // Transform data for recharts
  const chartData = data.map((value, index) => ({
    index,
    [dataKey]: value,
  }));

  return (
    <div style={{ width, height, display: 'inline-block', verticalAlign: 'middle' }}>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={chartData}>
          <YAxis domain={['auto', 'auto']} hide />
          <Line
            type="monotone"
            dataKey={dataKey}
            stroke={color}
            strokeWidth={1.5}
            dot={false}
            isAnimationActive={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
