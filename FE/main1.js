/*const PLACE_DB = [
      // 경주시 (Gyeongju)
      { id: 'gb-1', city: 'Gyeongju', cityName: '경주시', name: '경주 불국사', lat: 35.7902, lng: 129.3321, category: '관광지', desc: '유네스코 세계문화유산으로 지정된 신라 불교 예술의 최고 정수.', icon: 'landmark' },
      { id: 'gb-2', city: 'Gyeongju', cityName: '경주시', name: '경주 황리단길', lat: 35.8392, lng: 129.2093, category: '쇼핑', desc: '한옥 전통 가옥들 사이의 트렌디한 인테리어 소품샵과 공방 탐색 명소.', icon: 'shopping-bag' },
      { id: 'gb-3', city: 'Gyeongju', cityName: '경주시', name: '라한셀렉트 경주', lat: 35.8436, lng: 129.2785, category: '숙박', desc: '보문호수를 한눈에 담아낼 수 있는 최고급 호캉스 숙소.', icon: 'hotel' },
      { id: 'gb-4', city: 'Gyeongju', cityName: '경주시', name: '함양집 보문점', lat: 35.8421, lng: 129.2568, category: '음식점', desc: '한우 한 그릇의 정성, 전통 방식의 대기 필수 육회 물회 명가.', icon: 'utensils' },
      { id: 'gb-5', city: 'Gyeongju', cityName: '경주시', name: '경주 루지월드', lat: 35.8415, lng: 129.2450, category: '레포츠', desc: '보문관광단지의 비경을 감상하며 스릴 넘치는 하강 레이스를 경험하는 어트랙션.', icon: 'bike' },

      // 안동시 (Andong)
      { id: 'gb-6', city: 'Andong', cityName: '안동시', name: '안동 하회마을', lat: 36.5385, lng: 128.5173, category: '관광지', desc: '풍산류씨가 600년간 보존해온 씨족 한옥마을이자 세계문화유산의 보고.', icon: 'home' },
      { id: 'gb-7', city: 'Andong', cityName: '안동시', name: '안동 일직식당', lat: 36.5683, lng: 128.7330, category: '음식점', desc: '50년 장인의 내공이 녹아든 안동 간고등어 구이 정식의 성지.', icon: 'utensils' },
      { id: 'gb-8', city: 'Andong', cityName: '안동시', name: '전통리조트 구름에', lat: 36.5781, lng: 128.7583, category: '숙박', desc: '고풍스러운 한옥 고택을 품격 있는 편의시설로 가꾼 한국식 고전 숙박 리조트.', icon: 'hotel' },

      // 포항시 (Pohang)
      { id: 'gb-9', city: 'Pohang', cityName: '포항시', name: '호미곶 상생의 손', lat: 36.0792, lng: 129.5694, category: '관광지', desc: '호미곶 광장 바다 한가운데 우뚝 솟아 신년 일출을 맞이하는 가장 유명한 조형물.', icon: 'sun' },
      { id: 'gb-10', city: 'Pohang', cityName: '포항시', name: '포항 스페이스워크', lat: 36.0631, lng: 129.3831, category: '레포츠', desc: '하늘을 걷는 아찔한 곡선형 롤러코스터 구조의 철제 예술 산책로.', icon: 'wind' },
      { id: 'gb-11', city: 'Pohang', cityName: '포항시', name: '포항 죽도시장', lat: 36.0354, lng: 129.3672, category: '쇼핑', desc: '대게 및 활어가 펄떡이는 동해안 최고 스케일의 사계절 활력 넘치는 수산시장.', icon: 'shopping-cart' },

      // 구미시 (Gumi)
      { id: 'gb-12', city: 'Gumi', cityName: '구미시', name: '금오산 도립공원', lat: 36.1065, lng: 128.3148, category: '관광지', desc: '웅장한 절벽과 채미정, 금오지가 연출하는 경북 도내 도립공원의 명소.', icon: 'mountain' },
      { id: 'gb-13', city: 'Gumi', cityName: '구미시', name: '금오산 케이블카', lat: 36.1130, lng: 128.3120, category: '레포츠', desc: '대혜폭포와 해운사 인근까지 자연 풍치를 편안히 날아오르며 감상하는 탑승 시설.', icon: 'cable-car' },

      // 울진군 (Uljin)
      { id: 'gb-14', city: 'Uljin', cityName: '울진군', name: '죽변해안 스카이레일', lat: 37.0601, lng: 129.4128, category: '레포츠', desc: '울진 동해의 에메랄드 해안선을 따라 주행하는 모노레일 체험기.', icon: 'compass' },
      { id: 'gb-15', city: 'Uljin', cityName: '울진군', name: '덕구온천 스파월드', lat: 37.0805, lng: 129.2801, category: '숙박', desc: '인공수가 가미되지 않은 태고의 순수 자연 용출수로 몸을 풀어내는 웰니스 온천 리조트.', icon: 'droplet' }
    ];

    // --- 2. 경상북도 시/군 딕셔너리 ---
 const CITIES_DB = [
      { id: 'all', name: '전체지역', lat: 36.5760, lng: 128.5056, zoom: 8.5 },
      { id: 'Gyeongju', name: '경주시', lat: 35.8392, lng: 129.2093, zoom: 11 },
      { id: 'Andong', name: '안동시', lat: 36.5683, lng: 128.7294, zoom: 11 },
      { id: 'Pohang', name: '포항시', lat: 36.0190, lng: 129.3435, zoom: 11 },
      { id: 'Gumi', name: '구미시', lat: 36.1196, lng: 128.3443, zoom: 11 },
      { id: 'Uljin', name: '울진군', lat: 36.9932, lng: 129.4005, zoom: 10 }
    ];
// 허용 카테고리 목록 정의
const CATEGORIES_LIST = ['관광지', '레포츠', '쇼핑', '숙박', '음식점'];*/
import { PLACE_DB, CITIES_DB, CATEGORIES_LIST } from './mock_data.js';

const API_BASE_URL = 'http://localhost:8000';

// --- 3. 전역 상태 관리 ---
let myRoute = [];
let currentFilteredPlaces = [];
let dbMarkers = [];
let routeMarkers = [];
let routePolyline = null;
let map = null;

let selectedCityId = 'all';
let selectedCategory = '관광지';

// --- 4. DOM 요소 참조 ---
const tabDbBtn = document.getElementById('tab-db');
const tabRouteBtn = document.getElementById('tab-route');
const panelDb = document.getElementById('panel-db');
const panelRoute = document.getElementById('panel-route');
const dbItemsList = document.getElementById('db-items-list');
const routeItemsContainer = document.getElementById('route-items-container');
const emptyStateEl = document.getElementById('empty-state');
const routeCountBadge = document.getElementById('route-count-badge');
const clearAllBtn = document.getElementById('clear-all-btn');
const toastEl = document.getElementById('toast');
const toastMessageEl = document.getElementById('toast-message');

const categoryFilterContainer = document.getElementById('category-filter-container');
const citySelectorGrid = document.getElementById('city-selector-grid');
const resultMetaCity = document.getElementById('result-meta-city');
const resultMetaCount = document.getElementById('result-meta-count');
const dbLoadingOverlay = document.getElementById('db-loading-overlay');

const apiStatusIndicator = document.getElementById('api-status-indicator');
const statusDot = document.getElementById('status-dot');
const statusText = document.getElementById('status-text');

// --- 5. 초기화 함수 ---
function init() {
  lucide.createIcons();

  map = L.map('map', {
    center: [36.5760, 128.5056],
    zoom: 8.5,
    zoomControl: false
  });

  L.control.zoom({ position: 'bottomright' }).addTo(map);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map);

  tabDbBtn.addEventListener('click', () => switchTab('db'));
  tabRouteBtn.addEventListener('click', () => switchTab('route'));
  map.on('click', () => map.closePopup());
  clearAllBtn.addEventListener('click', clearEntireRoute);

  buildCategoryFilters();
  buildCitySelector();

  triggerFastApiFetch();
  updateItineraryUI();
}

function buildCategoryFilters() {
  categoryFilterContainer.innerHTML = '';

  CATEGORIES_LIST.forEach(cat => {
    const btn = document.createElement('button');
    btn.className = 'px-3.5 py-1.5 rounded-full text-xs font-bold transition-all duration-150 flex items-center space-x-1 border focus:outline-none';
    btn.setAttribute('data-category', cat);
    updateCategoryBtnStyle(btn, cat, cat === selectedCategory);

    btn.addEventListener('click', () => {
      if (selectedCategory === cat) return;

      selectedCategory = cat;

      categoryFilterContainer.querySelectorAll('button').forEach(button => {
        const buttonCategory = button.getAttribute('data-category');
        updateCategoryBtnStyle(button, buttonCategory, buttonCategory === selectedCategory);
      });

      triggerFastApiFetch();
    });

    categoryFilterContainer.appendChild(btn);
  });
}

function updateCategoryBtnStyle(element, category, isActive) {
  if (isActive) {
    element.className = "px-3.5 py-1.5 rounded-full text-xs font-bold transition-all duration-150 flex items-center space-x-1 bg-white text-emerald-900 border-white shadow-sm hover:bg-emerald-50 scale-105";
    element.innerHTML = `<span class="inline-block w-2 h-2 rounded-full bg-emerald-500 mr-1"></span> ${category}`;
  } else {
    element.className = "px-3.5 py-1.5 rounded-full text-xs font-bold transition-all duration-150 flex items-center space-x-1 bg-emerald-800/60 text-emerald-200 border-emerald-700/60 hover:bg-emerald-800 hover:text-white";
    element.innerHTML = `<span class="inline-block w-2 h-2 rounded-full bg-slate-500 mr-1"></span> ${category}`;
  }
}

let cityDropdownOpen = false;

function buildCitySelector() {
  citySelectorGrid.innerHTML = `
    <div class="relative">
      <button id="city-dropdown-toggle" type="button"
        class="w-full text-left px-4 py-3 rounded-2xl border border-slate-200 bg-white shadow-sm flex items-center justify-between space-x-3 transition hover:border-emerald-300">
        <span id="city-dropdown-label">${getCityName(selectedCityId)}</span>
        <i data-lucide="chevron-down" id="city-dropdown-arrow" class="w-4 h-4 transition-transform"></i>
      </button>

      <div id="city-dropdown-menu"
        class="absolute left-0 right-0 mt-2 max-h-56 overflow-y-auto rounded-2xl border border-slate-200 bg-white shadow-xl z-20 hidden">
      </div>
    </div>
  `;

  lucide.createIcons();

  const toggle = document.getElementById('city-dropdown-toggle');
  const menu = document.getElementById('city-dropdown-menu');
  const arrow = document.getElementById('city-dropdown-arrow');

  toggle.addEventListener('click', (event) => {
    event.stopPropagation();
    cityDropdownOpen = !cityDropdownOpen;
    menu.classList.toggle('hidden', !cityDropdownOpen);
    arrow.style.transform = cityDropdownOpen ? 'rotate(180deg)' : 'rotate(0deg)';
  });

  document.addEventListener('click', () => {
    if (cityDropdownOpen) {
      cityDropdownOpen = false;
      menu.classList.add('hidden');
      arrow.style.transform = 'rotate(0deg)';
    }
  });

  const sortedCities = [
    CITIES_DB[0],
    ...CITIES_DB.slice(1).sort((a, b) => a.name.localeCompare(b.name, 'ko'))
  ];

  sortedCities.forEach(city => {
    const item = document.createElement('button');
    item.type = 'button';
    item.className = 'w-full text-left px-4 py-3 border-b border-slate-100 text-sm transition hover:bg-slate-50';
    item.textContent = city.name;
    item.setAttribute('data-city-id', city.id);

    if (city.id === selectedCityId) {
      item.classList.add('bg-emerald-50', 'text-emerald-700', 'font-semibold');
    }

    item.addEventListener('click', () => {
      selectedCityId = city.id;
      updateCityDropdownLabel();
      cityDropdownOpen = false;
      menu.classList.add('hidden');
      arrow.style.transform = 'rotate(0deg)';
      map.setView([city.lat, city.lng], city.zoom);
      triggerFastApiFetch();
    });

    menu.appendChild(item);
  });
}

function getCityName(cityId) {
  const found = CITIES_DB.find(c => c.id === cityId);
  return found ? found.name : '전체지역';
}

function updateCityDropdownLabel() {
  const label = document.getElementById('city-dropdown-label');
  if (label) label.textContent = getCityName(selectedCityId);
}

async function triggerFastApiFetch() {
  dbItemsList.classList.add('hidden');
  dbLoadingOverlay.classList.remove('hidden');

  statusDot.className = "inline-block w-2.5 h-2.5 rounded-full bg-amber-500 animate-pulse";
  statusText.textContent = "FastAPI 쿼리 전송 중...";

  try {
    const results = await fetchPlacesFromFastAPI(selectedCityId, selectedCategory);
    currentFilteredPlaces = results.items || results;

    const targetCityObj = CITIES_DB.find(c => c.id === selectedCityId);
    resultMetaCity.textContent = `${targetCityObj.name} 검색 결과`;
    resultMetaCount.textContent = `총 ${currentFilteredPlaces.length}개 발견`;

    renderDatabaseList(currentFilteredPlaces);
    renderMapPlaces(currentFilteredPlaces);
  } catch (err) {
    console.error(err);
    showToast('서버 데이터를 불러오는 중 오류가 발생했습니다.');
  } finally {
    dbLoadingOverlay.classList.add('hidden');
    dbItemsList.classList.remove('hidden');

    statusDot.className = "inline-block w-2.5 h-2.5 rounded-full bg-emerald-500";
    statusText.textContent = `조회 완료 (선택: ${selectedCategory})`;
  }
}

async function fetchPlacesFromFastAPI(cityId, category) {
  const params = new URLSearchParams();
  if (cityId && cityId !== 'all') params.append('region', cityId);
  if (category) params.append('category', category);
  params.append('limit', '100');

  const res = await fetch(`${API_BASE_URL}/places/search?${params.toString()}`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

function addPlaceToRoute(dbId) {
  const selectedPlace = currentFilteredPlaces.find(p => p.id === dbId)
    || PLACE_DB.find(p => p.id === dbId);

  if (!selectedPlace) {
    console.warn('추가할 장소를 찾지 못했습니다.', dbId);
    showToast('선택한 장소를 코스에 추가하지 못했습니다.');
    return;
  }

  const alreadyAdded = myRoute.some(item => item.dbId === selectedPlace.id);
  if (alreadyAdded) {
    showToast('이미 코스에 추가된 장소입니다.');
    return;
  }

  const instanceId = 'route-' + Date.now() + '-' + Math.random().toString(36).substr(2, 5);
  const newRouteItem = {
    id: instanceId,
    dbId: selectedPlace.id,
    name: selectedPlace.name,
    lat: selectedPlace.lat,
    lng: selectedPlace.lng,
    category: selectedPlace.category,
    cityName: selectedPlace.cityName,
    desc: selectedPlace.desc
  };

  myRoute.push(newRouteItem);
  updateItineraryUI();
  showToast(`'${selectedPlace.name}' 일정이 최적 경로에 성공적으로 가미되었습니다.`);

  if (map) map.closePopup();
  switchTab('route');
}

window.addFromDb = function(dbId) {
  addPlaceToRoute(dbId);
};

function renderDatabaseList(places) {
  dbItemsList.innerHTML = '';

  if (places.length === 0) {
    dbItemsList.innerHTML = `
      <div class="p-8 text-center text-slate-400 bg-slate-50 rounded-xl border border-dashed border-slate-200 mt-2">
        <i data-lucide="info" class="w-8 h-8 text-slate-300 mx-auto mb-2"></i>
        <p class="font-medium text-slate-500 text-xs">선택하신 카테고리에 해당하는<br>명소가 현재 지역에 없습니다.</p>
      </div>
    `;
    lucide.createIcons();
    return;
  }

  places.forEach(place => {
    const item = document.createElement('div');
    item.className = 'p-3 bg-white border border-slate-100 rounded-xl hover:border-emerald-200 hover:shadow-md hover:shadow-emerald-50/20 transition duration-150 flex items-start justify-between group cursor-pointer';

    item.innerHTML = `
      <img src="${place.imageUrl}"
        class="w-20 h-20 rounded-lg object-cover shrink-0"
        onerror="this.src=''" />
      <div class="flex items-start space-x-3 flex-1 min-w-0">
        <div class="bg-emerald-50 text-emerald-600 p-2 rounded-lg mt-0.5 group-hover:bg-emerald-100 transition duration-150">
          <i data-lucide="star" class="w-4 h-4 fill-emerald-600"></i>
        </div>
        <div class="flex-1 min-w-0 pr-2">
          <div class="flex items-center space-x-2">
            <h4 class="font-bold text-slate-800 text-sm truncate">${place.name}</h4>
            <span class="bg-emerald-50 text-emerald-800 text-[10px] font-medium px-1.5 py-0.5 rounded">${place.category}</span>
          </div>
          <span class="text-[9px] text-emerald-700 font-bold bg-emerald-50/50 border border-emerald-100 px-1 py-0.2 rounded mt-0.5 inline-block">${place.cityName}</span>
          <p class="text-[11px] text-slate-500 mt-1 line-clamp-1 leading-relaxed">${place.desc}</p>
        </div>
      </div>
      <button class="bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold py-1.5 px-3 rounded-lg flex items-center space-x-1 shrink-0 transition" onclick="event.stopPropagation(); addFromDb('${place.id}')">
        <i data-lucide="plus" class="w-3.5 h-3.5"></i>
        <span>추가</span>
      </button>
    `;

    item.addEventListener('click', () => {
      map.setView([place.lat, place.lng], 14);
      const targetMarker = dbMarkers.find(m => m.options.dbId === place.id);
      if (targetMarker) targetMarker.openPopup();
    });

    dbItemsList.appendChild(item);
  });

  lucide.createIcons();
}

function renderMapPlaces(places) {
  dbMarkers.forEach(marker => map.removeLayer(marker));
  dbMarkers = [];

  places.forEach(place => {
    const iconHtml = `<div class="db-pin"><i data-lucide="star" style="fill: white;"></i></div>`;
    const customIcon = L.divIcon({
      className: 'custom-div-icon',
      html: iconHtml,
      iconSize: [30, 30],
      iconAnchor: [15, 15]
    });

    const marker = L.marker([place.lat, place.lng], {
      icon: customIcon,
      dbId: place.id
    }).addTo(map);

    const popupContent = `
      <div class="p-2.5 max-w-sm">
        <img src="${place.imageUrl}"
          class="w-full h-40 rounded-lg object-cover mb-2"
          onerror="this.src=''" />

        <div class="flex items-center space-x-1.5 mb-1">
          <span class="inline-block bg-emerald-100 text-emerald-800 text-[10px] font-bold px-2.5 py-0.5 rounded-full">${place.category}</span>
          <span class="text-[10px] text-slate-400 font-semibold">${place.cityName}</span>
        </div>
        <h4 class="font-bold text-base text-slate-900 mb-1">${place.name}</h4>
        <p class="text-xs text-slate-500 mb-3.5 leading-relaxed">${place.desc}</p>
        <button onclick="addFromDb('${place.id}')" class="w-full bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold py-2 rounded-lg shadow-sm transition flex items-center justify-center space-x-1">
          <i data-lucide="plus-circle" style="width:14px; height:14px;"></i>
          <span>일정에 추가하기</span>
        </button>
      </div>
    `;

    marker.bindPopup(popupContent, { minWidth: 200 });
    dbMarkers.push(marker);
  });

  lucide.createIcons();
}

function showToast(message) {
  toastMessageEl.textContent = message;
  toastEl.classList.remove('translate-y-20', 'opacity-0');
  toastEl.classList.add('translate-y-0', 'opacity-100');

  setTimeout(() => {
    toastEl.classList.remove('translate-y-0', 'opacity-100');
    toastEl.classList.add('translate-y-20', 'opacity-0');
  }, 2500);
}

function switchTab(tabName) {
  if (tabName === 'db') {
    tabDbBtn.classList.add('text-emerald-600', 'border-emerald-500');
    tabDbBtn.classList.remove('text-slate-400', 'border-transparent');
    tabRouteBtn.classList.add('text-slate-400', 'border-transparent');
    tabRouteBtn.classList.remove('text-emerald-600', 'border-emerald-500');
    panelDb.classList.remove('hidden');
    panelRoute.classList.add('hidden');
  } else {
    tabRouteBtn.classList.add('text-emerald-600', 'border-emerald-500');
    tabRouteBtn.classList.remove('text-slate-400', 'border-transparent');
    tabDbBtn.classList.add('text-slate-400', 'border-transparent');
    tabDbBtn.classList.remove('text-emerald-600', 'border-emerald-500');
    panelRoute.classList.remove('hidden');
    panelDb.classList.add('hidden');
  }
}

function removeItineraryItem(id) {
  const removedItem = myRoute.find(item => item.id === id);
  if (!removedItem) return;

  myRoute = myRoute.filter(item => item.id !== id);

  updateItineraryUI();
  showToast(`'${removedItem.name}' 일정을 코스에서 제거했습니다.`);
}

function clearEntireRoute() {
  if (myRoute.length === 0) return;
  myRoute = [];
  updateItineraryUI();
  showToast('모든 일정이 초기화되었습니다.');
}

function updateItineraryUI() {
  routeCountBadge.textContent = myRoute.length;
  renderRouteList();
  renderMapRouteLine();
}

function renderRouteList() {
  if (myRoute.length === 0) {
    emptyStateEl.classList.remove('hidden');
    const items = routeItemsContainer.querySelectorAll('.todo-item');
    items.forEach(item => item.remove());
    return;
  }

  emptyStateEl.classList.add('hidden');

  const existingItems = routeItemsContainer.querySelectorAll('.todo-item');
  existingItems.forEach(item => item.remove());

  myRoute.forEach((spot, index) => {
    const itemEl = document.createElement('div');
    itemEl.className = 'todo-item bg-white border border-slate-200 rounded-xl p-4 shadow-sm hover:shadow-md hover:border-blue-200 transition duration-150 cursor-grab active:cursor-grabbing relative flex items-start space-x-3 group';
    itemEl.setAttribute('draggable', 'true');
    itemEl.setAttribute('data-id', spot.id);
    itemEl.setAttribute('data-index', index);

    itemEl.innerHTML = `
      <div class="bg-blue-600 text-white font-extrabold text-xs rounded-full w-6 h-6 flex items-center justify-center shrink-0 mt-0.5 shadow-md">
        ${index + 1}
      </div>

      <div class="flex-1 min-w-0 pr-4 select-none">
        <h4 class="font-bold text-slate-800 text-sm truncate flex items-center justify-between">
          <span>${spot.name}</span>
        </h4>
        <div class="flex items-center space-x-1.5 mt-0.5">
          <span class="inline-block bg-slate-100 text-slate-600 text-[9px] font-medium px-1 rounded">${spot.category}</span>
          <span class="text-[9px] text-slate-400 font-bold">${spot.cityName}</span>
        </div>
        <p class="text-[11px] text-slate-400 mt-1 line-clamp-1">${spot.desc}</p>
      </div>

      <div class="text-slate-300 group-hover:text-slate-500 transition shrink-0 mt-1">
        <i data-lucide="grab" class="w-4 h-4"></i>
      </div>

      <div class="absolute right-3 bottom-1.5 opacity-0 group-hover:opacity-100 transition duration-150 text-[9px] text-rose-500 font-bold">
        마우스 우클릭 시 삭제
      </div>
    `;

    itemEl.addEventListener('contextmenu', (e) => {
      e.preventDefault();
      removeItineraryItem(spot.id);
    });

    itemEl.addEventListener('click', (e) => {
      if (e.target.closest('.text-slate-300')) return;
      map.setView([spot.lat, spot.lng], 14);
    });

    itemEl.addEventListener('dragstart', handleDragStart);
    itemEl.addEventListener('dragover', handleDragOver);
    itemEl.addEventListener('dragleave', handleDragLeave);
    itemEl.addEventListener('drop', handleDrop);
    itemEl.addEventListener('dragend', handleDragEnd);

    routeItemsContainer.appendChild(itemEl);
  });

  lucide.createIcons();
}

function renderMapRouteLine() {
  routeMarkers.forEach(m => map.removeLayer(m));
  routeMarkers = [];

  if (routePolyline) {
    map.removeLayer(routePolyline);
    routePolyline = null;
  }

  const coordinates = [];

  myRoute.forEach((spot, index) => {
    coordinates.push([spot.lat, spot.lng]);

    const iconHtml = `<div class="route-pin"><span>${index + 1}</span></div>`;
    const customIcon = L.divIcon({
      className: 'custom-div-icon',
      html: iconHtml,
      iconSize: [32, 32],
      iconAnchor: [16, 32]
    });

    const marker = L.marker([spot.lat, spot.lng], { icon: customIcon }).addTo(map);

    marker.bindTooltip(`<strong>${index + 1}순위: ${spot.name}</strong><br><span style="font-size:10px; color:#ef4444;">우클릭 시 제거</span>`, {
      direction: 'top',
      offset: [0, -25]
    });

    marker.on('click', (e) => {
      L.DomEvent.stopPropagation(e);
      map.setView([spot.lat, spot.lng], map.getZoom());
    });

    marker.on('contextmenu', (e) => {
      L.DomEvent.stopPropagation(e);
      removeItineraryItem(spot.id);
    });

    routeMarkers.push(marker);
  });

  if (coordinates.length >= 2) {
    routePolyline = L.polyline(coordinates, {
      color: '#2563eb',
      weight: 4,
      opacity: 0.9,
      dashArray: '8, 8',
      lineJoin: 'round'
    }).addTo(map);

    map.fitBounds(routePolyline.getBounds(), { padding: [80, 80] });
  }
}

let dragSrcElement = null;

function handleDragStart(e) {
  dragSrcElement = this;
  this.classList.add('dragging');
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/plain', this.getAttribute('data-id'));
}

function handleDragOver(e) {
  if (e.preventDefault) e.preventDefault();
  this.classList.add('border-blue-400', 'bg-blue-50/20', 'scale-[1.01]');
  return false;
}

function handleDragLeave(e) {
  this.classList.remove('border-blue-400', 'bg-blue-50/20', 'scale-[1.01]');
}

function handleDrop(e) {
  e.stopPropagation();
  e.preventDefault();

  const draggedId = e.dataTransfer.getData('text/plain');
  const targetId = this.getAttribute('data-id');

  if (draggedId !== targetId) {
    const draggedIndex = myRoute.findIndex(item => item.id === draggedId);
    const targetIndex = myRoute.findIndex(item => item.id === targetId);

    if (draggedIndex !== -1 && targetIndex !== -1) {
      const [movedItem] = myRoute.splice(draggedIndex, 1);
      myRoute.splice(targetIndex, 0, movedItem);
      updateItineraryUI();
    }
  }
  return false;
}

function handleDragEnd(e) {
  this.classList.remove('dragging');
  const items = routeItemsContainer.querySelectorAll('.todo-item');
  items.forEach(item => {
    item.classList.remove('border-blue-400', 'bg-blue-50/20', 'scale-[1.01]');
  });
}

function renderCityList(cities) {
  const container = document.getElementById('db-city-list');
  container.innerHTML = '';
  cities.forEach(city => {
    const btn = document.createElement('button');
    btn.textContent = city.name;
    btn.className = 'px-3.5 py-1.5 rounded-full text-xs font-bold bg-white text-emerald-900 border border-emerald-300';
    btn.onclick = () => {
      selectedCityId = city.id;
      triggerFastApiFetch();
      updateCitySelectionUI();
    };
    container.appendChild(btn);
  });
}

window.onload = init;