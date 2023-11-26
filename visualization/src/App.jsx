import { useEffect, useState } from "react"
import { BarChart, Bar, Rectangle, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function App() {

  // JUST FOR TESTING
  const testdata = {
    'Version A': { name: 'Version A', before: 4000, after: 2400, },
    'Version B': { name: 'Version B', before: 5432, after: 1324, },
    'Version C': { name: 'Version C', before: 4000, after: 1432, },
    'Version D': { name: 'Version D', before: 1432, after: 3333, },
    'Version E': { name: 'Version E', before: 4321, after: 4431, },
    'Version F': { name: 'Version F', before: 4000, after: 1223, },
    'Version G': { name: 'Version G', before: 4000, after: 1223, },
    'Version H': { name: 'Version H', before: 4000, after: 2400, },
    'Version I': { name: 'Version I', before: 5432, after: 1324, },
    'Version J': { name: 'Version J', before: 4000, after: 1432, },
    'Version K': { name: 'Version K', before: 1432, after: 3333, },
    'Version L': { name: 'Version L', before: 3232, after: 4431, },
    'Version M': { name: 'Version M', before: 4000, after: 1223, },
    'Version N': { name: 'Version N', before: 4000, after: 1223, }
  }

  const [versions, setVersions] = useState([])
  const [selected, setSelected] = useState([])
  const [chartData, setChartData] = useState([])

  // NOTE:
  // We're gonna need to either fetch a list of all versions or hard-code it
  useEffect(() => {
    setVersions(['Version A', 'Version B', 'Version C', 'Version D', 'Version E', 'Version F', 'Version G', 'Version H', 'Version I', 'Version J', 'Version K', 'Version L', 'Version M', 'Version N'])
    console.log("fetched versions")
  }, [])

  useEffect(() => {
    // NOTE:
    // when we fetch from neo4j, make sure to handle this with async
    setChartData(
      selected.map((i) => testdata[i])
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
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            width={500}
            height={300}
            data={chartData}
            margin={{
              top: 5,
              right: 30,
              left: 20,
              bottom: 5,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="after" fill="#8884d8" activeBar={<Rectangle fill="pink" stroke="blue" />} />
            <Bar dataKey="before" fill="#82ca9d" activeBar={<Rectangle fill="gold" stroke="purple" />} />
          </BarChart>
        </ResponsiveContainer>
      </div>
      <ul className="flex flex-shrink flex-col h-full overflow-y-scroll ">
        {versions.map((i) => <button
          key={i}
          onClick={() => {
            if (selected.includes(i)) {
              setSelected(selected.filter((element) => element !== i))
            } else {
              setSelected(selected.concat(i))
            }
          }}
          className={`border text-left p-1 border-neutral-300 w-40 ${selected.includes(i) ? "bg-blue-300" : "bg-neutral-200"}`}
        >
          {i}
        </button>)}
      </ul>
    </div>
  )
}

export default App
