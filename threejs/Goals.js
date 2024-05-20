import * as THREE from "three";
export const pos = [
  [4.06, 2.61, 0.15],
  [4.06, 3.1, 2.15],
  [2.59, -4.01, 0.15],
  [3.08, -4.01, 2.15],
  [4.05, 1.27, 0.15],
  [2.28, 3.1, 2.15],
  [1.87, 3.35, 2.15],
  [1.47, 3.35, 2.15],
  [3.43, 1.27, 0.15],
  [2.57, 1.27, 0.15],
  [1.2, 1.27, 0.15],
  [-1.27, 4.06, 0.15],
  [-2.61, 4.06, 0.15],
  [-3.09, 4.07, 2.15],
  [-3.1, 2.29, 2.15],
  [-3.34, 1.88, 2.15],
  [-3.34, 1.48, 2.15],
  [-1.27, 3.44, 0.15],
  [-3.99, -1.23, 0.15],
  [-4.02, -2.57, 0.15],
  [-4.02, -3.06, 2.15],
  [-3.36, -1.24, 0.15],
  [1.25, -3.99, 0.15],
  [3.09, -2.23, 2.15],
  [3.34, -1.83, 2.15],
  [3.34, -1.42, 2.15],
  [1.25, -3.37, 0.15],
  [2.92, 1.27, 4.15],
  [-2.61, 1.2, 4.15],
  [-2.85, -1.24, 4.15],
  [-1.13, -1.26, 4.15],
  [2.61, -1.15, 4.15],
  [2.1, -3.38, 0.15],
  [4.55, 4.55, 2.15],
  [-4.55, 4.55, 2.15],
  [-4.55, -4.55, 2.15],
  [4.55, -4.55, 2.15],
  [-4.55, -4.55, 2.15],
  [4.55, -4.55, 2.15],
  [1.47, 4.55, 6.15],
  [-4.55, 1.48, 6.15],
  [4.55, -4.55, 6.15],
  [4.55, -1.42, 6.15],
  [1.47, 1.56, 6.15],
  [-1.56, 1.46, 6.15],
  [-1.4, -1.56, 6.15],
  [1.56, -1.41, 6.15],
  [-4.55, 1.48, 8.15],
  [-1.43, -4.55, 8.15],
  [4.55, -1.42, 8.15],
  [1.47, 1.56, 8.15],
  [-1.56, 1.46, 8.15],
  [-1.4, -1.56, 8.15],
  [-1.43, -4.55, 6.15],
];
const sphereGeometry_goal = new THREE.SphereGeometry(0.05);
const sphereMaterial_goal_red = new THREE.MeshBasicMaterial({
  color: 0xff0000,
});
const sphereMaterial_goal_green = new THREE.MeshBasicMaterial({
  color: 0x00ff00,
});
const sphereMaterial_goal_yellow = new THREE.MeshBasicMaterial({
  color: 0xe5c06d,
});

export const Goals = pos.map(([x, y, z], index) => {
  const goal = {
    goalName: "G" + index,
    goalObj: createGoal("G" + index, x, y, z),
  };
  goal.turnToGreen = function () {
    goal.goalObj.children[0].material = sphereMaterial_goal_green;
  };
  goal.turnToRed = function () {
    goal.goalObj.children[0].material = sphereMaterial_goal_red;
  };
  return goal;
});

function createGoal(goalName, x, y, z) {
  const sphere_goal1 = new THREE.Mesh(
    sphereGeometry_goal,
    sphereMaterial_goal_yellow,
  );

  const goal = new THREE.Group();
  const nameLabel = createLabel(goalName);
  goal.add(sphere_goal1, nameLabel);
  goal.position.set(x, z, y);
  return goal;
}

function createLabel(goalName) {
  const nameLabel = new THREE.Sprite(
    new THREE.SpriteMaterial({
      map: createTextTexture(goalName),
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
