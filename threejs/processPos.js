// import { Robots } from "./robots";

const fs = require("fs");

try {
  const data = fs.readFileSync(
    "/Users/Raven/Desktop/pythonCod/Ros/scripts/mrga_tp/mrga_waypoints.txt",
    "utf8"
  );
  const xy = data.split("\n").map((str,index) => {
    if (!str) return;
    const arr = str.split("[")[1].split(",");
    let height = 0.15;
    switch (arr[2].trim()) {
      case "0.66":
        break;
      case "0.88":
        height += 2;
        break;
      case "6.06":
        height += 4;
        break;
      case "16":
        height += 6;
        break;
      case "26":
        height += 8;
        break;
      default:
        console.log(arr[2]);
        break;
    }

    let x = Number((arr[0] / 5.5).toFixed(2));
    let y = Number((arr[1] / 5.5).toFixed(2));
    x = Math.abs(x) < 1 ?  x + (x>0?1:-1) : x;
    y = Math.abs(y) < 1 ?  y + (y>0?1:-1) : y;
    return [x, y, Number(height)];
  });
} catch (err) {
}
// Robots.map()
