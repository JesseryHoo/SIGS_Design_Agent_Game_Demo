# "SIGS 寻宝记" - AR校园互动平台设计方案

## 🎯 核心概念重新定位

### 项目名称
**"SIGS Re:Make" - AR校园寻宝与共创平台**

### 核心理念
```
真实校园漫步 + AR虚拟收集 + AI创意改造 = 沉浸式校园参与体验
```

### 三大创新玩法

```
🌍 现实世界探索
   ↓
📱 AR增强现实交互
   ↓
🤖 AI辅助创意设计
   ↓
🎁 线下实体奖励
```

---

## 🎮 AR寻宝玩法详解

### 玩法1：AR位置寻宝（Pokemon Go模式）⭐

#### 核心机制
```
用户GPS定位到校园某位置
    ↓
打开AR摄像头扫描周围环境
    ↓
发现隐藏在真实环境中的虚拟物品
    ↓
点击/手势完成收集
    ↓
获得积分和数字藏品
```

#### 藏品设计

**校园文化系列**
```
📜 清华校史碎片
- 在校史馆附近AR扫描发现
- 收集5个拼成完整校史故事
- 解锁"文化传承者"徽章

🎨 建筑元素收集
- 信息大楼的"科技之砖"
- 图书馆的"智慧之书"
- 大礼堂的"艺术之音"
- 收集元素可合成数字模型

🔬 科研发现物
- 在实验室附近发现"创新火花"
- 收集10个解锁"科研启蒙者"称号
```

**校园生物系列**
```
🌸 校园植物图鉴
- 春季：发现AR樱花、紫荆花
- 夏季：发现AR凤凰木、鸡蛋花
- 秋季：发现AR银杏、枫叶
- 冬季：发现AR梅花

🐦 校园鸟类观察
- 通过AR"召唤"校园常见鸟类
- 学习鸟类知识
- 完成图鉴获得奖励

🦋 昆虫世界
- 发现隐藏的AR昆虫
- 了解校园生态系统
```

**清华IP系列**
```
🦁 清华吉祥物
- 收集不同装扮的清华狮
- 运动狮、学习狮、科研狮等
- 稀有度：普通/稀有/史诗/传说

🏫 校园建筑微缩模型
- AR扫描获得3D建筑模型
- 可在虚拟空间摆放
- 收集完整获得"校园建筑师"称号

🎓 学院符号
- 各学院的特色符号
- 信息、材料、环境、医药等
- 收集齐所有学院解锁特殊奖励
```

#### 技术实现

```javascript
// AR寻宝核心代码
// 使用WebXR + AR.js 或 8th Wall（有免费额度）

class ARScavengerHunt {
  constructor() {
    this.userLocation = null
    this.treasures = []
    this.collectedItems = []
  }

  // 初始化AR
  async initAR() {
    try {
      // 检查设备是否支持AR
      const isARSupported = await this.checkARSupport()

      if (isARSupported) {
        // 启动AR会话
        this.arSession = await this.startARSession()
        this.setupARScene()
      } else {
        // 降级到地图模式
        this.initMapMode()
      }
    } catch (error) {
      console.error('AR初始化失败:', error)
      this.initMapMode()
    }
  }

  // 检查AR支持
  async checkARSupport() {
    if ('xr' in navigator) {
      const isSupported = await navigator.xr.isSessionSupported('immersive-ar')
      return isSupported
    }
    return false
  }

  // 启动AR会话
  async startARSession() {
    const session = await navigator.xr.requestSession('immersive-ar', {
      optionalFeatures: ['dom-overlay', 'hit-test'],
      domOverlay: { root: document.body }
    })

    return session
  }

  // 获取用户位置
  async getUserLocation() {
    return new Promise((resolve, reject) => {
      if ('geolocation' in navigator) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            this.userLocation = {
              lat: position.coords.latitude,
              lng: position.coords.longitude,
              accuracy: position.coords.accuracy
            }
            resolve(this.userLocation)
          },
          (error) => {
            reject(error)
          },
          {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0
          }
        )
      } else {
        reject(new Error('地理位置不支持'))
      }
    })
  }

  // 加载附近的宝藏
  async loadNearbyTreasures() {
    try {
      const response = await fetch(`/api/treasures/nearby?lat=${this.userLocation.lat}&lng=${this.userLocation.lng}`)
      this.treasures = await response.json()

      // 在AR场景中渲染宝藏
      this.renderTreasuresInAR()
    } catch (error) {
      console.error('加载宝藏失败:', error)
    }
  }

  // 在AR中渲染宝藏
  renderTreasuresInAR() {
    this.treasures.forEach(treasure => {
      // 计算宝藏相对于用户的位置
      const position = this.calculateRelativePosition(treasure.location)

      // 创建AR对象
      const arObject = this.createARObject(treasure, position)

      // 添加到场景
      this.arScene.add(arObject)
    })
  }

  // 计算相对位置
  calculateRelativePosition(treasureLocation) {
    // 简化版：直接使用GPS距离计算
    const distance = this.getDistance(
      this.userLocation.lat,
      this.userLocation.lng,
      treasureLocation.lat,
      treasureLocation.lng
    )

    // 转换为3D空间坐标
    return {
      x: distance * Math.cos(this.getAngle(treasureLocation)),
      y: 0,
      z: distance * Math.sin(this.getAngle(treasureLocation))
    }
  }

  // 创建AR对象
  createARObject(treasure, position) {
    // 创建3D模型
    const geometry = new THREE.SphereGeometry(0.5, 32, 32)
    const material = new THREE.MeshStandardMaterial({
      color: treasure.color || 0xffff00,
      emissive: treasure.color || 0xffff00,
      emissiveIntensity: 0.5
    })

    const mesh = new THREE.Mesh(geometry, material)
    mesh.position.set(position.x, position.y + 1, position.z)
    mesh.userData = { treasure }

    // 添加光环效果
    const ringGeometry = new THREE.RingGeometry(0.6, 0.8, 32)
    const ringMaterial = new THREE.MeshBasicMaterial({
      color: treasure.color || 0xffff00,
      transparent: true,
      opacity: 0.5,
      side: THREE.DoubleSide
    })
    const ring = new THREE.Mesh(ringGeometry, ringMaterial)
    ring.rotation.x = Math.PI / 2
    ring.position.y = -0.2
    mesh.add(ring)

    // 添加浮动动画
    this.animateFloating(mesh)

    return mesh
  }

  // 浮动动画
  animateFloating(mesh) {
    const startY = mesh.position.y
    const animate = () => {
      const time = Date.now() * 0.001
      mesh.position.y = startY + Math.sin(time * 2) * 0.1
      requestAnimationFrame(animate)
    }
    animate()
  }

  // 收集宝藏
  async collectTreasure(treasureId) {
    try {
      const response = await fetch(`/api/treasures/${treasureId}/collect`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          location: this.userLocation,
          timestamp: Date.now()
        })
      })

      const result = await response.json()

      if (result.success) {
        this.collectedItems.push(result.item)
        this.showCollectionAnimation(result.item)
        this.updatePoints(result.points)
      }
    } catch (error) {
      console.error('收集失败:', error)
    }
  }

  // 显示收集动画
  showCollectionAnimation(item) {
    // 创建粒子效果
    this.createParticleExplosion()

    // 显示获得提示
    this.showToast(`✨ 获得 ${item.name}！`)

    // 震动反馈
    if ('vibrate' in navigator) {
      navigator.vibrate([100, 50, 100])
    }
  }

  // 粒子爆炸效果
  createParticleExplosion() {
    const particleCount = 50
    const particles = []

    for (let i = 0; i < particleCount; i++) {
      const geometry = new THREE.SphereGeometry(0.05, 8, 8)
      const material = new THREE.MeshBasicMaterial({
        color: Math.random() * 0xffffff
      })
      const particle = new THREE.Mesh(geometry, material)

      particle.velocity = new THREE.Vector3(
        (Math.random() - 0.5) * 5,
        Math.random() * 5,
        (Math.random() - 0.5) * 5
      )

      particles.push(particle)
      this.arScene.add(particle)
    }

    // 动画
    const animate = () => {
      let allDone = true

      particles.forEach(particle => {
        particle.position.add(particle.velocity)
        particle.velocity.y -= 0.1 // 重力
        particle.material.opacity -= 0.02

        if (particle.material.opacity > 0) {
          allDone = false
        }
      })

      if (!allDone) {
        requestAnimationFrame(animate)
      } else {
        particles.forEach(p => this.arScene.remove(p))
      }
    }

    animate()
  }

  // 获取距离
  getDistance(lat1, lon1, lat2, lon2) {
    const R = 6371e3 // 地球半径（米）
    const φ1 = lat1 * Math.PI / 180
    const φ2 = lat2 * Math.PI / 180
    const Δφ = (lat2 - lat1) * Math.PI / 180
    const Δλ = (lon2 - lon1) * Math.PI / 180

    const a = Math.sin(Δφ/2) * Math.sin(Δφ/2) +
              Math.cos(φ1) * Math.cos(φ2) *
              Math.sin(Δλ/2) * Math.sin(Δλ/2)
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a))

    return R * c
  }

  // 降级到地图模式
  initMapMode() {
    // 使用2D地图+AR预览
    console.log('AR不支持，使用地图模式')
  }
}
```

---

### 玩法2：AR建筑解锁与观察

#### 核心机制
```
走到建筑前
    ↓
扫描建筑（图像识别）
    ↓
解锁AR信息层
    ↓
看到建筑的"隐藏信息"
```

#### AR信息层内容

**历史时光层**
```
🕰️ 时间穿越效果
- 扫描建筑，看到不同历史时期的样貌
- 2002年建成时 vs 现在
- 虚拟"拆除"看到内部结构
```

**数据可视化层**
```
📊 建筑数据展示
- AR标签显示：层数、面积、能耗
- 实时数据：当前人数、温度、用电量
- 碳排放数据
```

**功能提示层**
```
💡 实用信息
- 开放时间
- 可用设施（自习室、会议室）
- 当前活动
- 用户评价
```

#### 代码实现

```javascript
// AR建筑识别
class ARBuildingScanner {
  constructor() {
    this.recognizedBuildings = []
  }

  // 扫描建筑
  async scanBuilding() {
    // 使用设备摄像头
    const video = await this.startCamera()

    // 使用图像识别（可选方案）
    // 方案1: Google ML Kit（免费）
    // 方案2: TensorFlow.js + 自训练模型
    // 方案3: 简化为GPS接近+用户确认

    const detected = await this.detectBuilding(video)

    if (detected) {
      this.showBuildingInfo(detected)
    }
  }

  // 检测建筑
  async detectBuilding(video) {
    // 简化方案：基于GPS+用户选择
    const location = await this.getUserLocation()

    // 查找附近建筑
    const nearbyBuildings = await this.getNearbyBuildings(location)

    if (nearbyBuildings.length === 1) {
      return nearbyBuildings[0]
    } else if (nearbyBuildings.length > 1) {
      // 显示选择界面
      return await this.promptUserSelection(nearbyBuildings)
    }

    return null
  }

  // 显示建筑信息AR层
  showBuildingInfo(building) {
    const infoLayer = this.createARLayer(building)

    // 添加到AR场景
    this.arScene.add(infoLayer)

    // 创建AR标签
    this.createARLabels(building)
  }

  // 创建AR信息层
  createARLayer(building) {
    const group = new THREE.Group()

    // 历史对比
    if (building.historyImages) {
      const historySlider = this.createHistorySlider(building.historyImages)
      group.add(historySlider)
    }

    // 数据标签
    const dataLabels = this.createDataLabels(building)
    group.add(dataLabels)

    return group
  }

  // 创建历史滑块
  createHistorySlider(historyImages) {
    // 左右滑动查看不同时期
    const slider = {
      current: 0,
      images: historyImages,
      next: () => {
        slider.current = (slider.current + 1) % slider.images.length
      },
      prev: () => {
        slider.current = (slider.current - 1 + slider.images.length) % slider.images.length
      }
    }

    return slider
  }
}
```

---

### 玩法3：AR虚拟搭建

#### 核心概念
```
用户在真实校园空间中
    ↓
使用AR"摆放"虚拟建筑/设施
    ↓
预览改造效果
    ↓
生成改造提案
```

#### 实现方案

**使用AR Foundation (Unity) 或 WebXR**

```javascript
// AR虚拟搭建
class ARBuilder {
  constructor() {
    this.placedObjects = []
  }

  // 初始化AR搭建模式
  async initBuildMode() {
    // 需要平面检测
    const session = await navigator.xr.requestSession('immersive-ar', {
      optionalFeatures: ['planes-detection', 'hit-test']
    })

    this.setupBuildUI()
  }

  // 放置对象
  async placeObject(modelId) {
    // 执行命中测试
    const hitTestResult = await this.performHitTest()

    if (hitTestResult) {
      // 加载3D模型
      const model = await this.loadModel(modelId)

      // 放置在命中点
      model.position.copy(hitTestResult.position)
      model.rotation.copy(hitTestResult.rotation)

      this.arScene.add(model)
      this.placedObjects.push(model)

      // 保存到提案
      this.saveToProposal(model)
    }
  }

  // 执行命中测试
  async performHitTest() {
    // 检测真实世界的平面/表面
    const hitTest = await this.arSession.requestHitTest({
      space: this.arSession.viewerSpace,
      offset: new XRRay({ origin: { x: 0, y: 0, z: 0 }, direction: { x: 0, y: 0, z: -1 } })
    })

    if (hitTest.length > 0) {
      return hitTest[0]
    }

    return null
  }

  // 加载模型
  async loadModel(modelId) {
    // 从API获取模型GLB
    const response = await fetch(`/api/models/${modelId}`)
    const glbData = await response.arrayBuffer()

    const loader = new GLTFLoader()
    const gltf = await new Promise((resolve, reject) => {
      loader.parse(glbData, '', resolve, reject)
    })

    return gltf.scene
  }

  // 保存到提案
  saveToProposal(model) {
    const proposalItem = {
      modelId: model.userData.id,
      position: model.position.toArray(),
      rotation: model.rotation.toArray(),
      scale: model.scale.toArray(),
      timestamp: Date.now()
    }

    this.currentProposal.items.push(proposalItem)
  }

  // 生成提案截图
  async captureProposalScreenshot() {
    // 渲染当前AR场景
    renderer.render(this.arScene, this.arCamera)

    // 获取截图
    const screenshot = this.arCanvas.toDataURL('image/png')

    return screenshot
  }

  // 提交提案
  async submitProposal() {
    const screenshot = await this.captureProposalScreenshot()

    const proposal = {
      userId: this.currentUser.id,
      location: this.userLocation,
      items: this.currentProposal.items,
      screenshot: screenshot,
      description: this.currentProposal.description,
      createdAt: Date.now()
    }

    const response = await fetch('/api/proposals', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(proposal)
    })

    return response.json()
  }
}
```

---

## 🎨 UE5 3D校园方案

### 为什么用UE5？

**优势**：
- ✅ 业界顶级画质（Nanite + Lumen）
- ✅ 蓝图可视化编程（快速开发）
- ✅ 像素流送（Pixel Streaming）- 网页运行
- ✅ VR/AR原生支持
- ✅ 大量免费资产

**学生版免费**：
- Epic Games对学生完全免费
- 可用于课程作业

### UE5开发方案

#### 方案1：像素流送到网页（推荐）⭐

```
UE5应用运行在服务器
    ↓
像素流送技术推送到浏览器
    ↓
用户在网页上交互
    ↓
实时传输画面和操作
```

**优点**：
- 用户无需安装
- 跨平台（任何设备都能看）
- 质量不受设备限制

**缺点**：
- 需要服务器运行
- 延迟取决于网络

**实施步骤**：

1. **在UE5中搭建场景**
```
- 使用Quixel Bridge免费资产
- 或用Photogrammetry扫描建筑
- Low Poly风格快速搭建
```

2. **配置像素流送**
```cpp
// 在UE5项目中
// Project Settings → Plugins → Pixel Streaming
// 启用像素流送

// 启动参数
yourgame.exe -RenderOffScreen -PixelStreamingIP=0.0.0.0 -PixelStreamingPort=8888
```

3. **网页前端接收**
```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/pixelstreamingfrontend@latest/dist/lib/pixelstreamingfrontend.min.js"></script>
</head>
<body>
  <div id="player"></div>

  <script>
    const { PixelStreaming } = window;

    const config = {
      initialSettings: {
        AutoConnect: true,
        ss: 'ws://your-server:8888'
      }
    };

    const player = new PixelStreaming(config);
    player.setSS('ws://your-server:8888');
  </script>
</body>
</html>
```

#### 方案2：导出WebGL（简化）

```
UE5场景 → glTF/GLB导出 → Three.js加载
```

**工具**：
- UE5 -> glTF Exporter插件
- 或使用Babylon.js（Microsoft的3D引擎）

**代码示例**：
```javascript
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader'

const loader = new GLTFLoader()
loader.load(
  '/models/campus.glb',
  (gltf) => {
    scene.add(gltf.scene)
  }
)
```

#### 方案3：UE4/Unity 移动端APP

```
开发原生应用
    ↓
发布到iOS/Android
    ↓
用户下载安装
```

**优点**：
- 性能最好
- 可访问设备全部功能

**缺点**：
- 开发周期长
- 用户需要下载

---

## 🎁 线下奖励系统

### 积分兑换机制

```
收集物品/完成任务 → 获得积分 → 线下兑换
```

### 奖励层级设计

#### 铜牌级（50-100分）
```
📌 清华书签
📌 SIGS明信片套装
📌 校园地图贴纸
📌 纪念徽章
```

#### 银牌级（150-300分）
```
📱 手机支架
🧲 清华校徽磁贴
📔 笔记本
🖊️ 签字笔套装
```

#### 金牌级（400-600分）
```
👕 T恤
🎒 帆布袋
☕ 马克杯
🧸 毛绒玩具
```

#### 钻石级（800+分）
```
🏆 限量版模型
🎨 艺术品
📚 精装画册
🎫 特殊权益（如优先参加活动）
```

### 兑换流程

```
1. 在App中查看积分
2. 选择想兑换的奖品
3. 生成兑换二维码
4. 到指定地点（如学生服务中心）
5. 工作人员扫码核销
6. 领取实物奖品
```

### 技术实现

```javascript
// 兑换系统
class RewardSystem {
  // 生成兑换码
  async generateRedemptionCode(userId, rewardId) {
    const code = await QRCode.toDataURL(
      JSON.stringify({
        userId,
        rewardId,
        timestamp: Date.now(),
        signature: this.signData(userId, rewardId)
      })
    )

    return code
  }

  // 核销兑换码
  async verifyRedemptionCode(codeData) {
    const data = JSON.parse(codeData)

    // 验证签名
    if (!this.verifySignature(data)) {
      return { valid: false, error: '签名无效' }
    }

    // 检查是否过期（24小时）
    if (Date.now() - data.timestamp > 24 * 60 * 60 * 1000) {
      return { valid: false, error: '已过期' }
    }

    // 检查积分是否足够
    const user = await User.findById(data.userId)
    const reward = await Reward.findById(data.rewardId)

    if (user.points < reward.pointsRequired) {
      return { valid: false, error: '积分不足' }
    }

    // 扣除积分
    user.points -= reward.pointsRequired
    await user.save()

    // 记录兑换
    await Redemption.create({
      userId: data.userId,
      rewardId: data.rewardId,
      timestamp: Date.now()
    })

    return { valid: true, reward }
  }
}
```

---

## 📅 实施计划（7周优化版）

### 第1周：框架+AR基础
```
□ 项目初始化
□ AR环境搭建（WebXR/AR.js）
□ GPS定位功能
□ 简单AR对象显示测试
```

### 第2周：寻宝系统核心
```
□ 宝藏数据结构设计
□ AR寻宝交互
□ 收集动画
□ 积分系统
```

### 第3周：AR建筑扫描
```
□ 图像识别集成
□ 建筑信息展示
□ AR标签系统
□ 历史对比功能
```

### 第4周：UE5校园场景
```
□ UE5场景搭建
□ 像素流送配置
□ 与前端集成
□ 性能优化
```

### 第5周：AI改造功能
```
□ AI接口集成
□ AR搭建功能
□ 提案系统
□ 截图保存
```

### 第6周：测试优化
```
□ 全面测试
□ Bug修复
□ 性能优化
□ 内容补充
```

### 第7周：展示准备
```
□ Demo演示准备
□ 线下奖品对接
□ PPT制作
□ 最终展示
```

---

## 🛠️ 技术栈总结

### AR技术
```
WebXR API - 浏览器原生AR
AR.js / A-Frame - 快速AR开发
8th Wall - 企业级AR（有免费额度）
Google ARCore - Android
Apple ARKit - iOS
```

### 3D引擎
```
Unreal Engine 5 - 高质量场景（像素流送）
Three.js - Web端3D
Unity - 原生应用
```

### 后端
```
Node.js/Python
MongoDB/PostgreSQL
Socket.io - 实时通信
```

### AI服务
```
OpenAI API - 文本生成
Stability AI - 图像生成
Google ML Kit - 图像识别
```

---

这个方案的核心亮点：

✅ **AR寻宝** - 像Pokemon Go一样有趣
✅ **真实校园** - 走出来探索，不只是看屏幕
✅ **AR搭建** - 直接在真实空间预览改造
✅ **UE5画质** - 媲美游戏的视觉效果
✅ **线下奖励** - 真实激励，参与动力强

需要我详细展开哪个部分？或者直接开始写AR寻宝的代码？
