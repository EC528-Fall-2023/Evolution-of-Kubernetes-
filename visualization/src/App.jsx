import { useEffect, useState } from "react";
import { BarChart, Bar, Rectangle, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import vulnerabilities from './data/vulnerabilities.json';

function App() {

  // JUST FOR TESTING
  // const testdata = {
  //   'Version A': { name: 'Version A', low: 2432, high: 2400, },
  //   'Version B': { name: 'Version B', low: 5432, high: 1324, },
  //   'Version C': { name: 'Version C', low: 4000, high: 1432, },
  //   'Version D': { name: 'Version D', low: 1432, high: 3333, },
  //   'Version E': { name: 'Version E', low: 4321, high: 4431, },
  //   'Version F': { name: 'Version F', low: 4000, high: 1223, },
  //   'Version G': { name: 'Version G', low: 1233, high: 1223, },
  //   'Version H': { name: 'Version H', low: 4000, high: 2400, },
  //   'Version I': { name: 'Version I', low: 5432, high: 1324, },
  //   'Version J': { name: 'Version J', low: 4000, high: 1432, },
  //   'Version K': { name: 'Version K', low: 1432, high: 3333, },
  //   'Version L': { name: 'Version L', low: 3232, high: 4431, },
  //   'Version M': { name: 'Version M', low: 4000, high: 1223, },
  //   'Version N': { name: 'Version N', low: 4000, high: 1223, }
  // }

  const testdata = vulnerabilities

  const [versions, setVersions] = useState([])
  const [selected, setSelected] = useState([])
  const [chartData, setChartData] = useState([])

  // NOTE:
  // We're gonna need to either fetch a list of all versions or hard-code it
  useEffect(() => {
    // setVersions(['Version A', 'Version B', 'Version C', 'Version D', 'Version E', 'Version F', 'Version G', 'Version H', 'Version I', 'Version J', 'Version K', 'Version L', 'Version M', 'Version N'])
    setVersions(Object.keys(testdata))
    console.log("fetched versions")
  }, [])

  useEffect(() => {
    // NOTE:
    // when we fetch from neo4j, make sure to handle this with async
    setChartData(
      selected.map(i => ({ name: i, ...testdata[i] }))
    )
    console.log(chartData)
  }, [selected])

  // const handleClick = async () => {
  //   try {
  //     const response = await (await fetch(`https://jsonplaceholder.typicode.com/albums/${id}`)).json()
  //     setData(data.concat(response))
  //   } catch (err) {
  //     console.log(err.message)
  //   }
  // }

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

export default App
