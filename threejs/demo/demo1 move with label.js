import * as THREE from 'three';

// 创建场景、相机和渲染器
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// 创建光球
const sphereGeometry = new THREE.SphereGeometry(0.5, 32, 32);
const sphereMaterial = new THREE.MeshBasicMaterial({ color: 0xff0000 });
const sphere = new THREE.Mesh(sphereGeometry, sphereMaterial);
scene.add(sphere);

// 创建文本纹理
function createTextTexture(text) {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    canvas.width = 256;
    canvas.height = 128;
    context.fillStyle = '#000';
    context.fillRect(0, 0, canvas.width, canvas.height);
    context.font = '24px Arial';
    context.fillStyle = '#fff';
    context.fillText(text, 10, 40);
    return new THREE.CanvasTexture(canvas);
}

// 创建Sprite材质和Sprite
const spriteMaterial = new THREE.SpriteMaterial({ map: createTextTexture('uav1') });
const label = new THREE.Sprite(spriteMaterial);
label.scale.set(2, 1, 1); // 根据需要调整尺寸
scene.add(label);

// 将标签定位到光球旁边
label.position.set(0.5, 0.5, 0);

// 相机位置
camera.position.z = 5;

// 渲染循环
function animate() {
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
}
animate();
