import { useEffect, useState } from "react";
import { BarChart, Bar, Rectangle, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import vulnerabilities from './data/vulnerabilities.json';

function App() {
  const testdata = vulnerabilities
  const [versions, setVersions] = useState([])
  const [selected, setSelected] = useState(["v1.19.13", "v1.20.9", "v1.21.3", "v1.22.0", "v1.23.0", "v1.24.0", "v1.25.4", "v1.26.0", "v1.27.0", "v1.28.0"])
  const [chartData, setChartData] = useState([])

  const compareSemVer = (a, b) => {
 
    // 1. Split the strings into their parts.
    const a1 = a.split('.');
    const b1 = b.split('.');    // 2. Contingency in case there's a 4th or 5th version
    const len = Math.min(a1.length, b1.length);    // 3. Look through each version number and compare.
    for (let i = 0; i < len; i++) {
        const a2 = +a1[ i ] || 0;
        const b2 = +b1[ i ] || 0;
        
        if (a2 !== b2) {
            return a2 > b2 ? 1 : -1;        
        }    }
    
    // 4. We hit this if the all checked versions so far are equal
    //
    return b1.length - a1.length;};
  // NOTE: We're gonna need to either fetch a list of all versions or hard-code it
  useEffect(() => {
    // setVersions(['Version A', 'Version B', 'Version C', 'Version D', 'Version E', 'Version F', 'Version G', 'Version H', 'Version I', 'Version J', 'Version K', 'Version L', 'Version M', 'Version N'])
    setVersions((Object.keys(testdata)).sort(compareSemVer))
    console.log("fetched versions")
  }, [])

  useEffect(() => {
    // NOTE:  if we fetch from neo4j, make sure to handle this with async
    setChartData(
      selected.map(i => ({ name: i, ...testdata[i] }))
    )
    console.log(chartData)
  }, [selected])

  return (
    <div className="h-screen flex flex-row p-10">
      <div className="flex-grow overflow-x-auto">
        <h1 className="absolute text-center font-semibold top-4 right-1/2">Kubernetes Vulnerabilities by Version</h1>
        <ResponsiveContainer >
          
          <BarChart
            className="p-5"
            data={chartData}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" angle={-45} textAnchor="end" height={80} />
            <YAxis label={{ value: 'Vulnerabilities', angle: -90, position: 'insideLeft' }} />
            <Tooltip />
            <Legend />
            <Bar dataKey="Negligible" fill="olivedrab" stackId="a" activeBar={<Rectangle fill="lightskyblue" />} />
            <Bar dataKey="Low" fill="gold" stackId="a" activeBar={<Rectangle fill="lightskyblue" />} />
            <Bar dataKey="Medium" fill="orange" stackId="a" activeBar={<Rectangle fill="lightskyblue" />} />
            <Bar dataKey="High" fill="orangered" stackId="a" activeBar={<Rectangle fill="lightskyblue" />} />
            <Bar dataKey="Critical" fill="red" stackId="a" activeBar={<Rectangle fill="lightskyblue" />} />
            <Bar dataKey="Unknown" fill="gray" stackId="a" activeBar={<Rectangle fill="lightskyblue" />} />
          </BarChart>
        </ResponsiveContainer>
      </div>
      <div className="flex flex-col w-32">
        <button onClick={() => setSelected([])} className="bg-neutral-200 p-1 border border-neutral-300 hover:bg-sky-200 w-full">Clear</button>
        <button onClick={() => setSelected(versions)} className="bg-neutral-200 p-1 border border-neutral-300 hover:bg-sky-200 w-full">Select All</button>
        <ul className="flex flex-shrink flex-col h-full overflow-y-scroll ">
        
          {versions.map((i) => <button
            key={i}
            onClick={() => {
              if (selected.includes(i)) {
                setSelected((selected.filter((element) => element !== i)).sort())
              } else {
                setSelected((selected.concat(i)).sort())
              }
            }}
            className={`border text-left p-1 border-neutral-300 ${selected.includes(i) ? "bg-sky-300 hover:bg-sky-200" : "bg-neutral-200 hover:bg-sky-100"}`}
          >
            {i}
          </button>)}
        </ul>
      </div>
    </div>
  )
}

export default App;