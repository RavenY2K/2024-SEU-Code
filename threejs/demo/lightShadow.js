import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(
  40,
  window.innerWidth / window.innerHeight,
  0.1,
  100
);
camera.position.set(15,15,15)

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

renderer.shadowMap.enabled = false;
renderer.shadowMap.type = THREE.PCFSoftShadowMap; // default THREE.PCFShadowMap

//Create a DirectionalLight and turn on shadows for the light
const light = new THREE.DirectionalLight( 0xffffff, 1 );
light.position.set( 0, 1, 0 ); //default; light shining from top
light.castShadow = true; // default false
scene.add( light );

//Set up shadow properties for the light
light.shadow.mapSize.width = 512; // default
light.shadow.mapSize.height = 512; // default
light.shadow.camera.near = 0.5; // default
light.shadow.camera.far = 500; // default

//Create a sphere that cast shadows (but does not receive them)
const sphereGeometry = new THREE.SphereGeometry( 5, 32, 32 );
const sphereMaterial = new THREE.MeshStandardMaterial( { color: 0xff0000 } );
const sphere = new THREE.Mesh( sphereGeometry, sphereMaterial );
sphere.castShadow = true; //default is false
sphere.receiveShadow = false; //default
scene.add( sphere );

//Create a plane that receives shadows (but does not cast them)
const planeGeometry = new THREE.PlaneGeometry( 20, 20, 32, 32 );
const planeMaterial = new THREE.MeshStandardMaterial( { color: 0x00ff00 } )
const plane = new THREE.Mesh( planeGeometry, planeMaterial );
plane.receiveShadow = true;
scene.add( plane );

//Create a helper for the shadow camera (optional)
const helper = new THREE.CameraHelper( light.shadow.camera );
scene.add( helper );

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
