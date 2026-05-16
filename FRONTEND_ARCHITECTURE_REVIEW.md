# FLOOD MONITORING SYSTEM - FRONTEND ARCHITECTURE REVIEW
**Generated: May 16, 2026 | Framework: React + Vite + TypeScript + Tailwind CSS**

---

## 1. PROJECT STRUCTURE

```
capstone-web/
├── src/
│   ├── main.tsx                    # Entry point, renders App to #root
│   ├── app/
│   │   ├── App.tsx                 # Router provider wrapper
│   │   ├── routes.tsx              # React Router v7 config
│   │   ├── pages/
│   │   │   ├── LoginPage.tsx        # Auth page (no protection yet)
│   │   │   ├── Dashboard.tsx        # Main monitoring dashboard
│   │   │   ├── DataPage.tsx         # Historical data & export
│   │   │   └── AdminPanel.tsx       # Admin & system management
│   │   └── components/
│   │       ├── DashboardLayout.tsx  # Sidebar + top bar + outlet
│   │       ├── figma/
│   │       │   └── ImageWithFallback.tsx
│   │       └── ui/                 # 30+ Shadcn UI components
│   │           ├── button.tsx
│   │           ├── card.tsx
│   │           ├── input.tsx
│   │           ├── table.tsx
│   │           ├── badge.tsx
│   │           ├── select.tsx
│   │           ├── tabs.tsx
│   │           └── ... (more UI primitives)
│   └── styles/
│       └── index.css               # Tailwind imports & globals
├── package.json                    # 287 packages (React, Vite, etc)
├── vite.config.ts                  # Vite build config
├── tailwind.config.ts              # Tailwind theming
├── tsconfig.json                   # TypeScript strict mode
└── .gitignore

```

---

## 2. CORE DEPENDENCIES & VERSIONS

### Production Dependencies (`package.json`)
```json
{
  "react": "18.3.1",                    // UI library
  "react-dom": "18.3.1",
  "react-router": "7.13.0",             // Routing (v7, not v6)
  "vite": "6.3.5",                      // Build tool
  
  // UI Components (Shadcn + Radix)
  "@radix-ui/react-*": "1.x",           // 20+ packages for accessible components
  "@mui/material": "7.3.5",
  "@mui/icons-material": "7.3.5",
  
  // Charts & Visualization
  "recharts": "2.15.2",                 // Line/Bar charts
  
  // Form & Input
  "react-hook-form": "7.55.0",
  "input-otp": "1.4.2",
  
  // Styling & Utilities
  "tailwindcss": "4.1.12",
  "tailwind-merge": "3.2.0",
  "class-variance-authority": "0.7.1",
  "clsx": "2.1.1",
  
  // Drag & Drop
  "react-dnd": "16.0.1",
  "react-dnd-html5-backend": "16.0.1",
  
  // Notifications & UI
  "sonner": "2.0.3",                    // Toast notifications
  "canvas-confetti": "1.9.4",           // Confetti effect
  "lucide-react": "0.487.0",            // Icon library
  
  // Utilities
  "date-fns": "3.6.0",
  "motion": "12.23.24"
}
```

### Dev Dependencies
```json
{
  "typescript": "latest",
  "@vitejs/plugin-react": "4.7.0",
  "tailwindcss": "^4.1.12",
  "autoprefixer": "^10.4.27",
  "postcss": "^8.5.9"
}
```

---

## 3. ROUTING ARCHITECTURE

**File: `src/app/routes.tsx`**

```tsx
// React Router v7 Configuration
export const router = createBrowserRouter([
  {
    path: "/",
    element: <LoginPage />,          // Public route - NO PROTECTION
  },
  {
    path: "/",
    element: <DashboardLayout />,    // Protected layout container
    children: [
      {
        path: "dashboard",
        element: <Dashboard />,       // Real-time monitoring
      },
      {
        path: "data",
        element: <DataPage />,        // Historical data & analytics
      },
      {
        path: "admin",
        element: <AdminPanel />,      // System administration
      },
    ],
  },
]);
```

### Current Routing Issues (⚠️ IMPORTANT FOR BACKEND):
- **No authentication middleware** - Any user can access all routes
- **No role-based access control** - No validation of user permissions
- **Login doesn't validate** - Just redirects to dashboard
- **No token management** - No localStorage/sessionStorage usage detected
- **No protected routes** - DashboardLayout accessible without login

**BACKEND NEEDS TO IMPLEMENT:**
1. JWT/token-based authentication
2. Route guards/middleware
3. Login validation API
4. Role-based route protection

---

## 4. PAGE COMPONENTS DETAILED BREAKDOWN

### A. LoginPage.tsx (Lines: ~130)
**Location:** `src/app/pages/LoginPage.tsx`

#### Constants:
```tsx
// No global constants - mock data embedded
```

#### State Variables:
```tsx
const [email, setEmail] = useState("");      // User email/username input
const [password, setPassword] = useState(""); // User password input
const [role, setRole] = useState("");        // Selected role (UI element not functional)
```

#### Key Functions:
```tsx
const handleLogin = (e: React.FormEvent) => {
  e.preventDefault();
  // TODO: Add API call here
  // Current: Just navigates without validation
  navigate("/dashboard");
};
```

#### UI Structure:
- **Background:** Gradient with unsplash image overlay
- **Card:** Email input, Password input, Role selector (unused)
- **Button:** Sign In (gradient blue)
- **Links:** "Forgot password?" (non-functional)

#### Expected Backend Integration:
```tsx
// NEEDED: Add API endpoint
const handleLogin = async (e: React.FormEvent) => {
  e.preventDefault();
  try {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    const { token, user } = await response.json();
    localStorage.setItem('authToken', token);
    localStorage.setItem('userRole', user.role);
    navigate("/dashboard");
  } catch (error) {
    console.error('Login failed', error);
  }
};
```

---

### B. Dashboard.tsx (Lines: ~310)
**Location:** `src/app/pages/Dashboard.tsx`

#### Mock Data Constants:
```tsx
const waterLevelData = [
  { time: "00:00", KRL: 45, KAI: 52 },
  { time: "04:00", KRL: 48, KAI: 55 },
  // ... 6 entries total
];

const rainIntensityData = [
  { time: "00:00", intensity: 2 },
  // ... 6 entries total
];

const monitoringData = [
  { 
    location: "Manggarai Station", 
    rainStatus: "Heavy", 
    waterLevel: 65, 
    status: "WARNING",  // SAFE | WARNING | CRITICAL
    lastUpdate: "2 min ago" 
  },
  // ... 5 locations total
];

const alerts = [
  {
    id: 1,
    type: "critical",     // critical | warning | info
    message: "Critical water level at Jatinegara Station (72 cm)",
    time: "2 minutes ago",
  },
  // ... 3 alerts total
];
```

#### Key Functions:
```tsx
const getStatusColor = (status: string) => {
  // Returns Tailwind classes based on status
  // SAFE → green, WARNING → yellow, CRITICAL → red
};

const getFloodStatus = () => {
  // Calculates overall system status from monitoring data
  // Returns: { label, color, icon }
  // TOTAL STOP (≥70cm), KRL STOP (≥60cm), AMAN (<60cm)
};
```

#### UI Components Used:
- `Card, CardContent, CardHeader, CardTitle` - Data containers
- `Badge` - Status indicators
- `LineChart, BarChart` from recharts
- `Table, TableBody, TableCell, etc` - Data tables
- Icons from lucide-react

#### Data Flow:
```
Mock Constants → Component State → UI Rendering
```

#### Backend Integration Needed:
```tsx
// Add state management
const [dashboardData, setDashboardData] = useState(null);
const [loading, setLoading] = useState(true);

// Add effect to fetch real data
useEffect(() => {
  fetchDashboardData();
}, []);

const fetchDashboardData = async () => {
  const response = await fetch('/api/dashboard/realtime', {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  const data = await response.json();
  setDashboardData(data);
  setLoading(false);
};
```

---

### C. DataPage.tsx (Lines: ~300)
**Location:** `src/app/pages/DataPage.tsx`

#### State Variables:
```tsx
const [dateFrom, setDateFrom] = useState("2026-03-31");
const [dateTo, setDateTo] = useState("2026-03-31");
const [location, setLocation] = useState("all");         // Filter: all|manggarai|tanah-abang|gambir|jatinegara|bekasi
const [statusFilter, setStatusFilter] = useState("all"); // Filter: all|safe|warning|critical
```

#### Mock Constants:
```tsx
const historicalData = [
  {
    timestamp: "2026-03-31 14:00",
    rain: 15,
    waterLevelKRL: 65,
    waterLevelKAI: 72,
    status: "WARNING",  // Data status
  },
  // ... 7 entries total
];

const trendData = [
  { time: "08:00", KRL: 40, KAI: 45 },
  // Chart data points
];

const rainData = [
  { time: "08:00", rain: 1 },
  // Chart data points
];
```

#### Key Functions:
```tsx
const getStatusColor = (status: string) => {
  // Returns Tailwind badge classes
};

const handleExport = (format: string) => {
  // format: 'csv' | 'pdf'
  alert(`Exporting data as ${format.toUpperCase()}...`);
  // TODO: Implement actual export
};
```

#### UI Components:
- Filter section (Date From/To, Location Select, Status Select)
- Action buttons (Apply Filters, Reset)
- Charts (LineChart for water levels, BarChart for rain)
- Data table with pagination placeholders
- Export buttons

#### Backend Integration Needed:
```tsx
// Need API endpoints:
// GET /api/data/historical?dateFrom=X&dateTo=Y&location=Z&status=W
// POST /api/data/export?format=csv|pdf
// GET /api/data/trends (for chart data)

const handleApplyFilters = async () => {
  const queryParams = new URLSearchParams({
    dateFrom,
    dateTo,
    location: location !== 'all' ? location : '',
    status: statusFilter !== 'all' ? statusFilter : '',
  });
  
  const response = await fetch(
    `/api/data/historical?${queryParams}`,
    { headers: { 'Authorization': `Bearer ${token}` } }
  );
  const data = await response.json();
  setHistoricalData(data);
};
```

---

### D. AdminPanel.tsx (Lines: ~391)
**Location:** `src/app/pages/AdminPanel.tsx`

#### Mock Data Constants:
```tsx
const users = [
  { id: 1, name: "John Doe", email: "john@railway.com", role: "Head of Station", status: "Active" },
  { id: 2, name: "Jane Smith", email: "jane@railway.com", role: "Field Officer", status: "Active" },
  // ... 4 total
];

const sensors = [
  { id: 1, name: "Sensor MG-01", location: "Manggarai", status: "Online", lastCalibration: "2026-03-25" },
  // ... 4 total
];

const activityLogs = [
  { id: 1, user: "John Doe", action: "Updated water level threshold", timestamp: "2026-03-31 14:30" },
  // ... 5 total
];

const errorLogs = [
  { id: 1, error: "Sensor GB-01 connection timeout", severity: "High", timestamp: "2026-03-31 14:20" },
  // ... 3 total
];
```

#### State Variables:
```tsx
const [thresholdKRL, setThresholdKRL] = useState("60");   // Water level threshold
const [thresholdKAI, setThresholdKAI] = useState("70");   // Water level threshold
```

#### Tabs:
1. **Users Tab**
   - User table with edit/delete buttons (non-functional)
   - Add user button

2. **Settings Tab**
   - Threshold adjustments (KRL, KAI)
   - Save thresholds button

3. **Sensors Tab**
   - Sensor status table
   - Calibration button per sensor

4. **Logs Tab**
   - Activity logs
   - Error logs
   - System logs

#### Backend Integration Needed:
```tsx
// User Management API
GET /api/admin/users
POST /api/admin/users
PUT /api/admin/users/{id}
DELETE /api/admin/users/{id}

// Sensor Management
GET /api/admin/sensors
PUT /api/admin/sensors/{id}/calibrate

// Settings/Thresholds
PUT /api/admin/settings/thresholds
GET /api/admin/logs/activity
GET /api/admin/logs/error
```

---

## 5. COMPONENT HIERARCHY

```
App.tsx (RouterProvider)
└── routes.tsx (BrowserRouter)
    ├── LoginPage
    └── DashboardLayout
        ├── Top Navigation Bar
        │   ├── Sidebar toggle
        │   ├── User menu
        │   └── Settings
        ├── Sidebar (Desktop & Mobile)
        │   ├── Logo
        │   ├── Navigation Items
        │   │   ├── Dashboard
        │   │   ├── Data
        │   │   └── Admin
        │   └── Logout Button
        └── Main Content (Outlet)
            ├── Dashboard (when at /dashboard)
            ├── DataPage (when at /data)
            └── AdminPanel (when at /admin)
```

---

## 6. DASHBOARD LAYOUT DETAILS

**File: `src/app/components/DashboardLayout.tsx`**

#### Constants (Menu Items):
```tsx
const menuItems = [
  { path: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { path: "/data", label: "Data", icon: Database },
  { path: "/admin", label: "Admin Panel", icon: Settings },
];
```

#### State:
```tsx
const [sidebarOpen, setSidebarOpen] = useState(false); // Mobile sidebar toggle
const navigate = useNavigate();                        // React Router navigation
const location = useLocation();                        // Current route
```

#### Key Functions:
```tsx
const handleLogout = () => {
  // TODO: Clear auth token and user data
  navigate("/");
};
```

#### Features:
- **Desktop Sidebar:** Fixed left sidebar (hidden <lg, visible ≥lg)
- **Mobile Sidebar:** Toggle with overlay backdrop
- **Active Link Highlighting:** Based on `location.pathname`
- **Top Bar:** Sticky header with mobile menu toggle
- **Outlet:** Renders nested route components

---

## 7. UI COMPONENT PRIMITIVES

**Location:** `src/app/components/ui/`

### Available Components (30+):
```
button.tsx           - Variant: primary|secondary|outline|ghost
card.tsx            - CardHeader, CardTitle, CardContent
input.tsx           - Text input with focus styles
label.tsx          - Form labels
select.tsx         - Dropdown with SelectTrigger, SelectContent, SelectItem
table.tsx          - Table structure (TableHeader, TableBody, TableRow, etc)
badge.tsx          - Status badges
tabs.tsx           - Tab navigation (TabsList, TabsTrigger, TabsContent)
tooltip.tsx        - Hover tooltips
dialog.tsx         - Modal dialogs
dropdown-menu.tsx  - Context menus
pagination.tsx     - Pagination controls
sidebar.tsx        - Sidebar component
avatar.tsx         - User avatars
skeleton.tsx       - Loading skeletons
... (and 15+ more)
```

### Styling Approach:
- **Framework:** Tailwind CSS v4.1.12
- **Pattern:** Utility-first CSS classes
- **Color Palette:**
  - Blue: `text-blue-500`, `bg-blue-50`, `border-blue-200`
  - Green (Success): `text-green-700`, `bg-green-100`
  - Yellow (Warning): `text-yellow-700`, `bg-yellow-100`
  - Red (Critical): `text-red-700`, `bg-red-100`
  - Gray (Neutral): Various shades for text, backgrounds, borders

---

## 8. DATA FLOW & STATE MANAGEMENT

### Current Architecture:
```
Component Level State (useState)
    ↓
Mock Data Constants (hardcoded)
    ↓
UI Rendering
```

### Issues:
- **No Context API** - No global state management
- **No Redux** - State isolated to each component
- **No API service layer** - All data is mocked
- **No Error handling** - No try/catch blocks

### Recommended Pattern for Backend Integration:
```tsx
// Option 1: React Query (recommended for data fetching)
import { useQuery, useMutation } from '@tanstack/react-query';

const { data: dashboardData, isLoading } = useQuery({
  queryKey: ['dashboard'],
  queryFn: () => fetch('/api/dashboard').then(r => r.json())
});

// Option 2: Context + useReducer (for auth state)
const AuthContext = createContext();

// Option 3: Custom hooks
const useDashboardData = () => {
  const [data, setData] = useState(null);
  useEffect(() => {
    fetch('/api/dashboard').then(r => r.json()).then(setData);
  }, []);
  return data;
};
```

---

## 9. FORMS & VALIDATION

### Current Status:
- **No form validation** - No react-hook-form usage detected
- **Basic onChange handlers** - Input values stored directly in state
- **No error messages** - No validation feedback

### Form Locations:
1. **LoginPage:** Email, Password fields
2. **DataPage:** Date filters, Location select, Status select
3. **AdminPanel:** Settings inputs, Threshold values
4. **AdminPanel:** User add/edit forms (non-functional)

### Backend Integration for Forms:
```tsx
// Use react-hook-form (already in dependencies)
import { useForm } from 'react-hook-form';

const { register, handleSubmit, formState: { errors } } = useForm({
  defaultValues: {
    email: '',
    password: '',
  }
});

const onSubmit = async (data) => {
  const response = await fetch('/api/auth/login', {
    method: 'POST',
    body: JSON.stringify(data)
  });
  // handle response
};
```

---

## 10. ICONS & ICONOGRAPHY

**Library:** lucide-react v0.487.0

### Icons Used:
```tsx
// Navigation
LayoutDashboard    // Dashboard route
Database          // Data route
Settings          // Admin route
Droplets          // Water/flood theme
LogOut            // Logout button

// Data
CloudRain         // Rain status
AlertTriangle     // Warnings/Critical
CheckCircle       // Status OK
Clock             // Time indicators

// UI
Menu, X           // Mobile sidebar toggle
Download          // Export buttons
Filter            // Filter section
Calendar          // Date pickers
Mail              // Email fields
Lock              // Password fields

// Admin
Users             // User management
Activity          // Activity logs
Wifi              // Network status
Server            // Server status
Radio             // Sensor status
Plus              // Add new
Edit              // Edit action
Trash2            // Delete action
```

---

## 11. STYLING & THEMING

### Tailwind Configuration:
- **Colors:** Customizable via `tailwind.config.ts`
- **Responsive:** `sm`, `md`, `lg`, `xl` breakpoints
- **Dark Mode:** Not implemented
- **Custom Utilities:** class-variance-authority for component variants

### Common Patterns:
```tsx
// Spacing
className="p-4"    // Padding
className="mb-2"   // Margin bottom
className="gap-2"  // Grid/flex gap

// Grid/Flex
className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4"
className="flex items-center justify-between gap-2"

// Responsive
className="hidden lg:block"        // Hide on mobile
className="flex flex-col md:flex-row" // Stack on mobile
className="w-full md:w-1/2"        // Width adjusts

// Colors
className="text-gray-900"         // Dark text
className="bg-blue-50"           // Light blue background
className="border-gray-200"      // Light gray border

// Status
className="bg-green-100 text-green-700 border-green-200"  // SAFE
className="bg-yellow-100 text-yellow-700 border-yellow-200" // WARNING
className="bg-red-100 text-red-700 border-red-200"        // CRITICAL
```

---

## 12. CHARTS & VISUALIZATION

**Library:** recharts v2.15.2

### Chart Usage:
```tsx
// Water Level Trends (LineChart)
<LineChart data={trendData}>
  <CartesianGrid strokeDasharray="3 3" />
  <XAxis dataKey="time" />
  <YAxis label={{ value: 'cm', angle: -90 }} />
  <Line dataKey="KRL" stroke="#3b82f6" strokeWidth={2} />
  <Line dataKey="KAI" stroke="#8b5cf6" strokeWidth={2} />
</LineChart>

// Rain Intensity (BarChart)
<BarChart data={rainData}>
  <XAxis dataKey="time" />
  <YAxis label={{ value: 'mm/h', angle: -90 }} />
  <Bar dataKey="rain" fill="#3b82f6" radius={[8, 8, 0, 0]} />
</BarChart>
```

### Chart Data Format:
```tsx
// Requires array of objects with consistent keys
const data = [
  { time: "08:00", KRL: 40, KAI: 45 },
  { time: "09:00", KRL: 42, KAI: 48 },
  { time: "10:00", KRL: 45, KAI: 52 },
];

// Dynamic data binding - charts update when data changes
```

---

## 13. TABLES & DATA DISPLAY

### Table Structure (Shadcn):
```tsx
<Table>
  <TableHeader>
    <TableRow>
      <TableHead>Column 1</TableHead>
      <TableHead>Column 2</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    {data.map((item, index) => (
      <TableRow key={index}>
        <TableCell>{item.field1}</TableCell>
        <TableCell>{item.field2}</TableCell>
      </TableRow>
    ))}
  </TableBody>
</Table>
```

### Tables in App:
1. **Dashboard:** Monitoring data table (5 locations)
2. **DataPage:** Historical data table (7 rows + pagination)
3. **AdminPanel:** Users table (4 users)
4. **AdminPanel:** Sensors table (4 sensors)
5. **AdminPanel:** Activity logs (5 entries)
6. **AdminPanel:** Error logs (3 entries)

### Current Issues:
- **No pagination** - Shows all rows
- **No sorting** - Can't sort columns
- **No filtering** - Filter UI present but not functional
- **No inline editing** - Edit/Delete buttons non-functional

---

## 14. RESPONSIVE DESIGN

### Breakpoints Used:
```tsx
// Mobile first
className="..."           // Mobile default
className="sm:..."        // ≥640px
className="md:..."        // ≥768px
className="lg:..."        // ≥1024px
className="xl:..."        // ≥1280px
```

### Responsive Components:
1. **Sidebar:** Hidden on mobile, toggle via menu button
2. **Grid layouts:** 1 column on mobile → 4 columns on desktop
3. **Tables:** Scroll on mobile, full width on desktop
4. **Forms:** Stacked inputs on mobile, side-by-side on desktop

### Mobile Considerations:
- Touch-friendly buttons (min 44px)
- Collapsible navigation
- Font sizes scale appropriately
- Spacing adjusts via Tailwind classes

---

## 15. BACKEND INTEGRATION CHECKLIST

### ✅ Authentication APIs Needed:
- [ ] POST `/api/auth/login` - Username/email + password → Token
- [ ] POST `/api/auth/logout` - Clear session
- [ ] POST `/api/auth/refresh` - Refresh expired token
- [ ] GET `/api/auth/verify` - Check token validity
- [ ] GET `/api/auth/me` - Get current user info

### ✅ Dashboard APIs Needed:
- [ ] GET `/api/dashboard/realtime` - Live water levels, rain info
- [ ] GET `/api/dashboard/alerts` - Active alerts
- [ ] GET `/api/dashboard/monitoring-status` - All station statuses
- [ ] WebSocket `/ws/dashboard` - Real-time updates

### ✅ Data Page APIs Needed:
- [ ] GET `/api/data/historical?dateFrom=X&dateTo=Y&location=Z&status=W`
- [ ] GET `/api/data/trends` - Chart data for trends
- [ ] POST `/api/data/export?format=csv|pdf` - Export functionality
- [ ] GET `/api/data/locations` - Available locations

### ✅ Admin Panel APIs Needed:
- [ ] CRUD `/api/admin/users` - User management
- [ ] GET `/api/admin/sensors` - Sensor list
- [ ] PUT `/api/admin/sensors/{id}/calibrate` - Calibrate sensor
- [ ] POST `/api/admin/sensors/{id}/test` - Test sensor
- [ ] PUT `/api/admin/settings/thresholds` - Update alert thresholds
- [ ] GET `/api/admin/logs/activity` - Activity audit logs
- [ ] GET `/api/admin/logs/error` - System error logs
- [ ] PUT `/api/admin/settings/notifications` - Alert preferences

### ✅ Real-time Data APIs:
- [ ] WebSocket support for streaming sensor data
- [ ] Server-sent events (SSE) for alerts
- [ ] MQTT integration (optional, for IoT sensors)

### ✅ Error Handling Needed:
- [ ] 401 Unauthorized - Redirect to login
- [ ] 403 Forbidden - Show permission error
- [ ] 404 Not Found - Display error message
- [ ] 500 Server Error - Show retry option
- [ ] Network timeout - Handle offline scenarios

---

## 16. SECURITY CONSIDERATIONS

### Current Gaps:
1. **No CSRF protection** - No tokens in forms
2. **No input sanitization** - No XSS protection
3. **No rate limiting** - Login not rate limited
4. **No session timeout** - No auto-logout
5. **Credentials in logs** - Password visible in form data

### Recommended Fixes:
```tsx
// Store token in secure httpOnly cookie (backend)
// OR localStorage with careful handling

// Sanitize user inputs
import DOMPurify from 'dompurify';
const cleanHtml = DOMPurify.sanitize(userInput);

// Add CSRF token to forms
<form>
  <input type="hidden" name="csrf" value={csrfToken} />
  ...
</form>

// Implement auto-logout on inactivity
const useAuthTimeout = (minutes = 15) => {
  useEffect(() => {
    let timeout;
    const resetTimer = () => {
      clearTimeout(timeout);
      timeout = setTimeout(() => {
        logout();
      }, minutes * 60 * 1000);
    };
    window.addEventListener('mousemove', resetTimer);
    return () => clearTimeout(timeout);
  }, []);
};
```

---

## 17. PERFORMANCE CONSIDERATIONS

### Current Optimization Status:
- ✅ Lazy loading components (React Router)
- ✅ CSS-in-JS minimization (Tailwind)
- ✅ Icon optimization (lucide-react)
- ❌ No data caching
- ❌ No API result caching
- ❌ No code splitting (beyond routes)
- ❌ No image optimization

### Recommendations:
```tsx
// Add React Query for caching
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5,      // 5 minutes
      cacheTime: 1000 * 60 * 10,     // 10 minutes
    },
  },
});

// Memoize expensive components
export const Dashboard = memo(DashboardComponent);

// Use useCallback for event handlers
const handleFilter = useCallback((filters) => {
  fetchData(filters);
}, [dependencies]);
```

---

## 18. TESTING CONSIDERATIONS

### Current Status:
- ❌ No unit tests
- ❌ No integration tests
- ❌ No E2E tests
- ❌ No test files present

### Files/Components Needing Tests:
1. LoginPage - Form validation, API calls
2. Dashboard - Data fetching, status calculations
3. DataPage - Filters, exports
4. AdminPanel - CRUD operations
5. DashboardLayout - Navigation, routing

### Recommended Test Stack:
```json
{
  "devDependencies": {
    "vitest": "latest",
    "@testing-library/react": "latest",
    "@testing-library/user-event": "latest",
    "msw": "latest"  // Mock Service Worker
  }
}
```

---

## 19. ENVIRONMENT & BUILD

### Build Configuration:
- **Bundler:** Vite v6.3.5
- **Build Command:** `npm run build`
- **Dev Server:** `npm run dev` (Port 5173)
- **Environment:** ES2020+ (modern browsers)

### Environment Variables Needed:
```env
VITE_API_BASE_URL=http://localhost:3000/api
VITE_WS_URL=ws://localhost:3000/ws
VITE_APP_ENV=development
```

### Vite Config:
```tsx
// vite.config.ts
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://localhost:3000'
    }
  },
  build: {
    outDir: 'dist',
    minify: 'terser'
  }
});
```

---

## 20. MIGRATION PATH TO BACKEND

### Phase 1: Authentication (Week 1)
1. Create JWT token-based auth
2. Replace mock login with API call
3. Add token storage (localStorage)
4. Implement route guards
5. Add logout functionality

### Phase 2: Real-time Data (Week 2)
1. Create REST API for dashboard metrics
2. Replace mock data with API calls
3. Add loading states + error handling
4. Implement real-time WebSocket (optional)
5. Add data caching

### Phase 3: Data Management (Week 3)
1. Create data query/ filter API
2. Implement historical data fetching
3. Add export functionality
4. Create search/pagination backend
5. Add data validation

### Phase 4: Admin Features (Week 4)
1. Implement user management API
2. Create sensor management endpoints
3. Build settings/thresholds API
4. Add audit logging
5. Implement role-based access control

---

## 21. SUMMARY: KEY FILES & THEIR PURPOSES

| File | Lines | Purpose | Backend Needed |
|------|-------|---------|---|
| `App.tsx` | 8 | Router wrapper | ✓ Auth middleware |
| `routes.tsx` | 40 | Route definitions | ✓ Route guards |
| `LoginPage.tsx` | 130 | Login form | ✓ Auth API |
| `Dashboard.tsx` | 310 | Real-time monitoring | ✓ Metrics API, WebSocket |
| `DataPage.tsx` | 300 | Historical data | ✓ Query/Export API |
| `AdminPanel.tsx` | 391 | System admin | ✓ Admin CRUD APIs |
| `DashboardLayout.tsx` | 183 | Layout container | ✓ User context |

---

## 22. RECOMMENDED NEXT STEPS

### Frontend (High Priority):
1. [ ] Add authentication context/reducer
2. [ ] Create API service layer (`services/api.ts`)
3. [ ] Add error boundary component
4. [ ] Implement loading skeletons
5. [ ] Add input validation with react-hook-form
6. [ ] Create custom hooks for API calls

### Backend (High Priority):
1. [ ] Design and implement database schema
2. [ ] Create authentication endpoints
3. [ ] Build real-time data APIs
4. [ ] Implement role-based access control
5. [ ] Create sensor data collection pipeline
6. [ ] Set up WebSocket server for real-time updates

### DevOps:
1. [ ] Docker containerization
2. [ ] CI/CD pipeline setup
3. [ ] Automated testing
4. [ ] Monitoring & logging

---

**Report Generated:** May 16, 2026  
**Last Updated:** Main branch  
**Status:** Ready for backend integration
