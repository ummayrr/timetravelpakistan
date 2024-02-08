import express from "express";
import { CronJob } from "cron";
import { IgApiClient } from "instagram-private-api";
import { promisify } from "util";
import { readFile } from "fs";

const app = express();
const readFileAsync = promisify(readFile);

app.use(express.static("public"));
app.listen(3000, function () {});

app.get("/", function (request, response) {
  response.send('stoichive is currently up and running <br><br> - Instagram @stoichive');
});

async function instagramPost() {
  try {
    console.log("Posting to Instagram begins..");
    const username = "your_username"; // replace with your username
    const password = "your_password"; // replace with your password
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
