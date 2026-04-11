import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "../components/ui/table";
import { Badge } from "../components/ui/badge";
import { Download, Filter, Calendar } from "lucide-react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar } from "recharts";

// Mock historical data
const historicalData = [
  {
    timestamp: "2026-03-31 14:00",
    rain: 15,
    waterLevelKRL: 65,
    waterLevelKAI: 72,
    status: "WARNING",
  },
  {
    timestamp: "2026-03-31 13:00",
    rain: 12,
    waterLevelKRL: 60,
    waterLevelKAI: 68,
    status: "WARNING",
  },
  {
    timestamp: "2026-03-31 12:00",
    rain: 8,
    waterLevelKRL: 52,
    waterLevelKAI: 58,
    status: "SAFE",
  },
  {
    timestamp: "2026-03-31 11:00",
    rain: 5,
    waterLevelKRL: 48,
    waterLevelKAI: 55,
    status: "SAFE",
  },
  {
    timestamp: "2026-03-31 10:00",
    rain: 3,
    waterLevelKRL: 45,
    waterLevelKAI: 52,
    status: "SAFE",
  },
  {
    timestamp: "2026-03-31 09:00",
    rain: 2,
    waterLevelKRL: 42,
    waterLevelKAI: 48,
    status: "SAFE",
  },
  {
    timestamp: "2026-03-31 08:00",
    rain: 1,
    waterLevelKRL: 40,
    waterLevelKAI: 45,
    status: "SAFE",
  },
];

// Chart data
const trendData = [
  { time: "08:00", KRL: 40, KAI: 45 },
  { time: "09:00", KRL: 42, KAI: 48 },
  { time: "10:00", KRL: 45, KAI: 52 },
  { time: "11:00", KRL: 48, KAI: 55 },
  { time: "12:00", KRL: 52, KAI: 58 },
  { time: "13:00", KRL: 60, KAI: 68 },
  { time: "14:00", KRL: 65, KAI: 72 },
];

const rainData = [
  { time: "08:00", rain: 1 },
  { time: "09:00", rain: 2 },
  { time: "10:00", rain: 3 },
  { time: "11:00", rain: 5 },
  { time: "12:00", rain: 8 },
  { time: "13:00", rain: 12 },
  { time: "14:00", rain: 15 },
];

export default function DataPage() {
  const [dateFrom, setDateFrom] = useState("2026-03-31");
  const [dateTo, setDateTo] = useState("2026-03-31");
  const [location, setLocation] = useState("all");
  const [statusFilter, setStatusFilter] = useState("all");

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

  const handleExport = (format: string) => {
    alert(`Exporting data as ${format.toUpperCase()}...`);
  };

  return (
    <div className="space-y-6">
      {/* Filter Section */}
      <Card className="border-0 shadow-md">
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <Filter className="w-5 h-5 text-blue-600" />
            Data Filters
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {/* Date From */}
            <div className="space-y-2">
              <Label htmlFor="dateFrom">Date From</Label>
              <div className="relative">
                <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                <Input
                  id="dateFrom"
                  type="date"
                  value={dateFrom}
                  onChange={(e) => setDateFrom(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>

            {/* Date To */}
            <div className="space-y-2">
              <Label htmlFor="dateTo">Date To</Label>
              <div className="relative">
                <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                <Input
                  id="dateTo"
                  type="date"
                  value={dateTo}
                  onChange={(e) => setDateTo(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>

            {/* Location Filter */}
            <div className="space-y-2">
              <Label htmlFor="location">Location</Label>
              <Select value={location} onValueChange={setLocation}>
                <SelectTrigger id="location">
                  <SelectValue placeholder="Select location" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Locations</SelectItem>
                  <SelectItem value="manggarai">Manggarai Station</SelectItem>
                  <SelectItem value="tanah-abang">Tanah Abang Station</SelectItem>
                  <SelectItem value="gambir">Gambir Station</SelectItem>
                  <SelectItem value="jatinegara">Jatinegara Station</SelectItem>
                  <SelectItem value="bekasi">Bekasi Station</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Status Filter */}
            <div className="space-y-2">
              <Label htmlFor="status">Status</Label>
              <Select value={statusFilter} onValueChange={setStatusFilter}>
                <SelectTrigger id="status">
                  <SelectValue placeholder="Select status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Status</SelectItem>
                  <SelectItem value="safe">Safe</SelectItem>
                  <SelectItem value="warning">Warning</SelectItem>
                  <SelectItem value="critical">Critical</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-2 mt-4">
            <Button className="bg-blue-600 hover:bg-blue-700">
              Apply Filters
            </Button>
            <Button variant="outline">
              Reset
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Water Level Trends */}
        <Card className="border-0 shadow-md">
          <CardHeader>
            <CardTitle className="text-lg">Water Level Trends</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={trendData}>
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
                <Line type="monotone" dataKey="KRL" stroke="#3b82f6" strokeWidth={2} />
                <Line type="monotone" dataKey="KAI" stroke="#8b5cf6" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Rain Intensity Chart */}
        <Card className="border-0 shadow-md">
          <CardHeader>
            <CardTitle className="text-lg">Rain Intensity</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={rainData}>
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
                <Bar dataKey="rain" fill="#3b82f6" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Data Table */}
      <Card className="border-0 shadow-md">
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle className="text-lg">Historical Data</CardTitle>
          <div className="flex gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => handleExport("csv")}
              className="gap-2"
            >
              <Download className="w-4 h-4" />
              Export CSV
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => handleExport("pdf")}
              className="gap-2"
            >
              <Download className="w-4 h-4" />
              Export PDF
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Timestamp</TableHead>
                  <TableHead>Rain (mm/h)</TableHead>
                  <TableHead>Water Level KRL (cm)</TableHead>
                  <TableHead>Water Level KAI (cm)</TableHead>
                  <TableHead>Flood Status</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {historicalData.map((item, index) => (
                  <TableRow key={index}>
                    <TableCell className="font-medium">{item.timestamp}</TableCell>
                    <TableCell>{item.rain}</TableCell>
                    <TableCell>{item.waterLevelKRL}</TableCell>
                    <TableCell>{item.waterLevelKAI}</TableCell>
                    <TableCell>
                      <Badge className={getStatusColor(item.status)} variant="outline">
                        {item.status}
                      </Badge>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>

          {/* Pagination */}
          <div className="flex items-center justify-between mt-4">
            <p className="text-sm text-gray-500">
              Showing 1-7 of 7 entries
            </p>
            <div className="flex gap-2">
              <Button variant="outline" size="sm" disabled>
                Previous
              </Button>
              <Button variant="outline" size="sm" disabled>
                Next
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
