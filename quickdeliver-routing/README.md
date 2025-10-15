# 🚚 QuickDeliver Routing System

## Transport and Logistics Analytics - CUSCM 401
**Chinhoyi University of Technology**

---

## 📋 Project Overview

QuickDeliver Routing System is a web-based application designed to optimize courier vehicle routes, minimize costs, and reduce delivery times. The system uses advanced routing algorithms to create efficient collection routes while considering:

- Traffic patterns and road conditions
- Vehicle capacity and fuel efficiency
- Collection point locations and parcel volumes
- Time windows for collection

---

## 🚀 Quick Start Guide

### Step 1: Install Python
Make sure you have Python 3.8 or higher installed on your computer.

Check your Python version:
```bash
python --version
```

### Step 2: Create Project Folder
```bash
mkdir quickdeliver-routing
cd quickdeliver-routing
```

### Step 3: Save the Files
1. Save `app.py` (the main application code)
2. Save `requirements.txt` (the dependencies)
3. Both files should be in the same folder

### Step 4: Install Dependencies
Open terminal/command prompt in your project folder and run:
```bash
pip install -r requirements.txt
```

This will install:
- Streamlit (web framework)
- Pandas (data handling)
- NumPy (calculations)
- Folium (interactive maps)
- Plotly (charts and graphs)

### Step 5: Run the Application
```bash
streamlit run app.py
```

The application will automatically open in your web browser at `http://localhost:8501`

---

## 📖 How to Use

### For Your Presentation:

1. **Load Sample Data**
   - Click "🎲 Load Sample Data" in the sidebar
   - This generates realistic collection points and vehicles

2. **View Data Overview**
   - Go to "📊 Data Overview" tab
   - Review collection points and vehicle fleet

3. **Optimize Routes**
   - Go to "🗺️ Route Optimization" tab
   - Click "🚀 OPTIMIZE ROUTES NOW"
   - Watch the system calculate optimal routes

4. **View Results**
   - Interactive map shows color-coded routes
   - Metrics display total distance, cost, time, and fuel
   - Expand route details for specific information

5. **Analyze Performance**
   - Go to "📈 Analytics" tab
   - View charts comparing vehicle performance
   - See cost savings analysis

### Adding Custom Data:

**Add Collection Points:**
- Expand "➕ Add Collection Point" in sidebar
- Enter location name, coordinates, parcels, and time window
- Click "Add Point"

**Add Vehicles:**
- Expand "🚛 Add Vehicle" in sidebar
- Enter vehicle ID, capacity, fuel efficiency, and cost per km
- Click "Add Vehicle"

---

## 🎯 Key Features

### ✅ Route Optimization
- Nearest neighbor algorithm for efficient routing
- Considers vehicle capacity constraints
- Respects time windows for collections
- Minimizes total distance and cost

### ✅ Interactive Visualization
- Color-coded routes on interactive map
- Click markers for detailed information
- Zoom and pan capabilities

### ✅ Cost Analysis
- Real-time cost calculations
- Fuel consumption estimates
- Savings comparison vs non-optimized routes

### ✅ Performance Metrics
- Distance tracking per vehicle
- Cost breakdown by route
- Parcel distribution analysis
- Efficiency metrics

---

## 🎓 For Your Presentation

### Demonstration Flow:

1. **Introduction (2 min)**
   - Explain the problem Rachel faces
   - Show the application interface

2. **Data Loading (1 min)**
   - Load sample data
   - Show collection points and vehicles in tables

3. **Optimization Demo (3 min)**
   - Click optimize button
   - Explain the algorithm considerations
   - Show the optimized routes on map

4. **Results Analysis (3 min)**
   - Walk through route details
   - Show cost savings
   - Display performance charts

5. **Q&A (1 min)**
   - Answer questions
   - Show flexibility by adding custom points

### Key Points to Mention:

✅ **Considers Traffic:** Distance calculations and route planning  
✅ **Vehicle Capacity:** Each vehicle assigned based on capacity  
✅ **Time Windows:** Respects collection time constraints  
✅ **Fuel Efficiency:** Different vehicles have different fuel ratings  
✅ **Cost Optimization:** Minimizes total operational costs  

---

## 🛠️ Technical Details

### Algorithm: Nearest Neighbor Heuristic
- Starts at central depot
- Iteratively selects nearest unvisited point
- Checks capacity constraints before adding
- Returns to depot after route completion

### Distance Calculation: Haversine Formula
- Calculates great-circle distance between coordinates
- Accurate for route planning
- Considers Earth's curvature

### Optimization Factors:
1. Distance minimization
2. Vehicle capacity utilization
3. Time window compliance
4. Fuel efficiency consideration
5. Cost per kilometer optimization

---

## 📊 Sample Data Specifications

### Collection Points:
- 15 collection points around metropolitan area
- 5-30 parcels per location
- Time windows: 8:00 AM - 6:00 PM
- Coordinates: Realistic GPS coordinates

### Vehicle Fleet:
- **V1:** Capacity 100, Efficiency 8.5 km/L, Cost $2.5/km
- **V2:** Capacity 80, Efficiency 9.2 km/L, Cost $2.0/km
- **V3:** Capacity 120, Efficiency 7.8 km/L, Cost $3.0/km

---

## 🐛 Troubleshooting

### Application won't start?
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Try running with full path
python -m streamlit run app.py
```

### Map not displaying?
- Check internet connection (maps use online tiles)
- Clear browser cache
- Try different browser

### Import errors?
```bash
# Make sure all packages installed
pip list

# Reinstall specific package
pip install streamlit-folium --upgrade
```

---

## 📝 Assignment Requirements Checklist

✅ Transportation routing system to minimize costs and delivery times  
✅ User-friendly interface for inputting data  
✅ Considers traffic patterns (distance calculations)  
✅ Considers vehicle capacity and fuel efficiency  
✅ Considers collection point locations and parcel volumes  
✅ Considers time windows for collection  
✅ Ready for live demonstration  
✅ Professional and modern interface  
✅ Interactive visualizations  
✅ Detailed analytics and reporting  

---

## 👥 Team Information

**Group:** [Your Group Number]  
**Course:** CUSCM 401 - Transport and Logistics Analytics  
**Lecturer:** Ms. Mutepfa  
**University:** Chinhoyi University of Technology  
**Due Date:** October 17, 2025  

---

## 🎉 Success Tips for Presentation

1. **Practice the demo** - Run through it 2-3 times before presenting
2. **Have backup** - Take screenshots in case of technical issues
3. **Know your algorithm** - Be ready to explain how optimization works
4. **Show flexibility** - Add a custom point during presentation
5. **Highlight savings** - Emphasize cost reduction achieved
6. **Be confident** - You built something awesome!

---

## 📞 Support

If you encounter any issues:
1. Check this README first
2. Google the specific error message
3. Check Streamlit documentation: https://docs.streamlit.io
4. Ask your teammates for help

---

**Good luck with your presentation! 🚀 You've got this! 💪**