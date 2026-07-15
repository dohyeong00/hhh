<template>
  <div class="bg-slate-100 text-slate-800 min-h-screen flex flex-col items-center justify-center p-3 md:p-6 relative overflow-x-hidden">
    <div class="w-full max-w-4xl bg-white rounded-3xl shadow-2xl border border-slate-200 overflow-hidden flex flex-col h-[850px] relative transition-all duration-300">
      
      <header class="p-6 bg-gradient-to-r from-indigo-700 via-indigo-800 to-slate-900 text-white flex items-center justify-between shrink-0 shadow-md">
        <div class="flex items-center space-x-4">
          <div class="bg-indigo-500/20 p-3 rounded-2xl border border-indigo-400/20">
            <svg class="w-6 h-6 text-indigo-300" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
            </svg>
          </div>
          <div>
            <div class="flex items-center space-x-2">
              <h1 class="font-extrabold text-lg tracking-tight">𐦂𖨆𐀪𖠋 구미 경북권 커뮤니티 🗫</h1>
              <span class="bg-indigo-600 text-[10px] px-2.5 py-0.5 rounded-full font-bold text-indigo-100">익명 소통</span>
            </div>
            <p class="text-xs text-slate-300 font-normal mt-0.5">경북의 음식점·숙박·관광지·쇼핑·레포츠 정보를 넓고 쾌적한 화면에서 공유해 보세요</p>
          </div>
        </div>
        
        <button v-if="currentViewMode === 'list'" @click="switchView('write')" class="bg-white text-indigo-800 hover:bg-indigo-50 px-4 py-2.5 rounded-xl flex items-center space-x-1.5 text-xs font-bold transition-all shadow-md hover:shadow-lg hover:scale-[1.02] active:scale-95">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3m0 0v3m0-3h3m-3 0H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>새 글 작성</span>
        </button>
      </header>

      <div v-if="topAlertVisible" :class="topAlertIsError ? 'bg-red-50 border-b border-red-150 text-red-800' : 'bg-emerald-50 border-b border-emerald-100 text-emerald-800'" class="px-6 py-3 text-xs flex justify-between items-center shrink-0">
        <span class="font-semibold flex items-center">
          <svg v-if="!topAlertIsError" class="w-4 h-4 mr-2 text-emerald-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <svg v-else class="w-4 h-4 mr-2 text-red-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          {{ topAlertMsg }}
        </span>
        <button @click="closeTopAlert()">
          <svg class="w-4 h-4 text-emerald-400 hover:text-emerald-600" :class="{'text-red-400 hover:text-red-600': topAlertIsError}" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div class="bg-slate-50 border-b border-slate-200 px-6 py-4 shrink-0">
        <div class="flex items-center space-x-2 overflow-x-auto pb-1 scrollbar-hide">
          <button @click="filterCategory('전체')" 
            :class="activeFilterCategory === '전체' ? 'bg-slate-700 text-white border-slate-800 shadow-md font-extrabold' : 'bg-slate-200 text-slate-700 border-slate-300'"
            class="px-5 py-3 rounded-full text-xs font-bold transition-all shrink-0 border">
            전체 보기
          </button>
          
          <button v-for="cat in ['음식점', '숙박', '관광지', '쇼핑', '레포츠']" :key="cat" @click="filterCategory(cat)"
            :class="activeFilterCategory === cat ? getCategoryActiveColor(cat) : getCategoryBaseColor(cat)"
            class="px-5 py-3 rounded-full text-xs font-semibold transition-all shrink-0 border hover:shadow-sm">
            {{ getCategoryEmoji(cat) }} {{ cat }}
          </button>
        </div>
      </div>

      <main class="flex-1 overflow-y-auto p-6 bg-slate-50/20">
        
        <div v-if="currentViewMode === 'list'" class="space-y-4">
          <div class="flex items-center justify-between pb-2">
            <div class="relative flex-1 max-w-sm">
              <span class="absolute inset-y-0 left-0 flex items-center pl-3">
                <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </span>
              <input type="text" v-model="searchQuery" placeholder="검색하고 싶은 키워드를 입력해 보세요..." class="w-full pl-10 pr-4 py-2.5 bg-white border border-slate-250 rounded-xl text-xs focus:ring-2 focus:ring-indigo-500 focus:outline-none transition">
            </div>
            
            <div class="flex items-center space-x-2 text-[11px] font-bold text-slate-400 ml-auto">
              <button @click="changeSortMode('latest')" :class="currentSortMode === 'latest' ? 'text-indigo-600 font-extrabold' : 'text-slate-400 hover:text-slate-600'" class="transition-all">최신순</button>
              <span class="text-slate-200">|</span>
              <button @click="changeSortMode('views')" :class="currentSortMode === 'views' ? 'text-indigo-600 font-extrabold' : 'text-slate-400 hover:text-slate-600'" class="transition-all">인기순</button>
              <span class="text-xs text-slate-400 font-bold bg-slate-100 px-3 py-1.5 rounded-full ml-2">총 {{ filteredPosts.length }}개 소식</span>
            </div>
          </div>

          <div class="space-y-4">
            <div v-if="filteredPosts.length === 0" class="text-center py-24 bg-white rounded-3xl border border-dashed border-slate-200 p-8 shadow-inner">
              <svg class="w-14 h-14 text-slate-300 mx-auto mb-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M5 19a2 2 0 01-2-2V7a2 2 0 012-2h4l2 2h4a2 2 0 012 2v1M5 19h14a2 2 0 002-2v-5M5 19v-4a2 2 0 012-2h11a2 2 0 012 2v3m-7-3h.01M9 16h.01" />
              </svg>
              <p class="text-xs font-extrabold text-slate-400">선택한 카테고리에 등록된 이야기가 없습니다.</p>
              <p class="text-[11px] text-slate-300 mt-1">상단의 "새 글 작성"을 눌러 첫 소식을 전해보세요!</p>
            </div>

            <div v-for="post in filteredPosts" :key="post.id" @click="viewDetail(post.id)" class="bg-white hover:border-indigo-400 hover:shadow-lg px-6 py-5 rounded-2xl border border-slate-200/80 cursor-pointer transition-all duration-200 flex flex-col space-y-2.5">
              <div class="flex justify-between items-start">
                <div class="flex items-center space-x-3 overflow-hidden">
                  <span :class="getCategoryActiveColor(post.category)" class="text-[10px] px-2.5 py-1 rounded-full font-extrabold border shrink-0">
                    {{ getCategoryEmoji(post.category) }} {{ post.category }}
                  </span>
                  <h3 class="font-extrabold text-sm text-slate-800 truncate">{{ post.title }}</h3>
                </div>
                <span class="text-[10px] text-slate-400 shrink-0 font-bold">{{ post.date.split(' ')[0] }}</span>
              </div>
              <p class="text-xs text-slate-500 line-clamp-2 leading-relaxed">{{ post.content }}</p>
              <div class="flex justify-between items-center text-[11px] text-slate-400 pt-1">
                <div class="flex items-center space-x-2">
                  <svg class="w-4 h-4 text-slate-300" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                  <span class="font-bold text-slate-600">{{ post.author }}</span>
                </div>
                <div class="flex items-center space-x-1 text-slate-400">
                  <svg class="w-3.5 h-3.5 text-slate-300" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                  <span class="font-medium text-[10px]">{{ post.views || 0 }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="currentViewMode === 'write'" class="space-y-5">
          <div class="flex justify-between items-center border-b border-slate-200 pb-3">
            <h2 class="font-extrabold text-slate-800 text-base flex items-center">
              <svg class="w-5 h-5 mr-2 text-indigo-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
              경북 익명 글 작성
            </h2>
            <button @click="switchView('list')" class="text-xs text-slate-400 hover:text-slate-600 flex items-center font-semibold">
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
              </svg> 취소하고 목록으로
            </button>
          </div>
          
          <div class="space-y-4">
            <div>
              <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">카테고리 구분 (필수)</label>
              <select v-model="newPost.category" class="w-full bg-white border border-slate-200 rounded-xl px-5 py-3 text-xs focus:ring-2 focus:ring-indigo-500 focus:outline-none transition">
                <option value="음식점">🍔 음식점 (맛집, 카페)</option>
                <option value="숙박">🏨 숙박 (호텔, 글램핑, 민박)</option>
                <option value="관광지">⛰️ 관광지 (자연, 역사, 유적지)</option>
                <option value="쇼핑">🛍️ 쇼핑 (전통시장, 마트, 소품샵)</option>
                <option value="레포츠">🏄 레포츠 (액티비티, 등산, 라이딩)</option>
              </select>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">작성자 닉네임</label>
                <input type="text" v-model="newPost.author" placeholder="익명" class="w-full bg-white border border-slate-200 rounded-xl px-5 py-3 text-xs focus:ring-2 focus:ring-indigo-500 focus:outline-none transition">
              </div>
              <div>
                <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">글 비밀번호 (4자리 필수)</label>
                <input type="password" v-model="newPost.password" maxlength="4" placeholder="수정/삭제 시 필요한 비밀번호" class="w-full bg-white border border-slate-200 rounded-xl px-5 py-3 text-xs focus:ring-2 focus:ring-indigo-500 focus:outline-none transition">
              </div>
            </div>
            
            <div>
              <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">글 제목</label>
              <input type="text" v-model="newPost.title" placeholder="경북 방문객 및 주민들이 한눈에 알아볼 수 있는 흥미로운 제목을 적어주세요." class="w-full bg-white border border-slate-200 rounded-xl px-5 py-3 text-xs focus:ring-2 focus:ring-indigo-500 focus:outline-none transition">
            </div>
            
            <div>
              <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">내용 작성</label>
              <textarea v-model="newPost.content" rows="8" placeholder="상세한 후기, 찾아가는 길, 비용 정보 등 유용한 이야기를 자유롭게 작성해 보세요!" class="w-full bg-white border border-slate-200 rounded-xl p-4 text-xs focus:ring-2 focus:ring-indigo-500 focus:outline-none transition resize-none"></textarea>
            </div>
            
            <button @click="saveNewPost()" class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-extrabold text-xs py-3.5 rounded-xl transition-all shadow-md hover:shadow-lg hover:scale-[1.01]">
              이야기 등록 완료
            </button>
          </div>
        </div>

        <div v-if="currentViewMode === 'detail' && currentDetailPost" class="space-y-5">
          <div class="flex justify-between items-center border-b border-slate-100 pb-3">
            <button @click="switchView('list')" class="flex items-center text-xs font-bold text-slate-500 hover:text-indigo-600 transition">
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
              </svg> 목록으로 가기
            </button>
            
            <div class="flex space-x-1.5">
              <button @click="initiateAuth('edit')" class="text-xs text-amber-600 hover:bg-amber-50 px-3 py-2 rounded-xl font-bold transition flex items-center border border-amber-100">
                <svg class="w-3.5 h-3.5 mr-1" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                </svg>수정
              </button>
              <button @click="initiateAuth('delete')" class="text-xs text-red-600 hover:bg-red-50 px-3 py-2 rounded-xl font-bold transition flex items-center border border-red-100">
                <svg class="w-3.5 h-3.5 mr-1" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>삭제
              </button>
            </div>
          </div>

          <article class="space-y-4">
            <div class="flex items-center space-x-2">
              <span :class="getDetailBadgeColor(currentDetailPost.category)" class="text-xs px-3 py-1.5 rounded-full font-extrabold">
                {{ currentDetailPost.category }}
              </span>
            </div>
            <h3 class="font-extrabold text-slate-900 text-xl leading-snug">{{ currentDetailPost.title }}</h3>
            
            <div class="flex items-center space-x-3 text-xs text-slate-400 border-b border-slate-100 pb-3">
              <span class="font-bold text-slate-700 bg-slate-100 px-2.5 py-1 rounded-lg">{{ currentDetailPost.author }}</span>
              <span>•</span>
              <span class="flex items-center">
                <svg class="w-3.5 h-3.5 mr-1" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                {{ currentDetailPost.date }}
              </span>
              <span>•</span>
              <span class="text-xs text-slate-400 flex items-center space-x-1 font-medium">
                <svg class="w-3.5 h-3.5 text-slate-300" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                <span class="pl-0.5">조회수 {{ currentDetailPost.views }}</span>
              </span>
            </div>
            
            <div class="bg-slate-50/50 p-6 border border-slate-200/80 rounded-2xl text-xs leading-relaxed text-slate-600 whitespace-pre-line min-h-[220px] shadow-inner">
              {{ currentDetailPost.content }}
            </div>
          </article>

          <div v-if="authDrawerVisible" class="border border-amber-200 bg-amber-50/50 rounded-2xl p-5 space-y-3.5">
            <div class="flex justify-between items-center">
              <span class="text-xs font-bold text-slate-700 flex items-center">
                <svg v-if="currentAuthAction === 'edit'" class="w-4 h-4 mr-1.5 text-amber-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                </svg>
                <svg v-else class="w-4 h-4 mr-1.5 text-red-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
                {{ currentAuthAction === 'edit' ? '수정 비밀번호 확인' : '삭제 비밀번호 확인' }}
              </span>
              <button @click="closeAuthDrawer()" class="text-xs text-slate-400 hover:text-slate-600 font-bold">닫기</button>
            </div>
            <div class="flex space-x-3">
              <input type="password" v-model="authPasswordInput" placeholder="인증 비밀번호 4자리" class="flex-1 border border-slate-200 rounded-xl px-3.5 py-2.5 text-xs focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white">
              <button @click="verifyPassword()" class="bg-indigo-600 text-white px-5 py-2.5 rounded-xl text-xs font-extrabold hover:bg-indigo-700 transition">인증 검사</button>
            </div>
            <p v-if="authErrorMsg" class="text-xs text-red-500 font-bold flex items-center">
              <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
              입력하신 비밀번호가 올바르지 않습니다.
            </p>
          </div>

          <div v-if="editFormVisible" class="border-t border-slate-200 pt-5 space-y-4">
            <div class="flex items-center space-x-1.5">
              <svg class="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
              <h4 class="text-xs font-bold text-slate-700">포스팅 원문 수정</h4>
            </div>
            <div class="space-y-4">
              <div>
                <label class="block text-xs font-bold text-slate-400 mb-1.5">제목 수정</label>
                <input type="text" v-model="editTitle" class="w-full border border-slate-200 rounded-xl px-3.5 py-3 text-xs focus:outline-none focus:ring-2 focus:ring-indigo-500">
              </div>
              <div>
                <label class="block text-xs font-bold text-slate-400 mb-1.5">내용 수정</label>
                <textarea v-model="editContent" rows="8" class="w-full border border-slate-200 rounded-xl p-4 text-xs focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none"></textarea>
              </div>
              <button @click="submitUpdatePost()" class="w-full bg-indigo-600 text-white py-3 rounded-xl text-xs font-bold hover:bg-indigo-700 transition">수정 사항 게시하기</button>
            </div>
          </div>

        </div>
      </main>
      
      <footer class="p-4 bg-slate-100 border-t border-slate-200 text-center text-xs text-slate-400 shrink-0">
        경북 LocalHub 커뮤니티 전용 모듈 • SQLite-like LocalStorage Engine 활성화 중
      </footer>

      <div class="absolute bottom-6 right-6 z-50">
        <button @click="toggleChatbot()" class="bg-indigo-600 hover:bg-indigo-700 text-white p-4 rounded-full shadow-2xl flex items-center justify-center transition-transform hover:scale-105 active:scale-95">
          <svg v-if="!isChatbotOpen" class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
          </svg>
          <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M19 13l-7 7-7-7m14-6l-7 7-7-7" />
          </svg>
        </button>
      </div>

      <div v-if="isChatbotOpen" class="absolute bottom-24 right-6 w-80 h-[450px] bg-white rounded-2xl shadow-2xl border border-slate-200/90 z-50 flex flex-col overflow-hidden transition-all duration-200">
        <header class="p-4 bg-indigo-800 text-white flex items-center justify-between">
          <div class="flex items-center space-x-2">
            <div class="bg-white/10 p-1.5 rounded-lg">
              <svg class="w-4 h-4 text-indigo-200" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <div>
              <h4 class="text-xs font-bold">경북 도우미 로컬봇</h4>
              <span class="text-[9px] text-indigo-300 font-medium">실시간 대화 응대 중</span>
            </div>
          </div>
          <button @click="toggleChatbot()" class="text-indigo-200 hover:text-white">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </header>

        <div id="chat-messages" class="flex-1 overflow-y-auto p-3.5 space-y-3 bg-slate-50/50 text-xs">
          <div v-for="(msg, index) in chatMessages" :key="index" :class="msg.sender === 'user' ? 'flex justify-end' : 'flex items-start space-x-2'">
            <div v-if="msg.sender === 'bot'" class="bg-indigo-100 p-1 rounded-full shrink-0">
              <svg class="w-3.5 h-3.5 text-indigo-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <div :class="msg.sender === 'user' ? 'bg-indigo-600 text-white p-2.5 rounded-l-xl rounded-br-xl' : 'bg-white p-2.5 rounded-r-xl rounded-bl-xl border border-slate-100 shadow-sm'" class="max-w-[80%] leading-relaxed" v-html="msg.text">
            </div>
          </div>
        </div>

        <div class="p-2 bg-slate-100 border-t border-slate-200 flex items-center space-x-1.5 overflow-x-auto shrink-0 scrollbar-hide">
          <button @click="sendQuickKeyword('추천 맛집')" class="bg-white hover:bg-indigo-50 hover:text-indigo-600 text-slate-600 border border-slate-200 px-2 py-1 rounded-lg text-[10px] shrink-0 transition-all">🍔 맛집</button>
          <button @click="sendQuickKeyword('주요 관광지')" class="bg-white hover:bg-indigo-50 hover:text-indigo-600 text-slate-600 border border-slate-200 px-2 py-1 rounded-lg text-[10px] shrink-0 transition-all">⛰️ 관광지</button>
          <button @click="sendQuickKeyword('레포츠 활동')" class="bg-white hover:bg-indigo-50 hover:text-indigo-600 text-slate-600 border border-slate-200 px-2 py-1 rounded-lg text-[10px] shrink-0 transition-all">🏄 레포츠</button>
          <button @click="sendQuickKeyword('전통시장')" class="bg-white hover:bg-indigo-50 hover:text-indigo-600 text-slate-600 border border-slate-200 px-2 py-1 rounded-lg text-[10px] shrink-0 transition-all">🛍️ 쇼핑</button>
        </div>

        <div class="p-2.5 bg-white border-t border-slate-200 flex space-x-1.5 shrink-0">
          <input type="text" v-model="chatInput" @keypress.enter="sendChatMessage()" placeholder="질문을 전송해보세요..." class="flex-1 border border-slate-200 rounded-xl px-3 py-1.5 text-xs focus:outline-none focus:ring-1 focus:ring-indigo-600">
          <button @click="sendChatMessage()" class="bg-indigo-600 text-white p-1.5 rounded-xl hover:bg-indigo-700 transition">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          </button>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      posts: [],
      currentDetailPost: null,
      currentViewMode: 'list', 
      currentAuthAction: null, 
      activeFilterCategory: '전체',
      currentSortMode: 'latest',
      searchQuery: '',
      
      // 글쓰기 입력 데이터 모델링
      newPost: {
        category: '음식점',
        author: '',
        password: '',
        title: '',
        content: ''
      },

      // 상단 피드백 토스트 알림 상태
      topAlertVisible: false,
      topAlertMsg: '',
      topAlertIsError: false,

      // 권한 검증 및 수정 처리 모달
      authDrawerVisible: false,
      authPasswordInput: '',
      authErrorMsg: false,
      editFormVisible: false,
      editTitle: '',
      editContent: '',

      // 챗봇 내부 대화 내역 모델링
      isChatbotOpen: false,
      chatInput: '',
      chatMessages: [
        { text: '반갑습니다! 경북 LocalHub 로컬 도우미 챗봇입니다. 😊 <br><br>경북지역 맛집, 유명 숙소, 가볼만한 관광지, 특색 쇼핑 시장, 재밌는 레포츠 활동에 대해 질문해주세요!', sender: 'bot' }
      ],

      // 파일 내장 기본 초기 팩토리 데이터셋
      defaultData: [
        { id: 1, category: "관광지", title: "안동 하회마을 부용대 가시는 분들 필수 정보!", content: "하회마을을 한눈에 내려다볼 수 있는 부용대는 나룻배를 타고 건너가는 방법과 차량으로 멀리 돌아가는 법이 있습니다. 나룻배 편도가 인당 몇천 원 하지 않으니 나룻배 체험 강추드려요! 가을에는 경치가 정말 아름답습니다.", author: "안동사랑", password: "1111", date: "2026-07-14 10:10", views: 12 },
        { id: 2, category: "음식점", title: "구미 금오산 근처 파전이랑 수제비 대박집 후기", content: "금오산 도립공원 입구 야외 식당가에 있는 파전집 정말 대단하네요. 비오는 날 갔는데 바삭하고 두꺼운 해물파전이랑 뜨끈한 들깨수제비 조합이 완전 사기적입니다. 주말에는 웨이팅 있으니 조금 일찍 가세요.", author: "수제비러버", password: "2222", date: "2026-07-14 13:45", views: 45 },
        { id: 3, category: "숙박", title: "경주 보문단지 근처 가성비 오션뷰 한옥펜션", content: "경주 보문호수가 멀리 살짝 보이는 한옥 스타일 펜션에서 묵고 왔는데 정원이 너무 아기자기하게 예쁩니다. 밤에 한옥 처마 아래서 별 구경하는 감성이 끝내줍니다. 사장님도 정말 친절하셔요.", author: "한옥스테이", password: "3333", date: "2026-07-14 15:20", views: 28 },
        { id: 4, category: "쇼핑", title: "포항 죽도시장 대게 저렴하게 구매하는 노하우", content: "죽도시장 수산 구역 안쪽으로 깊숙이 들어갈수록 호객행위도 덜하고 가격이 다운됩니다. 당일 시세를 모바일 어플로 대충 파악하고 가시는 것이 좋으며, 대게를 사면서 쪄달라고 한 뒤 2층 초장집에서 바로 게딱지 볶음밥까지 드시면 극락입니다.", author: "죽도대게짱", password: "4444", date: "2026-07-14 16:05", views: 33 },
        { id: 5, category: "레포츠", title: "경북 청도 오션파크 루지 액티비티 주말 탑승 소감", content: "경북 남부권에서 레포츠를 찾으신다면 청도 군파크 루지 무조건 가보세요. 아시아 최대 급 길이로 알고 있는데, 리프트 타고 올라가는 산 전경부터 속도감 넘치는 곡선 주행까지 스트레스가 싹 풀립니다. 아이들도 동반 탑승해서 안전해요.", author: "스피드왕", password: "5555", date: "2026-07-14 16:30", views: 19 }
      ]
    }
  },
  computed: {
    // 검색어 필터링, 카테고리 셀렉션 및 최신순/조회순 결합 파이프라인 연산
    filteredPosts() {
      let source = this.posts;

      // 카테고리 분기 필터링
      if (this.activeFilterCategory !== '전체') {
        source = source.filter(p => p.category === this.activeFilterCategory);
      }

      // 검색 키워드 인덱스 매칭 필터링
      if (this.searchQuery.trim()) {
        const query = this.searchQuery.toLowerCase();
        source = source.filter(p => 
          p.title.toLowerCase().includes(query) || 
          p.content.toLowerCase().includes(query) ||
          p.author.toLowerCase().includes(query)
        );
      }

      // 정렬 모드 분기 연산
      if (this.currentSortMode === 'views') {
        return [...source].sort((a, b) => b.views === a.views ? b.id - a.id : (b.views || 0) - (a.views || 0));
      } else {
        return [...source].sort((a, b) => b.id - a.id);
      }
    }
  },
  mounted() {
    this.loadPosts();
  },
  methods: {
    loadPosts() {
      const stored = localStorage.getItem('localhub_gb_posts');
      if (stored) {
        const parsed = JSON.parse(stored);
        parsed.forEach(p => {
          if (p.views === undefined) p.views = 0;
        });
        this.posts = parsed;
      } else {
        this.posts = [...this.defaultData];
        this.savePostsToStorage();
      }
    },
    savePostsToStorage() {
      localStorage.setItem('localhub_gb_posts', JSON.stringify(this.posts));
    },
    switchView(view) {
      this.currentViewMode = view;
      if (view === 'write') {
        this.clearWriteFields();
      }
    },
    filterCategory(cat) {
      this.activeFilterCategory = cat;
      this.currentSortMode = 'latest';
      this.switchView('list');
    },
    changeSortMode(mode) {
      this.currentSortMode = mode;
    },
    clearWriteFields() {
      this.newPost = {
        category: '음식점',
        author: '',
        password: '',
        title: '',
        content: ''
      };
    },
    saveNewPost() {
      const author = this.newPost.author.trim() || "익명";
      const password = this.newPost.password.trim();
      const title = this.newPost.title.trim();
      const content = this.newPost.content.trim();

      if (!password || password.length < 4) {
        this.triggerStatusNotification("비밀번호는 안전을 위해 최소 4글자 이상 지정해야 합니다.", true);
        return;
      }
      if (!title || !content) {
        this.triggerStatusNotification("글 제목과 이야기를 채워 넣어주세요.", true);
        return;
      }

      const now = new Date();
      const formattedDate = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')} ${String(now.getHours()).padStart(2,'0')}:${String(now.getMinutes()).padStart(2,'0')}`;

      const newCreatedPost = {
        id: Date.now(),
        category: this.newPost.category,
        title,
        content,
        author,
        password,
        date: formattedDate,
        views: 0
      };

      this.posts.unshift(newCreatedPost);
      this.savePostsToStorage();
      this.switchView('list');
      this.triggerStatusNotification("새로운 익명 소통 게시글이 발행되었습니다.");
    },
    viewDetail(id) {
      const post = this.posts.find(p => p.id === id);
      if (!post) return;

      post.views = (post.views || 0) + 1;
      this.savePostsToStorage();

      this.currentDetailPost = post;
      this.closeAuthDrawer();
      this.switchView('detail');
    },
    initiateAuth(action) {
      this.currentAuthAction = action;
      this.authDrawerVisible = true;
      this.editFormVisible = false;
      this.authPasswordInput = '';
      this.authErrorMsg = false;
    },
    closeAuthDrawer() {
      this.currentAuthAction = null;
      this.authDrawerVisible = false;
      this.editFormVisible = false;
      this.authErrorMsg = false;
    },
    verifyPassword() {
      if (this.authPasswordInput !== this.currentDetailPost.password) {
        this.authErrorMsg = true;
        return;
      }

      this.authErrorMsg = false;
      this.authDrawerVisible = false;

      if (this.currentAuthAction === 'delete') {
        this.posts = this.posts.filter(p => p.id !== this.currentDetailPost.id);
        this.savePostsToStorage();
        this.switchView('list');
        this.triggerStatusNotification("게시물이 안전하게 삭제 처리되었습니다.");
      } else if (this.currentAuthAction === 'edit') {
        this.editFormVisible = true;
        this.editTitle = this.currentDetailPost.title;
        this.editContent = this.currentDetailPost.content;
      }
    },
    submitUpdatePost() {
      const updatedTitle = this.editTitle.trim();
      const updatedContent = this.editContent.trim();

      if (!updatedTitle || !updatedContent) {
        this.triggerStatusNotification("수정할 양식을 모두 작성하셔야 합니다.", true);
        return;
      }

      this.currentDetailPost.title = updatedTitle;
      this.currentDetailPost.content = updatedContent;
      this.savePostsToStorage();

      this.editFormVisible = false;
      this.triggerStatusNotification("수정 반영이 완료되었습니다.");
    },
    toggleChatbot() {
      this.isChatbotOpen = !this.isChatbotOpen;
    },
    sendChatMessage() {
      const query = this.chatInput.trim();
      if (!query) return;

      this.chatMessages.push({ text: query, sender: 'user' });
      this.chatInput = '';

      setTimeout(() => {
        const reply = this.generateBotReply(query);
        this.chatMessages.push({ text: reply, sender: 'bot' });
        this.scrollToBottom();
      }, 700);
    },
    sendQuickKeyword(keyword) {
      this.chatMessages.push({ text: keyword, sender: 'user' });
      setTimeout(() => {
        const reply = this.generateBotReply(keyword);
        this.chatMessages.push({ text: reply, sender: 'bot' });
        this.scrollToBottom();
      }, 500);
    },
    generateBotReply(query) {
      const q = query.toLowerCase();

      if (q.includes('맛집') || q.includes('음식점') || q.includes('먹거리')) {
        return `🍔 <strong>경북 로컬 추천 맛집 리스트</strong>입니다:<br>
        1. <strong>구미 '싱글벙글 복어'</strong>: 얼큰한 국물과 미나리 미니 복어탕의 진수!<br>
        2. <strong>경주 '교리김밥'</strong>: 부드러운 달걀지단이 꽉 찬 명물 김밥.<br>
        3. <strong>안동 '안동찜닭골목'</strong>: 안동 구시장에 위치한 오리지널 간장 베이스 찜닭!`;
      }
      if (q.includes('관광지') || q.includes('구경') || q.includes('가볼만')) {
        return `⛰️ <strong>경북 대표 가볼만한 명소</strong>입니다:<br>
        1. <strong>구미 금오산 도립공원</strong>: 대혜폭포와 도선굴 코스가 환상적입니다.<br>
        2. <strong>경주 불국사 & 석굴암</strong>: 경북 역사의 얼을 보여주는 대표 사찰.<br>
        3. <strong>안동 하회마을 & 부용대</strong>: 고택 체험과 낙동강 수변 드라이브 코스 추천!`;
      }
      if (q.includes('레포츠') || q.includes('활동') || q.includes('레저')) {
        return `🏄 <strong>경북 스릴 가득 레포츠 추천</strong>:<br>
        1. <strong>청도 군파크 루지</strong>: 짜릿한 긴 트랙을 고속 다운힐로 내달려보세요.<br>
        2. <strong>문경 패러글라이딩</strong>: 문경 활공장에서 하늘을 나는 잊지 못할 경험!<br>
        3. <strong>포항 영일대 서핑</strong>: 시원한 파도를 타고 달리는 동해 해양 스포츠의 성지.`;
      }
      if (q.includes('쇼핑') || q.includes('전통시장') || q.includes('시장')) {
        return `🛍️ <strong>경북 특색 쇼핑 & 시장 정보</strong>:<br>
        1. <strong>포항 죽도시장</strong>: 싱싱한 해산물과 과메기, 대게 쇼핑 천국!<br>
        2. <strong>구미 새마을중앙시장</strong>: 찹쌀 도너츠와 가성비 좋은 순대골목 명물.<br>
        3. <strong>경주 황리단길 소품샵</strong>: 아기자기한 전통 장식물과 디저트 굿즈 쇼핑.`;
      }
      if (q.includes('숙소') || q.includes('숙박') || q.includes('호텔')) {
        return `🏨 <strong>경북 낭만 숙박 추천</strong>:<br>
        1. <strong>경주 라한셀렉트</strong>: 보문호수 전망을 가진 고급스러운 숙박 코스.<br>
        2. <strong>영덕 하벳 리조트</strong>: 동해바다 해안가 바로 앞에 자리 잡은 이국적인 수영장 리조트.<br>
        3. <strong>안동 구름에 리조트</strong>: 전통 한옥 고택을 프라이빗한 감성으로 개조한 프리미엄 한옥스테이.`;
      }

      return `경북 LocalHub와 관련한 정보를 분석하고 있습니다. 🔍<br><br><strong>"추천 맛집", "주요 관광지", "전통시장", "레포츠 활동"</strong> 등을 위 추천 키워드 칩스나 채팅으로 물어봐 주시면 경북 명소들을 정확하게 설명해 드릴 수 있습니다.`;
    },
    triggerStatusNotification(msg, isError = false) {
      this.topAlertMsg = msg;
      this.topAlertIsError = isError;
      this.topAlertVisible = true;
      setTimeout(() => {
        this.closeTopAlert();
      }, 3500);
    },
    closeTopAlert() {
      this.topAlertVisible = false;
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const chatBox = document.getElementById('chat-messages');
        if (chatBox) {
          chatBox.scrollTop = chatBox.scrollHeight;
        }
      });
    },
    getCategoryEmoji(cat) {
      const emojis = { '음식점': '🍔', '숙박': '🏨', '관광지': '⛰️', '쇼핑': '🛍️', '레포츠': '🏄' };
      return emojis[cat] || '📝';
    },
    getCategoryBaseColor(cat) {
      const classes = {
        '음식점': 'bg-orange-50 text-orange-700 border-orange-100',
        '숙박': 'bg-sky-50 text-sky-700 border-sky-100',
        '관광지': 'bg-emerald-50 text-emerald-700 border-emerald-100',
        '쇼핑': 'bg-purple-50 text-purple-700 border-purple-100',
        '레포츠': 'bg-amber-50 text-amber-700 border-amber-100'
      };
      return classes[cat] || 'bg-slate-200 text-slate-700 border-slate-300';
    },
    getCategoryActiveColor(cat) {
      const classes = {
        '음식점': 'bg-orange-600 text-white border-orange-700 shadow-md font-extrabold',
        '숙박': 'bg-sky-600 text-white border-sky-700 shadow-md font-extrabold',
        '관광지': 'bg-emerald-600 text-white border-emerald-700 shadow-md font-extrabold',
        '쇼핑': 'bg-purple-600 text-white border-purple-700 shadow-md font-extrabold',
        '레포츠': 'bg-amber-600 text-white border-amber-700 shadow-md font-extrabold'
      };
      return classes[cat] || 'bg-slate-700 text-white border-slate-800 shadow-md font-extrabold';
    },
    getDetailBadgeColor(cat) {
      const classes = {
        '음식점': 'bg-orange-50 text-orange-700 border border-orange-200',
        '숙박': 'bg-sky-50 text-sky-700 border border-sky-200',
        '관광지': 'bg-emerald-50 text-emerald-700 border border-emerald-200',
        '쇼핑': 'bg-purple-50 text-purple-700 border border-purple-200',
        '레포츠': 'bg-amber-50 text-amber-700 border border-amber-200'
      };
      return classes[cat] || 'bg-slate-100 text-slate-700 border border-slate-250';
    }
  }
}
</script>

<style scoped>
/* 가로 스크롤 시 브라우저 기본 스크롤바 숨김 */
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>