import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
import { Goals } from "./Goals";
import { Robots, axes } from "./robots";
import { routes, goalAchieveArr } from "./CreateRoutes";

// 场景、相机和渲染器
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xaaaaaa);
const camera = new THREE.PerspectiveCamera(40, 800 / 600, 0.1, 1000);
camera.position.set(16, 12, 18);
const renderer = new THREE.WebGLRenderer({
  // antialias:true,
  //alpha:true
});
renderer.physicallyCorrectLights = true;
renderer.setPixelRatio(window.devicePixelRatio * 2);

// renderer.shadowMap.enabled = true; // 启用阴影
renderer.setSize(800, 600);
// window.addEventListener('resize',)
document.body.appendChild(renderer.domElement);
renderer.domElement.style.display = "block";
renderer.domElement.style.margin = "0 auto";

//controls
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 0, 0);
controls.update();
controls.enablePan = false;
controls.enableDamping = true;
// 添加坐标轴辅助器 (AxesHelper)
const axesHelper = new THREE.AxesHelper(10);
scene.add(axesHelper);
// 添加网格辅助器 (GridHelper)
const gridHelper = new THREE.GridHelper(22, 22);
scene.add(gridHelper);

// light
const directionalLight = new THREE.DirectionalLight(0xffffff, 2);
directionalLight.position.set(70, 80, 90);
directionalLight.castShadow = true;
scene.add(directionalLight);

const light = new THREE.AmbientLight(0x404040, 2); // soft white light
scene.add(light);

// // 可视化光源位置（可选）
// const sphereSize = 1;
// const pointLightHelper = new THREE.PointLightHelper(pointLight, sphereSize);
// scene.add(pointLightHelper);
// 创建平台层
const createPlatform = (xSize, zSize, x, y, z) => {
  const geometry = new THREE.BoxGeometry(xSize, 0.2, zSize);
  const material = new THREE.MeshLambertMaterial({ color: 0xbbbbbb });
  const cube = new THREE.Mesh(geometry, material);
  cube.position.set(x, y, z);
  cube.receiveShadow = true; // 允许立方体接收阴影
  cube.castShadow = true; // 允许立方体投射阴影
  scene.add(cube);
  return cube;
};

const createFloor = (x, y, z, size = 5) => {
  //plat
  const plat = new THREE.Group();
  const material = new THREE.MeshLambertMaterial({ color: 0xbbbbbb });
  const geometry1 = new THREE.BoxGeometry(size * 0.8, 0.2, size);
  const geometry2 = new THREE.BoxGeometry(size / 5, 0.2, size / 4);
  const geometry4 = new THREE.BoxGeometry(size / 5, 0.1, size * 0.68);

  const cube1 = new THREE.Mesh(geometry1, material);
  const cube2 = new THREE.Mesh(geometry2, material);
  const cube3 = new THREE.Mesh(geometry2, material);
  const cube4 = new THREE.Mesh(geometry4, material);
  cube2.position.set(size * 0.5, 0, size * 0.375);
  cube3.position.set(size * 0.5, 0, -size * 0.375);
  cube4.position.set(size * 0.5, -1, 0);
  // CreateBuilding(2.5, 3, 0);
  cube4.rotation.x = (Math.PI / 180) * 38; //
  plat.add(cube1, cube2, cube3, cube4);

  // plat.children.forEach((cube) => {
  //   cube.receiveShadow = true; // 允许立方体接收阴影
  //   cube.castShadow = true; // 允许立方体投射阴影
  // });

  plat.position.set(x, y, z);

  //   cube1.receiveShadow = true; // 允许立方体接收阴影
  //   cube1.castShadow = true; // 允许立方体投射阴影

  scene.add(plat);
  return plat;
};

// 创建地基
createPlatform(16.5, 16.5, 0, 0, 0);

// 创建4栋楼之一
const CreateBuilding = (x, y, rotate) => {
  const building = new THREE.Group();
  const platform2 = createFloor(x, 2, y);
  const platform3 = createFloor(x, 4, y);
  const platform4 = createFloor(x, 6, y);
  const platform5 = createFloor(x, 8, y);
  building.add(platform2);
  building.add(platform3, platform4, platform5);
  building.rotation.y = (Math.PI / 180) * rotate;
  scene.add(building);
};

CreateBuilding(3, 2.5, 0);
// CreateBuilding(0, 0, 0);
CreateBuilding(3, 2.5, 90);
CreateBuilding(3, 2.5, 180);
CreateBuilding(3, 2.5, 270);

// 创建光球
const sphereGeometry_hus = new THREE.SphereGeometry(0.15);
const sphereGeometry_goal = new THREE.SphereGeometry(0.05);
const sphereMaterial_hus = new THREE.MeshBasicMaterial({ color: 0xeeeeee });
const sphereMaterial_goal = new THREE.MeshBasicMaterial({ color: 0xff0000 });
const sphere_hus1 = new THREE.Mesh(sphereGeometry_hus, sphereMaterial_hus);
const sphere_hus2 = new THREE.Mesh(sphereGeometry_hus, sphereMaterial_hus);
const sphere_goal1 = new THREE.Mesh(sphereGeometry_goal, sphereMaterial_goal);

function createTextTexture(text) {
  const canvas = document.createElement("canvas");
  const context = canvas.getContext("2d");

  canvas.width = 100;
  canvas.height = 50;
  context.font = "40px Arial";
  context.fillStyle = "#999";
  context.fillText(text, 0, 50);
  return new THREE.CanvasTexture(canvas);
}

// 创建Sprite材质和Sprite
const spriteMaterial_hus1 = new THREE.SpriteMaterial({
  map: createTextTexture("hus1"),
});
const spriteMaterial_hus2 = new THREE.SpriteMaterial({
  map: createTextTexture("hus2"),
});
const spriteMaterial_goal1 = new THREE.SpriteMaterial({
  map: createTextTexture("G1"),
});
const label_hus1 = new THREE.Sprite(spriteMaterial_hus1);
const label_hus2 = new THREE.Sprite(spriteMaterial_hus2);
const label_G1 = new THREE.Sprite(spriteMaterial_goal1);

label_hus1.scale.set(0.5, 0.3); // 根据需要调整尺寸
label_hus2.scale.set(0.5, 0.3); // 根据需要调整尺寸
label_G1.scale.set(0.5, 0.3); // 根据需要调整尺寸
label_hus1.position.set(0, 0.4, 0);
label_hus2.position.set(0, 0.4, 0);
label_G1.position.set(0, 0.4, 0);

const hus1 = new THREE.Group();
hus1.add(sphere_hus1, label_hus1);
hus1.position.set(1, 0.3, 0);
// scene.add(hus1);

const hus2 = new THREE.Group();
hus2.add(sphere_hus2, label_hus2);
hus2.position.set(1, 0.3, 0);
// scene.add(hus2,hus1);

for (const robot of Robots) {
  scene.add(robot.robotObj);
}

for (const goal of Goals) {
  scene.add(goal.goalObj);
}

for (const axe of axes) {
  // scene.add(axe.axeObj)
}

let customClock = {
  elapsedTime: 0,
  lastTimestamp: performance.now(),
  update: function() {
    if (isRobotAnimating) {
      let currentTimestamp = performance.now();
      this.elapsedTime += (currentTimestamp - this.lastTimestamp) / 1000; // convert to seconds
    }
    this.lastTimestamp = performance.now();
  }
};

`G10, G1, G13, G2, G14,
G47, G51, G12, G44,
G20, G37, G29, G45,
G41, G42, G18, G3,
G0, G39, G30, G28,
G6, G20, G31, G23,`.split(',').forEach(index=>{
  //删去item空格
  index = Number(index.trim().slice(1));
    Goals[index].turnToRed();
})
const clock = new THREE.Clock();
let isRobotAnimating = true;
// 渲染循环
function animate() {
  customClock.update();
  const now = customClock.elapsedTime;

  Object.keys(goalAchieveArr).forEach((key) => {
    const arr = goalAchieveArr[key];
    if (arr.length === 0) return;
    if (now > arr[0]) {
      setGoalToGreen(key);
      arr.shift();
    }
  });
  requestAnimationFrame(animate);
  renderer.render(scene, camera);
  // 更新动画混合器
  const delta = clock.getDelta();
  if (isRobotAnimating) {
    Robots.forEach((robot) => {
      if (robot.robotMixer) {
        robot.robotMixer.update(delta);
      }
    });
  }

  controls.update();
}
function pauseRobots() {
  isRobotAnimating = false;
}

function resumeRobots() {
  isRobotAnimating = true;
}

window.pauseRobots= pauseRobots;
window.resumeRobots= resumeRobots;
function setGoalToGreen(key) {
  const goalName = routes[key].shift();
  const goalIndex = +goalName.slice(1);
  console.log("🚀 ~ setGoalToGreen ~ goalIndex:", key ,goalIndex);

  Goals[goalIndex].turnToGreen();
}
// setInterval(() => {
//   console.log(clock.elapsedTime);
// }, 500);
animate();
