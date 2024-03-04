import * as THREE from 'three';

// 创建场景、相机和渲染器
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// 创建机器人模型
const robotGeometry = new THREE.BoxGeometry(1, 1, 1);
const robotMaterial = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
const robot = new THREE.Mesh(robotGeometry, robotMaterial);
scene.add(robot);

// 动画混合器
const mixer = new THREE.AnimationMixer(robot);
const clip = new THREE.AnimationClip('move', -1, [
    new THREE.VectorKeyframeTrack('.position', [0, 1, 2], [0, 0, 0, 5, 0, 0, 15, 5, 0]),
]);

const action = mixer.clipAction(clip);
action.play();

// 相机位置
camera.position.set(0, 10, 20);
camera.lookAt(scene.position);

// 时钟
const clock = new THREE.Clock();

// 渲染循环
function animate() {
    requestAnimationFrame(animate);

    // 更新动画混合器
    const delta = clock.getDelta();
    mixer.update(delta);

    renderer.render(scene, camera);
}
animate();
