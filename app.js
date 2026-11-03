// NSUT Dwarka Smart Campus Navigation & Resource Optimizer
// Production Frontend Controller with 3-View Architecture (Campus Map, Find Route, Directory)
// Features: Full HTML5 Geolocation, High-Accuracy Snapping, Live GPS Walk Tracking & Simulation

document.addEventListener("DOMContentLoaded", () => {
  if (!window.CAMPUS_DATA) {
    console.error("CAMPUS_DATA is missing! Ensure graphData.js is loaded.");
    return;
  }

  const { campusCenter, bounds, campusBoundary, zones, landmarks, nodes, edges, adjacency, buildingsGeoJSON } = window.CAMPUS_DATA;
  const algos = window.CampusAlgorithms;

  // -----------------------------------------------------------------
  // 1. Tile Layer Configurations (Voyager with Carto API Key & ESRI Satellite)
  // -----------------------------------------------------------------
  const CARTO_API_KEY = "cb1_50ek_1_0eebde7fd5f6d287d8f0bed6";

  const tileProviders = {
    voyager: `https://basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}.png?key=${CARTO_API_KEY}`,
    satellite: "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
  };

  // State Management
  const state = {
    currentStyle: "street",
    currentView: "view-campus-map",
    selectedAlgo: "dijkstra",
    selectedStart: "main_gate",
    selectedEnd: "apj_complex",
    selectedLocationId: "block_6",
    accessibleOnly: false,
    weatherFactor: 1.0,
    blockedEdgeIds: new Set(),
    rushEdgeIds: new Set(),
    activeRoutePolyline: null,
    activeRouteGlow: null,
    activeRouteDashes: null,
    routeStartMarker: null,
    routeEndMarker: null,
    routeTraceAnimationId: null,
    currentRouteResult: null,
    markersMap: {},
    baseTileLayer: null,
    buildingLayerGroup: null,
    networkLayerGroup: null,
    mstLayerGroup: null,
    showNetwork: false,

    // Geolocation & Live Walk Tracking State
    userLocation: null, // { lat, lon, accuracy, isOnCampus, nearestNodeId, snapDistMeters }
    userMarker: null,
    accuracyCircle: null,
    snapConnectorLine: null,
    watchId: null,
    isTracking: false,
    simWalkInterval: null,
    isSimWalking: false
  };

  // -----------------------------------------------------------------
  // 2. Leaflet Map Initialization
  // -----------------------------------------------------------------
  const map = L.map("map", {
    center: campusCenter,
    zoom: 16.5,
    minZoom: 15,
    maxZoom: 19,
    maxBounds: [
      [bounds[0][0] - 0.005, bounds[0][1] - 0.005],
      [bounds[1][0] + 0.005, bounds[1][1] + 0.005]
    ],
    zoomControl: true,
    attributionControl: false
  });

  state.baseTileLayer = L.tileLayer(tileProviders.voyager, {
    maxZoom: 19,
    subdomains: "abcd",
    opacity: 1.0
  }).addTo(map);

  // Dedicated z-indexed overlay panes for optimal route contrast
  if (!map.getPane("routeGlowPane")) {
    map.createPane("routeGlowPane");
    map.getPane("routeGlowPane").style.zIndex = 540;
    map.getPane("routeGlowPane").style.pointerEvents = "none";
  }
  if (!map.getPane("routePane")) {
    map.createPane("routePane");
    map.getPane("routePane").style.zIndex = 550;
    map.getPane("routePane").style.pointerEvents = "none";
  }

  // -----------------------------------------------------------------
  // 3. Render Campus Buildings Footprints (GeoJSON)
  // -----------------------------------------------------------------
  state.buildingLayerGroup = L.geoJSON(buildingsGeoJSON, {
    style: (feature) => {
      const name = feature.properties?.name || "";
      let fillColor = "#cbd5e1";
      let borderColor = "#94a3b8";

      if (name.includes("Lake") || name.includes("Pond") || feature.properties?.building === "water") {
        fillColor = "#38bdf8"; // Water blue for Campus Lake (Green Circle)
        borderColor = "#0284c7";
      } else if (name.includes("Design")) {
        fillColor = "#e9d5ff"; // Purple tint for Design Block (Purple Circle)
        borderColor = "#a855f7";
      } else if (name.includes("Block 6")) {
        fillColor = "#38bdf8"; // Azure Sky for Block 6 (Top)
        borderColor = "#0284c7";
      } else if (name.includes("Block 4")) {
        fillColor = "#818cf8"; // Indigo for Block 4 (Bottom-Left)
        borderColor = "#4f46e5";
      } else if (name.includes("Block 5")) {
        fillColor = "#2dd4bf"; // Teal for Block 5 (Bottom-Right)
        borderColor = "#0d9488";
      } else if (name.includes("Admin") || name.includes("Auditorium")) {
        fillColor = "#e0e7ff"; // Castle Lilac for Admin
        borderColor = "#6366f1";
      } else if (name.includes("APJ") || name.includes("Lecture")) {
        fillColor = "#bae6fd"; // Azure for APJ
        borderColor = "#0284c7";
      } else if (name.includes("Hostel") || name.includes("Quarters")) {
        fillColor = "#fed7aa"; // Warm peach/cottage brick for Hostels (Light Pink Circle)
        borderColor = "#ea580c";
      } else if (name.includes("Library") || name.includes("SAC")) {
        fillColor = "#dbeafe"; // Blue for Library & SAC
        borderColor = "#2563eb";
      } else if (name.includes("Sports") || name.includes("Ground")) {
        fillColor = "#bbf7d0"; // Turf green
        borderColor = "#22c55e";
      }

      return {
        fillColor: fillColor,
        fillOpacity: 0.75,
        color: borderColor,
        weight: 2
      };
    },
    onEachFeature: (feature, layer) => {
      if (feature.properties && feature.properties.name) {
        layer.bindTooltip(`<strong>${feature.properties.name}</strong>`, {
          permanent: false,
          direction: "center",
          className: "building-tooltip"
        });
      }
    }
  }).addTo(map);

  // -----------------------------------------------------------------
  // 4. Render Landmark Markers with Clean Location Name Badges
  // -----------------------------------------------------------------
  function getCleanLandmarkName(lm) {
    const customNames = {
      main_gate: "Main Gate",
      north_gate: "North Gate",
      mandir: "Campus Mandir",
      boys_hostels: "Boys' Hostels",
      design_block: "Design Block",
      admin_block: "Admin Block",
      central_fountain: "Central Fountain",
      block_6: "Block 6",
      block_4: "Block 4",
      block_5: "Block 5",
      mini_audi: "Mini Audi",
      central_library: "Central Library",
      sac: "SAC",
      apj_complex: "APJ Complex",
      student_center: "Student Center",
      amul_ground: "Amul Kiosk",
      smart_block: "Smart Block",
      stationery: "Stationery",
      clinic: "Campus Clinic",
      kaveri_hostel: "Kaveri Hostel",
      girls_hostels: "Girls' Hostels",
      tnp_building: "TnP Cell",
      sports_grounds: "Sports Complex",
      parking_west: "West Parking",
      nescii_lawns: "Nescii Lawns",
      moksha_ground: "Moksha Ground",
      mgmt_block: "Management Block",
      campus_lake: "Campus Lake"
    };
    return customNames[lm.id] || lm.name.split("(")[0].trim() || lm.name;
  }

  const markersGroup = L.layerGroup().addTo(map);

  landmarks.forEach((lm) => {
    const displayName = getCleanLandmarkName(lm);
    const catClass = getCategoryClass(lm.category);

    const customIcon = L.divIcon({
      className: "campus-name-div-icon",
      html: `
        <div class="campus-name-marker marker-${catClass}" data-id="${lm.id}" title="${lm.name}">
          <span class="marker-category-dot"></span>
          <span class="marker-label-text">${displayName}</span>
        </div>
      `,
      iconSize: null,
      iconAnchor: [0, 0],
      popupAnchor: [0, -14]
    });

    const marker = L.marker(lm.coords, { icon: customIcon });

    const popupHtml = `
      <div style="font-family: var(--font-family); min-width: 230px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
          <h3 style="font-size: 15px; font-weight: 800; margin: 0; color: #0f172a;">${lm.name}</h3>
          <span class="item-badge badge-${catClass}" style="font-size: 10px;">${lm.category}</span>
        </div>
        <p style="font-size: 12px; color: #475569; margin-bottom: 12px; line-height: 1.4;">${lm.description}</p>
        <div style="display: flex; gap: 8px;">
          <button onclick="window.setStartFromPopup('${lm.id}')" style="flex:1; padding: 7px 10px; font-size: 11px; font-weight: 700; background: #ecfdf5; color: #065f46; border: 1px solid #10b981; border-radius: 6px; cursor: pointer;">
            Set as Start
          </button>
          <button onclick="window.setEndFromPopup('${lm.id}')" style="flex:1; padding: 7px 10px; font-size: 11px; font-weight: 700; background: #eff6ff; color: #1e40af; border: 1px solid #3b82f6; border-radius: 6px; cursor: pointer;">
            Set Destination
          </button>
        </div>
      </div>
    `;

    marker.bindPopup(popupHtml);
    markersGroup.addLayer(marker);
    state.markersMap[lm.id] = marker;

    marker.on("click", () => {
      selectLocation(lm.id);
    });
  });

  function getCategoryClass(cat) {
    if (cat.includes("Academic")) return "academic";
    if (cat.includes("Hostel")) return "hostels";
    if (cat.includes("Food") || cat.includes("Hangout")) return "hangouts";
    if (cat.includes("Admin")) return "admin";
    if (cat.includes("Sports")) return "sports";
    if (cat.includes("Gate")) return "gates";
    if (cat.includes("Landmark")) return "landmarks";
    if (cat.includes("Utility")) return "utility";
    return "academic";
  }

  // Global popup helpers
  window.setStartFromPopup = (lmId) => {
    state.selectedStart = lmId;
    document.getElementById("start-select").value = lmId;
    map.closePopup();
    switchView("view-find-route");
    calculateAndDisplayRoute();
  };

  window.setEndFromPopup = (lmId) => {
    state.selectedEnd = lmId;
    document.getElementById("end-select").value = lmId;
    map.closePopup();
    switchView("view-find-route");
    calculateAndDisplayRoute();
  };

  // -----------------------------------------------------------------
  // 5. Navigation Tab Switching (Campus Map, Find Route, Directory)
  // -----------------------------------------------------------------
  const mapElement = document.getElementById("map");

  function switchView(viewId) {
    state.currentView = viewId;

    document.querySelectorAll(".nav-tab").forEach(tab => {
      tab.classList.toggle("active", tab.dataset.view === viewId);
    });

    document.querySelectorAll(".app-view").forEach(v => {
      if (v.id === viewId) {
        v.style.display = "flex";
      } else {
        v.style.display = "none";
      }
    });

    if (viewId === "view-campus-map") {
      const target = document.getElementById("campus-map-wrapper");
      if (mapElement.parentElement !== target) {
        target.appendChild(mapElement);
      }
      map.invalidateSize({ animate: false });
      setTimeout(() => {
        map.invalidateSize();
        if (state.activeRoutePolyline && state.activeRoutePolyline.getBounds && state.activeRoutePolyline.getBounds().isValid() && map.getSize().x > 0) {
          map.fitBounds(state.activeRoutePolyline.getBounds(), { padding: [40, 40], maxZoom: 18 });
        }
      }, 50);
    } else if (viewId === "view-find-route") {
      const target = document.getElementById("route-map-wrapper");
      if (mapElement.parentElement !== target) {
        target.appendChild(mapElement);
      }
      map.invalidateSize({ animate: false });
      setTimeout(() => {
        map.invalidateSize();
        if (state.activeRoutePolyline && state.activeRoutePolyline.getBounds && state.activeRoutePolyline.getBounds().isValid() && map.getSize().x > 0) {
          map.fitBounds(state.activeRoutePolyline.getBounds(), { padding: [40, 40], maxZoom: 18 });
        }
      }, 50);
    } else if (viewId === "view-directory") {
      renderDirectoryGrid();
    }
  }

  document.querySelectorAll(".nav-tab").forEach(tab => {
    tab.addEventListener("click", () => {
      const targetView = tab.getAttribute("data-view");
      switchView(targetView);
    });
  });

  // -----------------------------------------------------------------
  // 6. Style Switcher Handler (Street Map vs Satellite View)
  // -----------------------------------------------------------------
  document.querySelectorAll(".style-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".style-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      const chosenStyle = btn.getAttribute("data-style");
      setMapStyle(chosenStyle);
    });
  });

  function setMapStyle(styleName) {
    state.currentStyle = styleName;

    if (styleName === "satellite") {
      state.baseTileLayer.setUrl(tileProviders.satellite);
    } else {
      state.baseTileLayer.setUrl(tileProviders.voyager);
    }
    state.baseTileLayer.setOpacity(1.0);

    if (state.activeRouteGlow) state.activeRouteGlow.bringToFront();
    if (state.activeRoutePolyline) state.activeRoutePolyline.bringToFront();
    if (state.activeRouteDashes) state.activeRouteDashes.bringToFront();
    markersGroup.bringToFront();
    if (state.routeStartMarker) state.routeStartMarker.bringToFront();
    if (state.routeEndMarker) state.routeEndMarker.bringToFront();
    if (state.userMarker) state.userMarker.bringToFront();
  }

  // -----------------------------------------------------------------
  // 7. Location Metadata Mapping Helper
  // -----------------------------------------------------------------
  function getBuildingFloorMeta(lm) {
    const name = lm.name;
    let bldg = "Campus Facility";
    let floor = "Ground Floor";

    if (name.includes("Block 6")) {
      bldg = "Academic North Block";
      floor = "Ground to 3rd Floor";
    } else if (name.includes("Block 4")) {
      bldg = "Academic South-West Block";
      floor = "Ground to 3rd Floor";
    } else if (name.includes("Block 5")) {
      bldg = "Academic South-East Block";
      floor = "Ground to 3rd Floor";
    } else if (name.includes("Design")) {
      bldg = "Department of Design Studio";
      floor = "Ground & 1st Floor";
    } else if (name.includes("APJ")) {
      bldg = "APJ Lecture Theatre Complex";
      floor = "1st - 4th Floor";
    } else if (name.includes("Smart")) {
      bldg = "Smart Lecture & Research Wing";
      floor = "Ground to 2nd Floor";
    } else if (name.includes("Library")) {
      bldg = "Tagore Knowledge Hub";
      floor = "Ground to 3rd Floor";
    } else if (name.includes("Management")) {
      bldg = "Department of Management Studies";
      floor = "Ground & 1st Floor";
    } else if (name.includes("Admin")) {
      bldg = "Administrative Central Tower";
      floor = "Ground & 1st Floor";
    } else if (name.includes("Mini Audi")) {
      bldg = "Mini Audi Complex";
      floor = "Ground Floor";
    } else if (name.includes("TnP")) {
      bldg = "Corporate Relations Centre";
      floor = "Ground Floor";
    } else if (name.includes("SAC")) {
      bldg = "Student Recreation Hub";
      floor = "Ground & 1st Floor";
    } else if (name.includes("Clinic")) {
      bldg = "Health & Wellness Centre";
      floor = "Ground Floor";
    } else if (name.includes("Stationery")) {
      bldg = "Commercial & Utility Annex";
      floor = "Ground Floor";
    } else if (name.includes("Boys'")) {
      bldg = "Undergraduate Boys' Quad (BH 1-4)";
      floor = "1st - 4th Floor";
    } else if (name.includes("Kaveri")) {
      bldg = "Northern Girls' Residency";
      floor = "1st - 4th Floor";
    } else if (name.includes("Girls'")) {
      bldg = "Southern Girls' Residency";
      floor = "1st - 5th Floor";
    } else if (name.includes("Canteen")) {
      bldg = "Main Student Cafeteria";
      floor = "Ground Floor";
    } else if (name.includes("Amul")) {
      bldg = "Amul Refreshment Hub";
      floor = "Open Ground Kiosk";
    } else if (name.includes("Fountain")) {
      bldg = "Central Academic Plaza";
      floor = "Central Circle";
    } else if (name.includes("Lake")) {
      bldg = "Ecological Water Basin";
      floor = "North Woods Promenade";
    } else if (name.includes("Mandir")) {
      bldg = "Sanctuary & Lotus Garden";
      floor = "Ground Sanctum";
    } else if (name.includes("Main Gate")) {
      bldg = "Dwarka Mor Gate 1";
      floor = "Security Checkpoint";
    } else if (name.includes("North Gate")) {
      bldg = "Suraj Vihar Gate 2";
      floor = "Security Checkpoint";
    } else if (name.includes("Sports")) {
      bldg = "Running Track & Pavilion";
      floor = "Open Sports Complex";
    } else if (name.includes("Parking")) {
      bldg = "West Campus Lot";
      floor = "Open Paved Lot";
    } else if (name.includes("Nescii")) {
      bldg = "Shaheed Vatika Gardens";
      floor = "Central Lawns";
    } else if (name.includes("Moksha")) {
      bldg = "Festival & Concert Arena";
      floor = "Open Amphitheatre";
    }

    return { building: bldg, floor: floor };
  }

  // -----------------------------------------------------------------
  // 8. VIEW 1: Campus Map Sidebar (Selected Location Card & Locations List)
  // -----------------------------------------------------------------
  function selectLocation(lmId) {
    const lm = landmarks.find(l => l.id === lmId);
    if (!lm) return;

    state.selectedLocationId = lmId;
    const card = document.getElementById("selected-location-card");
    if (card) card.style.display = "flex";

    const catClass = getCategoryClass(lm.category);
    const meta = getBuildingFloorMeta(lm);

    const badgeEl = document.getElementById("sel-loc-badge");
    badgeEl.textContent = lm.category;
    badgeEl.className = `badge badge-${catClass}`;

    document.getElementById("sel-loc-name").textContent = lm.name;
    document.getElementById("sel-loc-building").innerHTML = `
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="16" height="20" x="4" y="2" rx="2"/><line x1="9" x2="9" y1="22" y2="2"/><line x1="15" x2="15" y1="22" y2="2"/></svg>
      Building: ${meta.building}
    `;
    document.getElementById("sel-loc-zone").innerHTML = `
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
      Floor: ${meta.floor}
    `;
    document.getElementById("sel-loc-coords").textContent = `Coordinates: ${lm.lat.toFixed(6)}, ${lm.lon.toFixed(6)}`;
    document.getElementById("sel-loc-desc").textContent = lm.description;

    document.querySelectorAll(".location-list-item").forEach(item => {
      item.classList.toggle("selected", item.dataset.id === lmId);
    });

    document.querySelectorAll(".campus-name-marker").forEach(el => {
      el.classList.toggle("selected", el.dataset.id === lmId);
    });
  }

  document.getElementById("btn-set-start-from-card").addEventListener("click", () => {
    if (state.selectedLocationId) {
      window.setStartFromPopup(state.selectedLocationId);
    }
  });

  document.getElementById("btn-set-dest-from-card").addEventListener("click", () => {
    if (state.selectedLocationId) {
      window.setEndFromPopup(state.selectedLocationId);
    }
  });

  document.getElementById("btn-close-loc-card").addEventListener("click", () => {
    document.getElementById("sel-loc-name").textContent = "Select a campus location";
    document.getElementById("sel-loc-desc").textContent = "Click any marker on the map or select from the list below to view detailed facility info.";
    document.querySelectorAll(".campus-name-marker").forEach(el => {
      el.classList.remove("selected");
    });
  });

  function renderMapLocationsList() {
    const container = document.getElementById("map-locations-scroll-list");
    const countEl = document.getElementById("locations-count");
    const filterCat = document.getElementById("map-category-filter").value;
    const searchVal = document.getElementById("map-search-input").value.toLowerCase().trim();

    container.innerHTML = "";

    const filtered = landmarks.filter(lm => {
      const matchCat = (filterCat === "all") || (lm.category.toLowerCase().includes(filterCat.toLowerCase()));
      const matchSearch = (searchVal === "") ||
        lm.name.toLowerCase().includes(searchVal) ||
        lm.description.toLowerCase().includes(searchVal) ||
        (lm.aliases && lm.aliases.some(a => a.toLowerCase().includes(searchVal)));
      return matchCat && matchSearch;
    });

    countEl.textContent = filtered.length;

    filtered.forEach(lm => {
      const item = document.createElement("div");
      item.className = "location-list-item";
      item.dataset.id = lm.id;
      if (lm.id === state.selectedLocationId) item.classList.add("selected");

      const catClass = getCategoryClass(lm.category);
      item.innerHTML = `
        <span class="item-left">${lm.name}</span>
        <span class="item-badge badge-${catClass}">${lm.category}</span>
      `;

      item.addEventListener("click", () => {
        selectLocation(lm.id);
        map.flyTo(lm.coords, 18, { duration: 1.2 });
        if (state.markersMap[lm.id]) {
          state.markersMap[lm.id].openPopup();
        }
        if (window.innerWidth <= 1024) {
          const mapCard = document.querySelector(".map-viewport-card");
          if (mapCard) {
            mapCard.scrollIntoView({ behavior: "smooth", block: "start" });
          }
        }
      });

      container.appendChild(item);
    });
  }

  document.getElementById("map-category-filter").addEventListener("change", renderMapLocationsList);
  document.getElementById("map-search-input").addEventListener("input", renderMapLocationsList);

  // Initialize selected location card with Block 6
  selectLocation("block_6");
  renderMapLocationsList();

  // -----------------------------------------------------------------
  // 9. VIEW 2: Find Route Dropdowns & Route Computation
  // -----------------------------------------------------------------
  const startSelect = document.getElementById("start-select");
  const endSelect = document.getElementById("end-select");

  landmarks.forEach((lm) => {
    const optStart = new Option(`${lm.name} (${lm.category})`, lm.id);
    const optEnd = new Option(`${lm.name} (${lm.category})`, lm.id);
    startSelect.add(optStart);
    endSelect.add(optEnd);
  });

  startSelect.value = state.selectedStart;
  endSelect.value = state.selectedEnd;

  // Immediate recalculation and tracing whenever dropdown options change
  startSelect.addEventListener("change", () => {
    state.selectedStart = startSelect.value;
    calculateAndDisplayRoute();
  });

  endSelect.addEventListener("change", () => {
    state.selectedEnd = endSelect.value;
    calculateAndDisplayRoute();
  });

  document.getElementById("swap-points").addEventListener("click", () => {
    const temp = startSelect.value;
    startSelect.value = endSelect.value;
    endSelect.value = temp;
    state.selectedStart = startSelect.value;
    state.selectedEnd = endSelect.value;
    calculateAndDisplayRoute();
  });

  document.querySelectorAll(".algo-chip").forEach((chip) => {
    chip.addEventListener("click", () => {
      document.querySelectorAll(".algo-chip").forEach(c => c.classList.remove("active"));
      chip.classList.add("active");
      state.selectedAlgo = chip.getAttribute("data-algo");
      calculateAndDisplayRoute();
    });
  });

  document.getElementById("pref-accessible").addEventListener("change", (e) => {
    state.accessibleOnly = e.target.checked;
    calculateAndDisplayRoute();
  });

  document.getElementById("btn-find-route").addEventListener("click", () => {
    calculateAndDisplayRoute();
  });

  function calculateAndDisplayRoute() {
    const srcId = startSelect.value;
    const dstId = endSelect.value;
    if (!srcId || !dstId) return;

    if (srcId === dstId) {
      showGeoBanner("⚠️ Start and destination are the same. Please choose different locations.", "#f59e0b", 3500);
      return;
    }

    let startNode;
    let startPointCoords = null;

    if (srcId === "user_current_location") {
      if (!state.userLocation) {
        showGeoBanner("Acquiring GPS position for origin...", "#0284c7");
        return;
      }
      startNode = state.userLocation.nearestNodeId;
      startPointCoords = [state.userLocation.lat, state.userLocation.lon];
    } else {
      const srcLm = landmarks.find(l => l.id === srcId);
      if (!srcLm) return;
      startNode = srcLm.nearest_node;
      startPointCoords = srcLm.coords;
    }

    const dstLm = landmarks.find(l => l.id === dstId);
    if (!dstLm) return;
    const endNode = dstLm.nearest_node;

    const options = {
      blockedEdges: state.blockedEdgeIds,
      accessibleOnly: state.accessibleOnly,
      weatherFactor: state.weatherFactor,
      rushEdges: state.rushEdgeIds
    };

    let result;
    if (state.selectedAlgo === "dijkstra") {
      result = algos.runDijkstra(adjacency, startNode, endNode, nodes, options);
    } else if (state.selectedAlgo === "astar") {
      result = algos.runAStar(adjacency, startNode, endNode, nodes, options);
    } else if (state.selectedAlgo === "bfs") {
      result = algos.runBFS(adjacency, startNode, endNode, nodes, options);
    } else if (state.selectedAlgo === "dfs") {
      result = algos.runDFS(adjacency, startNode, endNode, nodes, options);
    }

    state.currentRouteResult = result;
    const resultsBox = document.getElementById("route-results");

    if (!result || !result.success || !result.path || result.path.length === 0) {
      showGeoBanner("⚠️ No walkable path found between selected locations.", "#ef4444", 4000);
      resultsBox.style.display = "none";
      if (state.activeRoutePolyline) map.removeLayer(state.activeRoutePolyline);
      if (state.activeRouteGlow) map.removeLayer(state.activeRouteGlow);
      if (state.activeRouteDashes) map.removeLayer(state.activeRouteDashes);
      if (state.routeStartMarker) map.removeLayer(state.routeStartMarker);
      if (state.routeEndMarker) map.removeLayer(state.routeEndMarker);
      return;
    }

    resultsBox.style.display = "flex";

    // If starting from live user location, add lead-in connector distance
    let totalDist = result.distance;
    if (srcId === "user_current_location" && state.userLocation) {
      totalDist += state.userLocation.snapDistMeters;
    }

    const estMinutes = Math.max(1, Math.round(totalDist / 80));

    // Update statistics
    document.getElementById("stat-dist").textContent = `${Math.round(totalDist)} m`;
    document.getElementById("stat-time").textContent = `${estMinutes} min`;
    document.getElementById("stat-speed").textContent = `${result.executionTimeMs} ms`;

    const algoNames = {
      dijkstra: "Dijkstra's Algorithm (Min-Heap)",
      astar: "A* Heuristic Search",
      bfs: "Breadth-First Search (BFS)",
      dfs: "Depth-First Search (DFS)"
    };

    document.getElementById("stat-details").innerHTML = `
      Algorithm: <strong>${algoNames[state.selectedAlgo]}</strong> • Visited Nodes: <strong>${result.nodesVisited}</strong> • Waypoints: <strong>${result.path.length}</strong>
    `;

    // Turn-by-Turn Directions
    const directionsContainer = document.getElementById("directions-container");
    directionsContainer.innerHTML = "";

    try {
      const getDirectionsFn = algos.generateDirections || algos.generateTurnByTurn;
      const turnDirections = typeof getDirectionsFn === "function" ? getDirectionsFn(result.path, nodes, landmarks) : [];

      if (srcId === "user_current_location" && state.userLocation) {
        const leadStep = document.createElement("div");
        leadStep.className = "direction-item";
        leadStep.innerHTML = `
          <div style="font-weight: 700; color: #0284c7; min-width: 20px;">0.</div>
          <div>
            <div>Walk <strong>${Math.round(state.userLocation.snapDistMeters)} meters</strong> from your current position to join the campus walkway.</div>
            <div style="font-size: 11px; color: var(--text-muted); margin-top: 2px;">Connector Link</div>
          </div>
        `;
        directionsContainer.appendChild(leadStep);
      }

      turnDirections.forEach((step) => {
        const stepEl = document.createElement("div");
        stepEl.className = "direction-item";
        const dist = Math.round(step.distance !== undefined ? step.distance : (step.distanceMeters || 0));
        stepEl.innerHTML = `
          <div style="font-weight: 700; color: var(--primary); min-width: 20px;">${step.step}.</div>
          <div>
            <div>${step.instruction}</div>
            <div style="font-size: 11px; color: var(--text-muted); margin-top: 2px;">${dist > 0 ? `Segment: ${dist}m` : "Waypoint"}</div>
          </div>
        `;
        directionsContainer.appendChild(stepEl);
      });
    } catch (dirErr) {
      console.warn("Turn-by-turn directions generation warning:", dirErr);
    }

    // Clean up previous route layers & animations
    if (state.activeRoutePolyline) map.removeLayer(state.activeRoutePolyline);
    if (state.activeRouteGlow) map.removeLayer(state.activeRouteGlow);
    if (state.activeRouteDashes) map.removeLayer(state.activeRouteDashes);
    if (state.routeStartMarker) map.removeLayer(state.routeStartMarker);
    if (state.routeEndMarker) map.removeLayer(state.routeEndMarker);
    if (state.routeTraceAnimationId) {
      cancelAnimationFrame(state.routeTraceAnimationId);
      state.routeTraceAnimationId = null;
    }

    // Ensure map layout is current before rendering
    map.invalidateSize({ animate: false });

    // Ensure dedicated z-indexed panes above building footprints
    if (!map.getPane("routeGlowPane")) {
      map.createPane("routeGlowPane");
      map.getPane("routeGlowPane").style.zIndex = 540;
      map.getPane("routeGlowPane").style.pointerEvents = "none";
    }
    if (!map.getPane("routePane")) {
      map.createPane("routePane");
      map.getPane("routePane").style.zIndex = 550;
      map.getPane("routePane").style.pointerEvents = "none";
    }

    const glowPane = map.getPane("routeGlowPane") ? "routeGlowPane" : "overlayPane";
    const linePane = map.getPane("routePane") ? "routePane" : "overlayPane";

    // Assemble complete geographic latLng path
    let latLngPath = result.path.map(nid => nodes[nid]).filter(Boolean);
    if (srcId === "user_current_location" && startPointCoords) {
      latLngPath = [startPointCoords, ...latLngPath];
    } else if (startPointCoords) {
      const first = latLngPath[0];
      if (first && (first[0] !== startPointCoords[0] || first[1] !== startPointCoords[1])) {
        latLngPath = [startPointCoords, ...latLngPath];
      }
    }

    const dstCoords = dstLm.coords;
    const last = latLngPath[latLngPath.length - 1];
    if (dstCoords && last && (last[0] !== dstCoords[0] || last[1] !== dstCoords[1])) {
      latLngPath = [...latLngPath, dstCoords];
    }

    // Layer 1: Glowing underlay polyline (Cyan ambient glow)
    state.activeRouteGlow = L.polyline(latLngPath, {
      pane: glowPane,
      color: "#0284c7",
      weight: 10,
      opacity: 0.5,
      lineCap: "round",
      lineJoin: "round"
    }).addTo(map);

    // Layer 2: Solid vibrant path - initialized immediately with full path so it is 100% visible
    state.activeRoutePolyline = L.polyline(latLngPath, {
      pane: linePane,
      color: "#2563eb",
      weight: 6,
      opacity: 1.0,
      lineCap: "round",
      lineJoin: "round"
    }).addTo(map);

    // Layer 3: Animated directional flow overlay
    state.activeRouteDashes = L.polyline(latLngPath, {
      pane: linePane,
      color: "#ffffff",
      weight: 3.5,
      opacity: 0.95,
      dashArray: "8, 14",
      className: "route-polyline-flow",
      lineCap: "round",
      lineJoin: "round"
    }).addTo(map);

    // Drop Start and Destination endpoint badges
    const startIcon = L.divIcon({
      className: "route-endpoint-div-icon",
      html: `
        <div class="endpoint-badge badge-start">
          <span class="dot-live"></span>
          <span>START</span>
        </div>
      `,
      iconSize: [64, 26],
      iconAnchor: [32, 28]
    });

    const endIcon = L.divIcon({
      className: "route-endpoint-div-icon",
      html: `
        <div class="endpoint-badge badge-dest">
          <span>🏁 DEST</span>
        </div>
      `,
      iconSize: [64, 26],
      iconAnchor: [32, 28]
    });

    state.routeStartMarker = L.marker(latLngPath[0], {
      icon: startIcon,
      zIndexOffset: 3500
    }).addTo(map);

    state.routeEndMarker = L.marker(latLngPath[latLngPath.length - 1], {
      icon: endIcon,
      zIndexOffset: 3500
    }).addTo(map);

    // Bring all route elements to the absolute front
    state.activeRouteGlow.bringToFront();
    state.activeRoutePolyline.bringToFront();
    state.activeRouteDashes.bringToFront();
    state.routeStartMarker.bringToFront();
    state.routeEndMarker.bringToFront();

    // Progressive tracing animation from origin to destination
    const totalPts = latLngPath.length;
    if (totalPts > 2) {
      const traceDuration = Math.min(700, Math.max(300, totalPts * 16));
      const traceStart = performance.now();

      function traceStep(now) {
        const elapsed = now - traceStart;
        const progress = Math.min(1, elapsed / traceDuration);
        const count = Math.max(2, Math.min(totalPts, Math.ceil(progress * totalPts)));
        const slice = latLngPath.slice(0, count);

        state.activeRoutePolyline.setLatLngs(slice);
        state.activeRouteDashes.setLatLngs(slice);

        if (progress < 1) {
          state.routeTraceAnimationId = requestAnimationFrame(traceStep);
        } else {
          state.activeRoutePolyline.setLatLngs(latLngPath);
          state.activeRouteDashes.setLatLngs(latLngPath);
          state.routeTraceAnimationId = null;
        }
      }

      state.routeTraceAnimationId = requestAnimationFrame(traceStep);
    }

    // Auto-fit map viewport to route with padding
    const routeBounds = L.latLngBounds(latLngPath);
    if (routeBounds.isValid()) {
      try {
        map.fitBounds(routeBounds, { padding: [50, 50], maxZoom: 18 });
      } catch (fbErr) {
        console.warn("fitBounds warning:", fbErr);
      }
    }

    if (state.currentView === "view-find-route" && window.innerWidth <= 1024) {
      setTimeout(() => {
        const visCard = document.querySelector(".route-visualization-card");
        if (visCard) {
          visCard.scrollIntoView({ behavior: "smooth", block: "start" });
        }
      }, 120);
    }
  }

  // -----------------------------------------------------------------
  // 10. VIEW 3: Campus Location Directory Grid
  // -----------------------------------------------------------------
  let currentDirectoryFilter = "all";

  function renderDirectoryGrid() {
    const grid = document.getElementById("directory-cards-grid");
    const countLabel = document.getElementById("directory-count-label");
    const searchVal = document.getElementById("directory-search-input").value.toLowerCase().trim();

    grid.innerHTML = "";

    const filtered = landmarks.filter(lm => {
      const matchCat = (currentDirectoryFilter === "all") || (lm.category.toLowerCase().includes(currentDirectoryFilter.toLowerCase()));
      const matchSearch = (searchVal === "") ||
        lm.name.toLowerCase().includes(searchVal) ||
        lm.description.toLowerCase().includes(searchVal) ||
        (lm.aliases && lm.aliases.some(a => a.toLowerCase().includes(searchVal)));
      return matchCat && matchSearch;
    });

    countLabel.textContent = `Showing ${filtered.length} of ${landmarks.length} campus facilities`;
    document.getElementById("dir-all-count").textContent = landmarks.length;

    filtered.forEach(lm => {
      const catClass = getCategoryClass(lm.category);
      const meta = getBuildingFloorMeta(lm);

      const card = document.createElement("div");
      card.className = "facility-card";
      card.innerHTML = `
        <div>
          <div class="facility-header">
            <h3 class="facility-title">${lm.name}</h3>
            <span class="badge badge-${catClass}">${lm.category}</span>
          </div>
          <div class="facility-meta">
            <span>
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="16" height="20" x="4" y="2" rx="2"/><line x1="9" x2="9" y1="22" y2="2"/><line x1="15" x2="15" y1="22" y2="2"/></svg>
              ${meta.building}
            </span>
            <span>
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
              Floor: ${meta.floor}
            </span>
          </div>
          <p class="facility-desc">${lm.description}</p>
        </div>
        <div class="facility-actions">
          <button class="btn-view-map" data-id="${lm.id}">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/></svg>
            View on Map
          </button>
          <button class="btn-navigate" data-id="${lm.id}">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polygon points="3 11 22 2 13 21 11 13 3 11"/></svg>
            Navigate
          </button>
        </div>
      `;

      card.querySelector(".btn-view-map").addEventListener("click", () => {
        switchView("view-campus-map");
        selectLocation(lm.id);
        map.flyTo(lm.coords, 18, { duration: 1.2 });
        if (state.markersMap[lm.id]) {
          state.markersMap[lm.id].openPopup();
        }
        if (window.innerWidth <= 1024) {
          setTimeout(() => {
            const mapCard = document.querySelector(".map-viewport-card");
            if (mapCard) {
              mapCard.scrollIntoView({ behavior: "smooth", block: "start" });
            }
          }, 100);
        }
      });

      card.querySelector(".btn-navigate").addEventListener("click", () => {
        window.setEndFromPopup(lm.id);
      });

      grid.appendChild(card);
    });
  }

  document.querySelectorAll(".filter-pill").forEach(pill => {
    pill.addEventListener("click", () => {
      document.querySelectorAll(".filter-pill").forEach(p => p.classList.remove("active"));
      pill.classList.add("active");
      currentDirectoryFilter = pill.getAttribute("data-cat");
      renderDirectoryGrid();
    });
  });

  document.getElementById("directory-search-input").addEventListener("input", renderDirectoryGrid);

  // -----------------------------------------------------------------
  // 11. HTML5 Geolocation, Campus Snapping & Live Walk Tracking
  // -----------------------------------------------------------------
  const geoStatusBanner = document.getElementById("geo-status-banner");
  const geoStatusText = document.getElementById("geo-status-text");
  const geoStatusDot = document.getElementById("geo-status-dot");
  let bannerTimer = null;

  function showGeoBanner(msg, dotColor = "#0284c7", autoHideMs = 0) {
    if (!geoStatusBanner) return;
    geoStatusText.textContent = msg;
    if (dotColor) geoStatusDot.style.background = dotColor;
    geoStatusBanner.classList.add("active");

    if (bannerTimer) clearTimeout(bannerTimer);
    if (autoHideMs > 0) {
      bannerTimer = setTimeout(() => {
        geoStatusBanner.classList.remove("active");
      }, autoHideMs);
    }
  }

  document.getElementById("btn-close-geo-banner").addEventListener("click", () => {
    geoStatusBanner.classList.remove("active");
  });

  function getHaversineDistMeters(lat1, lon1, lat2, lon2) {
    const R = 6371000;
    const phi1 = (lat1 * Math.PI) / 180;
    const phi2 = (lat2 * Math.PI) / 180;
    const dphi = ((lat2 - lat1) * Math.PI) / 180;
    const dlambda = ((lon2 - lon1) * Math.PI) / 180;
    const a =
      Math.sin(dphi / 2) ** 2 +
      Math.cos(phi1) * Math.cos(phi2) * Math.sin(dlambda / 2) ** 2;
    return 2 * R * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  }

  function snapLocationToCampusGraph(lat, lon) {
    let bestNode = null;
    let minDist = Infinity;

    for (const [nid, coords] of Object.entries(nodes)) {
      const d = getHaversineDistMeters(lat, lon, coords[0], coords[1]);
      if (d < minDist) {
        minDist = d;
        bestNode = nid;
      }
    }

    return { nearestNodeId: bestNode, snapDistMeters: minDist };
  }

  const userMarkerIcon = L.divIcon({
    className: "user-loc-div-icon",
    html: `
      <div class="user-location-marker">
        <div class="user-location-pulse"></div>
        <div class="user-location-dot"></div>
      </div>
    `,
    iconSize: [24, 24],
    iconAnchor: [12, 12],
    popupAnchor: [0, -12]
  });

  function handleLocationUpdate(lat, lon, accuracy = 5, isLive = false, centerMap = false) {
    const distToCampus = getHaversineDistMeters(lat, lon, campusCenter[0], campusCenter[1]);
    const isOnCampus = distToCampus <= 1200;

    let nearestNodeId;
    let snapDist;

    if (isOnCampus) {
      const snap = snapLocationToCampusGraph(lat, lon);
      nearestNodeId = snap.nearestNodeId;
      snapDist = snap.snapDistMeters;
    } else {
      // Off campus: gracefully snap to closest campus entrance gate
      const distToGate1 = getHaversineDistMeters(lat, lon, 28.608484, 77.035251);
      const distToGate2 = getHaversineDistMeters(lat, lon, 28.613175, 77.033627);
      if (distToGate1 <= distToGate2) {
        nearestNodeId = "2129002378"; // Main Gate 1
        snapDist = distToGate1;
      } else {
        nearestNodeId = "2129002331"; // North Gate 2
        snapDist = distToGate2;
      }
    }

    state.userLocation = {
      lat,
      lon,
      accuracy,
      isOnCampus,
      nearestNodeId,
      snapDistMeters: snapDist
    };

    // Render / update user position marker
    if (state.userMarker) {
      state.userMarker.setLatLng([lat, lon]);
    } else {
      state.userMarker = L.marker([lat, lon], {
        icon: userMarkerIcon,
        zIndexOffset: 3000
      }).addTo(map);
    }

    const popupContent = `
      <div style="font-family: var(--font-family); min-width: 190px;">
        <h4 style="margin: 0 0 4px 0; font-size: 14px; color: #0284c7; font-weight: 800;">📍 You Are Here</h4>
        <div style="font-size: 11px; color: #64748b; line-height: 1.4;">
          ${isOnCampus ? "On NSUT Campus" : `Outside Campus (~${(distToCampus / 1000).toFixed(1)} km away)`}<br>
          GPS Accuracy: ±${Math.round(accuracy)}m<br>
          Nearest Walkway: ${Math.round(snapDist)}m away
        </div>
      </div>
    `;
    state.userMarker.bindPopup(popupContent);

    // Render / update GPS accuracy radius circle
    if (state.accuracyCircle) {
      state.accuracyCircle.setLatLng([lat, lon]).setRadius(Math.max(5, accuracy));
    } else {
      state.accuracyCircle = L.circle([lat, lon], {
        radius: Math.max(5, accuracy),
        color: "#0284c7",
        fillColor: "#38bdf8",
        fillOpacity: 0.12,
        weight: 1.5
      }).addTo(map);
    }

    // Render connector line to snapped network node
    if (nodes[nearestNodeId]) {
      const snapCoords = nodes[nearestNodeId];
      if (state.snapConnectorLine) {
        state.snapConnectorLine.setLatLngs([[lat, lon], snapCoords]);
      } else {
        state.snapConnectorLine = L.polyline([[lat, lon], snapCoords], {
          color: "#0284c7",
          weight: 2,
          dashArray: "3, 5",
          opacity: 0.65
        }).addTo(map);
      }
    }

    // Ensure option in start-select
    let opt = startSelect.querySelector('option[value="user_current_location"]');
    if (!opt) {
      opt = new Option("📍 Your Current Location", "user_current_location");
      startSelect.add(opt, 0);
    }

    if (centerMap) {
      map.setView([lat, lon], 17.5, { animate: true, duration: 0.8 });
    }

    // Live tracking updates route if active
    if (isLive && startSelect.value === "user_current_location") {
      calculateAndDisplayRoute();
    }

    if (!isOnCampus) {
      showGeoBanner(`📍 Location ~${(distToCampus / 1000).toFixed(1)} km outside campus. Using closest entrance.`, "#f59e0b", 6000);
    } else {
      showGeoBanner(`📍 Live on Campus • Accuracy ±${Math.round(accuracy)}m`, "#10b981", 3000);
    }
  }

  function handleGeoError(err) {
    let msg = "Could not retrieve GPS position.";
    if (err.code === 1) {
      msg = "Location permission denied. Click 'Allow' in your browser location prompt.";
    } else if (err.code === 2) {
      msg = "GPS position unavailable. Check device location services.";
    } else if (err.code === 3) {
      msg = "Location request timed out.";
    }
    showGeoBanner(`⚠️ ${msg}`, "#ef4444", 5000);
  }

  // Locate Me Button
  document.getElementById("btn-locate-me").addEventListener("click", () => {
    showGeoBanner("🛰️ Acquiring high-accuracy GPS position...", "#0284c7");

    if (!navigator.geolocation) {
      showGeoBanner("⚠️ Geolocation not supported by your browser.", "#ef4444", 4000);
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (pos) => {
        handleLocationUpdate(
          pos.coords.latitude,
          pos.coords.longitude,
          pos.coords.accuracy,
          false,
          true
        );
      },
      (err) => {
        handleGeoError(err);
      },
      { enableHighAccuracy: true, timeout: 12000, maximumAge: 0 }
    );
  });

  // Toggle Live Tracking Button
  document.getElementById("btn-live-tracking").addEventListener("click", () => {
    if (!state.isTracking) {
      startLiveTracking();
    } else {
      stopLiveTracking();
    }
  });

  function startLiveTracking() {
    if (!navigator.geolocation) {
      showGeoBanner("⚠️ Geolocation not supported by your browser.", "#ef4444", 4000);
      return;
    }

    showGeoBanner("🛰️ Initializing Live GPS walk tracking...", "#0284c7");

    state.watchId = navigator.geolocation.watchPosition(
      (pos) => {
        handleLocationUpdate(
          pos.coords.latitude,
          pos.coords.longitude,
          pos.coords.accuracy,
          true,
          !state.isTracking
        );
        state.isTracking = true;
        document.getElementById("btn-live-tracking").classList.add("tracking-active");
      },
      (err) => {
        console.warn("Live watch error:", err);
        handleGeoError(err);
        stopLiveTracking();
      },
      { enableHighAccuracy: true, timeout: 15000, maximumAge: 1000 }
    );
  }

  function stopLiveTracking() {
    if (state.watchId !== null) {
      navigator.geolocation.clearWatch(state.watchId);
      state.watchId = null;
    }
    state.isTracking = false;
    document.getElementById("btn-live-tracking").classList.remove("tracking-active");
    showGeoBanner("Live tracking paused.", "#64748b", 2500);
  }

  // "Use My Location" in Origin
  document.getElementById("btn-use-current-loc").addEventListener("click", () => {
    if (state.userLocation) {
      startSelect.value = "user_current_location";
      state.selectedStart = "user_current_location";
      calculateAndDisplayRoute();
      showGeoBanner("📍 Origin set to Your Current Location", "#10b981", 3000);
    } else {
      showGeoBanner("🛰️ Getting current location for origin...", "#0284c7");
      if (!navigator.geolocation) {
        showGeoBanner("⚠️ Geolocation not supported.", "#ef4444", 4000);
        return;
      }
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          handleLocationUpdate(
            pos.coords.latitude,
            pos.coords.longitude,
            pos.coords.accuracy,
            false,
            false
          );
          startSelect.value = "user_current_location";
          state.selectedStart = "user_current_location";
          calculateAndDisplayRoute();
          showGeoBanner("📍 Origin set to Your Current Location", "#10b981", 3000);
        },
        (err) => {
          handleGeoError(err);
        },
        { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
      );
    }
  });

  // Simulate Live Walking along active route
  document.getElementById("btn-simulate-walk").addEventListener("click", () => {
    toggleSimulatedLiveWalk();
  });

  function toggleSimulatedLiveWalk() {
    if (state.isSimWalking) {
      clearInterval(state.simWalkInterval);
      state.isSimWalking = false;
      document.getElementById("sim-walk-badge").textContent = "Start Walk";
      document.getElementById("sim-walk-badge").style.color = "var(--primary)";
      showGeoBanner("Walk simulation paused.", "#64748b", 2000);
      return;
    }

    if (!state.currentRouteResult || !state.currentRouteResult.path || state.currentRouteResult.path.length < 2) {
      alert("Please calculate a route first before simulating a live walk.");
      return;
    }

    const pathNodes = state.currentRouteResult.path;
    let idx = 0;
    state.isSimWalking = true;
    document.getElementById("sim-walk-badge").textContent = "Pause Walk";
    document.getElementById("sim-walk-badge").style.color = "var(--accent)";
    showGeoBanner("🚶 Simulating live walk along the optimal path...", "#10b981");

    switchView("view-find-route");

    state.simWalkInterval = setInterval(() => {
      if (idx >= pathNodes.length) {
        clearInterval(state.simWalkInterval);
        state.isSimWalking = false;
        document.getElementById("sim-walk-badge").textContent = "Start Walk";
        document.getElementById("sim-walk-badge").style.color = "var(--primary)";
        showGeoBanner("🎉 You have arrived at your destination!", "#10b981", 4000);
        return;
      }

      const nid = pathNodes[idx];
      const [wLat, wLon] = nodes[nid];

      // Update position to this node
      handleLocationUpdate(wLat, wLon, 3, false, false);

      // Pan smoothly
      map.panTo([wLat, wLon], { animate: true, duration: 0.6 });

      // Calculate remaining distance
      let remainingDist = 0;
      for (let i = idx; i < pathNodes.length - 1; i++) {
        const u = nodes[pathNodes[i]];
        const v = nodes[pathNodes[i + 1]];
        remainingDist += getHaversineDistMeters(u[0], u[1], v[0], v[1]);
      }

      document.getElementById("stat-dist").textContent = `${Math.round(remainingDist)} m`;
      document.getElementById("stat-time").textContent = `${Math.max(1, Math.round(remainingDist / 80))} min`;

      idx++;
    }, 850);
  }

  // -----------------------------------------------------------------
  // 12. Viva Simulation Sandbox & Modals
  // -----------------------------------------------------------------
  const modalViva = document.getElementById("modal-viva");
  document.getElementById("btn-open-viva-modal").addEventListener("click", () => {
    modalViva.classList.add("active");
  });

  // Road closures
  const btnBlockAdmin = document.getElementById("sim-block-admin");
  const badgeBlockAdmin = document.getElementById("badge-block-admin");
  let isAdminBlocked = false;

  btnBlockAdmin.addEventListener("click", () => {
    isAdminBlocked = !isAdminBlocked;
    if (isAdminBlocked) {
      btnBlockAdmin.classList.add("active");
      badgeBlockAdmin.textContent = "Closed";
      badgeBlockAdmin.style.color = "var(--danger)";
      state.blockedEdgeIds.add("e_8810045404_admin_west_entrance");
      state.blockedEdgeIds.add("e_admin_west_entrance_8812965151");
    } else {
      btnBlockAdmin.classList.remove("active");
      badgeBlockAdmin.textContent = "Normal";
      badgeBlockAdmin.style.color = "var(--text-muted)";
      state.blockedEdgeIds.delete("e_8810045404_admin_west_entrance");
      state.blockedEdgeIds.delete("e_admin_west_entrance_8812965151");
    }
    calculateAndDisplayRoute();
  });

  const btnBlockMoksha = document.getElementById("sim-block-moksha");
  const badgeBlockMoksha = document.getElementById("badge-block-moksha");
  let isMokshaBlocked = false;

  btnBlockMoksha.addEventListener("click", () => {
    isMokshaBlocked = !isMokshaBlocked;
    if (isMokshaBlocked) {
      btnBlockMoksha.classList.add("active");
      badgeBlockMoksha.textContent = "Closed";
      badgeBlockMoksha.style.color = "var(--danger)";
      state.blockedEdgeIds.add("e_8810045322_8812965134");
    } else {
      btnBlockMoksha.classList.remove("active");
      badgeBlockMoksha.textContent = "Normal";
      badgeBlockMoksha.style.color = "var(--text-muted)";
      state.blockedEdgeIds.delete("e_8810045322_8812965134");
    }
    calculateAndDisplayRoute();
  });

  const btnToggleRain = document.getElementById("sim-toggle-rain");
  const badgeRain = document.getElementById("badge-rain");
  let isRain = false;

  btnToggleRain.addEventListener("click", () => {
    isRain = !isRain;
    if (isRain) {
      btnToggleRain.classList.add("active");
      badgeRain.textContent = "Mud Penalty (2.5x)";
      badgeRain.style.color = "var(--secondary)";
      state.weatherFactor = 2.5;
    } else {
      btnToggleRain.classList.remove("active");
      badgeRain.textContent = "Off";
      badgeRain.style.color = "var(--text-muted)";
      state.weatherFactor = 1.0;
    }
    calculateAndDisplayRoute();
  });

  const btnToggleRush = document.getElementById("sim-toggle-rush");
  const badgeRush = document.getElementById("badge-rush");
  let isRush = false;

  btnToggleRush.addEventListener("click", () => {
    isRush = !isRush;
    if (isRush) {
      btnToggleRush.classList.add("active");
      badgeRush.textContent = "Congested";
      badgeRush.style.color = "var(--accent)";
      edges.slice(10, 35).forEach(e => state.rushEdgeIds.add(e.id));
    } else {
      btnToggleRush.classList.remove("active");
      badgeRush.textContent = "Off";
      badgeRush.style.color = "var(--text-muted)";
      state.rushEdgeIds.clear();
    }
    calculateAndDisplayRoute();
  });

  // Benchmark Comparison Modal
  const modalBenchmark = document.getElementById("modal-benchmark");
  document.getElementById("btn-compare-all").addEventListener("click", () => {
    const srcId = startSelect.value;
    const dstId = endSelect.value;

    let srcName = "Your Current Location";
    let startNode;
    if (srcId === "user_current_location") {
      startNode = state.userLocation ? state.userLocation.nearestNodeId : "2129002378";
    } else {
      const srcLm = landmarks.find(l => l.id === srcId);
      srcName = srcLm.name;
      startNode = srcLm.nearest_node;
    }

    const dstLm = landmarks.find(l => l.id === dstId);
    document.getElementById("bm-src").textContent = srcName;
    document.getElementById("bm-dst").textContent = dstLm.name;

    const endNode = dstLm.nearest_node;

    const opts = {
      blockedEdges: state.blockedEdgeIds,
      accessibleOnly: state.accessibleOnly,
      weatherFactor: state.weatherFactor,
      rushEdges: state.rushEdgeIds
    };

    const dRes = algos.runDijkstra(adjacency, startNode, endNode, nodes, opts);
    const aRes = algos.runAStar(adjacency, startNode, endNode, nodes, opts);
    const bRes = algos.runBFS(adjacency, startNode, endNode, nodes, opts);
    const dfRes = algos.runDFS(adjacency, startNode, endNode, nodes, opts);

    const tbody = document.getElementById("benchmark-tbody");
    tbody.innerHTML = `
      <tr class="best-algo">
        <td><strong>Dijkstra's (Min-Heap)</strong></td>
        <td><strong>${dRes.distance} m</strong></td>
        <td>${dRes.nodesVisited}</td>
        <td>${dRes.executionTimeMs} ms</td>
        <td><span class="badge badge-academic">Guaranteed Optimal</span></td>
      </tr>
      <tr>
        <td><strong>A* Search (Haversine)</strong></td>
        <td><strong>${aRes.distance} m</strong></td>
        <td>${aRes.nodesVisited} (Target Directed)</td>
        <td>${aRes.executionTimeMs} ms</td>
        <td><span class="badge badge-landmarks">Optimal (Admissible)</span></td>
      </tr>
      <tr>
        <td><strong>BFS (Breadth-First)</strong></td>
        <td>${bRes.distance} m</td>
        <td>${bRes.nodesVisited}</td>
        <td>${bRes.executionTimeMs} ms</td>
        <td><span class="badge badge-sports">Min Hops (${bRes.hops || 0})</span></td>
      </tr>
      <tr>
        <td><strong>DFS (Depth-First)</strong></td>
        <td>${dfRes.distance} m</td>
        <td>${dfRes.nodesVisited}</td>
        <td>${dfRes.executionTimeMs} ms</td>
        <td><span class="badge badge-gates">Sub-optimal Path</span></td>
      </tr>
    `;

    modalBenchmark.classList.add("active");
  });

  // Campus MST Modal
  const modalMst = document.getElementById("modal-mst");
  document.getElementById("btn-show-mst").addEventListener("click", () => {
    modalViva.classList.remove("active");
    modalMst.classList.add("active");
    runMSTComputation("kruskal");
  });

  document.getElementById("btn-run-kruskal").addEventListener("click", () => runMSTComputation("kruskal"));
  document.getElementById("btn-run-prim").addEventListener("click", () => runMSTComputation("prim"));

  function runMSTComputation(algoType) {
    const statusEl = document.getElementById("mst-status");
    statusEl.textContent = `Computing ${algoType.toUpperCase()} MST across 28 campus landmarks...`;

    setTimeout(() => {
      let mstResult;
      if (algoType === "kruskal") {
        mstResult = algos.runKruskalMST(landmarks, adjacency, nodes);
      } else {
        mstResult = algos.runPrimMST(landmarks, adjacency, nodes, "admin_block");
      }

      document.getElementById("mst-length").textContent = `${mstResult.totalLengthMeters} m`;
      const costEst = (mstResult.totalLengthMeters * 450).toLocaleString("en-IN");
      document.getElementById("mst-cost").textContent = `₹${costEst}`;
      document.getElementById("mst-landmarks").textContent = `${mstResult.connectedLandmarksCount} / ${landmarks.length}`;
      statusEl.textContent = `Completed in ${mstResult.executionTimeMs} ms (${mstResult.algorithm})`;

      const tbody = document.getElementById("mst-table-body");
      tbody.innerHTML = "";
      mstResult.treeEdges.forEach((e, idx) => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>#${idx + 1}</td>
          <td>${e.sourceName}</td>
          <td>${e.targetName}</td>
          <td>${Math.round(e.dist)} m</td>
        `;
        tbody.appendChild(row);
      });

      if (state.mstLayerGroup) map.removeLayer(state.mstLayerGroup);
      state.mstLayerGroup = L.layerGroup().addTo(map);

      mstResult.treeEdges.forEach(e => {
        if (e.path) {
          const coords = e.path.map(nid => nodes[nid]);
          L.polyline(coords, {
            color: "#06b6d4",
            weight: 3.5,
            opacity: 0.85,
            dashArray: "4, 4"
          }).addTo(state.mstLayerGroup);
        }
      });
    }, 50);
  }

  // Campus DP Event Optimizer
  const modalDp = document.getElementById("modal-dp");
  document.getElementById("btn-show-dp").addEventListener("click", () => {
    modalViva.classList.remove("active");
    modalDp.classList.add("active");
  });

  const sampleCampusEvents = [
    { name: "Moksha EDM Star Night", society: "Moksha Council", venue: "Moksha Arena", start: 18, end: 22, utility: 95 },
    { name: "Inaugural Keynote & Convocation", society: "Admin / VC Office", venue: "Admin Audi", start: 9, end: 12, utility: 90 },
    { name: "HackNSUT 24-Hour Hackathon", society: "CSI / IEEE", venue: "APJ Complex", start: 10, end: 18, utility: 88 },
    { name: "Cross-Campus Debate Finals", society: "Debating Society", venue: "Mini Audi", start: 10, end: 13, utility: 72 },
    { name: "Taarangana Dance Battle", society: "Capella Dance Club", venue: "SAC Hub", start: 13, end: 16, utility: 78 },
    { name: "Placement Preparation Seminar", society: "TnP Cell", venue: "APJ LT-1", start: 14, end: 17, utility: 84 },
    { name: "Robotics Arena Showcase", society: "RoboTech Club", venue: "Block 6 Foyer", start: 12, end: 15, utility: 68 },
    { name: "Acoustic Sunset Jam", society: "Crescendo Music Soc", venue: "Nescii Lawns", start: 17, end: 20, utility: 82 }
  ];

  document.getElementById("btn-run-dp").addEventListener("click", () => {
    const dpRes = algos.runDPEventAllocation(sampleCampusEvents);
    const box = document.getElementById("dp-results-box");
    box.style.display = "flex";

    document.getElementById("dp-score").textContent = `${dpRes.maxUtilityScore} pts`;
    document.getElementById("dp-count").textContent = `${dpRes.scheduledEvents.length} / ${sampleCampusEvents.length}`;

    const tbody = document.getElementById("dp-schedule-tbody");
    tbody.innerHTML = "";
    dpRes.scheduledEvents.forEach(ev => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td><strong>${ev.name}</strong></td>
        <td>${ev.society}</td>
        <td><span class="badge badge-hangouts">${ev.venue}</span></td>
        <td>${ev.start}:00 - ${ev.end}:00</td>
        <td><strong>${ev.utility} pts</strong></td>
      `;
      tbody.appendChild(row);
    });
  });

  // Modal Closers
  document.querySelectorAll(".close-modal").forEach((btn) => {
    btn.addEventListener("click", () => {
      const modalId = btn.getAttribute("data-modal");
      document.getElementById(modalId).classList.remove("active");
    });
  });

  document.querySelectorAll(".modal-overlay").forEach((overlay) => {
    overlay.addEventListener("click", (e) => {
      if (e.target === overlay) overlay.classList.remove("active");
    });
  });

  // -----------------------------------------------------------------
  // 14. Floating Controls & Theme Toggle
  // -----------------------------------------------------------------
  document.getElementById("btn-recenter").addEventListener("click", () => {
    map.flyTo(campusCenter, 16.5, { duration: 1 });
  });

  document.getElementById("btn-toggle-network").addEventListener("click", () => {
    state.showNetwork = !state.showNetwork;
    if (state.showNetwork) {
      if (!state.networkLayerGroup) {
        state.networkLayerGroup = L.layerGroup();
        edges.forEach(e => {
          L.polyline(e.coords, {
            color: "#64748b",
            weight: 1.5,
            opacity: 0.5
          }).addTo(state.networkLayerGroup);
        });
      }
      map.addLayer(state.networkLayerGroup);
    } else {
      if (state.networkLayerGroup) map.removeLayer(state.networkLayerGroup);
    }
  });

  const themeToggle = document.getElementById("theme-toggle");
  let isDark = false;
  themeToggle.addEventListener("click", () => {
    isDark = !isDark;
    document.body.setAttribute("data-theme", isDark ? "dark" : "light");
  });

  // Window resize & orientation change handler
  let resizeTimer = null;
  window.addEventListener("resize", () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
      map.invalidateSize();
      if (state.activeRoutePolyline && state.currentView === "view-find-route") {
        map.fitBounds(state.activeRoutePolyline.getBounds(), { padding: [30, 30] });
      }
    }, 150);
  });

  window.addEventListener("orientationchange", () => {
    setTimeout(() => {
      map.invalidateSize();
      if (state.activeRoutePolyline && state.currentView === "view-find-route") {
        map.fitBounds(state.activeRoutePolyline.getBounds(), { padding: [30, 30] });
      }
    }, 250);
  });

  // Initial Calculation
  calculateAndDisplayRoute();
});
