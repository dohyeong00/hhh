const PLACE_DB = [
      // 경주시 (Gyeongju)
      { id: 'gb-1', city: 'Gyeongju', cityName: '경주시', name: '경주 불국사', lat: 35.7902, lng: 129.3321, category: '관광지', desc: '유네스코 세계문화유산으로 지정된 신라 불교 예술의 최고 정수.', icon: 'landmark', imageUrl: 'https://picsum.photos/400/300?random=1' },
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
const CATEGORIES_LIST = ['관광지', '레포츠', '쇼핑', '숙박', '음식점'];

export { PLACE_DB, CITIES_DB, CATEGORIES_LIST };