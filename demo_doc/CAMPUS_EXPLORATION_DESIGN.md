# 校园探索游戏模块 - 详细设计方案

## 🎮 核心玩法流程

```
用户进入3D场景
    ↓
自由漫游校园
    ↓
发现高亮地标（发光/图标）
    ↓
点击地标查看信息卡片
    ↓
完成知识问答
    ↓
获得积分和徽章奖励
    ↓
解锁下一个地标
```

---

## 📋 地标数据结构

### MongoDB数据模型

```javascript
// 地标 (Landmark)
{
  _id: ObjectId,
  name: "信息大楼",
  nameEn: "Information Building",

  // 位置信息
  position: {
    x: 150,
    y: 0,
    z: 80
  },

  // 外观
  appearance: {
    model: "building_info.glb",
    color: "#3498db",
    icon: "building",
    highlightColor: "#f1c40f"
  },

  // 基础信息
  info: {
    description: "信息大楼是清华SIGS的主教学楼之一，...",
    descriptionEn: "The Information Building is...",
    buildYear: 2002,
    architect: "某某建筑事务所",
    area: "12000平方米",
    floors: 6
  },

  // 多媒体
  media: {
    images: [
      "https://example.com/info_building_1.jpg",
      "https://example.com/info_building_2.jpg"
    ],
    panorama: "https://example.com/info_building_360.jpg", // 可选
    video: "" // 可选
  },

  // 知识问答
  quiz: {
    question: "信息大楼主要用于什么用途？",
    options: [
      "A. 教学办公",
      "B. 学生宿舍",
      "C. 实验研究",
      "D. 食堂就餐"
    ],
    correctAnswer: 0,
    explanation: "信息大楼主要用于教学和办公，是..."
  },

  // 游戏数据
  game: {
    points: 20, // 打卡积分
    difficulty: "easy", // easy/medium/hard
    requiredLevel: 1, // 需要的等级
    order: 1, // 推荐探索顺序
    category: "teaching" // teaching/dormitory/life/research
  },

  // 状态
  isActive: true,
  createdAt: Date,
  updatedAt: Date
}

// 用户探索进度 (UserProgress)
{
  userId: ObjectId,
  landmarks: [
    {
      landmarkId: ObjectId,
      status: "completed", // pending/completed/skipped
      completedAt: Date,
      quizCorrect: true,
      pointsEarned: 20
    }
  ],
  totalPoints: 150,
  currentLevel: 2,
  badges: ["first_explorer", "quiz_master"]
}
```

---

## 🎨 界面设计

### 主界面布局

```
┌─────────────────────────────────────────────────────────┐
│  🔔  SIGS探索者                    Lv.2  🏆 150分   👤    │
├─────────────────────────────────────────────────────────┤
│                                                           │
│                                                           │
│                        3D场景区域                          │
│                                                           │
│                   [Low Poly校园模型]                       │
│                                                           │
│                    📍  📍  📍                            │
│                 (可点击的地标点)                           │
│                                                           │
│                                                           │
├─────────────────────────────────────────────────────────┤
│  🗺️ 地图    📍 地标列表    🏆 排行榜    👤 个人中心      │
└─────────────────────────────────────────────────────────┘
```

### 地标信息卡片

```
┌─────────────────────────────────────┐
│          信息大楼                     │
│     Information Building             │
├─────────────────────────────────────┤
│  [建筑照片]                          │
│                                      │
│  📍 教学楼 · 建于2002年              │
│                                      │
│  信息大楼是清华SIGS的主教学楼之一，   │
│  主要用于教学和办公活动。大楼设计     │
│  现代化，设施完善...                 │
│                                      │
│  ┌─────────────────────────────┐    │
│  │ ❓ 知识问答                   │    │
│  │                             │    │
│  │ 信息大楼主要用于什么用途？     │    │
│  │                             │    │
│  │ ⚪ A. 教学办公               │    │
│  │ ⚪ B. 学生宿舍               │    │
│  │ ⚪ C. 实验研究               │    │
│  │ ⚪ D. 食堂就餐               │    │
│  │                             │    │
│  │      [提交答案]              │    │
│  └─────────────────────────────┘    │
│                                      │
│           [关闭]                     │
└─────────────────────────────────────┘
```

### 答对后奖励弹窗

```
┌─────────────────────────────────────┐
│          🎉 恭喜你！                 │
│                                      │
│            ✅ 回答正确                │
│                                      │
│           +20 积分                    │
│                                      │
│        [获得徽章：知识探索者]         │
│                                      │
│           [继续探索]                 │
└─────────────────────────────────────┘
```

---

## 💻 前端代码实现

### 1. Three.js 3D场景核心代码

```vue
<!-- CampusExplorer.vue -->
<template>
  <div class="campus-explorer">
    <!-- 顶部导航栏 -->
    <div class="top-bar">
      <h1>🏫 SIGS校园探索</h1>
      <div class="user-info">
        <span class="level">Lv.{{ userLevel }}</span>
        <span class="points">🏆 {{ totalPoints }}分</span>
        <span class="avatar">👤</span>
      </div>
    </div>

    <!-- 3D场景容器 -->
    <div ref="canvasContainer" class="canvas-container"></div>

    <!-- 地标信息弹窗 -->
    <LandmarkCard
      v-if="selectedLandmark"
      :landmark="selectedLandmark"
      @close="selectedLandmark = null"
      @complete="handleLandmarkComplete"
    />

    <!-- 底部导航 -->
    <div class="bottom-nav">
      <button @click="showMap = true">🗺️ 地图</button>
      <button @click="showLandmarkList = true">📍 地标</button>
      <button @click="showLeaderboard = true">🏆 排行榜</button>
      <button @click="showProfile = true">👤 我的</button>
    </div>

    <!-- 小地图 -->
    <MiniMap v-if="showMap" :landmarks="landmarks" @close="showMap = false" />

    <!-- 进度提示 -->
    <div class="progress-hint">
      已探索 {{ completedCount }}/{{ totalLandmarks }} 个地标
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'
import LandmarkCard from './LandmarkCard.vue'
import MiniMap from './MiniMap.vue'

const canvasContainer = ref(null)
const selectedLandmark = ref(null)
const showMap = ref(false)
const showLandmarkList = ref(false)
const showLeaderboard = ref(false)
const showProfile = ref(false)

// 用户数据
const userLevel = ref(1)
const totalPoints = ref(0)
const completedCount = ref(0)
const totalLandmarks = ref(10)

// Three.js 变量
let scene, camera, renderer, controls
let landmarks = []
let landmarkMeshes = []

// 地标数据（从API获取）
const landmarkData = ref([])

onMounted(async () => {
  await loadLandmarks()
  initThreeScene()
  animate()
  loadUserProgress()
})

onUnmounted(() => {
  // 清理Three.js资源
  if (renderer) renderer.dispose()
})

// 加载地标数据
async function loadLandmarks() {
  try {
    const response = await fetch('/api/landmarks')
    landmarkData.value = await response.json()
    landmarks = landmarkData.value
  } catch (error) {
    console.error('加载地标失败:', error)
  }
}

// 初始化Three.js场景
function initThreeScene() {
  // 1. 创建场景
  scene = new THREE.Scene()
  scene.background = new THREE.Color(0x87CEEB) // 天空蓝
  scene.fog = new THREE.Fog(0x87CEEB, 50, 200)

  // 2. 创建相机
  const width = canvasContainer.value.clientWidth
  const height = canvasContainer.value.clientHeight
  camera = new THREE.PerspectiveCamera(60, width / height, 0.1, 1000)
  camera.position.set(50, 40, 50)

  // 3. 创建渲染器
  renderer = new THREE.WebGLRenderer({ antialias: true })
  renderer.setSize(width, height)
  renderer.shadowMap.enabled = true
  canvasContainer.value.appendChild(renderer.domElement)

  // 4. 添加控制器
  controls = new OrbitControls(camera, renderer.domElement)
  controls.enableDamping = true
  controls.dampingFactor = 0.05
  controls.maxPolarAngle = Math.PI / 2.1 // 限制不能钻到地下
  controls.minDistance = 20
  controls.maxDistance = 150

  // 5. 添加光照
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.6)
  scene.add(ambientLight)

  const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8)
  directionalLight.position.set(50, 100, 50)
  directionalLight.castShadow = true
  scene.add(directionalLight)

  // 6. 创建地面
  createGround()

  // 7. 创建地标建筑
  createLandmarks()

  // 8. 添加点击事件
  renderer.domElement.addEventListener('click', onCanvasClick)

  // 9. 响应窗口大小变化
  window.addEventListener('resize', onWindowResize)
}

// 创建地面
function createGround() {
  // 主地面
  const groundGeometry = new THREE.PlaneGeometry(300, 300)
  const groundMaterial = new THREE.MeshStandardMaterial({
    color: 0x7CBA3D, // 草绿色
    roughness: 0.8
  })
  const ground = new THREE.Mesh(groundGeometry, groundMaterial)
  ground.rotation.x = -Math.PI / 2
  ground.receiveShadow = true
  scene.add(ground)

  // 道路
  const roadGeometry = new THREE.PlaneGeometry(10, 200)
  const roadMaterial = new THREE.MeshStandardMaterial({
    color: 0x555555,
    roughness: 0.9
  })

  // 主干道
  const mainRoad = new THREE.Mesh(roadGeometry, roadMaterial)
  mainRoad.rotation.x = -Math.PI / 2
  mainRoad.position.y = 0.01
  scene.add(mainRoad)

  // 次干道
  const sideRoad = new THREE.Mesh(
    new THREE.PlaneGeometry(200, 8),
    roadMaterial
  )
  sideRoad.rotation.x = -Math.PI / 2
  sideRoad.position.y = 0.01
  scene.add(sideRoad)
}

// 创建地标建筑
function createLandmarks() {
  landmarkData.value.forEach((landmark, index) => {
    const group = new THREE.Group()

    // 根据类型创建不同形状的建筑
    let geometry
    const height = 10 + Math.random() * 15
    const width = 8 + Math.random() * 5

    switch (landmark.category) {
      case 'teaching':
        // 教学楼：长方体
        geometry = new THREE.BoxGeometry(width, height, width * 0.8)
        break
      case 'dormitory':
        // 宿舍：高层长方体
        geometry = new THREE.BoxGeometry(width * 1.2, height * 1.5, width)
        break
      case 'library':
        // 图书馆：扁平宽大
        geometry = new THREE.BoxGeometry(width * 1.5, height * 0.7, width * 1.2)
        break
      default:
        geometry = new THREE.BoxGeometry(width, height, width)
    }

    const material = new THREE.MeshStandardMaterial({
      color: new THREE.Color(landmark.appearance.color),
      roughness: 0.7,
      metalness: 0.1
    })

    const building = new THREE.Mesh(geometry, material)
    building.position.y = height / 2
    building.castShadow = true
    building.receiveShadow = true
    group.add(building)

    // 添加地标图标（发光的球体）
    const iconGeometry = new THREE.SphereGeometry(2, 16, 16)
    const iconMaterial = new THREE.MeshStandardMaterial({
      color: 0xffff00,
      emissive: 0xffff00,
      emissiveIntensity: 0.5
    })
    const icon = new THREE.Mesh(iconGeometry, iconMaterial)
    icon.position.y = height + 3
    icon.userData = { landmarkId: landmark._id, landmark: landmark }
    group.add(icon)

    // 添加标签（精灵）
    const canvas = document.createElement('canvas')
    const context = canvas.getContext('2d')
    canvas.width = 256
    canvas.height = 64

    context.fillStyle = 'rgba(0, 0, 0, 0.7)'
    context.fillRect(0, 0, 256, 64)
    context.fillStyle = 'white'
    context.font = 'bold 24px Arial'
    context.textAlign = 'center'
    context.fillText(landmark.name, 128, 40)

    const texture = new THREE.CanvasTexture(canvas)
    const spriteMaterial = new THREE.SpriteMaterial({ map: texture })
    const sprite = new THREE.Sprite(spriteMaterial)
    sprite.position.y = height + 6
    sprite.scale.set(20, 5, 1)
    group.add(sprite)

    // 设置位置
    group.position.set(
      landmark.position.x,
      0,
      landmark.position.z
    )

    scene.add(group)
    landmarkMeshes.push(group)
  })
}

// 点击事件处理
function onCanvasClick(event) {
  const rect = renderer.domElement.getBoundingClientRect()
  const mouse = new THREE.Vector2(
    ((event.clientX - rect.left) / rect.width) * 2 - 1,
    -((event.clientY - rect.top) / rect.height) * 2 + 1
  )

  const raycaster = new THREE.Raycaster()
  raycaster.setFromCamera(mouse, camera)

  // 检测是否点击了地标
  const intersects = raycaster.intersectObjects(scene.children, true)

  for (let intersect of intersects) {
    // 查找带有地标数据的对象
    let obj = intersect.object
    while (obj && !obj.userData.landmark) {
      obj = obj.parent
    }

    if (obj && obj.userData.landmark) {
      selectedLandmark.value = obj.userData.landmark
      break
    }
  }
}

// 地标完成处理
function handleLandmarkComplete(result) {
  if (result.correct) {
    totalPoints.value += result.points
    completedCount.value++

    // 检查是否升级
    checkLevelUp()

    // 保存进度
    saveProgress(result)
  }

  selectedLandmark.value = null
}

// 检查升级
function checkLevelUp() {
  const levelThresholds = [0, 100, 300, 600, 1000, 1500]
  const currentLevel = userLevel.value

  for (let i = levelThresholds.length - 1; i >= 0; i--) {
    if (totalPoints.value >= levelThresholds[i]) {
      userLevel.value = i
      break
    }
  }

  if (userLevel.value > currentLevel) {
    // 显示升级提示
    showLevelUpNotification()
  }
}

// 动画循环
function animate() {
  requestAnimationFrame(animate)

  // 让地标图标上下浮动
  const time = Date.now() * 0.001
  landmarkMeshes.forEach((group, index) => {
    const icon = group.children.find(c => c.userData.landmarkId)
    if (icon) {
      icon.position.y += Math.sin(time + index) * 0.02
    }
  })

  controls.update()
  renderer.render(scene, camera)
}

// 窗口大小调整
function onWindowResize() {
  if (!canvasContainer.value) return

  const width = canvasContainer.value.clientWidth
  const height = canvasContainer.value.clientHeight

  camera.aspect = width / height
  camera.updateProjectionMatrix()
  renderer.setSize(width, height)
}

// 加载用户进度
async function loadUserProgress() {
  try {
    const response = await fetch('/api/user/progress')
    const progress = await response.json()
    totalPoints.value = progress.totalPoints || 0
    completedCount.value = progress.completedCount || 0
    userLevel.value = progress.level || 1
  } catch (error) {
    console.error('加载进度失败:', error)
  }
}

// 保存进度
async function saveProgress(result) {
  try {
    await fetch('/api/user/progress', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        landmarkId: result.landmarkId,
        correct: result.correct,
        points: result.points
      })
    })
  } catch (error) {
    console.error('保存进度失败:', error)
  }
}

function showLevelUpNotification() {
  // 显示升级通知
  alert(`🎉 恭喜升级到 Lv.${userLevel.value}！`)
}
</script>

<style scoped>
.campus-explorer {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  position: relative;
}

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  z-index: 100;
}

.user-info {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.level {
  background: #667eea;
  color: white;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-weight: bold;
}

.points {
  font-weight: bold;
  color: #f59e0b;
}

.canvas-container {
  flex: 1;
  position: relative;
}

.bottom-nav {
  display: flex;
  justify-content: space-around;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
}

.bottom-nav button {
  padding: 0.8rem 1.5rem;
  border: none;
  background: #667eea;
  color: white;
  border-radius: 10px;
  font-size: 1rem;
  cursor: pointer;
  transition: transform 0.2s;
}

.bottom-nav button:hover {
  transform: scale(1.05);
}

.progress-hint {
  position: absolute;
  top: 80px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
}
</style>
```

### 2. 地标信息卡片组件

```vue
<!-- LandmarkCard.vue -->
<template>
  <div class="landmark-card-overlay" @click="close">
    <div class="landmark-card" @click.stop>
      <!-- 关闭按钮 -->
      <button class="close-btn" @click="close">✕</button>

      <!-- 标题 -->
      <h2>{{ landmark.name }}</h2>
      <p class="subtitle">{{ landmark.nameEn }}</p>

      <!-- 图片 -->
      <div class="image-gallery">
        <img
          v-for="(img, index) in landmark.media.images"
          :key="index"
          :src="img"
          :alt="landmark.name"
        />
      </div>

      <!-- 基础信息 -->
      <div class="info-section">
        <div class="info-item">
          <span class="icon">📍</span>
          <span>{{ getCategoryName(landmark.game.category) }}</span>
        </div>
        <div class="info-item">
          <span class="icon">📅</span>
          <span>建于 {{ landmark.info.buildYear }} 年</span>
        </div>
        <div class="info-item">
          <span class="icon">🏗️</span>
          <span>{{ landmark.info.area }}</span>
        </div>
      </div>

      <!-- 描述 -->
      <div class="description">
        <h3>关于这里</h3>
        <p>{{ landmark.info.description }}</p>
      </div>

      <!-- 知识问答 -->
      <div class="quiz-section" v-if="!quizCompleted">
        <h3>🎯 知识挑战</h3>
        <p class="question">{{ landmark.quiz.question }}</p>

        <div class="options">
          <button
            v-for="(option, index) in landmark.quiz.options"
            :key="index"
            :class="[
              'option-btn',
              {
                selected: selectedAnswer === index,
                correct: showResult && index === landmark.quiz.correctAnswer,
                wrong: showResult && selectedAnswer === index && index !== landmark.quiz.correctAnswer
              }
            ]"
            @click="selectAnswer(index)"
            :disabled="showResult"
          >
            {{ option }}
          </button>
        </div>

        <button
          v-if="!showResult"
          class="submit-btn"
          @click="submitAnswer"
          :disabled="selectedAnswer === null"
        >
          提交答案
        </button>

        <div v-if="showResult" class="result">
          <p v-if="isCorrect" class="correct-msg">✅ 回答正确！</p>
          <p v-else class="wrong-msg">❌ 回答错误</p>

          <p class="explanation">{{ landmark.quiz.explanation }}</p>

          <p class="points-earned">+{{ landmark.game.points }} 积分</p>

          <button class="continue-btn" @click="completeQuiz">继续探索</button>
        </div>
      </div>

      <!-- 已完成状态 -->
      <div v-else class="completed-section">
        <p class="completed-msg">✅ 你已完成此地标探索</p>
        <button class="close-btn-bottom" @click="close">关闭</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  landmark: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close', 'complete'])

const selectedAnswer = ref(null)
const showResult = ref(false)
const quizCompleted = ref(false)

const isCorrect = computed(() => {
  return selectedAnswer.value === props.landmark.quiz.correctAnswer
})

function close() {
  emit('close')
}

function selectAnswer(index) {
  if (!showResult.value) {
    selectedAnswer.value = index
  }
}

function submitAnswer() {
  showResult.value = true
}

function completeQuiz() {
  quizCompleted.value = true
  emit('complete', {
    landmarkId: props.landmark._id,
    correct: isCorrect.value,
    points: isCorrect.value ? props.landmark.game.points : 0
  })
}

function getCategoryName(category) {
  const map = {
    teaching: '教学楼',
    dormitory: '宿舍楼',
    library: '图书馆',
    research: '科研楼',
    life: '生活服务'
  }
  return map[category] || '其他'
}
</script>

<style scoped>
.landmark-card-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 1rem;
}

.landmark-card {
  background: white;
  border-radius: 20px;
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  padding: 2rem;
}

.close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #999;
}

.close-btn:hover {
  color: #333;
}

h2 {
  margin: 0 0 0.5rem 0;
  color: #333;
}

.subtitle {
  color: #666;
  margin: 0 0 1.5rem 0;
  font-size: 0.9rem;
}

.image-gallery {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 10px;
  margin-bottom: 1.5rem;
}

.image-gallery img {
  width: 100%;
  height: 120px;
  object-fit: cover;
  border-radius: 10px;
}

.info-section {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.info-item {
  background: #f5f5f5;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.85rem;
}

.info-item .icon {
  margin-right: 0.3rem;
}

.description {
  margin-bottom: 2rem;
}

.description h3 {
  font-size: 1rem;
  margin-bottom: 0.5rem;
  color: #667eea;
}

.description p {
  line-height: 1.6;
  color: #666;
}

.quiz-section {
  background: #f9f9f9;
  padding: 1.5rem;
  border-radius: 15px;
}

.quiz-section h3 {
  margin-top: 0;
  color: #667eea;
}

.question {
  font-weight: 600;
  margin: 1rem 0;
  color: #333;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
  margin-bottom: 1rem;
}

.option-btn {
  padding: 1rem;
  border: 2px solid #e0e0e0;
  background: white;
  border-radius: 10px;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s;
}

.option-btn:hover:not(:disabled) {
  border-color: #667eea;
  background: #f0f3ff;
}

.option-btn.selected {
  border-color: #667eea;
  background: #e8ecff;
}

.option-btn.correct {
  border-color: #10b981;
  background: #d1fae5;
}

.option-btn.wrong {
  border-color: #ef4444;
  background: #fee2e2;
}

.submit-btn {
  width: 100%;
  padding: 1rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: bold;
  cursor: pointer;
}

.submit-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.result {
  text-align: center;
}

.correct-msg {
  color: #10b981;
  font-size: 1.2rem;
  font-weight: bold;
  margin: 1rem 0;
}

.wrong-msg {
  color: #ef4444;
  font-size: 1.2rem;
  font-weight: bold;
  margin: 1rem 0;
}

.explanation {
  color: #666;
  line-height: 1.6;
  margin: 1rem 0;
}

.points-earned {
  color: #f59e0b;
  font-weight: bold;
  font-size: 1.2rem;
  margin: 1rem 0;
}

.continue-btn {
  width: 100%;
  padding: 1rem;
  background: #10b981;
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: bold;
  cursor: pointer;
  margin-top: 1rem;
}

.completed-section {
  text-align: center;
  padding: 2rem 0;
}

.completed-msg {
  color: #10b981;
  font-size: 1.2rem;
  font-weight: bold;
}

.close-btn-bottom {
  margin-top: 1rem;
  padding: 1rem 2rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
}
</style>
```

---

## 🔧 后端API实现

### Express.js API 路由

```javascript
// routes/landmarks.js
const express = require('express')
const router = express.Router()
const Landmark = require('../models/Landmark')
const UserProgress = require('../models/UserProgress')
const auth = require('../middleware/auth')

// 获取所有地标
router.get('/', async (req, res) => {
  try {
    const landmarks = await Landmark.find({ isActive: true })
      .select('name nameEn position appearance info media quiz game')
      .sort({ 'game.order': 1 })

    res.json(landmarks)
  } catch (error) {
    res.status(500).json({ error: error.message })
  }
})

// 获取单个地标详情
router.get('/:id', async (req, res) => {
  try {
    const landmark = await Landmark.findById(req.params.id)
    if (!landmark) {
      return res.status(404).json({ error: '地标不存在' })
    }
    res.json(landmark)
  } catch (error) {
    res.status(500).json({ error: error.message })
  }
})

// 提交地标打卡答案
router.post('/:id/quiz', auth, async (req, res) => {
  try {
    const { answer } = req.body
    const userId = req.user._id

    const landmark = await Landmark.findById(req.params.id)
    if (!landmark) {
      return res.status(404).json({ error: '地标不存在' })
    }

    // 检查是否已完成
    const progress = await UserProgress.findOne({ userId })
    const completed = progress?.landmarks.find(
      l => l.landmarkId.toString() === req.params.id
    )

    if (completed) {
      return res.status(400).json({ error: '已完成此地标' })
    }

    // 验证答案
    const isCorrect = answer === landmark.quiz.correctAnswer
    const pointsEarned = isCorrect ? landmark.game.points : 0

    // 更新进度
    await UserProgress.findOneAndUpdate(
      { userId },
      {
        $push: {
          landmarks: {
            landmarkId: landmark._id,
            status: isCorrect ? 'completed' : 'skipped',
            completedAt: new Date(),
            quizCorrect: isCorrect,
            pointsEarned
          }
        },
        $inc: {
          totalPoints: pointsEarned
        }
      },
      { upsert: true, new: true }
    )

    res.json({
      correct: isCorrect,
      pointsEarned,
      explanation: landmark.quiz.explanation
    })
  } catch (error) {
    res.status(500).json({ error: error.message })
  }
})

module.exports = router
```

### 用户进度API

```javascript
// routes/progress.js
const express = require('express')
const router = express.Router()
const UserProgress = require('../models/UserProgress')
const auth = require('../middleware/auth')

// 获取用户进度
router.get('/', auth, async (req, res) => {
  try {
    const progress = await UserProgress.findOne({ userId: req.user._id })
      .populate('landmarks.landmarkId', 'name game.points')

    if (!progress) {
      return res.json({
        landmarks: [],
        totalPoints: 0,
        currentLevel: 1,
        completedCount: 0
      })
    }

    const completedCount = progress.landmarks.filter(
      l => l.status === 'completed'
    ).length

    const currentLevel = calculateLevel(progress.totalPoints)

    res.json({
      ...progress.toObject(),
      completedCount,
      currentLevel
    })
  } catch (error) {
    res.status(500).json({ error: error.message })
  }
})

// 计算等级
function calculateLevel(points) {
  const thresholds = [0, 100, 300, 600, 1000, 1500]
  for (let i = thresholds.length - 1; i >= 0; i--) {
    if (points >= thresholds[i]) return i
  }
  return 1
}

module.exports = router
```

---

## 📊 需要准备的内容清单

### 第一周准备（数据层）

#### 地标信息表（10-15个）

| 地标名称 | 类别 | 位置坐标 | 简介要点 | 问答题 |
|---------|------|----------|----------|--------|
| 信息大楼 | 教学楼 | (0, 0, 0) | 主教学楼、2002年建成、12000㎡ | 主要用途？ |
| 图书馆 | 图书馆 | (50, 0, 30) | 24小时开放、藏书XX万册 | 开放时间？ |
| C栋宿舍 | 宿舍楼 | (-40, 0, 20) | 研究生宿舍、X层楼 | 住几人？ |
| ... | ... | ... | ... | ... |

#### 拍摄清单
```
每个地标需要：
□ 正面照片（1张，用于卡片展示）
□ 多角度照片（2-3张，用于画廊）
□ 全景照（可选，用于全景模式）
□ 细节特写（可选，增加趣味性）

拍摄建议：
- 选择天气晴朗的日子
- 避开人流高峰
- 构图要包含建筑特色
- 光线均匀，避免强逆光
```

#### 文案准备
```
每个地标准备：
□ 中文名称（2-4字）
□ 英文名称
□ 一句话介绍（15字内）
□ 详细介绍（100字左右）
□ 建造年份
□ 建筑面积
□ 特色功能

问答题准备：
□ 问题（1题，与地标相关）
□ 4个选项（1个正确，3个干扰）
□ 答案解析（30字左右）
```

---

## 🎯 简化版快速实现方案

### 如果时间紧张，可以这样简化：

#### 方案1：去掉3D，用2D地图
```vue
<!-- 使用2D平面地图 -->
<template>
  <div class="map-container">
    <div class="campus-map">
      <!-- 使用图片或SVG绘制校园地图 -->
      <img src="/campus-map.png" usemap="#landmark-map" />

      <!-- 地标标记点 -->
      <div
        v-for="landmark in landmarks"
        :key="landmark.id"
        class="landmark-marker"
        :style="{
          left: landmark.mapX + '%',
          top: landmark.mapY + '%'
        }"
        @click="showLandmark(landmark)"
      >
        📍
      </div>
    </div>

    <LandmarkCard
      v-if="selectedLandmark"
      :landmark="selectedLandmark"
      @close="selectedLandmark = null"
    />
  </div>
</template>
```

#### 方案2：使用现成3D模型库
```javascript
// 使用Sketchfab免费模型
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader'

const loader = new GLTFLoader()
loader.load(
  'https://sketchfab.com/...', // 免费模型链接
  (gltf) => {
    scene.add(gltf.scene)
  }
)
```

#### 方案3：全景图漫游（最快）
```vue
<!-- 使用现成全景图组件 -->
<template>
  <vue-panorama
    src="/campus-panorama.jpg"
    :hotspots="hotspots"
    @hotspot-click="showLandmark"
  />
</template>
```

---

## 🎁 额外交互功能（可加分）

### 1. 收集系统
```javascript
// 收集系统
const collectibles = [
  { name: '清华印章', icon: '🔖', rare: 'common' },
  { name: '校园明信片', icon: '🎴', rare: 'uncommon' },
  { name: '隐藏彩蛋', icon: '🥚', rare: 'rare' }
]
```

### 2. 成就系统
```javascript
const achievements = [
  { name: '初出茅庐', condition: '完成第1个地标', icon: '🌱' },
  { name: '校园向导', condition: '完成5个地标', icon: '🗺️' },
  { name: '知识达人', condition: '连续答对10题', icon: '🧠' },
  { name: '全图鉴', condition: '完成所有地标', icon: '👑' }
]
```

### 3. 彩蛋隐藏
```javascript
// 在特定位置隐藏彩蛋
const easterEggs = [
  { position: { x: 25, y: 0, z: -15 }, reward: '隐藏徽章' },
  { position: { x: -30, y: 0, z: 40 }, reward: '神秘道具' }
]
```

---

这个模块的核心价值：
✅ 通过游戏化的方式让学生主动了解校园
✅ 知识问答加深印象
✅ 积分奖励维持动力
✅ 为后续AI改造模块做铺垫

需要我详细说明哪个部分，或者直接开始写某个功能的代码？
