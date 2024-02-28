import * as THREE from "three";
let x = 1;

const sphereGeometry_hus = new THREE.SphereGeometry(0.15);
const sphereMaterial_hus = new THREE.MeshBasicMaterial({ color: 0xeeeeee });

const robotNames = ["hus1", "hus2", "hus3", "hus4", "auv1", "auv2"];

const axesName = ["1,0", "5,0", "1,5", "5,5",'5,3.75','5,1.25'];

export const Robots = robotNames.map((robotName) => {
  return {
    robotName,
    robotObj: createHus(robotName),
  };
});

export const axes = axesName.map((axesName) => {
    return {
      axesName,
      axeObj: createAxes(axesName),
    };
  });
  

function createAxes(axesName){
    let [x,y] = axesName.split(',').map(num => parseFloat(num));
    const axe=createHus(axesName)

    axe.position.set(x,2.3,y)
    return axe
}

function createHus(robotName) {
  const sphere_hus = new THREE.Mesh(sphereGeometry_hus, sphereMaterial_hus);
  const hus = new THREE.Group();
  const nameLabel = createLabel(robotName);
  hus.add(sphere_hus, nameLabel);
  hus.position.set(x, 0.3, 7);
  x+=0.5
  return hus;
}

function createLabel(robotName) {
  const nameLabel = new THREE.Sprite(
    new THREE.SpriteMaterial({
      map: createTextTexture(robotName),
    })
  );
  nameLabel.scale.set(0.5, 0.3);
  nameLabel.position.set(0, 0.4, 0);
  return nameLabel;
}

function createTextTexture(text) {
  const canvas = document.createElement("canvas");
  const context = canvas.getContext("2d");

  canvas.width = 100;
  canvas.height= 50;
  context.font = "33px Arial";
  context.fillStyle = "#999";
  context.fillText(text, 0, 50);
  return new THREE.CanvasTexture(canvas);
}
