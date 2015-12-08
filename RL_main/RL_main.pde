Maze maze;
Bot bot;

// a trial is completed when the bot reaches the reward
int ntrials;
float last_trial_reward;

boolean paused = true, showQ = false, showV = false;
int EAST = 0, SOUTH = 1, WEST = 2, NORTH = 3;

void setup() {
  maze = new Maze();
  size(maze.nx*maze.w + 180, maze.ny*maze.w + 180);
  bot = new Bot();
}

void draw() {
  if(!paused)bot.step();
  background(100,100,100);
  maze.display();
  bot.display();
  text_display();
}

void reset() {
  ntrials = 0;
  last_trial_reward = 0.0;
  bot.reset();
}

void nextTrial() {
  ntrials++;
  last_trial_reward = bot.summed_reward;
  bot.home();
}

void text_display() {
  textAlign(LEFT, CENTER);
  textSize(14);
  // Controls
  fill(255, 255, 255);
  int xoff = 15;
  int yoff = maze.ny * maze.w;
  int dy = 18;
  text("r - RESET", xoff, yoff += dy);
  text("p - PAUSE/RUN", xoff, yoff += dy);
  text("s - SINGLE STEP", xoff, yoff += dy);
  text("q - QVALS (show/hide)", xoff, yoff += dy);
  text("v - VALUES (show/hide)", xoff, yoff += dy);

  // Status info
  fill(255);
  xoff = width/2;
  yoff = maze.ny * maze.w;
  String[] actions = {"EAST", "SOUTH", "WEST", "NORTH", "NONE"};
  fill(255);
  text("action = " + actions[bot.last_action],     xoff, yoff+=dy);
  text("reward = " + bot.reward,                   xoff, yoff+=dy);
  text("summed_reward = " + bot.summed_reward,     xoff, yoff+=dy);
  text("------------------------",                 xoff, yoff+=dy);
  text("ntrials = " + ntrials,                     xoff, yoff+=dy);
  text("last_trial_reward = " + last_trial_reward, xoff, yoff+=dy);
}

void keyPressed() {
  if (key == 'p' || key == ' ') {
    paused = !paused;
  } else if (key == 'q') {
    showQ = !showQ;
  } else if (key == 'r') {
    reset();
  } else if (key == 's') {
    bot.step();
  } else if (key == 'v') {
    showV = !showV;
  } 
}
