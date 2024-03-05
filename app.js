//import express from "express";
import { CronJob, CronTime } from "cron";
import { IgApiClient } from "instagram-private-api";
import { promisify } from "util";
import { readFile, readdirSync } from "fs";
import dotenv from "dotenv";
dotenv.config();

console.log(process.env.INSTA_USERNAME);
//const app = express();
const readFileAsync = promisify(readFile);

//app.use(express.static("public"));
//app.listen(3000, function () {});

//app.get("/", function (request, response) {
 // response.send('chal raha hai bhai');
//});

let imageIndex = 1;

const username = process.env.INSTA_USERNAME;
const password = process.env.INSTA_PASSWORD;

const ig = new IgApiClient();
ig.state.generateDevice(username);
async function login() {
  //await ig.simulate.preLoginFlow();
  const user = await ig.account.login(username, password);
}
login();


function calculateInterval(totalPosts) {
  let interval;
  if (totalPosts >= 14) {
    interval = 60; // 1
  } else if (totalPosts >= 10) {
    interval = 90; // 1.5
  } else if (totalPosts >= 8) {
    interval = 120; // 2
  } else if (totalPosts >= 6) {
    interval = 150; // 2.5
  } else if (totalPosts >= 4) {
    interval = 180; // 3
  } else if (totalPosts == 3) {
    interval = 210; // 3.5
  } else if (totalPosts == 2) {
    interval = 300; // 5
  } else {
    interval = 330; // 5.5
  }

  //5-20 min
  const randomInterval = Math.floor(Math.random() * 16 + interval);
  return randomInterval;
}

function getNextJobTime(minutes) {
  const date = new Date();
  date.setMinutes(date.getMinutes() + minutes);
  return date;
}

let totalPosts = readdirSync('edited').length;
let randomInterval = calculateInterval(totalPosts);
let nextJobTime = getNextJobTime(randomInterval);
let postEveryMinute = new CronJob(
  nextJobTime,
  function () {
    console.log("cron shuru bhai");
    if (imageIndex <= totalPosts) {
      instagramPost();
    } else {
      console.log("kaam tamam bhai");
      this.stop();
    }
  },
  true
);

async function instagramPost() {
  try {
    console.log("kaam karne ki koshish start bhai");

    const imagePath = `edited/image${imageIndex}_edited.jpg`;
    const captionPath = `text${imageIndex}.txt`;
    const caption = await readFileAsync(captionPath, 'utf8');

    const published = await ig.publish.photo({
      file: await readFileAsync(imagePath),
      caption: caption,
    });
    console.log("kaam hogaya bhai");


    imageIndex++;
    totalPosts = readdirSync('edited').length;
    randomInterval = calculateInterval(totalPosts);

    postEveryMinute.stop();
    nextJobTime = getNextJobTime(randomInterval);
    postEveryMinute.setTime(new CronTime(nextJobTime));

    if (imageIndex <= totalPosts) {
      postEveryMinute.start();
      console.log(`agli post after ${randomInterval} minutes`);
    } else {
      console.log("kaam tamam bhai.");
    }

  } catch (error) {
    console.log(error);
  }
}

postEveryMinute.start();
console.log(`bilkul shuru wala shuru bhai, agli post after ${randomInterval} minutes`);
