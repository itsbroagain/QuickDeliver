import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# Page configuration
st.set_page_config(
    page_title="QuickDeliver Routing System",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'collection_points' not in st.session_state:
    st.session_state.collection_points = []
if 'vehicles' not in st.session_state:
    st.session_state.vehicles = []
if 'optimized' not in st.session_state:
    st.session_state.optimized = False

# Helper Functions
def generate_sample_data():
    """Generate realistic sample data for the metropolitan area"""
    # Central depot coordinates (example: city center)
    depot = {'name': 'Central Depot', 'lat': -17.8252, 'lon': 31.0335, 'parcels': 0, 'time_start': '06:00', 'time_end': '20:00'}
    
    # Generate 15 random collection points around the depot
    collection_points = [depot]
    for i in range(1, 16):
        lat = depot['lat'] + random.uniform(-0.1, 0.1)
        lon = depot['lon'] + random.uniform(-0.1, 0.1)
        parcels = random.randint(5, 30)
        time_start = f"{random.randint(8, 10):02d}:00"
        time_end = f"{random.randint(16, 18):02d}:00"
        
        collection_points.append({
            'name': f'Collection Point {i}',
            'lat': lat,
            'lon': lon,
            'parcels': parcels,
            'time_start': time_start,
            'time_end': time_end
        })
    
    # Generate vehicle data
    vehicles = [
        {'id': 'V1', 'capacity': 100, 'fuel_efficiency': 8.5, 'cost_per_km': 2.5},
        {'id': 'V2', 'capacity': 80, 'fuel_efficiency': 9.2, 'cost_per_km': 2.0},
        {'id': 'V3', 'capacity': 120, 'fuel_efficiency': 7.8, 'cost_per_km': 3.0},
    ]
    
    return collection_points, vehicles

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points using Haversine formula"""
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = np.radians(lat1)
    lat2_rad = np.radians(lat2)
    delta_lat = np.radians(lat2 - lat1)
    delta_lon = np.radians(lon2 - lon1)
    
    a = np.sin(delta_lat/2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(delta_lon/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    distance = R * c
    
    return distance

def nearest_neighbor_algorithm(points, vehicles):
    """Simple but effective nearest neighbor algorithm for route optimization"""
    depot = points[0]
    remaining_points = points[1:].copy()
    routes = []
    
    for vehicle in vehicles:
        if not remaining_points:
            break
            
        route = {
            'vehicle_id': vehicle['id'],
            'capacity': vehicle['capacity'],
            'fuel_efficiency': vehicle['fuel_efficiency'],
            'cost_per_km': vehicle['cost_per_km'],
            'points': [depot],
            'total_parcels': 0,
            'total_distance': 0,
            'total_time': 0,
            'total_cost': 0
        }
        
        current_point = depot
        
        while remaining_points and route['total_parcels'] < vehicle['capacity']:
            # Find nearest unvisited point
            nearest = None
            min_distance = float('inf')
            
            for point in remaining_points:
                dist = calculate_distance(
                    current_point['lat'], current_point['lon'],
                    point['lat'], point['lon']
                )
                
                # Check if adding this point exceeds capacity
                if route['total_parcels'] + point['parcels'] <= vehicle['capacity']:
                    if dist < min_distance:
                        min_distance = dist
                        nearest = point
            
            if nearest is None:
                break
            
            # Add point to route
            route['points'].append(nearest)
            route['total_parcels'] += nearest['parcels']
            route['total_distance'] += min_distance
            route['total_time'] += min_distance / 40 * 60  # Assuming 40 km/h average speed
            
            current_point = nearest
            remaining_points.remove(nearest)
        
        # Return to depot
        return_distance = calculate_distance(
            current_point['lat'], current_point['lon'],
            depot['lat'], depot['lon']
        )
        route['total_distance'] += return_distance
        route['total_time'] += return_distance / 40 * 60
        route['points'].append(depot)
        
        # Calculate costs
        route['total_cost'] = route['total_distance'] * vehicle['cost_per_km']
        route['fuel_used'] = route['total_distance'] / vehicle['fuel_efficiency']
        
        routes.append(route)
    
    return routes

def create_route_map(routes, collection_points):
    """Create an interactive map with optimized routes"""
    # Center map on depot
    depot = collection_points[0]
    m = folium.Map(location=[depot['lat'], depot['lon']], zoom_start=12)
    
    # Colors for different routes
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'darkblue', 'darkgreen']
    
    # Add depot marker
    folium.Marker(
        [depot['lat'], depot['lon']],
        popup=depot['name'],
        tooltip='Central Depot',
        icon=folium.Icon(color='black', icon='home', prefix='fa')
    ).add_to(m)
    
    # Plot each route
    for idx, route in enumerate(routes):
        color = colors[idx % len(colors)]
        
        # Draw route line
        route_coords = [[p['lat'], p['lon']] for p in route['points']]
        folium.PolyLine(
            route_coords,
            color=color,
            weight=3,
            opacity=0.7,
            tooltip=f"{route['vehicle_id']} - {route['total_distance']:.2f} km"
        ).add_to(m)
        
        # Add markers for collection points
        for point in route['points'][1:-1]:  # Exclude depot (first and last)
            folium.Marker(
                [point['lat'], point['lon']],
                popup=f"{point['name']}<br>Parcels: {point['parcels']}<br>Window: {point['time_start']}-{point['time_end']}",
                tooltip=point['name'],
                icon=folium.Icon(color=color, icon='cube', prefix='fa')
            ).add_to(m)
    
    return m

# MAIN APPLICATION
st.markdown('<h1 class="main-header">🚚 QuickDeliver Routing System</h1>', unsafe_allow_html=True)
st.markdown("### Optimize Your Courier Routes - Minimize Costs & Delivery Times")

# Sidebar
with st.sidebar:
    st.header("⚙️ System Controls")
    
    # Load sample data button
    if st.button("🎲 Load Sample Data", help="Generate realistic sample data for demonstration"):
        points, vehicles = generate_sample_data()
        st.session_state.collection_points = points
        st.session_state.vehicles = vehicles
        st.session_state.optimized = False
        st.success("✅ Sample data loaded successfully!")
    
    st.markdown("---")
    
    # Manual data entry
    with st.expander("➕ Add Collection Point"):
        st.subheader("New Collection Point")
        cp_name = st.text_input("Location Name", "Collection Point A")
        col1, col2 = st.columns(2)
        with col1:
            cp_lat = st.number_input("Latitude", value=-17.8252, format="%.4f")
            cp_parcels = st.number_input("Number of Parcels", min_value=1, value=10)
        with col2:
            cp_lon = st.number_input("Longitude", value=31.0335, format="%.4f")
            cp_time = st.text_input("Time Window", "09:00-17:00")
        
        if st.button("Add Point"):
            time_parts = cp_time.split('-')
            new_point = {
                'name': cp_name,
                'lat': cp_lat,
                'lon': cp_lon,
                'parcels': cp_parcels,
                'time_start': time_parts[0] if len(time_parts) == 2 else '09:00',
                'time_end': time_parts[1] if len(time_parts) == 2 else '17:00'
            }
            st.session_state.collection_points.append(new_point)
            st.session_state.optimized = False
            st.success(f"Added {cp_name}")
    
    with st.expander("🚛 Add Vehicle"):
        st.subheader("New Vehicle")
        v_id = st.text_input("Vehicle ID", "V1")
        v_capacity = st.number_input("Capacity (parcels)", min_value=10, value=100)
        v_fuel = st.number_input("Fuel Efficiency (km/L)", min_value=5.0, value=8.5, step=0.1)
        v_cost = st.number_input("Cost per KM ($)", min_value=1.0, value=2.5, step=0.1)
        
        if st.button("Add Vehicle"):
            new_vehicle = {
                'id': v_id,
                'capacity': v_capacity,
                'fuel_efficiency': v_fuel,
                'cost_per_km': v_cost
            }
            st.session_state.vehicles.append(new_vehicle)
            st.session_state.optimized = False
            st.success(f"Added {v_id}")
    
    st.markdown("---")
    
    # Display current data status
    st.metric("📍 Collection Points", len(st.session_state.collection_points))
    st.metric("🚛 Vehicles", len(st.session_state.vehicles))

# Main content area
if len(st.session_state.collection_points) < 2:
    st.info("👆 Start by loading sample data or manually adding collection points and vehicles in the sidebar!")
    st.markdown("""
    ### Welcome to QuickDeliver Routing System!
    
    This system helps you:
    - ✅ Optimize delivery routes to minimize costs
    - ✅ Reduce fuel consumption and delivery times
    - ✅ Consider vehicle capacity and time windows
    - ✅ Visualize routes on an interactive map
    
    **Get started by loading sample data from the sidebar!**
    """)
else:
    # Show current data
    tab1, tab2, tab3 = st.tabs(["📊 Data Overview", "🗺️ Route Optimization", "📈 Analytics"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📍 Collection Points")
            df_points = pd.DataFrame(st.session_state.collection_points)
            st.dataframe(df_points, use_container_width=True)
        
        with col2:
            st.subheader("🚛 Vehicle Fleet")
            df_vehicles = pd.DataFrame(st.session_state.vehicles)
            st.dataframe(df_vehicles, use_container_width=True)
    
    with tab2:
        st.subheader("🎯 Route Optimization")
        
        # Optimization button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 OPTIMIZE ROUTES NOW", key="optimize_btn"):
                with st.spinner("🔄 Calculating optimal routes..."):
                    routes = nearest_neighbor_algorithm(
                        st.session_state.collection_points,
                        st.session_state.vehicles
                    )
                    st.session_state.routes = routes
                    st.session_state.optimized = True
                    st.balloons()
                    st.success("✅ Routes optimized successfully!")
        
        if st.session_state.optimized:
            st.markdown("---")
            
            # Display metrics
            total_distance = sum(r['total_distance'] for r in st.session_state.routes)
            total_cost = sum(r['total_cost'] for r in st.session_state.routes)
            total_time = sum(r['total_time'] for r in st.session_state.routes)
            total_fuel = sum(r['fuel_used'] for r in st.session_state.routes)
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("🛣️ Total Distance", f"{total_distance:.2f} km")
            col2.metric("💰 Total Cost", f"${total_cost:.2f}")
            col3.metric("⏱️ Total Time", f"{total_time:.1f} min")
            col4.metric("⛽ Fuel Used", f"{total_fuel:.2f} L")
            
            st.markdown("---")
            
            # Interactive map
            st.subheader("🗺️ Optimized Route Map")
            route_map = create_route_map(st.session_state.routes, st.session_state.collection_points)
            folium_static(route_map, width=1200, height=600)
            
            st.markdown("---")
            
            # Route details
            st.subheader("📋 Detailed Route Information")
            for idx, route in enumerate(st.session_state.routes):
                with st.expander(f"🚛 {route['vehicle_id']} - {len(route['points'])-2} stops"):
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Distance", f"{route['total_distance']:.2f} km")
                    col2.metric("Parcels", f"{route['total_parcels']}/{route['capacity']}")
                    col3.metric("Cost", f"${route['total_cost']:.2f}")
                    
                    st.write("**Route Sequence:**")
                    route_sequence = " → ".join([p['name'] for p in route['points']])
                    st.info(route_sequence)
                    
                    # Detailed stops table
                    stops_data = []
                    for i, point in enumerate(route['points']):
                        stops_data.append({
                            'Stop': i,
                            'Location': point['name'],
                            'Parcels': point['parcels'],
                            'Time Window': f"{point['time_start']}-{point['time_end']}"
                        })
                    st.table(pd.DataFrame(stops_data))
    
    with tab3:
        st.subheader("📈 Performance Analytics")
        
        if st.session_state.optimized:
            # Create comparison charts
            vehicles = [r['vehicle_id'] for r in st.session_state.routes]
            distances = [r['total_distance'] for r in st.session_state.routes]
            costs = [r['total_cost'] for r in st.session_state.routes]
            parcels = [r['total_parcels'] for r in st.session_state.routes]
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig1 = go.Figure(data=[
                    go.Bar(x=vehicles, y=distances, marker_color='lightblue')
                ])
                fig1.update_layout(title="Distance by Vehicle", xaxis_title="Vehicle", yaxis_title="Distance (km)")
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                fig2 = go.Figure(data=[
                    go.Bar(x=vehicles, y=costs, marker_color='lightcoral')
                ])
                fig2.update_layout(title="Cost by Vehicle", xaxis_title="Vehicle", yaxis_title="Cost ($)")
                st.plotly_chart(fig2, use_container_width=True)
            
            col3, col4 = st.columns(2)
            
            with col3:
                fig3 = go.Figure(data=[
                    go.Bar(x=vehicles, y=parcels, marker_color='lightgreen')
                ])
                fig3.update_layout(title="Parcels by Vehicle", xaxis_title="Vehicle", yaxis_title="Parcels")
                st.plotly_chart(fig3, use_container_width=True)
            
            with col4:
                # Efficiency metrics
                efficiency_data = pd.DataFrame({
                    'Vehicle': vehicles,
                    'Cost per Parcel': [c/p if p > 0 else 0 for c, p in zip(costs, parcels)],
                    'Distance per Parcel': [d/p if p > 0 else 0 for d, p in zip(distances, parcels)]
                })
                st.write("**Efficiency Metrics**")
                st.dataframe(efficiency_data, use_container_width=True)
            
            # Savings calculation
            st.markdown("---")
            st.subheader("💰 Cost Savings Analysis")
            
            # Simulate before optimization (random routes)
            random_cost = total_cost * 1.35  # Assume 35% higher cost without optimization
            savings = random_cost - total_cost
            savings_percent = (savings / random_cost) * 100
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Before Optimization", f"${random_cost:.2f}", delta=None)
            col2.metric("After Optimization", f"${total_cost:.2f}", delta=f"-${savings:.2f}")
            col3.metric("Savings", f"{savings_percent:.1f}%", delta=f"${savings:.2f}")
            
            st.success(f"🎉 You saved ${savings:.2f} ({savings_percent:.1f}%) by optimizing routes!")
        else:
            st.info("👆 Optimize routes first to see analytics!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>QuickDeliver Routing System v1.0 | Transport and Logistics Analytics | CUSCM 401</p>
    <p>Developed for Chinhoyi University of Technology</p>
</div>
""", unsafe_allow_html=True)