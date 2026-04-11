import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { Droplets, CloudRain, AlertTriangle, CheckCircle, Clock } from "lucide-react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar } from "recharts";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "../components/ui/table";

// Mock data for charts
const waterLevelData = [
  { time: "00:00", KRL: 45, KAI: 52 },
  { time: "04:00", KRL: 48, KAI: 55 },
  { time: "08:00", KRL: 52, KAI: 58 },
  { time: "12:00", KRL: 65, KAI: 72 },
  { time: "16:00", KRL: 58, KAI: 65 },
  { time: "20:00", KRL: 48, KAI: 54 },
];

const rainIntensityData = [
  { time: "00:00", intensity: 2 },
  { time: "04:00", intensity: 5 },
  { time: "08:00", intensity: 8 },
  { time: "12:00", intensity: 15 },
  { time: "16:00", intensity: 10 },
  { time: "20:00", intensity: 4 },
];

// Mock monitoring data
const monitoringData = [
  { 
    location: "Manggarai Station", 
    rainStatus: "Heavy", 
    waterLevel: 65, 
    status: "WARNING", 
    lastUpdate: "2 min ago" 
  },
  { 
    location: "Tanah Abang Station", 
    rainStatus: "Moderate", 
    waterLevel: 45, 
    status: "SAFE", 
    lastUpdate: "3 min ago" 
  },
  { 
    location: "Gambir Station", 
    rainStatus: "Light", 
    waterLevel: 38, 
    status: "SAFE", 
    lastUpdate: "1 min ago" 
  },
  { 
    location: "Jatinegara Station", 
    rainStatus: "Heavy", 
    waterLevel: 72, 
    status: "CRITICAL", 
    lastUpdate: "just now" 
  },
  { 
    location: "Bekasi Station", 
    rainStatus: "Moderate", 
    waterLevel: 52, 
    status: "SAFE", 
    lastUpdate: "5 min ago" 
  },
];

// Mock alerts
const alerts = [
  {
    id: 1,
    type: "critical",
    message: "Critical water level at Jatinegara Station (72 cm)",
    time: "2 minutes ago",
  },
  {
    id: 2,
    type: "warning",
    message: "Water level rising at Manggarai Station (65 cm)",
    time: "5 minutes ago",
  },
  {
    id: 3,
    type: "info",
    message: "Heavy rainfall detected in East Jakarta area",
    time: "10 minutes ago",
  },
];

export default function Dashboard() {
  const getStatusColor = (status: string) => {
    switch (status) {
      case "SAFE":
        return "bg-green-100 text-green-700 border-green-200";
      case "WARNING":
        return "bg-yellow-100 text-yellow-700 border-yellow-200";
      case "CRITICAL":
        return "bg-red-100 text-red-700 border-red-200";
      default:
        return "bg-gray-100 text-gray-700 border-gray-200";
    }
  };

  const getFloodStatus = () => {
    const maxLevel = Math.max(...monitoringData.map(d => d.waterLevel));
    if (maxLevel >= 70) return { label: "TOTAL STOP", color: "bg-red-500", icon: AlertTriangle };
    if (maxLevel >= 60) return { label: "KRL STOP", color: "bg-yellow-500", icon: AlertTriangle };
    return { label: "AMAN", color: "bg-green-500", icon: CheckCircle };
  };

  const floodStatus = getFloodStatus();
  const StatusIcon = floodStatus.icon;

  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Water Level KRL */}
        <Card className="border-0 shadow-md">
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500 mb-1">Water Level KRL</p>
                <p className="text-3xl font-bold text-gray-900">65 cm</p>
                <p className="text-xs text-yellow-600 mt-1">↑ 5 cm from last hour</p>
              </div>
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <Droplets className="w-6 h-6 text-blue-600" />
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Water Level KAI */}
        <Card className="border-0 shadow-md">
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500 mb-1">Water Level KAI</p>
                <p className="text-3xl font-bold text-gray-900">72 cm</p>
                <p className="text-xs text-red-600 mt-1">↑ 8 cm from last hour</p>
              </div>
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <Droplets className="w-6 h-6 text-blue-600" />
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Rain Intensity */}
        <Card className="border-0 shadow-md">
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500 mb-1">Rain Intensity</p>
                <p className="text-3xl font-bold text-gray-900">15 mm/h</p>
                <p className="text-xs text-gray-600 mt-1">Heavy rainfall</p>
              </div>
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <CloudRain className="w-6 h-6 text-blue-600" />
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Flood Status */}
        <Card className={`border-0 shadow-md ${floodStatus.color} text-white`}>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-white/90 mb-1">Flood Status</p>
                <p className="text-3xl font-bold">{floodStatus.label}</p>
                <p className="text-xs text-white/80 mt-1">Current operational status</p>
              </div>
              <div className="w-12 h-12 bg-white/20 rounded-lg flex items-center justify-center">
                <StatusIcon className="w-6 h-6 text-white" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Water Level Chart */}
        <Card className="border-0 shadow-md">
          <CardHeader>
            <CardTitle className="text-lg">Water Level Trends (24h)</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={waterLevelData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis dataKey="time" stroke="#6b7280" />
                <YAxis stroke="#6b7280" label={{ value: 'cm', angle: -90, position: 'insideLeft' }} />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: 'white', 
                    border: '1px solid #e5e7eb',
                    borderRadius: '8px'
                  }} 
                />
                <Legend />
                <Line type="monotone" dataKey="KRL" stroke="#3b82f6" strokeWidth={2} dot={{ r: 4 }} />
                <Line type="monotone" dataKey="KAI" stroke="#8b5cf6" strokeWidth={2} dot={{ r: 4 }} />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Rain Intensity Chart */}
        <Card className="border-0 shadow-md">
          <CardHeader>
            <CardTitle className="text-lg">Rain Intensity (24h)</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={rainIntensityData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis dataKey="time" stroke="#6b7280" />
                <YAxis stroke="#6b7280" label={{ value: 'mm/h', angle: -90, position: 'insideLeft' }} />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: 'white', 
                    border: '1px solid #e5e7eb',
                    borderRadius: '8px'
                  }} 
                />
                <Legend />
                <Bar dataKey="intensity" fill="#3b82f6" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Monitoring Table and Alerts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Real-Time Monitoring Table */}
        <Card className="border-0 shadow-md lg:col-span-2">
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <Clock className="w-5 h-5 text-blue-600" />
              Real-Time Monitoring
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Location</TableHead>
                    <TableHead>Rain Status</TableHead>
                    <TableHead>Water Level</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Last Update</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {monitoringData.map((item, index) => (
                    <TableRow key={index}>
                      <TableCell className="font-medium">{item.location}</TableCell>
                      <TableCell>{item.rainStatus}</TableCell>
                      <TableCell>{item.waterLevel} cm</TableCell>
                      <TableCell>
                        <Badge className={getStatusColor(item.status)} variant="outline">
                          {item.status}
                        </Badge>
                      </TableCell>
                      <TableCell className="text-gray-500 text-sm">{item.lastUpdate}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </CardContent>
        </Card>

        {/* Alerts Panel */}
        <Card className="border-0 shadow-md">
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <AlertTriangle className="w-5 h-5 text-yellow-600" />
              Recent Alerts
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {alerts.map((alert) => (
                <div
                  key={alert.id}
                  className={`p-4 rounded-lg border-l-4 ${
                    alert.type === "critical"
                      ? "bg-red-50 border-red-500"
                      : alert.type === "warning"
                      ? "bg-yellow-50 border-yellow-500"
                      : "bg-blue-50 border-blue-500"
                  }`}
                >
                  <p className="text-sm font-medium text-gray-900 mb-1">
                    {alert.message}
                  </p>
                  <p className="text-xs text-gray-500">{alert.time}</p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
