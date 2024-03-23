import * as THREE from "three";
import { pos } from "./Goals";

const MOVE_SPEED = 2;
const UP_AND_DOWN_SPEED = 2;

export const routes = {
  hus1: ["G10", "G1", "G13", "G2", "G14"],
  hus2: ["G47", "G51", "G13", "G44"],
  hus3: ["G20", "G37", "G29", "G45"],
  hus4: ["G41", "G42", "G18", "G3"],
  auv1: ["G0", "G39", "G30", "G28"],
  auv2: ["G6", "G20", "G31", "G23"],
};
export const goalAchieveArr = {};

export function createRoute(robot) {
  if (!routes[robot.robotName]) return;

  const posArr = [robot.robotInitPos];
  if (robot.robotName.includes("auv")) {
    const [auvX, auvY, auvZ] = robot.robotInitPos;
    posArr.push([auvX, auvY + 0.7, auvZ]);
  }
  const timeSpanArr = [0];

  const posIndex = routes[robot.robotName].map(
    (labelName) => +labelName.slice(1)
  );

  posIndex.forEach((index) => {
    const [x, z, y] = pos[index];

    if (robot.robotName.includes("hus")) {
      ProcessHusRoutes(x, y, z, posArr);
    } else {
      ProcessAuvRoutes(x, y, z, posArr);
    }
  });

  const goalsTimeSpan = processTimeSpan(timeSpanArr, posArr);
  goalAchieveArr[robot.robotName] = goalsTimeSpan;
  console.log("🚀 ~ createRoute ~ goalsTimeSpan:", goalsTimeSpan);

  const mixer = new THREE.AnimationMixer(robot.robotObj);
  const clip = new THREE.AnimationClip("move", -1, [
    new THREE.VectorKeyframeTrack(
      ".position",
      timeSpanArr,
      [].concat(...posArr)
    ),
  ]);
  const action = mixer.clipAction(clip);
  action.play();
  return mixer;
}

function ProcessAuvRoutes(x, y, z, posArr) {
  let [preX, preY, preZ] = posArr[posArr.length - 1];

  if (Math.abs(preY - y) < 1) {
    posArr.push([x, preY, z], [x, y + 0.15, z], [x, y + 0.15, z], [x, preY, z]);
  } else {
    posArr.push(
      [0, preY, 0],
      [0, y + 0.7, 0],
      [x, y + 0.7, z],
      [x, y + 0.15, z],
      [x, y + 0.15, z],
      [x, y + 0.7, z]
    );
  }
}

function processTimeSpan(timeSpanArr, posArr) {
  let GoalsTimeSpan = [];
  let prePos = posArr[0];
  for (let i = 1; i < posArr.length; i++) {
    const curPos = posArr[i];
    prePos = posArr[i - 1];
    const dx = Math.abs(prePos[0] - curPos[0]);
    const dy = Math.abs(prePos[1] - curPos[1]);
    const dz = Math.abs(prePos[2] - curPos[2]);
    const distance = Math.sqrt(dx * dx + dy * dy + dz * dz);
    const time = Number(
      (
        distance / (dx > 0.1 && dz > 0.1 ? MOVE_SPEED : UP_AND_DOWN_SPEED)
      ).toFixed(1)
    );
    timeSpanArr.push(timeSpanArr[i - 1] + (time < 0.01 ? 5 : time));
    if (time < 0.01) {
      GoalsTimeSpan.push(timeSpanArr[timeSpanArr.length - 1]);
    }
  }
  return GoalsTimeSpan;
}

function ProcessHusRoutes(x, y, z, posArr) {
  let [preX, preY, preZ] = posArr[posArr.length - 1];

  if (preY < 1 && y < 1) {
    posArr.push([x, y + 0.15, z], [x, y + 0.15, z]);
    return;
  }

  // same Building
  if (preX * x > 0 && preZ * z > 0) {
    if (Math.abs(preY - y) < 0.5) {
      posArr.push([x, y + 0.15, z], [x, y + 0.15, z]);
      return;
    } else {
      changeStair(y, posArr);
      posArr.push([x, y + 0.15, z], [x, y + 0.15, z]);
      return;
    }
  } else {
    // diff Building
    changeStair(0, posArr);
    changeStair(y, posArr, x, z);
    posArr.push([x, y + 0.15, z], [x, y + 0.15, z]);
  }
}

function changeStair(y, posArr, x, z) {
  let [preX, preY, preZ] = posArr[posArr.length - 1];

  if (x !== undefined && z !== undefined) {
    preX = x;
    preZ = z;
  }

  while (Math.abs(preY - y) > 0.5) {
    posArr.push(...stairArr(preX, preY, preZ, y));
    [preX, preY, preZ] = posArr[posArr.length - 1];
  }
}

function stairArr(preX, preY, preZ, y) {
  if (preX > 0 && preZ > 0) {
    return y < preY
      ? [
          [5, preY, 1.25],
          [5.5, preY, 1.25],
          [5.5, preY - 2, 3.75],
          [5, preY - 2, 3.75],
        ]
      : [
          [5, preY, 3.75],
          [5.5, preY, 3.75],
          [5.5, preY + 2, 1.25],
          [5, preY + 2, 1.25],
        ];
  } else if (preX < 0 && preZ < 0) {
    return y < preY
      ? [
          [-5, preY, -1.25],
          [-5.5, preY, -1.25],
          [-5.5, preY - 2, -3.75],
          [-5, preY - 2, -3.75],
        ]
      : [
          [-5, preY, -3.75],
          [-5.5, preY, -3.75],
          [-5.5, preY + 2, -1.25],
          [-5, preY + 2, -1.25],
        ];
  } else if (preX < 0 && preZ > 0) {
    return y < preY
      ? [
          [-1.25, preY, 5],
          [-1.25, preY, 5.5],
          [-3.75, preY - 2, 5.5],
          [-3.75, preY - 2, 5],
        ]
      : [
          [-3.75, preY, 5],
          [-3.75, preY, 5.5],
          [-1.25, preY + 2, 5.5],
          [-1.25, preY + 2, 5],
        ];
  } else {
    return y < preY
      ? [
          [1.25, preY, -5],
          [1.25, preY, -5.5],
          [3.75, preY - 2, -5.5],
          [3.75, preY - 2, -5],
        ]
      : [
          [3.75, preY, -5],
          [3.75, preY, -5.5],
          [1.25, preY + 2, -5.5],
          [1.25, preY + 2, -5],
        ];
  }
}
