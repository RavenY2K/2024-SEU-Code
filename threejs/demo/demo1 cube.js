import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(
  40,
  window.innerWidth / window.innerHeight,
  0.1,
  100
);
camera.position.set(5,5,5)

const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 0, 0);
controls.update();
controls.enablePan = false;
controls.enableDamping = true;


// 添加坐标轴辅助器 (AxesHelper)
const axesHelper = new THREE.AxesHelper(5);
scene.add(axesHelper);

// 添加网格辅助器 (GridHelper)
const gridHelper = new THREE.GridHelper(10, 10);
scene.add(gridHelper);

//---------------------------------------------------------------------------//
//---------------------------------------------------------------------------//

const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshStandardMaterial({ color: 0x999999 });

const cube = new THREE.Mesh(geometry, material);
scene.add(cube);



// light
const ambientLight = new THREE.AmbientLight(0xffffff, 1); // soft white light
scene.add(ambientLight);

const pointLight = new THREE.PointLight(0xffffff, 1);
pointLight.position.set(5, 5, 5);
scene.add(pointLight);


//---------------------------------------------------------------------------//
//---------------------------------------------------------------------------//

function animate() {
  requestAnimationFrame(animate);

//   cube.rotation.x += 0.01;
//   cube.rotation.y += 0.01;
  controls.update();
  renderer.render(scene, camera);
}
setInterval(() => {
  console.log(camera.position)
    
}, 1000);
animate();
