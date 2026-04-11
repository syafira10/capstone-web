import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "../components/ui/table";
import { Badge } from "../components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../components/ui/tabs";
import { 
  Users, 
  Settings, 
  Activity, 
  Wifi, 
  Server, 
  AlertCircle,
  CheckCircle,
  Plus,
  Edit,
  Trash2,
  Radio
} from "lucide-react";

// Mock data
const users = [
  { id: 1, name: "John Doe", email: "john@railway.com", role: "Head of Station", status: "Active" },
  { id: 2, name: "Jane Smith", email: "jane@railway.com", role: "Field Officer", status: "Active" },
  { id: 3, name: "Bob Johnson", email: "bob@railway.com", role: "IT Support", status: "Active" },
  { id: 4, name: "Alice Brown", email: "alice@railway.com", role: "Field Officer", status: "Inactive" },
];

const sensors = [
  { id: 1, name: "Sensor MG-01", location: "Manggarai", status: "Online", lastCalibration: "2026-03-25" },
  { id: 2, name: "Sensor TA-01", location: "Tanah Abang", status: "Online", lastCalibration: "2026-03-28" },
  { id: 3, name: "Sensor GB-01", location: "Gambir", status: "Offline", lastCalibration: "2026-03-20" },
  { id: 4, name: "Sensor JN-01", location: "Jatinegara", status: "Online", lastCalibration: "2026-03-30" },
];

const activityLogs = [
  { id: 1, user: "John Doe", action: "Updated water level threshold", timestamp: "2026-03-31 14:30" },
  { id: 2, user: "Jane Smith", action: "Viewed dashboard", timestamp: "2026-03-31 14:15" },
  { id: 3, user: "Bob Johnson", action: "Calibrated sensor MG-01", timestamp: "2026-03-31 13:45" },
  { id: 4, user: "John Doe", action: "Added new user", timestamp: "2026-03-31 12:20" },
  { id: 5, user: "Alice Brown", action: "Exported data report", timestamp: "2026-03-31 11:10" },
];

const errorLogs = [
  { id: 1, error: "Sensor GB-01 connection timeout", severity: "High", timestamp: "2026-03-31 14:20" },
  { id: 2, error: "MQTT broker reconnection", severity: "Medium", timestamp: "2026-03-31 13:50" },
  { id: 3, error: "Database query slow response", severity: "Low", timestamp: "2026-03-31 12:30" },
];

export default function AdminPanel() {
  const [thresholdKRL, setThresholdKRL] = useState("60");
  const [thresholdKAI, setThresholdKAI] = useState("70");

  return (
    <div className="space-y-6">
      {/* System Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="border-0 shadow-md">
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500 mb-1">Server Status</p>
                <div className="flex items-center gap-2">
                  <CheckCircle className="w-5 h-5 text-green-500" />
                  <span className="text-lg font-semibold text-gray-900">Online</span>
                </div>
                <p className="text-xs text-gray-500 mt-1">Uptime: 99.8%</p>
              </div>
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                <Server className="w-6 h-6 text-green-600" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border-0 shadow-md">
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500 mb-1">MQTT Connection</p>
                <div className="flex items-center gap-2">
                  <CheckCircle className="w-5 h-5 text-green-500" />
                  <span className="text-lg font-semibold text-gray-900">Connected</span>
                </div>
                <p className="text-xs text-gray-500 mt-1">Last ping: 2s ago</p>
              </div>
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <Radio className="w-6 h-6 text-blue-600" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border-0 shadow-md">
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500 mb-1">Network Status</p>
                <div className="flex items-center gap-2">
                  <CheckCircle className="w-5 h-5 text-green-500" />
                  <span className="text-lg font-semibold text-gray-900">Stable</span>
                </div>
                <p className="text-xs text-gray-500 mt-1">Latency: 45ms</p>
              </div>
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                <Wifi className="w-6 h-6 text-purple-600" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Tabs Section */}
      <Card className="border-0 shadow-md">
        <Tabs defaultValue="users" className="w-full">
          <CardHeader className="border-b">
            <TabsList className="grid w-full grid-cols-2 lg:grid-cols-4">
              <TabsTrigger value="users" className="gap-2">
                <Users className="w-4 h-4" />
                <span className="hidden sm:inline">User Management</span>
                <span className="sm:hidden">Users</span>
              </TabsTrigger>
              <TabsTrigger value="settings" className="gap-2">
                <Settings className="w-4 h-4" />
                <span className="hidden sm:inline">System Settings</span>
                <span className="sm:hidden">Settings</span>
              </TabsTrigger>
              <TabsTrigger value="sensors" className="gap-2">
                <Radio className="w-4 h-4" />
                <span className="hidden sm:inline">Sensors</span>
                <span className="sm:hidden">Sensors</span>
              </TabsTrigger>
              <TabsTrigger value="logs" className="gap-2">
                <Activity className="w-4 h-4" />
                <span className="hidden sm:inline">Logs</span>
                <span className="sm:hidden">Logs</span>
              </TabsTrigger>
            </TabsList>
          </CardHeader>

          <CardContent className="pt-6">
            {/* User Management Tab */}
            <TabsContent value="users" className="space-y-4">
              <div className="flex justify-between items-center">
                <h3 className="text-lg font-semibold text-gray-900">User List</h3>
                <Button className="gap-2 bg-blue-600 hover:bg-blue-700">
                  <Plus className="w-4 h-4" />
                  Add User
                </Button>
              </div>
              <div className="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Name</TableHead>
                      <TableHead>Email</TableHead>
                      <TableHead>Role</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {users.map((user) => (
                      <TableRow key={user.id}>
                        <TableCell className="font-medium">{user.name}</TableCell>
                        <TableCell>{user.email}</TableCell>
                        <TableCell>{user.role}</TableCell>
                        <TableCell>
                          <Badge
                            variant="outline"
                            className={
                              user.status === "Active"
                                ? "bg-green-100 text-green-700 border-green-200"
                                : "bg-gray-100 text-gray-700 border-gray-200"
                            }
                          >
                            {user.status}
                          </Badge>
                        </TableCell>
                        <TableCell>
                          <div className="flex gap-2">
                            <Button variant="outline" size="sm" className="gap-1">
                              <Edit className="w-3 h-3" />
                              Edit
                            </Button>
                            <Button variant="outline" size="sm" className="gap-1 text-red-600 hover:bg-red-50">
                              <Trash2 className="w-3 h-3" />
                              Delete
                            </Button>
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </TabsContent>

            {/* System Settings Tab */}
            <TabsContent value="settings" className="space-y-6">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Water Level Thresholds</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-2xl">
                  <div className="space-y-2">
                    <Label htmlFor="thresholdKRL">KRL Warning Threshold (cm)</Label>
                    <Input
                      id="thresholdKRL"
                      type="number"
                      value={thresholdKRL}
                      onChange={(e) => setThresholdKRL(e.target.value)}
                    />
                    <p className="text-sm text-gray-500">Current: 60 cm</p>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="thresholdKAI">KAI Warning Threshold (cm)</Label>
                    <Input
                      id="thresholdKAI"
                      type="number"
                      value={thresholdKAI}
                      onChange={(e) => setThresholdKAI(e.target.value)}
                    />
                    <p className="text-sm text-gray-500">Current: 70 cm</p>
                  </div>
                </div>
                <Button className="mt-4 bg-blue-600 hover:bg-blue-700">
                  Save Settings
                </Button>
              </div>

              <div className="border-t pt-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Alert Configuration</h3>
                <div className="space-y-4 max-w-2xl">
                  <div className="flex items-center justify-between p-4 border rounded-lg">
                    <div>
                      <p className="font-medium text-gray-900">Email Notifications</p>
                      <p className="text-sm text-gray-500">Receive alerts via email</p>
                    </div>
                    <Button variant="outline">Configure</Button>
                  </div>
                  <div className="flex items-center justify-between p-4 border rounded-lg">
                    <div>
                      <p className="font-medium text-gray-900">SMS Notifications</p>
                      <p className="text-sm text-gray-500">Receive alerts via SMS</p>
                    </div>
                    <Button variant="outline">Configure</Button>
                  </div>
                </div>
              </div>
            </TabsContent>

            {/* Sensors Tab */}
            <TabsContent value="sensors" className="space-y-4">
              <div className="flex justify-between items-center">
                <h3 className="text-lg font-semibold text-gray-900">Sensor Configuration</h3>
                <Button className="gap-2 bg-blue-600 hover:bg-blue-700">
                  <Plus className="w-4 h-4" />
                  Add Sensor
                </Button>
              </div>
              <div className="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Sensor Name</TableHead>
                      <TableHead>Location</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Last Calibration</TableHead>
                      <TableHead>Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {sensors.map((sensor) => (
                      <TableRow key={sensor.id}>
                        <TableCell className="font-medium">{sensor.name}</TableCell>
                        <TableCell>{sensor.location}</TableCell>
                        <TableCell>
                          <Badge
                            variant="outline"
                            className={
                              sensor.status === "Online"
                                ? "bg-green-100 text-green-700 border-green-200"
                                : "bg-red-100 text-red-700 border-red-200"
                            }
                          >
                            {sensor.status}
                          </Badge>
                        </TableCell>
                        <TableCell>{sensor.lastCalibration}</TableCell>
                        <TableCell>
                          <div className="flex gap-2">
                            <Button variant="outline" size="sm">
                              Calibrate
                            </Button>
                            <Button variant="outline" size="sm">
                              Configure
                            </Button>
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </TabsContent>

            {/* Logs Tab */}
            <TabsContent value="logs" className="space-y-6">
              {/* Activity Logs */}
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Activity Logs</h3>
                <div className="overflow-x-auto">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>User</TableHead>
                        <TableHead>Action</TableHead>
                        <TableHead>Timestamp</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {activityLogs.map((log) => (
                        <TableRow key={log.id}>
                          <TableCell className="font-medium">{log.user}</TableCell>
                          <TableCell>{log.action}</TableCell>
                          <TableCell className="text-gray-500">{log.timestamp}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </div>

              {/* Error Logs */}
              <div className="border-t pt-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Error Logs</h3>
                <div className="space-y-3">
                  {errorLogs.map((log) => (
                    <div
                      key={log.id}
                      className={`p-4 rounded-lg border-l-4 ${
                        log.severity === "High"
                          ? "bg-red-50 border-red-500"
                          : log.severity === "Medium"
                          ? "bg-yellow-50 border-yellow-500"
                          : "bg-blue-50 border-blue-500"
                      }`}
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex items-start gap-3">
                          <AlertCircle
                            className={`w-5 h-5 mt-0.5 ${
                              log.severity === "High"
                                ? "text-red-600"
                                : log.severity === "Medium"
                                ? "text-yellow-600"
                                : "text-blue-600"
                            }`}
                          />
                          <div>
                            <p className="font-medium text-gray-900">{log.error}</p>
                            <p className="text-sm text-gray-500 mt-1">{log.timestamp}</p>
                          </div>
                        </div>
                        <Badge
                          variant="outline"
                          className={
                            log.severity === "High"
                              ? "bg-red-100 text-red-700 border-red-200"
                              : log.severity === "Medium"
                              ? "bg-yellow-100 text-yellow-700 border-yellow-200"
                              : "bg-blue-100 text-blue-700 border-blue-200"
                          }
                        >
                          {log.severity}
                        </Badge>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </TabsContent>
          </CardContent>
        </Tabs>
      </Card>
    </div>
  );
}
