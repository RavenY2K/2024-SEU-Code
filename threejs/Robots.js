import * as THREE from "three";
import { createRoute } from "./CreateRoutes";
let x = 1;

const sphereGeometry_hus = new THREE.SphereGeometry(0.15);
const sphereMaterial_hus = new THREE.MeshBasicMaterial({ color: 0xeeeeee });

const robotNames = ["hus1", "hus2", "hus3", "hus4", "auv1", "auv2"];

const axesName = ["-5,-3.75", "-5,-1.25", "-1.25,5","-3.75,5","1.25,-5","3.75,-5", "5,5", "5,3.75", "5,1.25"];

export const Robots = robotNames.map((robotName) => {
  const robotInitPos = robotName.includes("hus") ? [x++, 0.3, 7] : [7, 0.3, x++];

  const robot = {
    robotName,
    robotInitPos,
    robotObj: null,
    robotMixer: null,
  };
  robot.robotObj = createHus(robot);
  robot.robotMixer = createRoute(robot);
  return robot;
});

export const axes = axesName.map((axesName) => {
  return {
    axesName,
    axeObj: createAxes(axesName),
  };
});

function createAxes(axesName) {
  let [x, y] = axesName.split(",").map((num) => parseFloat(num));
  const sphere_hus = new THREE.Mesh(sphereGeometry_hus, sphereMaterial_hus);
  const axe = new THREE.Group();
  const nameLabel = createLabel(axesName);
  axe.add(sphere_hus, nameLabel);
  axe.position.set(x, 8.3, y);
  return axe;
}

function createHus(robot) {
  const sphere_hus = new THREE.Mesh(sphereGeometry_hus, sphereMaterial_hus);
  const hus = new THREE.Group();
  const nameLabel = createLabel(robot.robotName);
  hus.add(sphere_hus, nameLabel);
  if (robot.robotInitPos) {
    hus.position.set(...robot.robotInitPos);
  }
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
  canvas.height = 50;
  context.font = "40px Arial";
  context.fillStyle = "#999";
  context.fillText(text, 0, 50);
  return new THREE.CanvasTexture(canvas);
}
