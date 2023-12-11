import { useEffect, useState } from "react";
import { BarChart, Bar, Rectangle, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function App() {
  const [versions, setVersions] = useState([])
  const [selected, setSelected] = useState(["v1.19.13", "v1.20.9", "v1.21.3", "v1.22.0", "v1.23.0", "v1.24.0", "v1.25.4", "v1.26.0", "v1.27.0", "v1.28.0"])
  const [chartData, setChartData] = useState([])
  const [vulnSL, setVulnSL] = useState()
  const [vulnBA, setVulnBA] = useState()
  const [viewSeverities, setViewSeverities] = useState(true)

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
    return b1.length - a1.length;
  };

  useEffect(() => {
    const fetchData = async () => {
      const response1 = await fetch('https://raw.githubusercontent.com/EC528-Fall-2023/Evolution-of-Kubernetes-/master/SBOM/severitylevel.json')
      const data1 = await (response1.json())
      const object1 = data1.reduce((obj, item) => Object.assign(obj, { [item['KubeVersion']]: item }), {})
      setVulnSL(object1);

      const response2 = await fetch('https://raw.githubusercontent.com/EC528-Fall-2023/Evolution-of-Kubernetes-/master/SBOM/beforeafter.json')
      const data2 = await (response2.json())
      const object2 = data2.reduce((obj, item) => Object.assign(obj, { [item['KubeVersion']]: item }), {})
      setVulnBA(object2);
      
      setVersions((Object.keys(object1)).sort(compareSemVer))
    }
    fetchData()
    console.log("fetched versions")
  }, [])

  useEffect(() => {
    if (vulnSL) {
      if (viewSeverities) {
        setChartData(selected.map(i => ({ name: i, ...vulnSL[i] })))
      } else {
        setChartData(selected.map(i => ({ name: i, ...vulnBA[i] })))
      }
    }
  }, [selected, vulnSL, viewSeverities])

  return (
    <div className="h-screen flex flex-col sm:flex-row p-10">
      <div className="flex-grow">
        <h1 className="absolute text-center font-semibold top-4 w-full right-0 overflow-y-auto">Kubernetes Vulnerabilities by Version</h1>
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
            {viewSeverities ? 
              <>
                <Bar dataKey="Negligible" fill="olivedrab" stackId="a" activeBar={<Rectangle fill="lightskyblue" />} />
                <Bar dataKey="Low" fill="gold" stackId="a" activeBar={<Rectangle fill="lightskyblue" />} />
                <Bar dataKey="Medium" fill="orange" stackId="a" activeBar={<Rectangle fill="lightskyblue" />} />
                <Bar dataKey="High" fill="orangered" stackId="a" activeBar={<Rectangle fill="lightskyblue" />} />
                <Bar dataKey="Critical" fill="red" stackId="a" activeBar={<Rectangle fill="lightskyblue" />} />
                <Bar dataKey="Unknown" fill="gray" stackId="a" activeBar={<Rectangle fill="lightskyblue" />} />
              </>
              :
              <>
                <Bar dataKey="Before" fill="peachpuff" stackId="a" activeBar={<Rectangle fill="lightskyblue" />} />
                <Bar dataKey="After" fill="pink" stackId="a" activeBar={<Rectangle fill="lightskyblue" />} />
              </>
            }

          </BarChart>
        </ResponsiveContainer>
      </div>
      <div className="flex flex-col sm:w-32 space-y-1 overflow-y-auto">
        <button onClick={() => setSelected([])} className="text-left shadow-md bg-neutral-200 p-1 border border-neutral-300 hover:bg-sky-200 w-full">Clear</button>
        <button onClick={() => setSelected(versions)} className="text-left shadow-md bg-neutral-200 p-1 border border-neutral-300 hover:bg-sky-200 w-full">Select All</button>
        <button onClick={() => setViewSeverities(!viewSeverities)} className="text-left shadow-md bg-neutral-200 p-1 border border-neutral-300 hover:bg-sky-200 w-full">{viewSeverities ? "Severity" : "Before/After"}</button>
        <ul className="flex flex-col h-full pr-1">
        
          {versions.map((i) => <button
            key={i}
            onClick={() => {
              if (selected.includes(i)) {
                setSelected((selected.filter((element) => element !== i)).sort())
              } else {
                setSelected((selected.concat(i)).sort())
              }
            }}
            className={`border text-left py-px px-2 border-neutral-300 ${selected.includes(i) ? "bg-sky-300 hover:bg-sky-200" : "bg-neutral-200 hover:bg-sky-100"}`}
          >
            {i}
          </button>)}
        </ul>
      </div>
    </div>
  )
}

export default App;