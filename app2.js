import express from "express";
import { CronJob } from "cron";
import dotenv from "dotenv";
import { IgApiClient } from "instagram-private-api";
import { promisify } from "util";
import { readFile } from "fs";

const app = express();
const readFileAsync = promisify(readFile);
dotenv.config();

app.use(express.static("public"));
app.listen(process.env.PORT || 3000, function () {});

app.get("/", function (request, response) {
  response.send('up and running');
});

async function instagramPost() {
  try {
    console.log("Posting to Instagram begins..");
    const { username, password } = process.env;
    const ig = new IgApiClient();
    const caption = "Enter caption here";
    ig.state.generateDevice(username);
    const user = await ig.account.login(username, password);
    const path = `todaysPost.jpg`;
    const published = await ig.publish.photo({
      file: await readFileAsync(path),
      caption: caption,
    });
    console.log("Posted to Instagram!");
  } catch (error) {
    console.log(error);
  }
}

// Run every minute
let dailyPost = new CronJob(
  "* * * * *",
  function () {
    console.log("Auto post to Instagram begins..");
    instagramPost();
  },
  true
);

dailyPost.start();
console.log('Successfully started, now posting to Instagram every minute!');
